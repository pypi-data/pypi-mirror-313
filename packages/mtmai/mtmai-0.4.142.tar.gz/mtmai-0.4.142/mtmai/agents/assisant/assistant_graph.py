from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel, Field

import mtmai.chainlit as cl
from mtmai.agents.assisant.assisant_state import AssistantState
from mtmai.agents.assisant.nodes.assisant_node import (
    PrimaryAssistantNode,
    primary_assistant_tools,
    route_assistant,
)
from mtmai.agents.assisant.nodes.entry_node import EntryNode
from mtmai.agents.ctx import init_mtmai_http_context, mtmai_context
from mtmai.agents.graphutils import (
    create_tool_node_with_fallback,
    pop_dialog_state,
)
from mtmai.chainlit import context
from mtmai.core.coreutils import is_in_dev
from mtmai.core.logging import get_logger

logger = get_logger()


class ToFlightBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle flight updates and cancellations."""

    request: str = Field(
        description="Any necessary followup questions the update flight assistant should clarify before proceeding."
    )


class ToDevelopAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle development tasks."""

    request: str = Field(
        description="Any necessary followup questions or specific development tasks the developer assistant should address."
    )


class ToBookCarRental(BaseModel):
    """Transfers work to a specialized assistant to handle car rental bookings."""

    location: str = Field(
        description="The location where the user wants to rent a car."
    )
    start_date: str = Field(description="The start date of the car rental.")
    end_date: str = Field(description="The end date of the car rental.")
    request: str = Field(
        description="Any additional information or requests from the user regarding the car rental."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Basel",
                "start_date": "2023-07-01",
                "end_date": "2023-07-05",
                "request": "I need a compact car with automatic transmission.",
            }
        }


class ToHotelBookingAssistant(BaseModel):
    """Transfer work to a specialized assistant to handle hotel bookings."""

    location: str = Field(
        description="The location where the user wants to book a hotel."
    )
    checkin_date: str = Field(description="The check-in date for the hotel.")
    checkout_date: str = Field(description="The check-out date for the hotel.")
    request: str = Field(
        description="Any additional information or requests from the user regarding the hotel booking."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Zurich",
                "checkin_date": "2023-08-15",
                "checkout_date": "2023-08-20",
                "request": "I prefer a hotel near the city center with a room that has a view.",
            }
        }


class ToBookExcursion(BaseModel):
    """Transfers work to a specialized assistant to handle trip recommendation and other excursion bookings."""

    location: str = Field(
        description="The location where the user wants to book a recommended trip."
    )
    request: str = Field(
        description="Any additional information or requests from the user regarding the trip recommendation."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Lucerne",
                "request": "The user is interested in outdoor activities and scenic views.",
            }
        }


class AssistantGraph:
    def __init__(self):
        pass

    @classmethod
    def name(cls):
        return "assistant"

    async def chat_start(self):
        init_mtmai_http_context()
        user_session = cl.user_session
        user = user_session.get("user")
        thread_id = context.session.thread_id
        # await cl.Message(content="欢迎使用博客文章生成器").send()
        # await cl.Message(content=f"你是：{user.email}").send()

        graph = await AssistantGraph().compile_graph()
        # assistant_config = mtmai_context.graph_config.assistants[0]
        # primary_assistant = AssistantNode(assistant_config)
        # graph = await primary_assistant.compile_graph()

        user_session.set("graph", graph)

        # thread: RunnableConfig = {
        #     "configurable": {
        #         "thread_id": thread_id,
        #     }
        # }
        # await self.run_graph(thread, {"messages": []})

    async def build_graph(self):
        wf = StateGraph(AssistantState)

        wf.add_node("entry", EntryNode())
        wf.add_edge("entry", "assistant")
        wf.set_entry_point("entry")

        wf.add_node("assistant", PrimaryAssistantNode())

        wf.add_conditional_edges(
            "assistant",
            tools_condition,
        )

        wf.add_node(
            "tools",
            create_tool_node_with_fallback(primary_assistant_tools),
        )
        wf.add_conditional_edges(
            "tools",
            route_assistant,
            {
                "assistant": "assistant",
                # "error": END,
            },
        )
        wf.add_node("leave_skill", pop_dialog_state)
        wf.add_edge("leave_skill", "assistant")

        return wf

    async def compile_graph(self) -> CompiledGraph:
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            interrupt_before=[
                # "human_chat",
                # "update_flight_sensitive_tools",
                # "develop_sensitive_tools",
                # "book_car_rental_sensitive_tools",
                # "book_hotel_sensitive_tools",
                # "book_excursion_sensitive_tools",
            ],
            debug=True,
        )

        if is_in_dev():
            image_data = graph.get_graph(xray=1).draw_mermaid_png()
            save_to = "./.vol/assistant_graph.png"
            with open(save_to, "wb") as f:
                f.write(image_data)
        return graph

    # async def run_graph(
    #     self,
    #     messages: list[AnyMessage] = [],
    #     # thread_id: str | None = None,
    #     user_id: str | None = None,
    #     params: dict | None = None,
    # ):
    #     await cl.Message(content="欢迎使用博客文章生成器").send()
    #     graph = await self.compile_graph()
    #     inputs = {
    #         "messages": messages,
    #         "userId": user_id,
    #         "params": params,
    # }
    # await mtmai_context.init_mq()

    # async for event in graph.astream_events(
    #     inputs,
    #     version="v2",
    #     config={
    #         "configurable": {
    #             "thread_id": mtmai_context.thread_id,
    #         }
    #     },
    #     subgraphs=True,
    # ):
    #     kind = event["event"]
    #     node_name = event["name"]
    #     data = event["data"]

    #     if kind == "on_chat_model_stream":
    #         # send_chat_event()
    #         # content = event["data"]["chunk"].content
    #         # if content:
    #         # yield aisdk.data(event)
    #         await mtmai_context.mq.send_event(event)
    #     else:
    #         # yield aisdk.data(event)
    #         pass
    async def on_message(self, message: cl.Message):
        init_mtmai_http_context()
        # user_session = cl.user_session
        # graph = user_session.get("graph")
        # if not graph:
        #     raise ValueError("graph 未初始化")
        # logger.info("on_message: %s", json.dumps(jsonable_encoder(message), indent=4))
        # init_mtmai_http_context()

        # active_steps = context.active_steps
        # logger.info(
        #     "active_steps: %s",
        #     json.dumps(
        #         jsonable_encoder(
        #             {
        #                 "incoming_message": message,
        #                 "active_steps": active_steps,
        #             }
        #         ),
        #         indent=4,
        #     ),
        # )
        user_session = cl.user_session
        thread_id = context.session.thread_id
        graph = user_session.get("graph")
        graph2 = user_session.get("chat_agent")

        # graph: CompiledGraph = user_session.get("graph")
        # graph = await self.compile_graph()
        # if not graph:
        #     cl.Message(content="工作流初始化失败").send()
        #     raise ValueError("graph 未初始化")

        # is_new = not thread_id
        # if not thread_id:
        #     thread_id = uuid.uuid4()

        # TODO：使用 first_interaction 来判断是否是第一次交互, 更加合适
        # if not is_new:
        #     pre_state = await graph.aget_state(
        #         {
        #             "configurable": {
        #                 "thread_id": thread_id,
        #             }
        #         },
        #         subgraphs=True,
        #     )
        #     await graph.aupdate_state(
        #         {
        #             "configurable": {
        #                 "thread_id": thread_id,
        #             }
        #         },
        #         {
        #             **pre_state.values,
        #             "user_input": message.content,
        #         },
        #         as_node="entry",
        #     )
        #     # if not pre_state.next:
        #     #     logger.info("流程已经结束")
        #     #     await context.emitter.emit(
        #     #         "logs",
        #     #         {
        #     #             "message": "流程已经结束",
        #     #         },
        #     #     )
        #     #     await cl.Message(content="出错: 因流程已经结束").send()
        #     #     return

        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        # await graph.aupdate_state(
        #     thread,
        #     {
        #         "user_input": message.content,
        #     },
        #     as_node="entry",
        # )
        # await mtmai_context.init_mq()

        # 流式传输过程：
        # 1. 先发送一个消息，让前端立即显示ai消息占位，后续流程处理可随时更新这个消息，包括流式传输。
        # 2. 一旦整个流程结束，再次调用 .send()，触发消息的持久化。

        resp_msg = cl.Message(content="")
        await resp_msg.send()

        input = {
            "user_input": message.content,
        }
        async for event in graph.astream_events(
            input=input,
            config=thread,
            version="v2",
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    await resp_msg.stream_token(content)

            if kind == "on_chat_model_end":
                output = data.get("output")
                if output:
                    chat_output = output.content
                    await resp_msg.send()
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
                                "output": jsonable_encoder(message),
                            },
                        )
