"""
Relation convertion table:

    .. include:: relation_table.demo.py.txt
"""
from enum import Enum

import enum_tools

# noinspection PyUnresolvedReferences
from .._core._c_uutils_base_relation import _CRelation, _c_sym_relation, _c_sub2super, _c_super2sub

__all__ = [
    'Relation',
    'sym_relation',
    'sub2super',
    'super2sub'
]


# noinspection PyProtectedMember
@enum_tools.documentation.document_enum
class Relation(Enum):
    """
    Enum for base relations between sets.
    """

    DIFFERENT = _CRelation._c_DIFFERENT
    """
    Incomparable or not (set1 <= set2) depending on exactness
    """

    SUPERSET = _CRelation._c_SUPERSET
    """
    Set1 is a superset of set2 or not used
    """

    GREATER = _CRelation._c_GREATER
    """
    Same as superset
    """

    SUBSET = _CRelation._c_SUBSET
    """
    Set1 is a subset of set2 or set1 <= set2 depending on exactness
    """

    LESS = _CRelation._c_LESS
    """
    Same as subset
    """

    EQUAL = _CRelation._c_EQUAL
    """
    Set1 is equal to set2 or not used
    """

    @classmethod
    def from_raw(cls, raw: _CRelation) -> 'Relation':
        for _, member in cls.__members__.items():
            if member.value == raw:
                return member
        raise ValueError(f'Unknown value - {raw!r}.')


def sym_relation(rel: Relation) -> Relation:
    """
    Return the symmetric of a relation (invert subset and superset bits).

    :param rel: Relation to invert.
    :return: Inverted relation.
    """
    return Relation.from_raw(_c_sym_relation(rel.value))


def sub2super(rel: Relation) -> Relation:
    """
    Convert a subset relation to a superset relation.

    :param rel: Relation to convert.
    :return: Converted relation.
    """
    return Relation.from_raw(_c_sub2super(rel.value))


def super2sub(rel: Relation) -> Relation:
    """
    Convert a superset relation to a subset relation.

    :param rel: Relation to convert.
    :return: Converted relation.
    """
    return Relation.from_raw(_c_super2sub(rel.value))
