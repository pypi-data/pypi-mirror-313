from mtmai.agents.assisant.assistant_graph import AssistantGraph
from mtmai.agents.chat_profiles.chat_post_gen import PostGenAgent
from mtmai.agents.chat_profiles.home_agent import HomeAgent
from mtmai.agents.task_graph.task_graph import TaskGraph

all_chat_agents = [
    PostGenAgent,
    HomeAgent,
    AssistantGraph,
    TaskGraph,
]


async def get_all_profiles():
    all_profiles = [agent.get_chat_profile() for agent in all_chat_agents]
    return all_profiles


async def get_default_chat_profile():
    return next(
        (profile for profile in await get_all_profiles() if profile.default), None
    )


async def get_chat_profile_by_name(name: str):
    """
    根据名称获取聊天配置, TODO: 可能有问题
    """
    all_profiles = await get_all_profiles()
    return next((profile for profile in all_profiles if profile.name == name), None)


async def get_chat_agent(name: str):
    for agent_class in all_chat_agents:
        if agent_class.name() == name:
            return agent_class()
    return None
