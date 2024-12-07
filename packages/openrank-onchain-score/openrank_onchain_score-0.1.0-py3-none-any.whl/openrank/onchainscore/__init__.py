"""A package and CLI tool to manage OpenRank scores onchain."""

from __future__ import annotations

__version__ = "0.1.0"

import struct
from dataclasses import dataclass


@dataclass
class DecomposedFloat:
    """Decomposed IEEE 754 double-precision floating-point number."""
    sign: int
    exponent: int
    mantissa: int

    @classmethod
    def from_number(cls, number: float) -> DecomposedFloat:
        packed = struct.pack('>d', number)
        bits, = struct.unpack('>Q', packed)
        sign = (bits >> 63) & 1
        exponent = (bits >> 52) & 0x7ff
        mantissa = bits & 0xfffffffffffff
        return cls(sign=sign, exponent=exponent, mantissa=mantissa)

    def to_number(self) -> float:
        assert isinstance(self.sign, int) and self.sign in (0, 1), \
            f"invalid {self.sign=}"
        assert isinstance(self.exponent, int) and 0 <= self.exponent < 2048, \
            f"invalid {self.exponent=}"
        assert isinstance(self.mantissa, int) and \
               0 <= self.mantissa < (1 << 52), \
            f"invalid {self.mantissa=}"
        bits = (self.sign << 63) | (self.exponent << 52) | self.mantissa
        packed = struct.pack('>Q', bits)
        number, = struct.unpack('>d', packed)
        return number


def score_to_uint256(score: float) -> int:
    """Convert an OpenRank score to an uint256."""
    assert 0.0 <= score <= 1.0
    if score == 1.0:
        return UINT256_MAX
    d = DecomposedFloat.from_number(score)
    m = 0x0010000000000000 | d.mantissa
    e = d.exponent - 819
    u = m << e if e >= 0 else m >> -e
    assert 0 <= u < UINT256_MAX
    return u


def score_from_uint256(u: int) -> float:
    """Restore an OpenRank score from its uint256 representation."""
    assert 0 <= u <= UINT256_MAX
    if u == 0:
        return 0.0
    if u == UINT256_MAX:
        return 1.0
    m = u
    e = 1023
    while m <= UINT256_MAX:
        m <<= 1
        e -= 1
    m = (m & UINT256_MAX) >> 204
    return DecomposedFloat(sign=0, exponent=e, mantissa=m).to_number()


UINT256_MAX = (1 << 256) - 1
