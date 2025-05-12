import httpx
from src import app
import pytest
import pytest_asyncio
from sqlmodel import SQLModel
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.main import get_session
import fakeredis
from src.db.redis import token_blocklist
from asgi_lifespan import LifespanManager


@pytest_asyncio.fixture
async def test_db_session():

    engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db",
        connect_args={
            "check_same_thread": False
        },
        poolclass=sqlalchemy.pool.StaticPool
    )

    #tables creation
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def fake_redis_client():
    fake_redis = fakeredis.FakeAsyncRedis(decode_responses=True)
    await fake_redis.flushall()
    yield fake_redis
    await fake_redis.aclose()


@pytest_asyncio.fixture
async def test_app(test_db_session, fake_redis_client, monkeypatch):
    
    monkeypatch.setattr(
            "src.db.redis.token_blocklist",
            fake_redis_client,
            raising=True
        )

    async def get_test_db():
        yield test_db_session
    
    app.dependency_overrides[get_session] = get_test_db

    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url='http://test',
                                    follow_redirects=True) as client:
            yield client

    app.dependency_overrides.clear()
    
