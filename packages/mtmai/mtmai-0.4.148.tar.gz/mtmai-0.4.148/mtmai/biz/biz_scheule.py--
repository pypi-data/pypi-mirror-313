from mtmai.db.db import get_async_session
from mtmai.crud import crud_task
from mtmai.models.task import MtTaskType


async def make_new_task_by_schedule(schedule_id: str, is_auto: bool = False):
    async with get_async_session() as session:
        sched = await crud_task.get_schedule(session=session, id=schedule_id)
        if not sched:
            raise ValueError(f"schedule {schedule_id} 不存在")

        new_task = None
        if sched.task_type == MtTaskType.ARTICLE_GEN:
            new_task = await crud_task.mttask_create(
                session=session,
                schedule_id=schedule_id,
                name=MtTaskType.ARTICLE_GEN,
                init_state={
                    **sched.params,
                },
            )
        else:
            raise ValueError(f"未知的任务类型 {sched.task_type}")

        return new_task


async def delete_chat_profile(id: str):
    async with get_async_session() as session:
        await crud_task.delete_chat_profile(session=session, id=id)
