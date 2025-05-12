from .models import User
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreate
from .utils import hash_password


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        res = await session.execute(statement)
        return res.scalars().first()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user: UserCreate, session: AsyncSession):
        user_to_add = User(**user.model_dump())
        user_to_add.password_hash = hash_password(user.password)

        session.add(user_to_add)
        await session.commit()
        await session.refresh(user_to_add)

        return user_to_add
    

def get_user_service():
    return UserService()