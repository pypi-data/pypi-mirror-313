import asyncio

import click

# from mtmai.core.bootstraps import bootstrap_core  # noqa: E402

# bootstrap_core()


def main():
    # from mtmai.cli.build import register_build_commands
    # from mtmai.cli.clean import register_clean_commands
    # from mtmai.cli.db import register_db_commands
    # from mtmai.cli.dp import register_deploy_commands
    # from mtmai.cli.gen import register_gen_commands
    # from mtmai.cli.init import register_init_commands
    # from mtmai.cli.release import register_release_commands
    # from mtmai.cli.selenium import register_selenium_commands

    @click.group()
    def cli():
        pass

    # register_build_commands(cli)
    # register_clean_commands(cli)
    # register_db_commands(cli)
    # register_deploy_commands(cli)
    # register_gen_commands(cli)
    # register_init_commands(cli)
    # register_release_commands(cli)
    # register_selenium_commands(cli)

    # register_serve_commands(cli)
    # def register_serve_commands(cli):
    @cli.command()
    def serve():
        import asyncio

        from mtmai.core.config import settings
        from mtmai.core.logging import get_logger
        from mtmai.server import serve

        logger = get_logger()
        logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
        asyncio.run(serve())

    @cli.command()
    @click.option("--url", required=False)
    def worker(url):
        print("start worker with url: ", url)
        from mtmai.workflows.workers import deploy_mtmai_workers

        asyncio.run(deploy_mtmai_workers(url))

    @cli.command()
    def mcpserver():
        from mtmai.mtmcp.server import run_default_mcp_server

        asyncio.run(run_default_mcp_server())

    # register_tunnel_commands(cli)
    # register_dev_commands(cli)
    # register_agent_worker_commands(cli)
    cli()


if __name__ == "__main__":
    main()
