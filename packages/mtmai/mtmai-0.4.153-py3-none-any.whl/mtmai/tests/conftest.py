import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from sqlmodel.pool import StaticPool

from mtmai.core.config import settings
from mtmai.db.db import init_db
from mtmai.cli.seed import seed_db

# from mtmai.server import build_app
from mtmai.tests.utils.user import authentication_token_from_email
from mtmai.tests.utils.utils import get_superuser_token_headers

os.environ["PYTEST_CURRENT_TEST"] = "1"
print(
    "testing start ========================================================================================================="
)


@pytest.fixture(scope="module")
def engine() -> Generator:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine

    print("==================================drop db")
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite://", connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="module")
async def asession(async_engine) -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=SQLModelAsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# @pytest.fixture(scope="session")
@pytest.fixture(scope="module")
def db(engine) -> Generator:
    with Session(engine) as session:
        seed_db(session)
        init_db(session)
        yield session


def override_get_db(db: Session):
    def _override_get_db() -> Generator[Session, None, None]:
        yield db

    return _override_get_db


# @pytest.fixture(scope="module")
# def client(db: Session) -> Generator[TestClient, None, None]:
#     app = build_app()
#     app.dependency_overrides[get_db] = override_get_db(db)
#     with TestClient(app) as c:
#         yield c
#     app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
async def normal_user_token_headers(
    client: TestClient, db: AsyncSession
) -> dict[str, str]:
    return await authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


# # chainlit 相关
# from contextlib import asynccontextmanager
# from unittest.mock import AsyncMock, Mock

# import pytest
# import pytest_asyncio

# from mtmai.chainlit.context import ChainlitContext, context_var
# from mtmai.chainlit.session import HTTPSession, WebsocketSession
# from mtmai.chainlit.user import PersistedUser
# from mtmai.chainlit.user_session import UserSession


# @asynccontextmanager
# async def create_chainlit_context():
#     mock_session = Mock(spec=WebsocketSession)
#     mock_session.id = "test_session_id"
#     mock_session.user_env = {"test_env": "value"}
#     mock_session.chat_settings = {}
#     mock_user = Mock(spec=PersistedUser)
#     mock_user.id = "test_user_id"
#     mock_session.user = mock_user
#     mock_session.chat_profile = None
#     mock_session.http_referer = None
#     mock_session.client_type = "webapp"
#     mock_session.languages = ["en"]
#     mock_session.thread_id = "test_thread_id"
#     mock_session.emit = AsyncMock()
#     mock_session.has_first_interaction = True

#     context = ChainlitContext(mock_session)
#     token = context_var.set(context)
#     try:
#         yield context
#     finally:
#         context_var.reset(token)


# @pytest_asyncio.fixture
# async def mock_chainlit_context():
#     return create_chainlit_context()


# @pytest.fixture
# def user_session():
#     return UserSession()


# @pytest.fixture
# def mock_websocket_session():
#     session = Mock(spec=WebsocketSession)
#     session.emit = AsyncMock()

#     return session


# @pytest.fixture
# def mock_http_session():
#     return Mock(spec=HTTPSession)
