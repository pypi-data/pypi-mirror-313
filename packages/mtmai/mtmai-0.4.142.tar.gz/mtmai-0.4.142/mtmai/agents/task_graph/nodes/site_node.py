from langchain_core.runnables import RunnableConfig

from mtmai.agents.task_graph.task_state import ArticleArtifact, TaskState
from mtmai.core.logging import get_logger
from mtmai.agents.agentfuncs import agentfuncs
logger = get_logger()


class SiteNode:
    """
    站点自动托管入口节点
    """
    def __init__(self):
        pass

    async def __call__(self, state: TaskState, config: RunnableConfig):
        logger.info("进入 site node")

        site_detect_info = await agentfuncs.site_info_detect(state.task_config.get("siteUrl"))
        return {
            "human_ouput_message": "整站文章生成自动托管",
            # "artifacts": [article_artifact.model_dump()],
        }
