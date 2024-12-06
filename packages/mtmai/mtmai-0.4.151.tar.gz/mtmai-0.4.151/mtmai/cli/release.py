"""部署相关的子命令"""

import logging

from mtmlib.mtutils import bash, is_in_gitpod

logger = logging.getLogger()


def register_release_commands(cli):
    """
    释放版本:
    1 发布到 pypi
    2 发布到 npm
    3 发布到 docker hub
    4 发布到 huggingface(未实现)
    """

    @cli.command()
    def release():
        from mtmai.mtlibs import dev_helper

        if is_in_gitpod():
            bash("git pull")
        dev_helper.release_py()
