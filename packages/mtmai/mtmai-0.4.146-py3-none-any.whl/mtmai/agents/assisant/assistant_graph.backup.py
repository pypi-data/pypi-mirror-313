import uuid
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel, Field

import mtmai.chainlit as cl
from mtmai.agents.ctx import mtmai_context
from mtmai.agents.graphutils import (
    create_entry_node,
    create_tool_node_with_fallback,
    is_internal_node,
    is_skip_kind,
    pop_dialog_state,
)
from mtmai.agents.nodes.node_human import HumanNode
from mtmai.agents.tools.tools import search_flights
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import Assistant, HomeChatState
from mtmai.models.models import User
from mtmai.mtlibs import aisdk

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


primary_assistant_tools = [
    # TavilySearchResults(max_results=1),
    search_flights,
    # lookup_policy,
]


class AssistantGraph:
    def __init__(self, assistant_config: Assistant):
        self.assistant_config = assistant_config

    async def get_prompt(self, state: HomeChatState):
        primary_assistant_prompt = ChatPromptTemplate.from_messages(
            [
                # (
                #     "system",
                #     "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                #     "Your primary role is to search for flight information and company policies to answer customer queries. "
                #     "If a customer requests to update or cancel a flight, book a car rental, book a hotel, or get trip recommendations, "
                #     "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                #     " Only the specialized assistants are given permission to do this for the user."
                #     "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                #     "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                #     " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                #     " If a search comes up empty, expand your search before giving up."
                #     "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                #     "\n 必须使用中文回复用户"
                #     "\nCurrent time: {time}."
                #     "{additional_instructions}",
                # ),
                (
                    "system",
                    "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                    "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                    " Only the specialized assistants are given permission to do this for the user."
                    "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                    "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    " If a search comes up empty, expand your search before giving up."
                    "\n 必须使用中文回复用户"
                    "\nCurrent time: {time}."
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())
        return primary_assistant_prompt

    def is_primary_assistant(self):
        # TODO: 正确识别根节点
        return self.assistant_config.id == "assistant_1"

    async def build_children_graphs(self):
        compile_sub_graphs = []
        if self.assistant_config.children:
            for sub_assistant in self.assistant_config.children:
                sub_node = AssistantGraph(sub_assistant)
                sub_graph = await sub_node.build_graph()
                compile_sub_graphs.append(sub_graph)
        return compile_sub_graphs

    async def build_graph(self):
        logger.info("开始构建 assistent 图: %s", self.assistant_config.id)
        llm_runnable = await mtmai_context.get_llm_openai("chat")
        wf = StateGraph(HomeChatState)
        # wf.add_node("on_chat_start_node", OnChatStartNode(llm_runnable))
        # wf.set_entry_point("on_chat_start_node")

        # wf.add_conditional_edges("on_chat_start_node", route_to_workflow)
        # wf.add_edge("on_chat_start_node", "primary_assistant")
        node_name = "assistant_" + self.assistant_config.name
        tool_node_name = "tools_" + self.assistant_config.name

        def route_assistant(
            state: HomeChatState,
        ):
            route = tools_condition(state)
            if route == END:
                # 这里的工具调用名称，本质是路由表达
                # 如果没有路由，则转到 human_chat 节点，获取用户新输入的消息
                # return END
                return "human_chat"
            tool_calls = state.messages[-1].tool_calls
            if tool_calls:
                route_to = tool_calls[0]["name"]
                logger.info(f"route_assistant: {route_to}")
                # if route_to == ToFlightBookingAssistant.__name__:
                #     return "enter_update_flight"
                # elif route_to == ToDevelopAssistant.__name__:
                #     return "enter_develop_mode"
                # elif route_to == ToArticleWriterAssistant.__name__:
                #     return "enter_article_writer"
                # elif route_to == ToBookCarRental.__name__:
                #     return "enter_book_car_rental"
                # return "primary_assistant_tools"
                return tool_node_name
            raise ValueError("Invalid route")

        assistant_edges = [
            "human_chat",
            # node_name,
            tool_node_name,
            END,
        ]
        wf.add_node(node_name, self)
        if self.is_primary_assistant():
            wf.set_entry_point(node_name)
            assistant_edges.append(node_name)
        else:
            # 作为子图，不设置 entry 节点，而是前置参数节点
            entry_node = create_entry_node(
                "Flight Updates & Booking Assistant", node_name
            )
            entry_node_name = "entry_" + node_name
            wf.add_node(entry_node_name, entry_node)
            wf.set_entry_point(entry_node_name)
            assistant_edges.append(entry_node_name)

        if not self.is_primary_assistant():
            # 子图才有 退回边
            assistant_edges.append("leave_skill")

        # if self.assistant_config.children:
        #     for children in self.assistant_config.children:
        #         sub_assistant_node = AssistantNode(children)
        #         sub_graph = await sub_assistant_node.build_graph()
        #         compile_sub_graph = sub_graph.compile()
        #         child_node_name = children.name
        #         assistant_edges.append(child_node_name)
        #         wf.add_node(child_node_name, compile_sub_graph)

        wf.add_conditional_edges(node_name, route_assistant, assistant_edges)
        tools = []  # TODO: 这里需要动态添加工具
        wf.add_node(
            tool_node_name,
            create_tool_node_with_fallback(tools),
        )
        wf.add_conditional_edges(
            tool_node_name,
            route_assistant,
            [
                "human_chat",
                node_name,
                # END,
            ],
        )
        wf.add_node("human_chat", HumanNode(llm_runnable))
        wf.add_edge("human_chat", node_name)

        # ------------------------------
        # leave_skill
        if self.is_primary_assistant():
            pass
        else:
            # 当处于子助理状态时，退出到上级助理
            wf.add_node("leave_skill", pop_dialog_state)
            wf.add_edge("leave_skill", node_name)

        # ------------------------------
        # 二级工作节点
        # flight_booking_node = FlightBookingNode(name="update_flight")
        # await flight_booking_node.addto_primary_assistant(wf)
        # await DevelopNode.addto_primary_assistant(wf)
        # await WriteArticleNode.addto_primary_assistant(wf)

        return wf

    async def compile_graph(self):
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            interrupt_before=[
                "human_chat",
                # "update_flight_sensitive_tools",
                # "develop_sensitive_tools",
                # "book_car_rental_sensitive_tools",
                # "book_hotel_sensitive_tools",
                # "book_excursion_sensitive_tools",
            ],
            debug=True,
        )

        image_data = graph.get_graph(xray=1).draw_mermaid_png()
        save_to = "./graph.png"
        with open(save_to, "wb") as f:
            f.write(image_data)
        return graph

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        prompt_tpl = await self.get_prompt(state)
        tools = primary_assistant_tools + [
            ToFlightBookingAssistant,
            ToBookCarRental,
            ToDevelopAssistant,
        ]

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
        thread_id: str | None = None,
        user: User | None = None,
    ):
        graph = await self.compile_graph()
        # user_session = cl.user_session
        # graph = user_session.get("graph")
        # if not graph:
        #     raise ValueError("graph 未初始化")

        inputs = {
            "messages": messages,
        }

        if not thread_id:
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

            if not is_internal_node(node_name):
                if not is_skip_kind(kind):
                    logger.info("[event] %s@%s", kind, node_name)

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield aisdk.text(content)
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
                        # await context.emitter.emit(
                        #     "ui_state_upate",
                        #     jsonable_encoder(thread_ui_state),
                        # )
                        pass

                if node_name == "LangGraph":
                    logger.info("中止节点")
                    if (
                        data
                        and (output := data.get("output"))
                        and (final_messages := output.get("messages"))
                    ):
                        for message in final_messages:
                            message.pretty_print()
                        # await context.emitter.emit(
                        #     "logs",
                        #     {
                        #         "on": "中止",
                        #         "node_name": node_name,
                        #         "output": message.pretty_print(),
                        #     },
                        # )

            if kind == "on_tool_start":
                # await context.emitter.emit(
                #     "logs",
                #     {
                #         "on": kind,
                #         "node_name": node_name,
                #     },
                # )
                pass

            if kind == "on_tool_end":
                output = data.get("output")
                # await context.emitter.emit(
                #     "logs",
                #     {
                #         "on": kind,
                #         "node_name": node_name,
                #         "output": jsonable_encoder(output),
                #     },
                # )
                pass
