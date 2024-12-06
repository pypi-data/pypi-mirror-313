from textwrap import dedent

import structlog
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai.tools.base_tool import Tool
from mem0 import Memory
from mtmaisdk import Context

from mtmai.workflows.crews import call_crew
from mtmai.workflows.flowbase.Flowbase import MtFlowBase
from mtmai.workflows.flowbase.helper import get_wf_log_callbacks
from mtmai.workflows.wfapp import wfapp

m = Memory()

LOG = structlog.get_logger()


@wfapp.workflow(on_events=["task:blog:main"])
class SystemBackendTask(MtFlowBase):
    """全局任务自动调度"""

    @wfapp.step(timeout="24h", retries=3)
    async def task_dispatch(self, hatctx: Context):
        return await StepTaskDispatch(hatctx).run()


class StepTaskDispatch(MtFlowBase):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.isDispatched = False

    async def run(self):
        input = self.ctx.workflow_input()
        callback = get_wf_log_callbacks(self.ctx)
        researcher_agent = Agent(
            role="Backend Task Runner",
            backstory=dedent("""你是系统的全局工作流调度器，擅长通过调用工具查询系统的状态来决定如何启动相关的子工作流,
                            现有一份 openapi v3 的文档，可以作为操作的依据"""),
            goal=dedent(
                """根据任务要求, 认真查看 openapi 文档，根据文档的描述进行api 调用，完成任务"""
            ),
            tools=[
                Tool.from_langchain(self.get_guide_tool(self.ctx)),
                Tool.from_langchain(self.get_system_state_tool(self.ctx)),
                self.task_dispatcher_tool(self.ctx),
                # TaskDispatcherTool(self.ctx),
                Tool.from_langchain(self.blog_query_tool(self.ctx)),
            ],
            llm=self.getLlm(self.ctx),
            verbose=True,
            max_retry_limit=100,
            max_rpm=60,
            step_callback=callback,
            task_callback=callback,
            memory=True,
        )
        research_topic_task = Task(
            description=dedent(
                dedent(
                    """按操作指引进行相关工作和系统状态自动启动新的"BlogTask"任务(如果需要)
- 确保正确的参数传入
- 如果确实需要启动任务，必须返回任务启动的结果
- 如果工具出错，必须详细输出出错的细节，可以输出 debugtrace 细节
"""
                )
            ),
            expected_output="操作结果，说明原因",
            agent=researcher_agent,
            callback=callback,
            tools=[
                self.task_dispatcher_tool(self.ctx),
            ],
        )

        crew = Crew(
            agents=[researcher_agent],
            tasks=[research_topic_task],
            process=Process.sequential,
            verbose=True,
            step_callback=callback,
            task_callback=callback,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "crew_user_1"},
            },
        )

        result = await call_crew(crew, input)
        if isinstance(result, str):
            return {"raw": result}
        return result

    def get_guide_tool(self, ctx: Context):
        @tool("OperationGuide")
        def operation_guide():
            """operation guide"""

            LOG.info("工具调用(operation_guide)")
            return dedent("""环境说明：
            工作流组件:hatchat
            操作系统: debain
            系统功能: 全自动多用户博客文章生成及发布
            当前模块: DispatchBlogTask, 根据系统状态启动派生的 BlogTask 子任务
            操作步骤：
            1: 调用工具查询系统状态, 系统状态中相关名称对应的字段会描述当前的系统相关负载，
                例如: 假设系统最大允许10个"BlogTask"并行运行，当查询到当前有5个正在运行的任务，则应启动新"BlogTask"任务
            2: 任务的运行或触发内部相关状态改变，当发现存在问题是，应该检查相关状态，及时调整策略。
            3: 重要:当决定启动新的 BlogTask 时，必须调用"RunBlogTask"工具

        """)

        return operation_guide

    def get_system_state_tool(self, ctx: Context):
        @tool("SystemState")
        def system_state():
            """get current system state"""

            LOG.info("工具调用(system_state)")
            return dedent("""
        blogTaskState:{
            "task_running_count": 8,
            "max_task_run_limit": 10,
        }
        """)

        return system_state

    def blog_query_tool(self, ctx: Context):
        @tool("BlogsQuery")
        def blog_query():
            """blog info list view"""

            LOG.info("工具调用(system_state)")
            return dedent("""
{
                        "items":[{
                            id: "blog-123",
                            title: "example-blog",
                            isTaskRunning: false,
                        },
                        {
                            id: "blog-124",
                            title: "example-blog",
                            isTaskRunning: true,
                        },
                        {
                            id: "blog-125",
                            title: "example-blog",
                            isTaskRunning: true,
                        },
                        ]}
        """)

        return blog_query

    def task_dispatcher_tool(self, ctx: Context):
        async def fn(blog_id: str):
            LOG.info(f"工具调用(task_dispatcher), blog_id:{blog_id}")
            if self.isDispatched:
                return "操作失败，不要过于频频启动相同 blogId 的任务"
            try:
                # asyncio.run( ctx.aio.spawn_workflow("BlogGenV3",{
                #     "blogId": blog_id,
                # }))

                await ctx.aio.spawn_workflow(
                    "BlogGenV3",
                    {
                        "blogId": blog_id,
                    },
                )

                self.isDispatched = True
                return dedent("""操作成功""")
            except Exception as e:
                return f"""操作失败，原因: {e}"""

        serper_tool = Tool(
            name="RunBlogTask",
            func=fn,
            description="spawn workflow BlogTask",
        )
        return serper_tool
