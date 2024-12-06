from crewai import LLM
from mtmai.workflows.ctx import init_step_context
from mtmai.workflows.step_base import MtFlowBase, get_wf_log_callbacks
from mtmai.workflows.wfapp import wfapp
from mtmaisdk.clients.rest.models.call_agent import CallAgent
from mtmaisdk.clients.rest.models.call_agent_llm import CallAgentLlm
from mtmaisdk.context.context import Context


@wfapp.workflow(on_events=["graph:call"])
class GraphFlow:
    @wfapp.step(timeout="10m", retries=3)
    async def call_agent(self, hatctx: Context):
        init_step_context(hatctx)
        return await StepGraph(hatctx).run()


def get_llm(llm_config: CallAgentLlm, callback):
    return LLM(
        model=llm_config.model,
        temperature=llm_config.temperature,
        base_url=llm_config.base_url,
        api_key=llm_config.api_key,
        num_retries=llm_config.num_retries or 3,
        logger_fn=callback,
    )


class StepGraph(MtFlowBase):
    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def run(self):
        input = CallAgent.model_validate(self.ctx.workflow_input())
        callback = get_wf_log_callbacks(self.ctx)
        llm = get_llm(input.llm, callback)
        self.emit("hello graph")
