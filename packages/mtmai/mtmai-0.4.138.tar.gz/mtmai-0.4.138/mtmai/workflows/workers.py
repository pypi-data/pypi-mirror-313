async def deploy_mtmai_workers(backend_url: str):
    import asyncio

    from mtmai.workflows.agentcall import AgentCall
    from mtmai.workflows.wfapp import wfapp

    # 获取配置文件
    # response = httpx.get("http://localhost:8383/api/v1/worker/config")
    # hatchet = Hatchet(debug=True)
    # list: WorkflowList = await wfapp.rest.aio.default_api.worker_config()
    worker = wfapp.worker("pyworker")
    # worker.register_workflow(BasicRagWorkflow())
    # worker.register_workflow(FlowMcpClientExample())
    # worker.register_workflow(FlowArticleGen())
    # worker.register_workflow(FlowWriteChapter())
    # worker.register_workflow(BlogGen())
    worker.register_workflow(AgentCall())
    # worker.register_workflow(SystemBackendTask())

    await worker.async_start()

    while True:
        await asyncio.sleep(1)
