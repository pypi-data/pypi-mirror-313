"""客户端代码生成"""

import json
import logging
from pathlib import Path

from mtmlib.mtutils import bash


def register_gen_commands(cli):
    logger = logging.getLogger()

    @cli.command()
    def gen():
        from mtmai.core.config import settings
        from mtmai.server import build_app

        app = build_app()
        openapi = app.openapi()
        with Path(settings.OPENAPI_JSON_PATH).open("w") as f:
            logger.info(
                "openapi.json exported %s to %s",
                openapi.get("openapi", "unknown version"),
                settings.OPENAPI_JSON_PATH,
            )
            json.dump(openapi, f, indent=2)


        # typescript 客户端库
        bash("cd packages/mtmaiapi && bun run gen")
