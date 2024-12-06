"""
前端机器人脚本
"""

from pathlib import Path

import httpx
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

from mtmai.core import coreutils
from mtmai.core.config import settings
from mtmai.core.logging import get_logger
# from mtmai.models.bot import BotConfig

router = APIRouter()
logger = get_logger()


# @router.get("/main.js", include_in_schema=False)
# async def bot_script():
#     """前端机器人脚本"""

#     config_data = BotConfig(
#         baseUrl=coreutils.backend_url_base(),
#         apiPrefix=settings.API_V1_STR,
#         accessToken=settings.ACCESS_TOKEN,
#     )

#     script_chunks = []
#     script_chunks.append(f"const config = {config_data}; window.mtmaiConfig = config;")

#     style_url = config_data.baseUrl + config_data.apiPrefix + "/style.css"
#     if coreutils.is_in_dev():
#         style_url = "https://cdn.jsdelivr.net/npm/mtmaibot/dist/globals.css"
#     script_chunks.append(f"""
#         const styleUrl = '{style_url}';
#         const linkElement = document.createElement('link');
#         linkElement.rel = 'stylesheet';
#         linkElement.href = styleUrl;
#         document.head.appendChild(linkElement);
#     """)

#     if coreutils.is_in_dev():
#         bot_script_path = Path(settings.work_dir) / "packages/mtmaibot/dist/index.js"
#         if not bot_script_path.exists():
#             logger.error(f"Bot script not found: {bot_script_path}")
#             return Response(status_code=404, content="File not found")
#         script_chunks.append(bot_script_path.read_text())
#     else:
#         cdn_script_url = "https://cdn.jsdelivr.net/npm/mtmaibot/dist/index.js"
#         logger.info(f"cdn_script_url: {cdn_script_url}")
#         async with httpx.AsyncClient() as client:
#             response = await client.get(cdn_script_url)
#             script_content = response.text
#         script_chunks.append(script_content)

#     return Response(
#         content="\n".join(script_chunks), media_type="application/javascript"
#     )


# @router.get("/style.cs", include_in_schema=False)
# def bot_style():
#     """前端机器人脚本样式"""
#     bot_script_path = Path(settings.work_dir) / "packages/mtmaibot/dist/globals.css"
#     if not bot_script_path.exists():
#         logger.error(f"Bot script not found: {bot_script_path}")
#         return Response(status_code=404, content="File not found")
#     return FileResponse(str(bot_script_path), media_type="text/css")


# @router.get("/mtmaibot_config", response_model=BotConfig)
# def mtmaibot_config():
#     """前端机器人配置"""

#     data = BotConfig(
#         baseUrl="/login",
#     )
#     return data
