import structlog


LOG = structlog.get_logger()


class GraphService:
    async def execute_graph(
        self,
        task_id: str,
        graph_id: str,
        thread_id: str,
        organization_id: str,
        max_steps_override: int | None = None,
        api_key: int | None = None,
    ) :
        LOG.info("Executing task(graph) using background task executor", graph_id=graph_id)
