from http import HTTPStatus


def test_create_livro(client, token, romancista):
    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': 'Livro Muito Bom',
            'romancista_id': romancista.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'ano': 2024,
        'titulo': 'livro muito bom',
        'romancista_id': 1,
    }


def test_create_livro_already_exists(client, token, romancista, livro):
    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': livro.titulo,
            'romancista_id': romancista.id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já consta no MADR'}


def test_delete_livro(client, token, romancista, livro):
    response = client.delete(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_delete_livro_not_exists(client, token):
    response = client.delete(
        '/livros/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_update_livro(client, token, romancista, livro):
    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 2023},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano': 2023,
        'romancista_id': livro.romancista_id,
    }


def test_update_livro_with_titulo(client, token, romancista, livro):
    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 2023, 'titulo': 'novo titulo'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': 'novo titulo',
        'ano': 2023,
        'romancista_id': livro.romancista_id,
    }


def test_update_livro_with_romancista_id(
    client, token, romancista, other_romancista
):
    livro = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': 'Livro Muito Bom',
            'romancista_id': romancista.id,
        },
    )

    response = client.patch(
        f'/livros/{livro.json()['id']}',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 2023, 'romancista_id': other_romancista.id},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.json()['id'],
        'titulo': 'livro muito bom',
        'ano': 2023,
        'romancista_id': other_romancista.id,
    }


def test_update_livro_not_exists(client, token, romancista, livro):
    response = client.patch(
        '/livros/0',
        headers={'Authorization': f'Bearer {token}'},
        json={'ano': 2023},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_update_livro_title_already_exists(client, token, romancista, livro):
    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': livro.titulo},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já consta no MADR'}


def test_get_livro_by_id(client, token):
    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': 'Livro Muito Bom',
            'romancista_id': 1,
        },
    )

    response = client.get('/livros/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'ano': 2024,
        'titulo': 'livro muito bom',
        'romancista_id': 1,
    }


def test_get_livro_by_id_not_exists(client):
    response = client.get('/livros/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_get_livro_by_search(client, token):
    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': 'Livro Muito Bom',
            'romancista_id': 1,
        },
    )

    response = client.get('/livros?titulo=muito')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['livros'] == [
        {'id': 1, 'ano': 2024, 'titulo': 'livro muito bom', 'romancista_id': 1}
    ]


def test_get_livro_by_search_not_found(client):
    response = client.get('/livros')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['livros'] == []


def test_get_livro_by_search_with_ano(client, token):
    client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'Clarice Lispector'},
    )

    client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': 2024,
            'titulo': 'Livro Muito Bom',
            'romancista_id': 1,
        },
    )

    response = client.get('/livros?titulo=muito&ano=2024')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['livros'] == [
        {'id': 1, 'ano': 2024, 'titulo': 'livro muito bom', 'romancista_id': 1}
    ]
