import operator
from collections.abc import Sequence
from typing import Annotated, TypedDict

from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnableConfig
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel
from sqlmodel import Session

from mtmai.core.logging import get_logger
from mtmai.crud.curd_chat import get_conversation_messages
from mtmai.llm.llm import get_llm_chatbot_default
from mtmai.models.models import User
from mtmai.mtlibs import aisdk

logger = get_logger()
subjects_prompt = """Generate a comma separated list of between 2 and 5 examples related to: {topic}."""
joke_prompt = """Generate a joke about {subject}"""
best_joke_prompt = """Below are a bunch of jokes about {topic}. Select the best one! Return the ID of the best one.

{jokes}"""


class Subjects(BaseModel):
    subjects: list[str]


class Joke(BaseModel):
    joke: str


class BestJoke(BaseModel):
    id: int


class OverallState(TypedDict):
    topic: str
    subjects: list
    jokes: Annotated[list, operator.add]
    best_selected_joke: str


class JokeState(TypedDict):
    subject: str


class JokeAgentState(BaseModel):
    # id: str = Field(default_factory=mtutils.nano_gen, primary_key=True)
    # topic: str | None = None
    # subjects: list | None = []
    # subjects: list[str] | None = Field(sa_column=Column(JSON))
    subjects: list[str] | None = None
    # jokes: Annotated[Sequence[str], operator.add] = []
    jokes: Annotated[Sequence[str], operator.add] | None = (
        None  # = Field(sa_column=Column(JSON))
    )
    best_selected_joke: str | None = None
    # messages: Annotated[list, add_messages] = Field(sa_column=Column(JSON))
    messages: list[dict] | None = None  # = Field(sa_column=Column(JSON))
    ask_human: bool = False


# This is the function we will use to generate the subjects of the jokes
def generate_topics(state: JokeAgentState):
    llm = get_llm_chatbot_default()

    latest_message = state.messages[-1]
    prompt = subjects_prompt.format(topic=latest_message["content"])
    response = llm.with_structured_output(Subjects).invoke(prompt)
    state.subjects = response.subjects
    # return {"subjects": response.subjects}
    return state


# Here we generate a joke, given a subject
def generate_joke(state: JokeState):
    llm = get_llm_chatbot_default()
    prompt = joke_prompt.format(subject=state["subject"])
    response = llm.with_structured_output(Joke).invoke(prompt)
    # state.jokes = [response.joke]
    return {"jokes": [response.joke]}


# Here we define the logic to map out over the generated subjects
# We will use this an edge in the graph
def continue_to_jokes(state: JokeAgentState):
    # We will return a list of `Send` objects
    # Each `Send` object consists of the name of a node in the graph
    # as well as the state to send to that node
    send_list = []
    for s in state.subjects:
        joke_state = JokeState(
            subject=s,
        )
        send_list.append(Send("generate_joke", joke_state))
    # return [Send("generate_joke", ) for JokeAgentState(subjects=s) in state.subjects]
    return send_list


def best_joke(state: JokeAgentState):
    llm = get_llm_chatbot_default()

    jokes = "\n\n".join(state.jokes)
    latest_message = state.messages[-1]

    prompt = best_joke_prompt.format(topic=latest_message["content"], jokes=jokes)
    response = llm.with_structured_output(BestJoke).invoke(prompt)

    idx = response.id

    # Ensure idx is within the bounds of the jokes list
    if idx >= len(state.jokes):
        idx = len(state.jokes) - 1

    return {"best_selected_joke": state.jokes[idx]}


class JokeAgent:
    def __init__(self):
        pass

    @property
    def name(self):
        return "joke"

    def get_workflow(self) -> CompiledStateGraph:
        graph = StateGraph(JokeAgentState)
        graph.add_node("generate_topics", generate_topics)
        graph.add_node("generate_joke", generate_joke)
        graph.add_node("best_joke", best_joke)
        graph.add_edge(START, "generate_topics")
        graph.add_conditional_edges(
            "generate_topics", continue_to_jokes, ["generate_joke"]
        )
        graph.add_edge("generate_joke", "best_joke")
        graph.add_edge("best_joke", END)
        app = graph.compile()
        return app

    # def handle_chat_messages(self, messages: list[MtmChatMessage]):
    #     try:
    #         logger.info("JokeAgent handle Message %s", messages)

    #         latest_message = messages[-1]
    #         wf = self.get_workflow()
    #         result = wf.invoke(input={"topic": latest_message.content})
    #         logger.info("joke 运行结束 %s", result)
    #     except Exception as e:
    #         logger.exception("调用智能体 joke 出错 %s", e)  # noqa: TRY401

    async def chat(
        self,
        # messages: Iterable[ChatCompletionMessageParam],
        db: Session,
        conversation_id: str,
        user: User | None = None,
    ):
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", "You are a helpful assistant"),
        #         MessagesPlaceholder("chat_history", optional=True),
        #         # ("human", "{input}"),
        #         MessagesPlaceholder("agent_scratchpad"),
        #     ]
        # )

        chat_messages = get_conversation_messages(conversation_id)

        wf = self.get_workflow()
        thread_id = "1"
        # input = {"messages": messages,}
        input = JokeAgentState(messages=chat_messages)
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        async for event in wf.astream_events(
            input=input,
            version="v2",
            config=config,
        ):
            kind = event["event"]
            name = event["name"]
            data = event["data"]
            if kind == "on_chat_model_stream":
                print("------")
                print(event["data"]["chunk"].dict())
                content = event["data"]["chunk"].content
                if content:
                    yield aisdk.text(content)
            print(f"astream_event: kind: {kind}, name={name},{data}")

            if kind == "on_chain_end" and name == "LangGraph":
                # 完全结束可以拿到最终数据
                # yield f"2: {json.dumps(jsonable_encoder(data))}\n"
                yield aisdk.data(jsonable_encoder(data))

        yield aisdk.finish()
