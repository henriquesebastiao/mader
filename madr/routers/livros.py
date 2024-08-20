from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr.models import Livro
from madr.schemas import (
    LivroList,
    LivroPublic,
    LivroSchema,
    LivroUpdate,
    Message,
)
from madr.utils import T_CurrentUser, T_Session

router = APIRouter(prefix='/livros', tags=['livros'])


@router.post('/', response_model=LivroPublic, status_code=HTTPStatus.OK)
def create_livro(
    livro: LivroSchema, current_user: T_CurrentUser, session: T_Session
):
    titulo = livro.titulo

    livro_db = session.scalar(select(Livro).where(Livro.titulo == titulo))

    if livro_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Livro já consta no MADR',
        )

    livro_db = Livro(
        ano=livro.ano,
        titulo=titulo,
        romancista_id=livro.romancista_id,
    )

    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    return livro_db


@router.delete(
    '/{livro_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_livro(
    livro_id: int, session: T_Session, current_user: T_CurrentUser
):
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    session.delete(livro_db)
    session.commit()

    return {'message': 'Livro deletado no MADR'}


@router.patch(
    '/{livro_id}', response_model=LivroPublic, status_code=HTTPStatus.OK
)
def update_livro(
    livro_id: int,
    livro: LivroUpdate,
    current_user: T_CurrentUser,
    session: T_Session,
):
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    if livro.titulo:
        titulo = livro.titulo

        title_already_exists = session.scalar(
            select(Livro).where(Livro.titulo == titulo)
        )

        if title_already_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Livro já consta no MADR',
            )

        livro_db.titulo = titulo
    if livro.ano:
        livro_db.ano = livro.ano
    if livro.romancista_id:
        livro_db.romancista_id = livro.romancista_id

    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    return livro_db


@router.get(
    '/{livro_id}', response_model=LivroPublic, status_code=HTTPStatus.OK
)
def get_livro_by_id(livro_id: int, session: T_Session):
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    return livro_db


@router.get('/', response_model=LivroList, status_code=HTTPStatus.OK)
def get_livro_by_search(
    session: T_Session,
    titulo: str | None = None,
    ano: int | None = None,
):
    query = select(Livro)

    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))
    if ano:
        query = query.filter(Livro.ano == ano)

    livros_db = session.scalars(query).all()

    return {'livros': livros_db}
