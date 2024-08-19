from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema
from madr.security import get_password_hash
from madr.utils import T_CurrentUser, T_Session, sanitize

router = APIRouter(prefix='/contas', tags=['contas'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_account(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email)
            | (User.username == sanitize(user.username))
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='conta já consta no MADR',
        )

    db_user = User(
        username=sanitize(user.username),
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='conta já consta no MADR',
        )

    current_user.username = sanitize(user.username)
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
