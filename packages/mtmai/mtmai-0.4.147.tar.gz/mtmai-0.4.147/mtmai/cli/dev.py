"""
开发环境辅助
"""

from mtmai.core.logging import get_logger


def register_dev_commands(cli):
    @cli.command()
    def dev_commands():
        """Database related commands"""
        logger = get_logger()
        logger.info("dev commands")
