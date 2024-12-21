from datetime import date

from src.app.dependencies import PaginationDep, DBDep, UserIdDep
from src.schemas.snippets import SnippetAdd, SnippetPATCH, SnippetCreate
from fastapi import APIRouter, Body, Query, HTTPException

router_snippets = APIRouter(prefix="/snippets", tags=["Сниппеты"])


@router_snippets.get("/", summary="Получение полного списка сниппетов")
async def get_hotels(pagination: PaginationDep,
                     db: DBDep,
                     code: str | None = Query(None, description="Код"),
                     title: str | None = Query(None, description="Название сниппета"),
                     ):
    per_page = pagination.per_page or 5
    return await db.snippets.get_all(
        code=code,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page -1)
    )

@router_snippets.get("/{snippet_id}", summary="Получение отеля по идентификатору")
async def get_snippet_by_id(snippet_id: str, db: DBDep):
    return await db.snippets.get_one_or_none(id=snippet_id)

@router_snippets.post("/create", summary="Добавление сниппета")
async def create_hotel(db: DBDep, user_id: UserIdDep, snippet_data: SnippetCreate):
    _snippet_data = SnippetAdd(user_id=user_id, **snippet_data.model_dump())
    snippet = await db.snippets.add(_snippet_data)
    await db.commit()
    return {"status": "OK", "data": snippet}

@router_snippets.delete("/{snippet_id}", summary="Удаление сниппета по идентификатору")
async def delete_snippet(snippet_id: str, db: DBDep, user_id: UserIdDep):
    try:
        await db.snippets.delete(id=snippet_id, user_id=user_id)
        await db.commit()
        return {"status": "Ok"}
    except:
        raise HTTPException(status_code=403, detail="Нельзя удалить чужой сниппет")

@router_snippets.put("/{snippet_id}", summary="Изменение данных сниппета")
async def edit_snippet(snippet_id: str, snippet_data: SnippetCreate, db: DBDep, user_id: UserIdDep):
    _snippet_data = SnippetAdd(user_id=user_id, **snippet_data.model_dump())
    try:
        await db.snippets.update(snippet_data, id=snippet_id, user_id=user_id)
        await db.commit()
        return {"status": "Ok"}
    except:
        raise HTTPException(status_code=403, detail="Нельзя изменить чужой сниппет")

@router_snippets.patch("/{snippet_id}", summary="Частичное изменение данных сниппета")
async def partial_edit_snippet(snippet_id: str, snippet_data: SnippetPATCH, db: DBDep, user_id: UserIdDep):
    try:
        await db.snippets.update(snippet_data, id=snippet_id, user_id=user_id, exclude_unset=True)
        await db.commit()
        return {"status": "Ok"}
    except:
        raise HTTPException(status_code=403, detail="Нельзя изменить чужой сниппет")


