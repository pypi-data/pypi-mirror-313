### Stack:

- [x] <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-plain.svg" alt="python" width="15" height="15"/>
  Python 3.11+ <br/></a>
- [x] <a href="https://docs.sqlalchemy.org/en/20"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlalchemy/sqlalchemy-plain.svg" alt="sqlalchemy" width="15" height="15"/>
  SqlAlchemy 2<br/></a>
- [x] <a href="https://docs.pydantic.dev/">🕳 Pydantic 2<br/></a>

### Installation

    pip install pydantic-sqlalchemy-filter

### Usage

#### Implement UserFilter

    from pydantic_sqlalchemy_filter import BaseQueryBuilder, DatabaseModel


    class UserFilter(BaseQueryBuilder):
        username: str | None = Field(default=None)
        order_by: str | None = Field(default='username', alias='orderBy')

        def _filter(
            self,
            model: DatabaseModel,
            exclude_deleted: bool = False,
            query: sqlalchemy.Select | None = None,
        ) -> sqlalchemy.Select:
            if query is None:
                query = self.build_base_query(
                    model=model,
                    exclude_deleted=exclude_deleted,
                )

            if self.username is not None
                query = query.filter_by(username=self.username)

            return query

#### In FastAPI router:

        @router.get(path='')
        async def get_all_filtered_users(
            query_builder: Annotated[UserFilter, Depends()],
            session: Annotated[AsyncSession, Depends(get_async_session)],
        ) -> list[Users]:
            query = query_builder.build_select_query(model=User)
            results = await session.execute(query)
            users = results.scalars().all()

            return list(users)
