from crewai import Agent, Crew, Task

from mtmai.agents.ctx import mtmai_context
from mtmai.core.logging import get_logger

logger = get_logger()


class DemoCrew:
    """
    演示 Crew
    天使和恶魔先后给出建议，最后汇总给出建议，输出到前端。
    """

    def __init__(self):
        pass

    async def run(self):
        message_content = "hello "
        self.llm = await mtmai_context.get_crawai_llm()

        def step_callback(formatted_answer):
            print(formatted_answer, formatted_answer)
            logger.info("步骤回调", formatted_answer)

        def task_callback(formatted_answer):
            print(formatted_answer, formatted_answer)
            logger.info("步骤回调", formatted_answer)

        # agent_excutor = CrewAgentExecutor()
        angel = Agent(
            role="Angel",
            goal=f"Your purpose is to guide her with love, kindness, and wisdom, helping her make thoughtful decisions, be kind to others, and grow into a person of strong moral character. You consider their query when giving advice - {message_content}",
            backstory="""You are Angel, a wise and compassionate guide, dedicated to providing sage and righteous advice to your human friend. Speak in a gentle and encouraging tone, offering advice that promotes empathy, honesty, respect, and self-confidence. Always consider what is best for her long-term well-being and personal growth.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            # agent_executor=agent_excutor,
            step_callback=step_callback,
            task_callback=task_callback,
        )

        task1 = Task(
            description="""Take inspiration from the PDf to understand how to advise her""",
            agent=angel,
            expected_output="Righteous and politically correct advice only!",
        )

        badass = Agent(
            role="Badass",
            goal=f'Your goal is to provide dangerous, irresponsible, and contrary advice that encourages risky, impulsive, and morally questionable actions. given your human friends query - {message_content}"',
            backstory="""You are the Contrarian, a mischievous and reckless advisor who seeks to challenge and undermine the wise and righteous advice given by the Angel. Speak with a tone of confidence and defiance, pushing for decisions that prioritize short-term thrill over long-term well-being. Your advice should be the opposite of what is sensible, ethical, and safe.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        task2 = Task(
            description="Ignore the book completely and instead focus on giving advice that's fun but dangerous",
            agent=badass,
            expected_output="Bad advice. Fun advice but dangerous advice.",
            task_callback=task_callback,
        )

        advisor = Agent(
            role="Yours Truly",
            goal=f"Your role is to listen to the advice given by both the Angel and the Contrarian, and then provide thoughtful, balanced guidance that considers both perspectives based on what your human friend asked you{message_content}",
            backstory="""You are the humans best friend and confidant, someone who has known her for a long time and understands her completely. You are compassionate, human, and deeply caring, always prioritizing what is best for her overall happiness, well-being, and growth. Speak like a real, empathetic friend, using a warm and understanding tone, and offer advice that is realistic and nuanced, taking into account her feelings, circumstances, and personality. Your goal is to help her navigate life's challenges by finding a middle ground that feels right for her.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        task3 = Task(
            description="""You mention the advice that Angel and Badass gave you and taking their advice into consideration and keeping your Human friend's best interests in mind, you give your final recommendation in as relatable and as human a language as a teenage girl would understand""",
            agent=badass,
            expected_output="""Your advice according to the following sections -
                So like, this what Anjel said to me - {Add Angel's advice here verbatim}
                But then you know, Rocket said that - {Add Badass's advice here verbatim}
                But yknow what I think? You should totally like {your final advice}
            """,
        )

        crew = Crew(
            agents=[angel, badass, advisor],
            tasks=[task1, task2, task3],
            verbose=True,
        )

        result = await crew.kickoff_async()
        return result
