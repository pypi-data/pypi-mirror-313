"""部署相关的子命令"""

import asyncio

from mtmai.core.logging import get_logger

logger = get_logger()


def register_init_commands(cli):
    @cli.command()
    def init():
        from mtmai.mtlibs import dev_helper

        asyncio.run(dev_helper.init_project())
