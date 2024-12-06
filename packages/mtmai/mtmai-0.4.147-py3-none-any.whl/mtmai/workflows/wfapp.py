import os
import sys
from time import sleep

import structlog
from dotenv import load_dotenv
from mtmai.core.config import settings
from mtmaisdk import ClientConfig, Hatchet, loader

load_dotenv()

LOG = structlog.get_logger()


def new_hatchat(backend_url: str):
    maxRetry = 10
    interval = 5
    for i in range(maxRetry):
        try:
            LOG.info("worker 连接服务器", backend_url=backend_url)
            # 不验证 tls 因后端目前 证数 是自签名的。
            os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
            os.environ["HATCHET_CLIENT_TOKEN"] = settings.HATCHET_CLIENT_TOKEN

            # cc= ClientConfig()
            tls_config = loader.ClientTLSConfig(
                tls_strategy="none",
                cert_file="None",
                key_file="None",
                ca_file="None",
                server_name="localhost",
            )

            config_loader = loader.ConfigLoader(".")
            cc = config_loader.load_client_config(
                ClientConfig(
                    # 提示 client token 本身已经包含了服务器地址（host_port）信息
                    server_url=settings.GOMTM_URL,
                    host_port="0.0.0.0:7070",
                    tls_config=tls_config,
                )
            )

            # 原本的加载器 绑定了 jwt 中的信息，这里需要重新设置
            # cc.host_port="0.0.0.0:7070"
            wfapp = Hatchet.from_config(cc, debug=True)

            return wfapp
        except Exception as e:
            LOG.error(f"failed to create hatchet: {e}")
            if i == maxRetry - 1:
                sys.exit(1)
            sleep(interval)


wfapp = new_hatchat(settings.GOMTM_URL)
