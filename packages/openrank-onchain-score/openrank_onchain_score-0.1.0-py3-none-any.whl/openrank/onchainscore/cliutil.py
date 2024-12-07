from __future__ import annotations

from typing import Any, Annotated

import typer
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3

from .util import set_defaults


def annotated_typer_argument(cls: type, kwargs: dict[str, Any], /, **defaults):
    set_defaults(kwargs, **defaults)
    return Annotated[cls, typer.Argument(**kwargs)]


def annotated_typer_option(cls: type, kwargs: dict[str, Any], /, **defaults):
    set_defaults(kwargs, **defaults)
    return Annotated[cls, typer.Option(**kwargs)]


def checksum_address_option(**kwargs):
    return annotated_typer_option(ChecksumAddress, kwargs,
                                  parser=AsyncWeb3.to_checksum_address,
                                  metavar='ADDRESS')
