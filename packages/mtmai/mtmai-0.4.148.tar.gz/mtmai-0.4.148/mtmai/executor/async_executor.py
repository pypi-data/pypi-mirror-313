import abc

import structlog
from fastapi import BackgroundTasks, Request

from mtmai import mtmai_app
from mtmai.exceptions import OrganizationNotFound
from mtmai.forge import app
from mtmai.forge.sdk.core import skyvern_context
from mtmai.forge.sdk.core.skyvern_context import SkyvernContext
from mtmai.forge.sdk.schemas.tasks import TaskStatus

LOG = structlog.get_logger()


class AsyncExecutor(abc.ABC):
    @abc.abstractmethod
    async def execute_task(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        task_id: str,
        organization_id: str,
        max_steps_override: int | None,
        api_key: str | None,
        **kwargs: dict,
    ) -> None:
        pass

    @abc.abstractmethod
    async def execute_workflow(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        organization_id: str,
        workflow_id: str,
        workflow_run_id: str,
        max_steps_override: int | None,
        api_key: str | None,
        **kwargs: dict,
    ) -> None:
        pass

    @abc.abstractmethod
    async def execute_graph(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        organization_id: str | None=None,
        graph_id: str |None =None,
        thread_id: str | None=None,
        max_steps_override: int | None =None,
        api_key: str | None=None,
        **kwargs: dict,
    ) -> None:
        pass


class BackgroundTaskExecutor(AsyncExecutor):
    async def execute_task(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        task_id: str,
        organization_id: str,
        max_steps_override: int | None,
        api_key: str | None,
        **kwargs: dict,
    ) -> None:
        LOG.info("Executing task using background task executor", task_id=task_id)

        organization = await app.DATABASE.get_organization(organization_id)
        if organization is None:
            raise OrganizationNotFound(organization_id)

        step = await app.DATABASE.create_step(
            task_id,
            order=0,
            retry_index=0,
            organization_id=organization_id,
        )

        task = await app.DATABASE.update_task(
            task_id,
            status=TaskStatus.running,
            organization_id=organization_id,
        )

        context: SkyvernContext = skyvern_context.ensure_context()
        context.task_id = task.task_id
        context.organization_id = organization_id
        context.max_steps_override = max_steps_override

        background_tasks.add_task(
            app.agent.execute_step,
            organization,
            task,
            step,
            api_key,
        )

    async def execute_workflow(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        organization_id: str,
        workflow_id: str,
        workflow_run_id: str,
        max_steps_override: int | None,
        api_key: str | None,
        **kwargs: dict,
    ) -> None:
        LOG.info(
            "Executing workflow using background task executor",
            workflow_run_id=workflow_run_id,
        )

        organization = await app.DATABASE.get_organization(organization_id)
        if organization is None:
            raise OrganizationNotFound(organization_id)

        background_tasks.add_task(
            app.WORKFLOW_SERVICE.execute_workflow,
            workflow_run_id=workflow_run_id,
            api_key=api_key,
            organization=organization,
        )

    async def execute_graph(
        self,
        request: Request | None,
        background_tasks: BackgroundTasks,
        organization_id: str | None=None,
        graph_id: str |None =None,
        thread_id: str | None=None,
        max_steps_override: int | None =None,
        api_key: str | None=None,
        **kwargs: dict,
    ) -> None:
        LOG.info("Executing task(graph) using background task executor", graph_id=graph_id)

        # 前置条件检测
        # organization = await app.DATABASE.get_organization(organization_id)
        # if organization is None:
        #     raise OrganizationNotFound(organization_id)

        background_tasks.add_task(
            mtmai_app.GRAPH_SERVICE.execute_graph,
            task_id=graph_id,
            graph_id=graph_id,
            thread_id=thread_id,
            api_key=api_key,
            # organization=organization,
        )
