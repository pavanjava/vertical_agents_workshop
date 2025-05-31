import asyncio

from dotenv import load_dotenv, find_dotenv
import agent_factory

load_dotenv(find_dotenv())

legal_agent = agent_factory.create_legal_agent()

async def run_agent():
    # comment after the first run
    # legal_agent.knowledge.load(recreate=False)

    response = await legal_agent.arun(
        message="I am a firm lawyer and i want to know the contractual agreement of HealthCare Rewards Inc, what is the project timeline schedule?",
        user_id="pavanm",
        stream=False
    )

    print(response.content)


if __name__ == "__main__":
    asyncio.run(run_agent())