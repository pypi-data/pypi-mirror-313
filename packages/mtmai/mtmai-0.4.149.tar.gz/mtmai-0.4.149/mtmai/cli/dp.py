import asyncio
import click


def register_deploy_commands(cli):
    """部署相关的子命令"""

    @cli.group(invoke_without_command=True)
    @click.pass_context
    def dp(ctx):
        if ctx.invoked_subcommand is None:
            ctx.invoke(default)

    @dp.command()
    def default():
        """
        一键部署
        含:
        1 构建并发布本项目用到的 npm 包（能公开的部分）
        2 pypi 包, 含本项目及另外几个依赖的包
        3 自动将前端代码部署到 vercel 上，和 cloudflare worker (page) 上
        4 构建主 docker 镜像，并推送到 docker hub 上
        5 自动部署本项目到 huggingface space 上 (含前后端)，以单个 docker 容器方式运行
        """
        from mtmai.mtlibs import dev_helper

        asyncio.run(dev_helper.run_deploy())

    @dp.command()
    def cfpage():
        """
        部署 cf page
        """
        from mtmai.mtlibs import dev_helper

        asyncio.run(dev_helper.dp_cfpage())
