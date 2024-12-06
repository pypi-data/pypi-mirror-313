import uuid
from typing import Annotated, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.message import AnyMessage, add_messages

import mtmai.chainlit as cl
from mtmai.agents.ctx import mtmai_context
from mtmai.agents.nodes.hello_node import NodeHello
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState
from mtmai.mtlibs import aisdk

logger = get_logger()


class HelloState(TypedDict):
    messages: Annotated[list, add_messages]
    some_value: str | None


class HelloGraph:
    def __init__(self):
        # self.assistant_config = assistant_config
        pass

    async def build_graph(self):
        # llm_runnable = await mtmai_context.get_llm_openai("chat")
        wf = StateGraph(HelloState)
        # wf.set_entry_point(chatbot)
        # wf.add_node(chatbot, self)

        wf.add_node("hello", NodeHello())
        wf.set_entry_point("hello")

        return wf

    async def compile_graph(self):
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            # interrupt_before=[
            #     "human_chat",
            #     # "update_flight_sensitive_tools",
            #     # "develop_sensitive_tools",
            #     # "book_car_rental_sensitive_tools",
            #     # "book_hotel_sensitive_tools",
            #     # "book_excursion_sensitive_tools",
            # ],
            debug=True,
        )

        image_data = graph.get_graph(xray=1).draw_mermaid_png()
        save_to = "./graph.png"
        with open(save_to, "wb") as f:
            f.write(image_data)
        return graph

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        prompt_tpl = await self.get_prompt(state)
        tools = []

        dialog_state = state.dialog_state
        if dialog_state != "pop":
            ai_msg = await mtmai_context.ainvoke_model(prompt_tpl, state, tools=tools)

            if ai_msg.content:
                await cl.Message("primary:" + ai_msg.content).send()
            return {"messages": ai_msg}
        else:
            # 下级的assistant 本身是直接回复用户，所以这里不需要再回复用户
            return {"messages": []}

    async def run_graph(
        self,
        # thread: RunnableConfig,
        messages: list[AnyMessage] = [],
        # thread_id: str | None = None,
        # user: User | None = None,
    ):
        graph = await self.compile_graph()
        inputs = {
            "messages": messages,
        }

        # if not thread_id:
        thread_id = str(uuid.uuid4())
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            yield aisdk.data(event)
            # if not is_internal_node(node_name):
            #     if not is_skip_kind(kind):
            #         logger.info("[event] %s@%s", kind, node_name)

            # if kind == "on_chat_model_stream":
            #     content = event["data"]["chunk"].content
            #     if content:
            #         yield aisdk.text(content)
