import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from madr.app import app
from madr.database import get_session
from madr.models import Livro, Romancista, User, table_registry
from madr.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.Sequence(lambda n: f'romancista_{n}')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    ano = 2024
    titulo = 'titulo_fake'
    romancista_id = 1


@pytest.fixture
def client(session):
    def test_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = test_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session):
    password = 'password'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # Monkey Path

    return user


@pytest.fixture
def other_user(session: Session):
    password = 'password'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # Monkey Path

    return user


@pytest.fixture
def romancista(session: Session):
    romancista_db = RomancistaFactory()

    session.add(romancista_db)
    session.commit()
    session.refresh(romancista_db)

    return romancista_db


@pytest.fixture
def other_romancista(session: Session):
    romancista_db = RomancistaFactory()

    session.add(romancista_db)
    session.commit()
    session.refresh(romancista_db)

    return romancista_db


@pytest.fixture
def livro(session: Session):
    livro_db = LivroFactory()

    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    return livro_db


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
