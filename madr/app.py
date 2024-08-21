from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from madr.models import User
from madr.routers import contas, livros, romancistas
from madr.schemas import Token
from madr.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from madr.utils import T_OAuth2Form, T_Session

description = """
Esta API foi desenvolvida como  projeto final do curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/)
#### Documentação mais legível: [Redoc](https://api.henriquesebastiao.com/redoc)
"""

app = FastAPI(
    title='Meu Acervo Digital de Romances (MADR)',
    version='dev',
    docs_url='/',
    description=description,
    contact={
        'name': 'Henrique Sebastião',
        'email': 'contato@henriquesebastiao.com',
        'url': 'https://github.com/henriquesebastiao',
    },
)

app.include_router(contas.router)
app.include_router(romancistas.router)
app.include_router(livros.router)


@app.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    invalid_credentials_exception = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Incorrect email or password',
    )

    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise invalid_credentials_exception
    elif not verify_password(form_data.password, user.password):
        raise invalid_credentials_exception

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
