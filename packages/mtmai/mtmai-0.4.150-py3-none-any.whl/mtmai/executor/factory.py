# from mtmai.forge.sdk.executor.async_executor import (
#     AsyncExecutor,
#     BackgroundTaskExecutor,
# )


from mtmai.executor.async_executor import AsyncExecutor, BackgroundTaskExecutor


class AsyncExecutorFactory:
    __instance: AsyncExecutor = BackgroundTaskExecutor()

    @staticmethod
    def set_executor(executor: AsyncExecutor) -> None:
        AsyncExecutorFactory.__instance = executor

    @staticmethod
    def get_executor() -> AsyncExecutor:
        return AsyncExecutorFactory.__instance
