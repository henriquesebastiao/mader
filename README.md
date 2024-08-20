# Meu Acervo Digital de Romances

[![CI](https://github.com/henriquesebastiao/madr/actions/workflows/ci.yml/badge.svg)](https://github.com/henriquesebastiao/madr/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/henriquesebastiao/madr/graph/badge.svg?token=h1LHjY5hZb)](https://codecov.io/gh/henriquesebastiao/madr)
[![codecov](https://img.shields.io/badge/python-3.12.4-blue)]()
[![codecov](https://img.shields.io/badge/fastapi-0.112.1-blue)]()

Link do deploy: [http://server.henriquesebastiao.com:8093/docs](http://server.henriquesebastiao.com:8093/docs)

Projeto final do curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/)

## Endpoints

### Autenticação e autorização

- POST `/token`
- POST `/token_refresh`

### Contas

- POST `/contas/`

```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

- PUT `/contas/{user_id}`

```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

- DELETE `/contas/{user_id}`

### Romancistas

- POST `/romancistas/`

```json
{
  "nome": "string"
}
```

- GET `/romancistas?nome=xxx`
- GET `/romancistas/{romancista_id}`

- PATCH `/romancistas/{romancista_id}`

```json
{
  "nome": "string"
}
```

- DELETE `/romancistas/{romancista_id}`

### Livros

- POST `/livros/`

```json
{
  "ano": 0,
  "titulo": "string",
  "romancista_id": 0
}
```

- GET `/livros/{livro_id}`
- GET `/livros?titulo=xxx&ano=iiii`

- PATCH `/livros/{livro_id}`

```json
{
  "ano": 0,
  "titulo": "string",
  "romancista_id": 0
}
```

- DELETE `/livros/{livro_id}`
