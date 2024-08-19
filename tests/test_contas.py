from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/contas',
        json={
            'username': 'test',
            'email': 'test@email.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'test@email.com',
        'username': 'test',
    }


def test_create_user_already_exist(user, client):
    response = client.post(
        '/contas',
        json={
            'username': user.username,
            'email': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


def test_update_user(user, client, token):
    response = client.put(
        f'/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'update',
            'email': 'update@email.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'update',
        'email': 'update@email.com',
    }


def test_update_other_user(user, client, token):
    response = client.put(
        '/contas/0',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'update',
            'email': 'update@email.com',
            'password': 'password',
        },
    )

    response.status_code == HTTPStatus.FORBIDDEN
    response.json() == {'detail': 'Not enough permission'}


def test_update_user_with_credentials_already_exists(
    user, other_user, client, token
):
    response = client.put(
        f'/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': other_user.email,
            'password': 'password',
        },
    )

    response.status_code == HTTPStatus.CONFLICT
    response.json() == {'detail': 'conta já consta no MADR'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_other_user(client, user, token):
    response = client.delete(
        '/contas/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
