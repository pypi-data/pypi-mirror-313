import structlog
from psycopg_pool import AsyncConnectionPool
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings
from mtmai.crud import curd
from mtmai.crud.crud_sysitem import get_sys_items
from mtmai.crud.curd import get_user_by_email
from mtmai.db.db import get_async_session, get_engine
from mtmai.models.models import SysItem, UserCreate

LOG = structlog.get_logger()


async def _seed_users(db: AsyncSession):
    super_user = await get_user_by_email(
        session=db, email=settings.FIRST_SUPERUSER_EMAIL
    )
    if not super_user:
        #     super_user = await create_user(
        #         session=db,
        #         user_create=UserCreate(
        #             email=settings.FIRST_SUPERUSER_EMAIL,
        #             username=settings.FIRST_SUPERUSER,
        #             password=settings.FIRST_SUPERUSER_PASSWORD,
        #             is_superuser=True,
        #         ),
        #     )
        #     organization = await get_organization_by_user_id(super_user.id)
        #     if not organization:
        #         await DATABASE.create_organization(
        #             organization_name="mt",
        #             webhook_callback_url="",
        #             organization_type="test",
        #             max_steps_per_run="100",
        #             max_retries_per_step="3",
        #             max_concurrent_runs="10",
        #             domain="mtmai.com",
        #         )
        await curd.register_user(
            session=db,
            user_in=UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            ),
        )


async def seed_db(session: AsyncSession):
    await _seed_users(session)


async def setup_checkpointer(connectStr: str | None = None):
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    LOG.info(
        "setup_checkpointer: ",
        connectStr=connectStr or settings.DATABASE_URL,
        connection_kwargs=connection_kwargs,
    )
    pool = AsyncConnectionPool(
        conninfo=connectStr or settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    await pool.close()


async def init_database():
    """初始化数据库
    确保在空数据库的情况下能启动系统
    """


    LOG.warning("⚠️   SEDDING DB v3", dbStr=settings.DATABASE_URL)
    try:
        from mtmai.models.chat import ChatStep, ChatThread  # noqa: F401
        from mtmai.models.search_index import SearchIndex  # noqa: F401
        from mtmai.models import site  # noqa: F401
        from mtmai.models.site import Site  # 显式导入 Site 模型
        from mtmai.models.task import MtTask  # noqa: F401

        # 初始化 skyvern 数据库(基于sqlalchemy)
        LOG.info("Seeding skyvern database")
        from mtmai.forge.sdk.db import models
        engine = get_engine()

        # 确保所有模型都被注册到 metadata
        SQLModel.metadata.create_all(engine)

        # 如果还是没有创建表，可以尝试显式创建
        # Site.metadata.create_all(engine)

        async with get_async_session() as session:
            await seed_db(session)
        LOG.info("setup_checkpointer")

        await setup_checkpointer(settings.DATABASE_URL)
        await seed_sys_items(session)



        LOG.info("🟢 Seeding database finished")
    except Exception as e:
        LOG.error(e)


async def seed_sys_items(session: AsyncSession):
    all_sys_items = [
        SysItem(
            type="task_type",
            key="articleGen",
            value="articleGen",
            description="生成站点文章",
        ),
        SysItem(
            type="task_type",
            key="siteAnalysis",
            value="siteAnalysis",
            description="流量分析(功能未实现)",
        ),
    ]
    for item in all_sys_items:
        existing_item = await session.exec(
            select(SysItem).where(SysItem.type == item.type, SysItem.key == item.key)
        )
        existing_item = existing_item.first()

        if existing_item:
            # Update existing item
            # for key, value in item.items():
            #     setattr(existing_item, key, value)
            pass
        else:
            # Create new item
            # new_item = SysItem(**item.model_dump())
            session.add(item)

    await session.commit()
