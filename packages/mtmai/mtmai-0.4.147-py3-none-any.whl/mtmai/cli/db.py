"""
数据库相关操作
"""

import asyncio

import click


def register_db_commands(cli):
    @cli.group(invoke_without_command=True)
    @click.pass_context
    def db(ctx):
        if ctx.invoked_subcommand is None:
            ctx.invoke(default)

    @db.command()
    def default():
        """Database related commands"""
        from mtmai.cli.seed import init_database

        asyncio.run(init_database())
