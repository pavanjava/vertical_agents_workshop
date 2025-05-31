import asyncio
from dotenv import load_dotenv, find_dotenv
import agent_factory

load_dotenv(find_dotenv())

agent = agent_factory.create_medical_agent_1(debug_mode=True)

async def run_agent():
    # Use the agent with MongoDB-backed memory
    response = await agent.arun(
        """
        I am a Diabetic Doctor and here is my case details: Diabetic Ketoacidosis (DKA)

Case Narrative:
A 23-year-old female with type 1 diabetes mellitus presents with vomiting, abdominal pain, and deep rapid breathing. She reports missing her insulin doses for 2 days.

History & Physical:
Vitals: T36.8°C, HR110bpm, BP100/60mmHg, RR28bpm
General: Alert but fatigued
Hydration: Moderate dehydration, dry mucous membranes
Neurologic: No focal deficits

Key Laboratory Data:
Blood glucose: 520mg/dL
Serum bicarbonate: 10mEq/L
Anion gap: 24
Serum ketones: Positive
ABG (pH): 7.18

Assessment & Management Questions:
1. What criteria confirm the diagnosis of DKA?
2. List the priorities in her acute management including fluids and insulin.
3. How will you monitor and adjust potassium during treatment?
        """,
        user_id="pavanm",
    )

    print(response.content)

if __name__ == "__main__":
    asyncio.run(run_agent())