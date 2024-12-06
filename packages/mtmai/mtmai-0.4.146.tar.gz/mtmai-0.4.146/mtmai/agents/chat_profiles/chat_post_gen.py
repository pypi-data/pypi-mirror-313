import json

from fastapi.encoders import jsonable_encoder

import mtmai.chainlit as cl
from mtmai.agents.nodes.hello_agent import (
    NodeSectionWriterRequest,
    RefineOutlineNodeRequest,
    init_outline_v3,
    node_refine_outline,
    node_section_writer,
    node_survey_subjects,
)
from mtmai.agents.nodes.qa_node import QaNodeRequest, QaNodeResult, node_qa
from mtmai.chainlit.context import context
from mtmai.db.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.deps import AsyncSessionDep
from mtmai.models.chat import ChatProfile
from mtmai.models.graph_config import ResearchState
from mtmai.models.search_index import SearchIndex
from mtmai.models.site import Site
from mtmai.mtlibs.inputs.input_widget import TextInput, ThreadForm

logger = get_logger()


class PostGenAgent:
    """
    前端站点的 “AI生成新文章”按钮，调用这个agent
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口

        return {}

    @classmethod
    def name(cls):
        return "postGen"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="postGen",
            description="博客文章生成器",
        )

    async def chat_start(self):
        user = cl.user_session.get("user")
        await cl.Message(content="欢迎使用博客文章生成器").send()

        fnCall_result = await context.emitter.send_call_fn("fn_get_site_id", {})
        # # logger.info("函数调用结果 %s", fnCall_result)
        siteId = fnCall_result.get("siteId", "")
        if not siteId:
            # text_content = "你还没配置站点，请先配置站点"
            # elements = [
            #     cl.Text(name="simple_text", content=text_content, display="inline")
            # ]
            await cl.Message(
                content="你还没配置站点，请先配置站点，点击下面的操作按钮，配置站点",
                # elements=elements,
            ).send()

            ask_form_result = await context.emitter.send_form(
                ThreadForm(
                    open=True,
                    inputs=[
                        TextInput(
                            name="url",
                            label="网址",
                            placeholder="https://www.example123.com",
                            description="AI将自带识别网站类型，生成的文章可以自动发布到该网站",
                            value="",
                        ),
                    ],
                )
            )
        logger.info("表单调用结果 %s", ask_form_result)
        async with get_async_session() as session:
            site = await add_target_site(
                session, ask_form_result.get("url"), owner_id=user.id
            )
            # site = await get_site_by_id(session, uuid.UUID(siteId))

            site_description = site.description
            topic = site.description or "some topic"

        graph_state = ResearchState(
            topic=topic,
        )

        if not graph_state.outline:
            # 生成初始大纲
            init_outline = await init_outline_v3(topic=topic)
            graph_state.outline = init_outline

        if not graph_state.editors:
            # 获取相关主题
            async with cl.Step(name="获取相关主题", type="llm") as step:
                step.input = "Test hello input"
                subjects = await node_survey_subjects(topic=topic)
                step.output = subjects

                graph_state.editors = subjects.editors
        if not graph_state.interview_results:
            # 请教领域专家
            async with cl.Step(name="请教领域专家", type="llm") as step:
                # step.input = "Test hello input"

                qa_results: list[QaNodeResult] = []
                # TODO: 这里应该有多个专家，不过，目前开发阶段暂时只处理一个
                result = await node_qa(
                    req=QaNodeRequest(
                        topic=site_description,
                        editor=graph_state.editors[0],
                    )
                )
                qa_results.append(result)
                step.output = json.dumps(jsonable_encoder(result.format_conversation()))

                graph_state.interview_results = result
            # 根据专家对话重新大纲
            await cl.Message(content="根据专家对话改进大纲").send()
            await node_refine_outline(
                RefineOutlineNodeRequest(
                    topic=graph_state.topic,
                    old_outline=graph_state.outline,
                    qa_results=qa_results,
                )
            )
            # 专家对话的结果, 以及引用的网址存入知识库(暂时跳过，因为还没完善)
            # await cl.Message(content="将专家对话的结果存入知识库").send()
            # ctx = get_mtmai_ctx()
            # vs = ctx.vectorstore
            # all_docs = []
            # for interview_state in graph_state.interview_results:
            #     reference_docs = [
            #         Document(page_content=v, metadata={"source": k})
            #         for k, v in interview_state.references.items()
            #     ]
            #     all_docs.extend(reference_docs)
            # await vs.aadd_documents(all_docs)

        # 根据大纲编写章节内容(TODO: 这里需要并发执行)
        await cl.Message(content="开始编写章节内容").send()
        all_sections = []
        for section in graph_state.outline.sections:
            a = await node_section_writer(
                NodeSectionWriterRequest(
                    topic=graph_state.topic,
                    outline=graph_state.outline,
                    section=section,
                )
            )
            all_sections.append(a)

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass


async def step_hello2():
    async with cl.Step(name="TestStep2", type="llm") as step:
        step.input = "step_hello2 input"
        step.output = "step_hello2 output"
        await cl.Message(content="step_hello2 hello output").send()


async def add_target_site(db_session: AsyncSessionDep, site_url: str, owner_id: str):
    site_detected_info = {
        "title": "fake_site_title",
        "framework": "wordpress",
    }

    new_site = Site(
        url=site_url,
        owner_id=owner_id,
        title=site_detected_info.get("title"),
        description=site_detected_info.get("title"),
    )
    db_session.add(new_site)
    await db_session.commit()
    await db_session.refresh(new_site)

    # 创建列表索引
    content_summary = f"site: {new_site.title} {new_site.description}"
    search_index = SearchIndex(
        content_type="site",
        content_id=new_site.id,
        title=new_site.title,
        content_summary=content_summary,
        owner_id=owner_id,
        meta={
            # "author_id": str(new_blog_post.author_id),
            # "tags": [tag.name for tag in new_blog_post.tags],
        },
        # search_vector=generate_search_vector(post.title, post.content),
        # embedding=generate_embedding(post.title, post.content)
    )
    db_session.add(search_index)
    await db_session.commit()
    await db_session.refresh(new_site)
    return new_site
