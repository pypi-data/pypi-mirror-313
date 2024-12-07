"""Utilities for working with SqlAlchemy."""

from __future__ import annotations

# Python Modules
import logging
from functools import lru_cache
from typing import Any, Literal, Optional, Type, TypeVar, get_args

# 3rd Party Modules
import sqlalchemy as sa

from icontract import require
from pydantic.dataclasses import dataclass
from sqlalchemy import orm

# Project Modules
from rwskit.config import YamlConfig
from rwskit.strings_ import camel_to_snake_case


log = logging.getLogger(__name__)


B = TypeVar("B", bound=orm.DeclarativeBase)
"""
A type extending :class:`~sqlalchemy.orm.DeclarativeBase`.
"""

SqlOperator = Literal[
    "==", "!=", ">", ">=", "<", "<=", "like", "in", "not_in", "is_null", "is_not_null"
]
"""
The supported SQL operators for use in an :class:`SqlBinaryExpression`.
"""


class BaseModel(orm.DeclarativeBase):
    """A base class for creating declarative SqlAlchemy models from.

    This class provides functionality for finding any model derived from
    this clas by their table name.
    """
    __abstract__ = True

    @orm.declared_attr.directive
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)

    @classmethod
    @lru_cache
    @require(lambda table_name: table_name.count(".") < 2)
    def find_by_table_name(cls, table_name: str) -> Optional[Type[BaseModel]]:
        """
        Find a model derived from this class by its table name.

        Parameters
        ----------
        table_name : str
            The name of the table whose model class you want to find.

        Returns
        -------
        Type[FindByNameBase], optional
            Returns the model class if the table is found, otherwise ``None``.
        """
        # See: https://stackoverflow.com/a/68862329
        registry = getattr(cls, "registry")

        try:
            find_schema, find_table_name = table_name.split(".", 1)
        except ValueError:
            find_schema, find_table_name = "public", table_name

        for mapper in registry.mappers:
            model = mapper.class_
            table = model.__table__
            candidate_schema = table.schema or "public"
            candidate_table_name = model.__tablename__

            if candidate_schema == find_schema and candidate_table_name == find_table_name:
                return model

        return None


@dataclass(frozen=True, kw_only=False)
class SqlBinaryExpression(YamlConfig):
    """A class that represents the basic binary expression for an SQL column."""

    column: str
    """
    The column name.
    """

    operator: SqlOperator
    """
    The operator to compare the ``column`` and ``value`` with.
    """

    value: Any
    """
    The value used as a comparison.
    """

    @require(
        lambda self: self.operator in get_args(SqlOperator),
        f"The operator must be one of: {get_args(SqlOperator)}",
    )
    def __post_init__(self):
        pass

    def __call__(self, model_or_table: Type[B] | sa.Table) -> sa.BinaryExpression:
        return self.to_expression(model_or_table)

    @require(
        lambda self, model_or_table:
            self.column in model_or_table.columns
            if isinstance(model_or_table, sa.Table) else
            hasattr(model_or_table, self.column),
        "Invalid column"
    )
    @require(
        lambda model_or_table:
            isinstance(model_or_table, sa.Table) or issubclass(model_or_table, orm.DeclarativeBase),
        (
            "The 'model_or_table' must either be an SqlAlchemy Table or an SqlAlchemy ORM model "
            "(subclass of DeclarativeBase)."
        )
    )
    def to_expression(self, model_or_table: Type[B] | sa.Table) -> sa.BinaryExpression:
        """Return a clause that can be used with an SqlAlchemy ``where`` statement.

        Parameters
        ----------
        model_or_table : sqlalchemy.Table
            The table object that contains the column.

        Returns
        -------
        BinaryExpression
            The corresponding SqlAlchemy binary expression.

        """
        column = (
            model_or_table.c[self.column]
            if isinstance(model_or_table, sa.Table) else
            getattr(model_or_table, self.column)
        )
        operator = self.operator

        if operator == "==":
            return column == self.value  # noqa
        if operator == "==" and self.value is None:
            return column.is_(None)
        if operator == "!=":
            return column != self.value  # noqa
        if operator == "!=" and self.value is None:
            return column.isnot(None)
        if operator == '>':
            return column > self.value   # noqa
        if operator == '>=':
            return column >= self.value  # noqa
        if operator == '<':
            return column < self.value   # noqa
        if operator == '<=':
            return column <= self.value  # noqa
        if operator == "like":
            return column.like(self.value)
        if operator == "in":
            return column.in_(self.value)
        if operator == "not_in":
            return column.not_in(self.value)
        if operator == "is_null":
            return column.is_(None)
        if operator == "is_not_null":
            return column.isnot(None)
        else:
            raise ValueError(f'Invalid operator: {operator}')


@dataclass(kw_only=False, frozen=True)
class SqlSelectionCriteria(YamlConfig):
    """A class that represents a conjunction of SqlBinaryExpression."""

    expressions: list[SqlBinaryExpression]
    """
    The list of binary expressions that will be used to filter the query. 
    """

    @require(
        lambda self: all(isinstance(e, SqlBinaryExpression) for e in self.expressions),
        "The expressions must be instances of 'SqlBinaryExpression'.",
    )
    def __post_init__(self):
        pass

    def to_conjunction(self, table: sa.Table) -> sa.BinaryExpression | sa.BooleanClauseList:
        """
        Return a conjunction of binary expressions that can be used with an
        SqlAlchemy ``where`` statement.

        Returns
        -------

        """
        return sa.and_(*[e.to_expression(table) for e in self.expressions])
