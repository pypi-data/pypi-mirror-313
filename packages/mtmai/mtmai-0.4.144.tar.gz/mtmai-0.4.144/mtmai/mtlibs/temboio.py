import asyncio
import json
import logging
import re
from pathlib import Path

import httpx
from fastapi import APIRouter
from mtmlib.mtutils import bash

from mtmai.core.config import settings
from mtmai.mtlibs import mtutils

router = APIRouter()

logger = logging.getLogger()


# api 文档:  https://api.tembo.io/swagger-ui/#/instance/patch_instance


def get_pyproject_version(pyprojectTomlPath: str = "pyproject.toml"):
    content = Path(pyprojectTomlPath).read_text()
    match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
    if not match:
        msg = "版本号未在 pyproject.toml 中找到"
        raise ValueError(msg)
    return match.group(1)


async def docker_build_mtmai():
    project_version = mtutils.get_pyproject_version("pyprojects/mtmai/pyproject.toml")
    logger.info("当前项目版本 %s", project_version)

    await asyncio.to_thread(
        bash,
        f"""docker build --progress=plain -t {settings.DOCKER_IMAGE_TAG} --no-cache --build-arg DOCKERHUB_USER=gitgit188 --target temboapi -f docker/temboapi/Dockerfile . \
        && docker push {settings.DOCKER_IMAGE_TAG} \
        && docker tag {settings.DOCKER_IMAGE_TAG} {settings.DOCKER_IMAGE_TAG}:{project_version}\
        && docker push {settings.DOCKER_IMAGE_TAG}:{project_version} """,
    )


async def run_tmpbo_instance1():
    python_project_dir = "pyprojects/mtmai"
    project_version = mtutils.get_pyproject_version(
        str(Path(python_project_dir).joinpath("pyproject.toml"))
    )
    await asyncio.to_thread(
        bash,
        f"cd {python_project_dir} && poetry export --format requirements.txt --output requirements.txt --without-hashes --without dev",
    )
    await docker_build_mtmai()

    logger.info("应用 tembo %s/%s", settings.TEMBO_ORG, settings.TEMBO_INST)
    logger.info("HUGGINGFACEHUB_API_TOKEN %s", settings.HUGGINGFACEHUB_API_TOKEN)

    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            url=f"https://api.tembo.io/api/v1/orgs/{settings.TEMBO_ORG}/instances/{settings.TEMBO_INST}",
            headers={"Authorization": f"Bearer {settings.TEMBO_TOKEN}"},
            json={
                "app_services": [
                    {
                        "custom": {
                            "image": f"{settings.DOCKER_IMAGE_TAG}:{project_version}",
                            "name": "tmpboaiv3",
                            "routing": [
                                {
                                    "port": 8000,
                                    "ingressPath": "/api",
                                },
                            ],
                            "env": [
                                {"name": "PORT", "value": "8000"},
                                {"name": "INTEMBO", "value": "1"},
                                {
                                    "name": "DATABASE_URL",
                                    "value": settings.DATABASE_URL,
                                },
                                {
                                    "name": "LANGFLOW_DATABASE_URL",
                                    "value": settings.DATABASE_URL,
                                },
                                {
                                    "name": "CF_TUNNEL_TOKEN",
                                    "value": settings.CF_TUNNEL_TOKEN_TEMBO,
                                },
                                {
                                    "name": "MAIN_GH_TOKEN",
                                    "value": settings.MAIN_GH_TOKEN,
                                },
                                {
                                    "name": "MAIN_GH_USER",
                                    "value": settings.MAIN_GH_USER,
                                },
                                {
                                    "name": "GITHUB_CLIENT_ID",
                                    "value": settings.GITHUB_CLIENT_ID,
                                },
                                {
                                    "name": "GITHUB_CLIENT_SECRET",
                                    "value": settings.GITHUB_CLIENT_SECRET,
                                },
                                {
                                    "name": "HUGGINGFACEHUB_API_TOKEN",
                                    "value": settings.HUGGINGFACEHUB_API_TOKEN,
                                },
                                {
                                    "name": "SEARXNG_URL_BASE",
                                    "value": settings.SEARXNG_URL_BASE,
                                },
                                {
                                    "name": "GROQ_TOKEN",
                                    "value": settings.GROQ_TOKEN,
                                },
                                {
                                    "name": "TOGETHER_TOKEN",
                                    "value": settings.TOGETHER_TOKEN,
                                },
                                {
                                    "name": "CLOUDFLARE_AI_TOKEN",
                                    "value": settings.CLOUDFLARE_AI_TOKEN,
                                },
                                {
                                    "name": "CHAINLIT_AUTH_SECRET",
                                    "value": settings.CHAINLIT_AUTH_SECRET,
                                },
                                {"name": "MTM_DATA_DIR", "value": "/app/storage"},
                            ],
                            "resources": {
                                "requests": {"cpu": "500m", "memory": "2000Mi"},
                                "limits": {"cpu": "4000m", "memory": "4000Mi"},
                            },
                            "storage": {
                                "volumeMounts": [
                                    {
                                        "mountPath": "/app/storage",
                                        "name": "hf-model-vol",
                                    },
                                    {
                                        "mountPath": "/home/user",
                                        "name": "user-home",
                                    },
                                    {
                                        "mountPath": "/tmp",  # noqa: S108
                                        "name": "tmp",
                                    },
                                ],
                                "volumes": [
                                    {
                                        "name": "hf-model-vol",
                                        "ephemeral": {
                                            "volumeClaimTemplate": {
                                                "spec": {
                                                    "accessModes": ["ReadWriteOnce"],
                                                    "resources": {
                                                        "requests": {"storage": "10Gi"}
                                                    },
                                                }
                                            }
                                        },
                                    },
                                    {
                                        "name": "user-home",
                                        "ephemeral": {
                                            "volumeClaimTemplate": {
                                                "spec": {
                                                    "accessModes": ["ReadWriteOnce"],
                                                    "resources": {
                                                        "requests": {"storage": "10Gi"}
                                                    },
                                                }
                                            }
                                        },
                                    },
                                    {
                                        "name": "tmp",
                                        "ephemeral": {
                                            "volumeClaimTemplate": {
                                                "spec": {
                                                    "accessModes": ["ReadWriteOnce"],
                                                    "resources": {
                                                        "requests": {"storage": "2Gi"}
                                                    },
                                                }
                                            }
                                        },
                                    },
                                ],
                            },
                        }
                    },
                ]
            },
        )
        resp.raise_for_status()

    json_data = resp.json()
    log_file1 = Path(settings.storage_dir).joinpath("tembo1.log")
    Path(log_file1).write_text(json.dumps(json_data, indent=2))
    logger.info("tempo.io state file: %s", log_file1)
    return {"ok": True}
