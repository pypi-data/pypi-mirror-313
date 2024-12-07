from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from openrank.onchainscore.cliutil import annotated_typer_argument, \
    annotated_typer_option


class Id(Enum):
    BASE = 8453
    LOCAL = 31337

    @classmethod
    def from_str(cls, s: str) -> Id:
        try:
            return getattr(cls, s.upper().replace('-', '_'))
        except AttributeError:
            raise RuntimeError(f"no such chain {s!r}")

    def __str__(self) -> str:
        return self.name.lower().replace('_', '-')

    @classmethod
    def typer_arg(cls, **kwargs):
        return annotated_typer_argument(int, kwargs,
                                        metavar='NAME',
                                        help="""target chain""",
                                        parser=cls.from_str)

    @classmethod
    def typer_opt(cls, **kwargs):
        return annotated_typer_option(int, kwargs,
                                      metavar='NAME',
                                      help="""target chain""",
                                      parser=cls.from_str)


@dataclass(kw_only=True)
class Config:
    id: Id
    rpc: str


CONFIGS = [
    Config(id=Id.BASE, rpc='https://mainnet.base.org'),
    Config(id=Id.LOCAL, rpc='http://127.0.0.1:8545')
]

CONFIGS_BY_ID = {config.id: config for config in CONFIGS}
