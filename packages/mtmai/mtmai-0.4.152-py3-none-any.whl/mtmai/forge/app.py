from typing import Awaitable, Callable

from fastapi import FastAPI
from mtmai.db.db import fix_conn_str
from playwright.async_api import Frame, Page

from mtmai.forge.agent import ForgeAgent
from mtmai.forge.agent_functions import AgentFunction
from mtmai.forge.sdk.api.llm.api_handler_factory import LLMAPIHandlerFactory
from mtmai.forge.sdk.artifact.manager import ArtifactManager
from mtmai.forge.sdk.artifact.storage.factory import StorageFactory
from mtmai.forge.sdk.artifact.storage.s3 import S3Storage
from mtmai.forge.sdk.cache.factory import CacheFactory
from mtmai.forge.sdk.db.client import AgentDB
from mtmai.core.config import settings as mtmai_settings

from mtmai.forge.sdk.experimentation.providers import (
    BaseExperimentationProvider,
    NoOpExperimentationProvider,
)
from mtmai.forge.sdk.models import Organization
from mtmai.forge.sdk.settings_manager import SettingsManager
from mtmai.forge.sdk.workflow.context_manager import WorkflowContextManager
from mtmai.forge.sdk.workflow.service import WorkflowService
from mtmai.webeye.browser_manager import BrowserManager

SETTINGS_MANAGER = SettingsManager.get_settings()
DATABASE = AgentDB(
    # SettingsManager.get_settings().DATABASE_STRING,
    fix_conn_str(mtmai_settings.DATABASE_URL),
    debug_enabled=SettingsManager.get_settings().DEBUG_MODE,
)
if SettingsManager.get_settings().SKYVERN_STORAGE_TYPE == "s3":
    StorageFactory.set_storage(S3Storage())
STORAGE = StorageFactory.get_storage()
CACHE = CacheFactory.get_cache()
ARTIFACT_MANAGER = ArtifactManager()
BROWSER_MANAGER = BrowserManager()
EXPERIMENTATION_PROVIDER: BaseExperimentationProvider = NoOpExperimentationProvider()
LLM_API_HANDLER = LLMAPIHandlerFactory.get_llm_api_handler(
    SettingsManager.get_settings().LLM_KEY
)
SECONDARY_LLM_API_HANDLER = LLMAPIHandlerFactory.get_llm_api_handler(
    SETTINGS_MANAGER.SECONDARY_LLM_KEY
    if SETTINGS_MANAGER.SECONDARY_LLM_KEY
    else SETTINGS_MANAGER.LLM_KEY
)
WORKFLOW_CONTEXT_MANAGER = WorkflowContextManager()
WORKFLOW_SERVICE = WorkflowService()
AGENT_FUNCTION = AgentFunction()
scrape_exclude: Callable[[Page, Frame], Awaitable[bool]] | None = None
authentication_function: Callable[[str], Awaitable[Organization]] | None = None
setup_api_app: Callable[[FastAPI], None] | None = None

agent = ForgeAgent()
