import asyncio
import contextlib
from os import getenv

from core import db_helper, User
from core.database.dto.user import UserCreate
from core.authentication.user_manager import UserManager
from api.dependencies.authentication.users import get_user_db
from api.dependencies.authentication.user_manager import get_user_manager


get_async_session_context = contextlib.asynccontextmanager(db_helper.session_getter)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = getenv("DEFAULT_EMAIL", default="admin@example.com")
default_password = getenv("DEFAULT_PASSWORD", default="1234")
default_is_super: bool = True
default_is_active: bool = True
default_is_verified: bool = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    email: str = default_email,
    password: str = default_password,
    is_superuser: bool = default_is_super,
    is_active: bool = default_is_active,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_superuser=is_superuser,
        is_active=is_active,
        is_verified=is_verified,
    )

    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


if __name__ == "__main__":
    asyncio.run(create_superuser())
