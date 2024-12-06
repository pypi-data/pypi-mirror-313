import asyncio
from typing import Optional

import litellm
from fastapi.encoders import jsonable_encoder
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.models.book_gen import (
    BookOutline,
    ChapterOutline,
    WriteOutlineRequest,
    WriteSingleChapterRequest,
)
from mtmai.mtlibs.aiutils import get_json_format_instructions
from mtmai.workflows.crews import call_crew, crew_gen_outline
from mtmai.workflows.flowbase.helper import get_wf_log_callbacks
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        None, description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    articles: list[NewsArticle]


class ScrapedArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        None, description="Summary of the article if available."
    )
    content: Optional[str] = Field(
        None,
        description="Content of the in markdown format if available. Return None if the content is not available or does not make sense.",
    )


@wfapp.workflow(on_events=["article:gen"])
class FlowArticleGen:
    @wfapp.step(timeout="10m", retries=3)
    async def gen_outlines(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        topic = hatctx.workflow_input().get("topic", "如何编写SEO文章")
        req = WriteOutlineRequest(
            topic=topic,
            goal="",
        )
        crew = await crew_gen_outline(get_wf_log_callbacks(hatctx))

        inputs = req
        if isinstance(req, BaseModel):
            inputs = req.model_dump()
        inputs["format_instructions"] = get_json_format_instructions(BookOutline)
        # output = await crew.kickoff_async(inputs=inputs)
        try:
            output = await call_crew(crew, inputs)
            # result = output.pydantic
            # ctx.log(f"上一步骤生成的 topic：{topic}, 大纲 {result.chapters}")
            if not isinstance(output, BookOutline):
                try:
                    output = BookOutline.model_validate_json(output)
                except Exception as e:
                    ctx.log(f"解释 BookOutline 出错 {jsonable_encoder(output)}")
                    raise e
            outlines = output.chapters
            results = []
            for index, chapter_dict in enumerate(outlines, start=1):
                ctx.log(f"编写第 {index} 章节")
                ouline = ChapterOutline.model_validate(chapter_dict)
                req = WriteSingleChapterRequest(
                    goal="",
                    topic=topic,
                    chapter_title=ouline.title,
                    chapter_description=ouline.description,
                    book_outlines=outlines,
                )

                child_flow = await hatctx.aio.spawn_workflow(
                    "FlowWriteChapter", req.model_dump()
                )
                r = await child_flow.result()
                results.append(r)
            return {
                "topic": topic,
                "results": jsonable_encoder(results),
            }
        except litellm.RateLimitError as e:
            await asyncio.sleep(20)
            ctx.log("速率限制，休眠")
            raise e
