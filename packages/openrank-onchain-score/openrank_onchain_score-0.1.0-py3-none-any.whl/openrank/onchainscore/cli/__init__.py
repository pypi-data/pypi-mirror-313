from __future__ import annotations

import csv
import logging
import os
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Optional, Any

import aiohttp
import structlog.processors
import typer
from eth_account import Account
from eth_typing import ChecksumAddress
from rich.console import Console
from rich.logging import RichHandler
from web3 import AsyncWeb3
from web3.middleware import SignAndSendRawMiddlewareBuilder

from openrank.onchainscore.cliutil import checksum_address_option
from .. import chainconf as chain_, score_from_uint256, score_to_uint256
from ..abi import DEFAULT_ABI, load_bundled
from ..util import sync

logger = structlog.get_logger()

DEFAULT_CHAIN = 'base'

DEFAULT_CONTRACT_ADDRESSES = {
    chain_.Id.BASE: '0xaC1EBa9e86740e38F0aCbE016d32b3B015206cd8',
    chain_.Id.LOCAL: '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512',
}

app = typer.Typer()


@dataclass(kw_only=True)
class Options:
    chain: chain_.Id
    contract: ChecksumAddress
    rpc: str
    abi: dict[str, Any]
    dry_run: bool


options: Optional[Options] = None


@app.callback()
def callback(
        chain: chain_.Id.typer_opt() = DEFAULT_CHAIN,
        contract: checksum_address_option(
            help="""score contract address""",
            show_default="chain default",
        ) = None,
        abi: Annotated[str, typer.Option(
            help="""contract ABI name""",
        )] = DEFAULT_ABI,
        rpc: Annotated[Optional[str], typer.Option(
            metavar='URI',
            help="""JSON-RPC endpoint""",
            show_default="chain default",
        )] = None,
        dry_run: Annotated[bool, typer.Option(
            help="""dry-run write transactions (just print gas estimate)""",
        )] = False,
        log_level: Annotated[str, typer.Option(
            metavar='NAME',
            help="""logging level, e.g. debug, info, warning""",
        )] = 'warning',
):
    global options
    try:
        chain_config = chain_.CONFIGS_BY_ID[chain]
    except KeyError:
        typer.secho(f"unsupported chain {chain!s}", err=True)
        raise typer.Abort()
    if rpc is None:
        rpc = chain_config.rpc
    options = Options(
        chain=chain,
        contract=(contract or DEFAULT_CONTRACT_ADDRESSES[chain]),
        abi=load_bundled(abi),
        rpc=(rpc or chain_config.rpc),
        dry_run=dry_run,
    )
    logging.getLogger().setLevel(log_level.upper())
    logger.debug("initialized global options", options=options)


@asynccontextmanager
async def web3_setup():
    async with aiohttp.ClientSession() as session:
        provider = AsyncWeb3.AsyncHTTPProvider(endpoint_uri=options.rpc)
        await provider.cache_async_session(session)
        w3 = AsyncWeb3(provider)
        account = Account.from_key(os.environ['WEB3_KEY'])
        w3.middleware_onion.inject(
            SignAndSendRawMiddlewareBuilder.build(account), layer=0)
        w3.eth.default_account = account.address
        await w3.is_connected()
        contract = w3.eth.contract(address=options.contract, abi=options.abi)
        logger.debug(f"web3 client initialized",
                     account=account.address,
                     contract=contract.address)
        yield w3, contract


@app.command()
@sync
async def length():
    """Print the number of entries in the leaderboard."""
    async with web3_setup() as (w3, contract):
        print(await contract.functions.leaderboardLength().call())


@app.command()
@sync
async def get_score_at_rank(
        rank: Annotated[int, typer.Argument(
            metavar='RANK',
            help="""rank position, 1-based""",
        )],
        raw: Annotated[bool, typer.Option(
            help="""output the raw uint256 score""",
        )] = False,
):
    """Print the FID and the OpenRank score at the given rank (1-based)."""
    if rank < 1:
        logger.error("rank must be positive", rank=rank)
        raise typer.Abort()
    async with web3_setup() as (w3, contract):
        fid, score = await contract.functions.leaderboard(rank - 1).call()
        if not raw:
            score = score_from_uint256(score)
        print(fid, score)


@app.command()
@sync
async def get_rank_for_fid(
        fid: Annotated[int, typer.Argument(
            metavar='FID',
            help="""Farcaster FID""",
        )],
):
    """Print the 1-based rank of the given FID."""
    if fid < 1:
        logger.error("FID must be positive", fid=fid)
        raise typer.Abort()
    async with web3_setup() as (w3, contract):
        rank = await contract.functions.fidRank(fid).call()
        if rank == 0:
            logger.error("FID not ranked", fid=fid)
            raise typer.Abort()
        print(rank)


@app.command()
@sync
async def truncate(
        count: Annotated[Optional[int], typer.Argument(
            metavar='COUNT',
            help="""number of entries to truncate""",
        )],
):
    """
    Truncate leaderboard.

    Leaderboard entries are always removed from the last.
    """
    if count < 1:
        logger.error("count must be positive", count=count)
        raise typer.Abort()
    async with web3_setup() as (w3, contract):
        logger.info(f"truncating last entries", count=count)
        call = contract.functions.truncate(count)
        await run_call(w3, call)


@app.command()
@sync
async def upload_from_csv(
        file: Annotated[typer.FileText, typer.Option(
            metavar='FILE',
            help="""input CSV file with "fid" and "score" columns""",
            show_default="standard input",
        )] = sys.stdin,
        offset: Annotated[int, typer.Option(
            metavar='NUM',
            help="""number of top entries to skip in the CSV""",
        )] = 0,
        limit: Annotated[Optional[int], typer.Option(
            metavar='NUM',
            help="""maximum number of entries to upload""",
            show_default="no limit",
        )] = None,
        batch_size: Annotated[int, typer.Option(
            metavar='COUNT',
            help="""upload at most COUNT in each transaction""",
        )] = 1000,
):
    """
    Upload scores from a CSV file.

    The CSV file must have two columns named "fid" and "score";
    entries must be sorted in descending score order.

    The scores must be in [0.0, 1.0] range.
    """
    if batch_size < 1:
        logger.error("batch size must be positive", batch=batch_size)
        raise typer.Abort()
    async with web3_setup() as (w3, contract):
        batch = []

        async def upload():
            logger.info(f"uploading batch", size=len(batch))
            call = contract.functions.appendScores(batch)
            receipt = await run_call(w3, call)
            if receipt is not None:
                print(receipt.gasUsed)
            batch.clear()

        for row in csv.DictReader(file):
            if offset > 0:
                offset -= 1
                continue
            if limit == 0:
                break
            fid = int(row['fid'])
            score = float(row['score'])
            batch.append(dict(fid=fid, score=score_to_uint256(score)))
            if len(batch) >= batch_size:
                await upload()
            if limit is not None:
                limit -= 1

        if batch:
            await upload()


@app.command()
def version():
    """Print the version number."""
    from .. import __version__
    print(f"openrank-onchain-score {__version__}")


async def run_call(w3, call, tx={}):
    assert not options.dry_run
    if options.dry_run:
        gas = await call.estimate_gas(tx)
        print(gas)
        return
    tx_hash = await call.transact(tx)
    logger.info(f"transaction submitted, waiting", hash=tx_hash)
    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
    logger.info(f"transaction finished")
    return tx_receipt


def main():
    logging.basicConfig(format="%(message)s",
                        datefmt="[%X]",
                        handlers=[RichHandler(rich_tracebacks=True,
                                              console=Console(stderr=True))])
    structlog.configure(processors=[
        structlog.stdlib.filter_by_level,
        # structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ], logger_factory=structlog.stdlib.LoggerFactory())
    return app()
