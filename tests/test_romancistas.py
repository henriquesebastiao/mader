from http import HTTPStatus


def test_create_romancista(client, token):
    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'clarice lispector',
    }


def test_create_romancista_already_exists(client, token, romancista):
    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': romancista.nome},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_get_romancista_by_id(client, romancista):
    response = client.get(f'/romancistas/{romancista.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancista.id,
        'nome': romancista.nome,
    }


def test_get_romancista_by_id_not_exists(client):
    response = client.get('/romancistas/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_update_romancista(client, romancista, token):
    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'nome': 'clarice lispector',
    }


def test_update_romancista_not_exists(client, token):
    response = client.patch(
        '/romancistas/0',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_update_romancista_nome_already_exists(client, romancista, token):
    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': romancista.nome},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_delete_romancista(client, token, romancista):
    response = client.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado do MADR'}


def test_delete_romancista_not_exists(client, token):
    response = client.delete(
        '/romancistas/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_get_romancistas_by_search(client, token):
    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Manuel Bandeira'},
    )

    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Paulo Leminski'},
    )

    response = client.get('/romancistas?nome=a')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['romancistas'] == [
        {'nome': 'clarice lispector', 'id': 1},
        {'nome': 'manuel bandeira', 'id': 2},
        {'nome': 'paulo leminski', 'id': 3},
    ]
