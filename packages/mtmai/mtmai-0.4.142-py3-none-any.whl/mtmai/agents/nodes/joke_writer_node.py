import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

import mtmai.chainlit as cl
from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import ResearchState

logger = get_logger()


class JokeContent(BaseModel):
    content: str = Field(
        description="Joke content.",
    )


class JokeWriterNode:
    state: ResearchState = None

    def __init__(self):
        pass

    def node_name(self):
        return "joke_writer"

    @cl.step(name="笑话生成-图入口")
    async def __call__(self, state: ResearchState, config: RunnableConfig):
        logger.info("进入 joke writer node")
        topic = state["prompt"]
        self.state = state
        write_joke_result = await self.write_joke_article(topic)

        return {
            **state,
            "joke_content": json.dumps(write_joke_result),
        }

    @cl.step(name="笑话生成-正文编写")
    async def write_joke_article(self, topic: str):
        """初始化大纲"""
        ctx = get_mtmai_ctx()
        # parser = PydanticOutputParser(pydantic_object=Outline)
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a witty and humorous joke generator. Please create a joke based on the given topic. The joke should be amusing and elicit laughter. "
                    "[ IMPORTANT ]:"
                    "\n- 必须使用简体中文"
                    "\n- Content length should be suitable for mobile device screens"
                    "\n- The joke should be witty and humorous, provoking laughter"
                    "\n- The content should be positive and uplifting, avoiding vulgarity"
                    "\n- The joke should be wholesome, free from violence, sexual content, or other inappropriate themes"
                    "\n- Ensure the joke is family-friendly and suitable for all audiences",
                ),
                ("user", "{topic}"),
            ]
        )
        ai_response = await ctx.call_model_chat(
            direct_gen_outline_prompt, {"topic": topic}
        )
        return {
            "joke_content": ai_response.content,
        }

        # loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
        # outline: Outline = Outline.model_validate(loaded_data)
        # return outline
