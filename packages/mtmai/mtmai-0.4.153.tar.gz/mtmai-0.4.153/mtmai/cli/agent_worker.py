import asyncio


def register_agent_worker_commands(cli):
    @cli.command()
    def agentworker():
        print("agent worker")
        from mtmai.agent_worker import AgentWorker

        agent_worker = AgentWorker()
        asyncio.run(agent_worker.start())
