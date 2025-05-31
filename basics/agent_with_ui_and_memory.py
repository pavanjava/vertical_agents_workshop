import os

import streamlit as st
from textwrap import dedent
import uuid
import pandas as pd
from datetime import datetime

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Import your memory utility
from basics.mem0_memory.mem0_util import memory

# Page configuration
st.set_page_config(
    page_title="Agent with Realtime Memory",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #4284f3;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #9b59b6;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    .error-message {
        background-color: #ffebee;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #f44336;
        color: #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agent_id' not in st.session_state:
    st.session_state.agent_id = str(uuid.uuid4())
if 'user_id' not in st.session_state:
    st.session_state.user_id = "pavanm"

def initialize_agent(user_id):
    """Initialize the restaurant recommendation agent"""
    try:
        # Claude(id="claude-sonnet-4-20250514", temperature=0.6)
        # OpenAIChat(id="gpt-4.1", temperature=0.6)
        # Gemini(id="gemini-2.0-flash", temperature=0.6)
        agent = Agent(
            model=Claude(id="claude-sonnet-4-20250514", temperature=0.6),
            tools=[GoogleSearchTools()], # DuckDuckGoTools()
            context={"context": memory.get_all(user_id=user_id)},
            instructions=dedent("""\
            1. Always give your recommendations in the table format.
            2. Include the restaurant name, location, rating, speciality as the table columns.
            """),
            additional_context=dedent("""\
            IMPORTANT: Always check the context and identify the user behaviour and adapt to the users preferences while answering.
            """),
            add_context=True,
            debug_mode=True,  # Set to False for cleaner UI
            show_tool_calls=True
        )
        return agent
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return None

def process_agent_response(run_response):
    """Process the agent response and extract table data"""
    try:
        # Get the response content
        if run_response.content:
            response_text = str(run_response.content)

            # Try to extract table data from the response
            # This is a simple approach - you might need to enhance this based on your agent's output format
            lines = response_text.split('\n')
            table_data = []
            headers = []

            for line in lines:
                if '|' in line and line.strip():
                    cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                    if cells:
                        if not headers:
                            headers = cells
                        else:
                            table_data.append(cells)

            return response_text, table_data, headers
        return "", [], []
    except Exception as e:
        st.error(f"Error processing response: {str(e)}")
        return "", [], []

# Main UI
st.markdown("<h1 class='main-header'> Agent With Realtime Memory</h1>", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    # User ID input
    user_id = st.text_input("User ID", value=st.session_state.user_id, key="user_id_input")
    if user_id != st.session_state.user_id:
        st.session_state.user_id = user_id
        st.session_state.agent = None  # Reset agent when user changes

    # Model temperature
    temperature = st.slider("Model Temperature", 0.0, 1.0, 0.6, 0.1)

    # Initialize agent button
    if st.button("Initialize Agent", type="primary"):
        with st.spinner("Initializing agent..."):
            st.session_state.agent = initialize_agent(st.session_state.user_id)
        if st.session_state.agent:
            st.success("Agent initialized successfully!")
        else:
            st.error("Failed to initialize agent")

    # Memory section
    st.header("Memory Context")
    if st.button("View Memory"):
        try:
            user_memory = memory.get_all(user_id=st.session_state.user_id)
            if user_memory:
                st.json(user_memory)
            else:
                st.info("No memory found for this user")
        except Exception as e:
            st.error(f"Error retrieving memory: {str(e)}")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Chat with the Agent")

    # Initialize agent if not already done
    if st.session_state.agent is None:
        st.info("Please initialize the agent from the sidebar before starting the conversation.")
        if st.button("Quick Initialize"):
            with st.spinner("Initializing agent..."):
                st.session_state.agent = initialize_agent(st.session_state.user_id)
            if st.session_state.agent:
                st.success("Agent initialized!")
                st.rerun()

    else:
        # Chat input
        user_input = st.text_input("Your message:", key="user_input", placeholder="Hi, I'm looking for restaurants near Gachibowli for lunch...")

        send_message = st.button("Send", type="primary")

        # Process user input
        if send_message and user_input.strip():
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })

            # Show loading spinner
            with st.spinner("Agent is thinking..."):
                try:
                    # Create prompt with context
                    prompt = dedent(f"""\
                    Given the context:
                    ----------------------------
                    {memory.get_all(user_id=st.session_state.user_id)}
                    ----------------------------
                    Answer the user query based on the context provided.
                    User: {user_input}
                    """)

                    # Run the agent
                    run_response = st.session_state.agent.run(prompt)

                    # Process response
                    response_text, table_data, headers = process_agent_response(run_response)

                    # Add agent response to chat history
                    st.session_state.chat_history.append({
                        "role": "agent",
                        "content": response_text,
                        "table_data": table_data,
                        "headers": headers,
                        "timestamp": datetime.now()
                    })

                    # Store in memory
                    if run_response.messages:
                        messages = [
                            {"role": msg.role, "content": str(msg.content)}
                            for msg in run_response.messages
                        ]
                        memory.add(
                            messages,
                            user_id=st.session_state.user_id,
                            agent_id=st.session_state.agent_id,
                            infer=False
                        )

                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "error",
                        "content": f"Error: {str(e)}",
                        "timestamp": datetime.now()
                    })

            # Clear the input box by deleting from session state
            if 'user_input' in st.session_state:
                del st.session_state['user_input']

            # Refresh to show new message and clear input
            st.rerun()

        # Display chat history
        st.header("Conversation History")
        chat_container = st.container()

        with chat_container:
            # Display most recent messages at the top
            for message in reversed(st.session_state.chat_history):
                timestamp = message["timestamp"].strftime("%H:%M:%S")

                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You ({timestamp}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

                elif message["role"] == "agent":
                    st.markdown(f"""
                    <div class="agent-message">
                        <strong>Agent ({timestamp}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

                    # Display table if available
                    if message.get("table_data") and message.get("headers"):
                        try:
                            df = pd.DataFrame(message["table_data"], columns=message["headers"])
                            st.table(df)
                        except Exception as e:
                            st.error(f"Error displaying table: {str(e)}")

                elif message["role"] == "error":
                    st.markdown(f"""
                    <div class="error-message">
                        <strong>Error ({timestamp}):</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

# Right column for additional features
with col2:
    # Statistics
    st.header("Chat Statistics")
    total_messages = len(st.session_state.chat_history)
    user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    agent_messages = len([m for m in st.session_state.chat_history if m["role"] == "agent"])

    st.metric("Total Messages", total_messages)
    st.metric("Your Messages", user_messages)
    st.metric("Agent Responses", agent_messages)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Powered by Claude Sonnet 4", unsafe_allow_html=True)