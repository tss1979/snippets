from fastapi import APIRouter, HTTPException, Response
from src.app.dependencies import UserIdDep, DBDep


from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router_auth = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router_auth.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}

@router_auth.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router_auth.get("/me")
async def get_me(db: DBDep, user_id = UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user

