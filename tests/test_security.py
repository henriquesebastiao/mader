from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from madr.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from madr.settings import Settings
from madr.utils import T_Session

settings = Settings()


def test_jwt():
    data = {'sub': 'user@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/contas/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_valid_token_with_user_not_exists(client, token):
    client.delete(
        '/contas/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response = client.delete(
        '/contas/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_verify_password():
    plain_text = 'password'
    pwd_hash = get_password_hash(plain_text)

    assert verify_password(plain_text, pwd_hash)


def test_get_current_user_without_sub():
    token = create_access_token(data={})

    with pytest.raises(HTTPException):
        get_current_user(T_Session, token)
