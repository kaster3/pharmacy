from fastapi import APIRouter

from core import settings
from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.my_fastapi_users import fastapi_users
from core.database.dto.user import UserCreate, UserRead

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login, /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=False,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)


# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(
        UserRead,
    ),
)

# forgot-password
# reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
