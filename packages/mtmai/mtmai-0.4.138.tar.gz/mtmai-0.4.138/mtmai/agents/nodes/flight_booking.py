from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import tools_condition
import mtmai.chainlit as cl

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.graphutils import (
    CompleteOrEscalate,
    create_entry_node,
    create_tool_node_with_fallback,
)
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


@tool
def update_ticket_to_new_flight(
    ticket_no: str, new_flight_id: int, *, config: RunnableConfig
) -> str:
    """Update the user's ticket to a new valid flight."""
    configuration = config.get("configurable", {})
    passenger_id = configuration.get("passenger_id", None)
    if not passenger_id:
        raise ValueError("No passenger ID configured.")

    # TODO: 操作数据库实现具体逻辑
    return "Ticket successfully updated to new flight."


@tool
def cancel_ticket(ticket_no: str, *, config: RunnableConfig) -> str:
    """Cancel the user's ticket and remove it from the database."""
    configuration = config.get("configurable", {})
    passenger_id = configuration.get("passenger_id", None)
    if not passenger_id:
        raise ValueError("No passenger ID configured.")
    # TODO: 操作数据库实现具体逻辑
    return "Ticket successfully cancelled."


update_flight_safe_tools = []
update_flight_sensitive_tools = [update_ticket_to_new_flight, cancel_ticket]
update_flight_tools = update_flight_safe_tools + update_flight_sensitive_tools


def route_update_flight(
    state: HomeChatState,
):
    route = tools_condition(state.messages)
    if route == END:
        # return END
        # return "leave_skill"
        return "human_chat"

    tool_calls = state.messages[-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    safe_toolnames = [t.name for t in update_flight_safe_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "update_flight_safe_tools"
    sensitive_toolnames = [t.name for t in update_flight_sensitive_tools]
    if all(tc["name"] in sensitive_toolnames for tc in tool_calls):
        return "update_flight_sensitive_tools"

    raise ValueError(f"update_flight 节点出现不正确的路由：{tool_calls}")
    # return "update_flight_sensitive_tools"


class FlightBookingNode:
    def __init__(self, name:str):
        self.name = name

    def agent_role(self):
        return "flight updates"


    async def addto_primary_assistant(self, wf: StateGraph):
        llm_runnable = await mtmai_context.get_llm_openai("chat")

        wf.add_node(
            "enter_"+self.name,
            create_entry_node("Flight Updates & Booking Assistant", "update_flight"),
        )
        wf.add_node("update_flight", FlightBookingNode(llm_runnable))
        wf.add_edge("enter_update_flight", "update_flight")
        wf.add_node(
            "update_flight_sensitive_tools",
            create_tool_node_with_fallback(update_flight_sensitive_tools),
        )
        wf.add_node(
            "update_flight_safe_tools",
            create_tool_node_with_fallback(update_flight_safe_tools),
        )

        wf.add_edge("update_flight_sensitive_tools", "update_flight")
        wf.add_edge("update_flight_safe_tools", "update_flight")
        wf.add_conditional_edges(
            "update_flight",
            route_update_flight,
            [
                "human_chat",
                "update_flight_sensitive_tools",
                "update_flight_safe_tools",
                "leave_skill",
                END,
            ],
        )

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        logger.info(f"进入 flight_booking")
        flight_booking_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a specialized assistant for role **{role}**. "
                    " The primary assistant delegates work to you whenever the user needs help updating their bookings. "
                    "Confirm the updated flight details with the customer and inform them of any additional fees. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    "If you need more information or the customer changes their mind, escalate the task back to the main assistant."
                    " Remember that a booking isn't completed until after the relevant tool has successfully been used."
                    "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                    "\nCurrent time: {time}."
                    "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
                    ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.'
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(
            time=datetime.now(),
            role=self.agent_role(),
        )
        ai_msg = await mtmai_context.ainvoke_model(
            flight_booking_prompt,
            state,
            tools=update_flight_tools + [CompleteOrEscalate],
        )
        if ai_msg.content:
            await cl.Message("flight_booking:"+ai_msg.content).send()
        return {"messages": ai_msg}
