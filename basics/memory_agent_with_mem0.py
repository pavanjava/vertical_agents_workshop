from textwrap import dedent

from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
import uuid

from basics.mem0_memory.mem0_util import memory

agent_id = str(uuid.uuid4())
user_id = "pavanm"

agent = Agent(
    model=Claude(id="claude-sonnet-4-20250514", temperature=0.6),
    tools=[DuckDuckGoTools(), GoogleSearchTools()],
    context={"context": memory.get_all(user_id=user_id)},
    instructions=dedent("""\
    1. Always give your recommendations in the table format.
    2. Include the restaurant name, location, rating, speciality as the table columns.
    """),
    additional_context=dedent("""\
    IMPORTANT: Always check the context and identify the user behaviour and adapt to the users preferences while answering.
    """),
    add_context=True,
    debug_mode=True,
    show_tool_calls=True
)

if __name__ == "__main__":
    # print(_memory.get_all(user_id=user_id, limit=5))
    # Hi, my name is Pavan Mantha. I am speaking at HydPy meetup at Gachibowli. Could you find some nearby restaurants for Lunch?
    print("Agent: Introduce yourself and ask your question\n")

    while True:
        try:
            user_input = input("User: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle exit conditions
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Agent: Goodbye!")
                break

            # Run the agent
            prompt = dedent(f"""\
            Given the context:
            ----------------------------
            {memory.get_all(user_id=user_id)}
            ----------------------------
            Answer the user query based on the context provided.
            User: {user_input}
            """)
            run: RunResponse = agent.run(prompt)
            pprint_run_response(run)

            # Process and store messages if they exist
            if run.messages:
                messages = [
                    {"role": msg.role, "content": str(msg.content)}
                    for msg in run.messages
                ]
                memory.add(
                    messages,
                    user_id=user_id,
                    agent_id=agent_id,
                    infer=False
                )

        except KeyboardInterrupt:
            print("\nAgent: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            # Optionally continue or break based on error severity
