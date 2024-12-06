from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from mtmai.core.logging import get_logger

logger = get_logger()


class EntryNode:
    def __init__(self):
        pass

    async def __call__(self, state, config: RunnableConfig):
        # logger.info(f"entry node thread id: {mtmai_context.thread_id}")
        # hello_prompt = ChatPromptTemplate.from_messages(
        #     [
        #         (
        #             "system",
        #             "You are a specialized assistant for handling development tasks. "
        #             "The primary assistant delegates work to you whenever the user needs help with development-related queries or tasks. "
        #             "You can use various tools to assist developers, such as reading logs, retrieving system status information, and performing other development-related actions. "
        #             "Be thorough and precise in your responses, providing detailed information when necessary. "
        #             "If a task requires multiple steps, guide the user through each step clearly. "
        #             "If you need more information or if the task is beyond your capabilities, escalate the task back to the main assistant. "
        #             "Remember to use the appropriate tools for each task and provide clear explanations of your actions. "
        #             "Always prioritize security and best practices in your recommendations."
        #             "\nCurrent time: {time}."
        #             "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
        #             ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        #         ),
        #         ("placeholder", "{messages}"),
        #     ]
        # ).partial(time=datetime.now())

        # # develop_runnable = develop_prompt | self.runnable.bind_tools(
        # #     develop_tools + [CompleteOrEscalate]
        # # )
        # return {
        #     "messages": await mtmai_context.ainvoke_model(hello_prompt, state, tools=[])
        # }
        if state.user_input:
            return {
                "next": "assistant",
                "messages": [HumanMessage(content=state.user_input)],
            }
        return {
            "next": "assistant",
        }
