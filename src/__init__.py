from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.logger import logger
from src.auth.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception as e:
        logger.error(f'Unexpected error during DB initialization: {e}')
    yield
    logger.info('App Shutdown')



version = 'v1'
app = FastAPI(version=version, lifespan=lifespan)

app.include_router(auth_router, prefix=f'/api/{version}/auth')


