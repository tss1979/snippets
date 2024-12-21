from datetime import date

from src.repositories.base import BaseRepository
from src.models.snippets import SnippetsOrm
from src.schemas.snippets import Snippet
from sqlalchemy import func, select


class SnippetsRepository(BaseRepository):
    model = SnippetsOrm
    schema = Snippet

    async def get_all(
            self,
            title,
            code,
            limit,
            offset,
    ):
        query = select(self.model)
        if code:
            query = query.filter(func.lower(self.model.code).contains(code.strip().lower()))
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Snippet.model_validate(model, from_attributes=True) for model in result.scalars().all()]



