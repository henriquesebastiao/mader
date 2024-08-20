from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.models import Romancista
from madr.schemas import (
    Message,
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
)
from madr.utils import (
    T_CurrentUser,
    T_Session,
)

router = APIRouter(prefix='/romancistas', tags=['romancistas'])


@router.post(
    '/', response_model=RomancistaPublic, status_code=HTTPStatus.CREATED
)
def create_romancista(
    romancista: RomancistaSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    nome = romancista.nome
    romancisata_db = session.scalar(
        select(Romancista).where(Romancista.nome == nome)
    )

    if romancisata_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    romancisata_db = Romancista(nome=romancista.nome)

    session.add(romancisata_db)
    session.commit()
    session.refresh(romancisata_db)

    return romancisata_db


@router.delete(
    '/{romancista_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_romancista(
    romancista_id: int, session: T_Session, current_user: T_CurrentUser
):
    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not romancista_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(romancista_db)
    session.commit()

    return {'message': 'Romancista deletado do MADR'}


@router.patch(
    '/{romancista_id}',
    response_model=RomancistaPublic,
    status_code=HTTPStatus.OK,
)
def update_user(
    romancista_id: int,
    romancista: RomancistaSchema,
    current_user: T_CurrentUser,
    session: T_Session,
):
    nome = romancista.nome

    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not romancista_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    name_already_exists = session.scalar(
        select(Romancista).where(Romancista.nome == nome)
    )

    if name_already_exists:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    romancista_db.nome = nome

    session.add(romancista_db)
    session.commit()
    session.refresh(romancista_db)

    return romancista_db


@router.get(
    '/{romancista_id}',
    response_model=RomancistaPublic,
    status_code=HTTPStatus.OK,
)
def get_romancista_by_id(romancista_id: int, session: T_Session):
    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not romancista_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    return romancista_db


@router.get('/', response_model=RomancistaList, status_code=HTTPStatus.OK)
def get_romancista_by_search(session: T_Session, nome: str | None = None):
    romancistas = session.scalars(
        select(Romancista).filter(Romancista.nome.contains(nome))
    ).all()

    return {'romancistas': romancistas}
