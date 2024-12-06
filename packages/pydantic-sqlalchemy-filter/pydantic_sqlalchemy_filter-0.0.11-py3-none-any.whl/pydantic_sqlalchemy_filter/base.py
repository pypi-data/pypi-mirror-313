from abc import ABC
from typing import Type

from pydantic import BaseModel, Field
from sqlalchemy import Column, Select, asc, desc, func, select

from pydantic_sqlalchemy_filter.interfaces.query_builder import IQueryBuilder
from pydantic_sqlalchemy_filter.types import DatabaseModel


class BaseQueryBuilder(IQueryBuilder, BaseModel, ABC):
    """Base class for build default filtering SQL query.

    In children need to implement method _filter.

    """

    order_by: str | None = Field(default=None, alias='orderBy')
    post_order_by: str | None = Field(default=None, alias='postOrderBy')
    page: int | None = Field(default=None, gt=0)
    size: int | None = Field(default=None, gt=0)

    def filter(
        self,
        model: Type[DatabaseModel],
        exclude_deleted: bool,
        query: Select | None = None,
    ) -> Select:
        """Returns query for custom filtering."""

        return self._filter(model, exclude_deleted, query)

    def build_count_query(
        self,
        model: Type[DatabaseModel],
        exclude_deleted: bool = False,
        query: Select | None = None,
    ) -> Select:
        """Returns count of model rows after filter.

        If exclude_deleted is True - Mark as deleted rows won`t be returned.

        """

        if query is None:
            query = select(func.count(model.id))

        if exclude_deleted:
            query = query.where(model.deleted_at.is_(None))

        query = self.filter(
            model=model,
            exclude_deleted=exclude_deleted,
            query=query,
        )

        return query

    def build_select_query(
        self,
        model: Type[DatabaseModel],
        exclude_deleted: bool = False,
        query: Select | None = None,
    ) -> Select:
        """Generate query if not exists.
        Call method "filter" (must be implemented in child class).
        Then sort, paginate and post sort results.

        """
        if query is None:
            query = self.build_base_query(
                model=model,
                exclude_deleted=exclude_deleted,
            )
        query = self.filter(
            model=model,
            exclude_deleted=exclude_deleted,
            query=query,
        )
        query = self.sort(query, model=model)
        query = self.paginate(query)
        query = self.sort_subquery(query)

        return query

    def build_base_query(
        self,
        model: Type[DatabaseModel],
        exclude_deleted: bool = False,
    ) -> Select:
        """Returns query Select with all model fields."""

        query = select(model)

        if exclude_deleted:
            query = query.where(model.deleted_at.is_(None))

        return query

    def sort(
        self,
        query: Select,
        model: Type[DatabaseModel],
        collate_name: str | None = None,
    ) -> Select:
        """Sort by field name.

        If order_by startswith "-" - sort by DESC. Default - ASC.
        If with_collate is not None - will be using COLLATE with this string.
        You need to add this collate name to your database collations.
        """

        return self._sort(query, model=model, collate_name=collate_name)

    def _sort(
        self,
        query: Select,
        model: Type[DatabaseModel],
        collate_name: str | None = None,
    ) -> Select:

        if self.order_by is None:
            return query

        reverse: bool = False
        if self.order_by.startswith(('-', '+')):
            reverse = self.order_by[0] == '-'
            self.order_by = self.order_by[1:]

        field: Column = model.field_by_name(name=self.order_by)
        if not field:
            raise KeyError(
                f'Model <{model}> have not field with name "{self.order_by}"'
            )

        return self.__sort(
            query=query,
            field=field,
            reverse=reverse,
            collate_name=collate_name,
        )

    def __sort(
        self,
        query: Select,
        field: Column,
        reverse: bool,
        collate_name: str | None = None,
    ) -> Select:
        add_collation: bool = (
            field.type.python_type is str and collate_name is not None
        )

        if not reverse and not add_collation:
            return query.order_by(field.asc())

        if reverse and add_collation:
            return query.order_by(
                func.lower(field).collate(collate_name).desc()
            )

        if add_collation:
            return query.order_by(
                func.lower(field).collate(collate_name).asc()
            )

        return query.order_by(field.desc())

    def paginate(
        self,
        query: Select,
    ) -> Select:
        """Add pagination to query."""

        return self._paginate(query)

    def _paginate(
        self,
        query: Select,
    ) -> Select:
        """Add pagination to query."""

        if self.page is not None and self.size is not None:
            offset: int = (self.page - 1) * self.size
            query = query.limit(self.size).offset(offset)

        return query

    def sort_subquery(
        self,
        subquery: Select,
    ) -> Select:
        """Sort subquery by post_order_by field name.
        If post_order_by startswith "-" - sort by DESC. Default - ASC.

        """

        return self._sort_subquery(subquery)

    def _sort_subquery(
        self,
        subquery: Select,
    ) -> Select:
        """Sort subquery by post_order_by field name.
        If post_order_by startswith "-" - sort by DESC. Default - ASC.

        """

        if self.post_order_by is None:
            return subquery

        reverse = False
        if self.post_order_by.startswith(('-', '+')):
            reverse = self.post_order_by[0] == '-'
            self.post_order_by = self.post_order_by[1:]

        subquery = subquery.subquery()

        if reverse:
            query = select(subquery).order_by(
                desc(getattr(subquery.c, self.post_order_by))
            )
        else:
            query = select(subquery).order_by(
                asc(getattr(subquery.c, self.post_order_by))
            )

        return query
