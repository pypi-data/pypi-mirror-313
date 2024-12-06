import asyncio
import logging

logger = logging.getLogger()


def register_selenium_commands(cli):
    @cli.command()
    def selenium():
        from mtmai.mtlibs.server.selenium import start_selenium_server

        asyncio.run(start_selenium_server())
