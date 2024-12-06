from typing import Union, List

# noinspection PyUnresolvedReferences
from .._core._c_uutils_hash_compute import (
    _c_hash_murmur2_U8, _c_hash_computeU32, _c_hash_computeU16,
    _c_hash_computeI32, _c_hash_computeI16, _c_hash_computeI8,
    _c_hash_computeStr, _c_hash_compute3
)

__all__ = [
    'hash_compute_i16',
    'hash_murmur2_u8',
    'hash_compute3',
    'hash_compute_str',
    'hash_compute_i32',
    'hash_compute_u16',
    'hash_compute_u32',
    'hash_compute_i8',
]


def hash_murmur2_u8(data: Union[bytes, bytearray], initval: int = 0) -> int:
    """
    Compute hash value using Murmur2 for uint8_t data.

    :param data: Input data
    :type data: bytes or bytearray
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_murmur2_U8(data, len(data), initval)


def hash_compute_u32(data: List[int], initval: int = 0) -> int:
    """
    Compute hash value for uint32_t data.

    :param data: Input data
    :type data: List[int]
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeU32(data, initval)


def hash_compute_u16(data: List[int], initval: int = 0) -> int:
    """
    Compute hash value for uint16_t data.

    :param data: Input data
    :type data: List[int]
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeU16(data, initval)


def hash_compute_i32(data: List[int], initval: int = 0) -> int:
    """
    Compute hash value for int32_t data.

    :param data: Input data
    :type data: List[int]
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeI32(data, initval)


def hash_compute_i16(data: List[int], initval: int = 0) -> int:
    """
    Compute hash value for int16_t data.

    :param data: Input data
    :type data: List[int]
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeI16(data, initval)


def hash_compute_i8(data: Union[bytes, bytearray], initval: int = 0) -> int:
    """
    Compute hash value for int8_t data.

    :param data: Input data
    :type data: bytes or bytearray
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeI8(data, initval)


def hash_compute_str(s: str, initval: int = 0) -> int:
    """
    Compute hash value for a string.

    :param s: Input string
    :type s: str
    :param initval: Initial value for hash computation
    :type initval: int
    :return: Computed hash value
    :rtype: int
    """
    return _c_hash_computeStr(s, initval)


def hash_compute3(a: int, b: int, c: int) -> int:
    """
    Compute a new hash from 3 previous hash values.

    :param a: First hash value
    :type a: int
    :param b: Second hash value
    :type b: int
    :param c: Third hash value
    :type c: int
    :return: Combined hash value
    :rtype: int
    """
    return _c_hash_compute3(a, b, c)
