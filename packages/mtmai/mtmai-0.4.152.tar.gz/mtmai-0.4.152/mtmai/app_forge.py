from fastapi import FastAPI
import jwt
from mtmai.core import security

from mtmai.crud import curd
from mtmai.forge.sdk.models import Organization
import structlog

from mtmai.core.config import settings


from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from mtmai.db.db import fix_conn_str
from mtmai.models.models import TokenPayload
from mtmai.config import settings as base_settings
from mtmai.core.config import settings as mtmai_settings

LOG = structlog.stdlib.get_logger()


def setup_forge_app(app: FastAPI):
    LOG.info("setup_forge_app")
    from mtmai.forge.sdk.routes.agent_protocol import base_router
    from mtmai.forge import app as forge_app

    base_settings.DATABASE_STRING = fix_conn_str(mtmai_settings.DATABASE_URL)

    app.include_router(base_router, prefix="/api/v1/forge")

    from mtmai.forge.sdk.routes.streaming import websocket_router

    app.include_router(websocket_router, prefix="/api/v1/stream")

    forge_app.authentication_function = _custom_authentication_function


async def _custom_authentication_function(token: str) -> Organization:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await curd.get_user_by_id2(token_data.sub)
    organization = await curd.get_organization_by_user_id(user.id)
    return organization
    #     organization_id="o_319961449264227090", organization_name="test",
    #     organization_domain="test.com",
    #     organization_type="test",
    #     created_at=datetime.now(),
    #     updated_at=datetime.now(),
    #     modified_at=datetime.now(),
    # )
