from textwrap import dedent

import structlog
from crewai import Agent, Crew, Process, Task
from crewai.tools.base_tool import Tool
from langchain_core.tools import tool
from mtmai.agents.ctx import init_mtmai_step_context
from mtmai.workflows.crews import call_crew
from mtmai.workflows.flowbase.Flowbase import MtFlowBase
from mtmai.workflows.flowbase.helper import get_wf_log_callbacks
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context
from mtmaisdk.clients.rest.models.blog_task_state import BlogTaskState

LOG = structlog.get_logger()


@wfapp.workflow(on_events=["task:blog:main"])
class BlogGenV3(MtFlowBase):
    """博客生成系统"""

    @wfapp.step(timeout="10m", retries=3)
    async def gen_topic(self, hatctx: Context):
        ctx = init_mtmai_step_context(hatctx)
        input = hatctx.workflow_input()
        # blogTaskInput = BlogTaskState.model_validate(input)

        # blogTaskState =BlogTaskState(
        #     blog_description="专注于广州美食的个人博客，介绍时令点心的制作技巧，逛店、店铺推荐",
        #     DayPublishCountHint=0,
        #     llm= self.getLlm(ctx),
        # )

        callback = get_wf_log_callbacks(hatctx)
        researcher_agent = Agent(
            role="Blog Task Dispatcher",
            backstory=dedent(
                """你是专业的任务调度器，擅长使用工具，和操作指引完成工作流任务的调度"""
            ),
            # tools=get_tools("search_engine"),
            tools=[
                Tool.from_langchain(self.getBlogInfoTool(ctx)),
                Tool.from_langchain(self.get_guide_tool(ctx)),
                Tool.from_langchain(self.get_dispatch_task_tool(ctx)),
            ],
            llm=self.getLlm(ctx),
            verbose=True,
            max_retry_limit=100,
            max_rpm=60,
            step_callback=callback,
            task_callback=callback,
        )

        # format_instructions = get_json_format_instructions(GenBlogTopicsOutput)
        # format_instructions = format_instructions.replace("{", "{{").replace("}", "}}")

        research_topic_task = Task(
            description=dedent(
                dedent(
                    """启动新的 "文章生成任务" (如果需要), 请正确输入文章生成所需的任务参数"""
                )
            ),
            expected_output="操作的结果，以及原因",
            agent=researcher_agent,
            # output_pydantic=GenBlogTopicsOutput,
            # output_json=
            callback=callback,
        )

        crew = Crew(
            agents=[researcher_agent],
            tasks=[research_topic_task],
            process=Process.sequential,
            verbose=True,
            step_callback=callback,
            task_callback=callback,
        )

        return await call_crew(crew, input)

    # @wfapp.step(timeout="10m", retries=3, parents=["gen_topic"])
    # async def gen_post(self, hatctx: Context):
    #     ctx = init_mtmai_step_context(hatctx)
    #     topics = hatctx.step_output("gen_topic").get("topics")
    #     ctx.log(f"挑选第一个主题生成文章 {topics}")
    #     flow_article = await hatctx.aio.spawn_workflow(
    #         "FlowArticleGen",
    #         {
    #             "topic": topics[0],
    #         },
    #     )
    #     post = await flow_article.result()

    #     return {"post": post}

    def getBlogInfoTool(self, ctx: Context):
        @tool("getBlogInfo")
        def getBlogInfo():
            """获取博客系统的基本信息"""

            LOG.info("工具调用(blog_task_operation_guide)")
            a = blogTaskState = BlogTaskState(
                blog_description="专注于广州美食的个人博客，介绍时令点心的制作技巧，逛店、店铺推荐",
                DayPublishCountHint=0,
                llm=self.getLlm(ctx),
            )
            return a

        return getBlogInfo

    def get_guide_tool(self):
        @tool("OperationGuide")
        def blog_task_operation_guide():
            """操作向导"""

            LOG.info("工具调用(blog_task_operation_guide)")
            return dedent("""环境说明：
            工作流组件:hatchat
            操作系统: debain
            系统功能: 全自动多用户博客文章生成及发布
            当前模块: BlogTask，用于单个博客的所有自动化操作任务

            操作步骤：
            1: 调用工具查询Blog状态信息, 相关字段名能正确反应相关的含义
            2: 判断 "建议日更博文数量" 和 "已完成日更博文数量"，尽量完成当前需要发布的文章数量
            3: 注意并发数量，低于阈值则表示可以启动新的 "文章生成" 任务
            4: 调用工具启动 "文章生成" 任务，需要正确输出参数，因为参数对于生成文章的质量有决定性影响, 如果不清楚如何填写参数，可以参考模板
            5: 重要: 当前系统处于开发早期阶段，可能有bug，或者出现错误，如果你认为有问题，应该及时输出反馈和建议，而不是强行执行相关的工具运行任务。
        """)

        return blog_task_operation_guide

    def get_dispatch_task_tool(self):
        @tool("DispatchTask")
        def dispatch_task(topic: str, title_hint: str):
            """运行新的任务"""

            LOG.info(f"工具调用(dispatch_task), {topic}, title_hint:{title_hint}")
            return dedent("""
{
 "ok": true
}
""")

        return dispatch_task
