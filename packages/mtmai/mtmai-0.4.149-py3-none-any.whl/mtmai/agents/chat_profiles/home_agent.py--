from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field

import mtmai.chainlit as cl
from mtmai.agents.graphutils import is_internal_node, is_skip_kind
from mtmai.chainlit import context
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


class get_current_weather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


@tool(parse_docstring=False, response_format="content_and_artifact")
def home_ui_tool():
    """通过调用此工具，可以展示不同的UI 面板，当用户有需要时可以调用这个函数向用户显示不同的操作面板"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


class HomeAgent:
    """
    首页 聊天机器人
    1: 相当于客服的功能
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        return {}

    @classmethod
    def name(cls):
        return "HomeAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="HomeAgent",
            description="助手聊天机器人",
        )

    async def chat_start(self):
        user_session = cl.user_session
        thread_id = context.session.thread_id

        # 实验： 使用crawai
        # crew = DemoCrew()
        # result = await crew.run()
        # await cl.Message(content=result).send()

        # 实验2:
        # book_flow = BookFlow()
        # plot = book_flow.plot()
        # await task_gen_book()

        # graph = await ChatGraph().get_compiled_graph()
        # assistant_config = mtmai_context.graph_config.assistants[0]
        # primary_assistant = AssistantNode(assistant_config)
        # graph = await primary_assistant.compile_graph()
        # user_session.set("graph", graph)

        # thread: RunnableConfig = {
        #     "configurable": {
        #         "thread_id": thread_id,
        #     }
        # }
        # await self.run_graph(thread, {"messages": []})

    async def on_message(self, message: cl.Message):
        try:
            user_session = cl.user_session
            thread_id = context.session.thread_id

            graph: CompiledGraph = user_session.get("graph")
            if not graph:
                cl.Message(content="工作流初始化失败").send()
                raise ValueError("graph 未初始化")
            thread: RunnableConfig = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }
            pre_state = await graph.aget_state(thread, subgraphs=True)
            if not pre_state.next:
                logger.info("流程已经结束")
                await context.emitter.emit(
                    "logs",
                    {
                        "message": "流程已经结束",
                    },
                )
                cl.Message(content="流程已经结束").send()
                return
            await graph.aupdate_state(
                thread,
                {
                    **pre_state.values,
                    "user_input": message.content,
                },
                # as_node="primary_assistant",
            )
            await self.run_graph(thread)
        except Exception as e:
            import traceback

            error_message = f"An error occurred: {str(e)}\n\nDetailed traceback:\n{traceback.format_exc()}"
            logger.error(error_message)
            await cl.Message(content=error_message).send()

    async def run_graph(
        self,
        thread: RunnableConfig,
        inputs=None,
    ):
        user_session = cl.user_session
        graph = user_session.get("graph")
        if not graph:
            raise ValueError("graph 未初始化")

        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            if not is_internal_node(node_name):
                if not is_skip_kind(kind):
                    logger.info("[event] %s@%s", kind, node_name)
            # if kind == "on_chat_model_end":
            #     output = data.get("output")
            #     if output:
            #         chat_output = output.content
            #         if chat_output:
            #             await cl.Message("node_name:"+node_name+"\n"+chat_output).send()

            if kind == "on_chain_end":
                output = data.get("output")

                if node_name == "on_chat_start_node":
                    thread_ui_state = output.get("thread_ui_state")
                    if thread_ui_state:
                        await context.emitter.emit(
                            "ui_state_upate",
                            jsonable_encoder(thread_ui_state),
                        )

                if node_name == "LangGraph":
                    logger.info("中止节点")
                    if (
                        data
                        and (output := data.get("output"))
                        and (final_messages := output.get("messages"))
                    ):
                        for message in final_messages:
                            message.pretty_print()
                        await context.emitter.emit(
                            "logs",
                            {
                                "on": "中止",
                                "node_name": node_name,
                                "output": message.pretty_print(),
                            },
                        )

            if kind == "on_tool_start":
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                    },
                )

            if kind == "on_tool_end":
                output = data.get("output")
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                        "output": jsonable_encoder(output),
                    },
                )
