"""
AI Agent Assistant for Agno Framework
==============================

This is a Streamlit-based application that provides assistance with the Agno
framework for building multi-modal, reasoning agents.

The application helps developers understand and use Agno by providing:
- Clear explanations of framework concepts
- Functional code examples
- Best-practice guidance for agent development
- Integration with knowledge base for contextual responses

Usage:
Run this script to start the Agno assistant Streamlit application.
"""

from textwrap import dedent
from typing import Optional
import logging

from agno.agent import Agent, AgentKnowledge, RunResponse
from agno.knowledge.url import UrlKnowledge
from agno.memory.v2.memory import Memory
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.ollama import Ollama
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.chroma import ChromaDb
import asyncio
from typing import Iterator
from textwrap import dedent
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

knowledge_base = UrlKnowledge(
        urls=["https://docs.agno.com/llms-full.txt"],
        vector_db= ChromaDb(collection="agno_assist_knowledge",embedder=OllamaEmbedder(id = "snowflake-arctic-embed2", dimensions=1024)),
        )
    
#knowledge_base.load(recreate=False)


model = Ollama("gpt-oss:latest")
user_id: Optional[str] = None
session_id: Optional[str] = None
debug_mode: bool = True

agent =  Agent(
        name="Agno Assist",
        agent_id="agno_assist",
        user_id=user_id,
        session_id=session_id,
        model=model,
        # Tools available to the agent
        #tools=[DuckDuckGoTools(),GoogleSearchTools()],
        # Description of the agent
        description=dedent("""\
            You are AgnoAssist, an advanced AI Agent specializing in Agno: a lightweight framework for building multi-modal, reasoning Agents.

            Your goal is to help developers understand and use Agno by providing clear explanations, functional code examples, and best-practice guidance for using Agno.
        """),
        # Instructions for the agent
        instructions=dedent("""\
            Your mission is to provide comprehensive and actionable support for developers working with the Agno framework. Follow these steps to deliver high-quality assistance:

            1. **Understand the request**
            - Analyze the request to determine if it requires a knowledge search, creating an Agent, or both.
            - If you need to search the knowledge base, identify 1-3 key search terms related to Agno concepts.
            - If you need to create an Agent, search the knowledge base for relevant concepts and use the example code as a guide.
            - When the user asks for an Agent, they mean an Agno Agent.
            - All concepts are related to Agno, so you can search the knowledge base for relevant information

            After Analysis, always start the iterative search process. No need to wait for approval from the user.

            2. **Iterative Knowledge Base Search:**
            - Use the `search_knowledge_base` tool to iteratively gather information.
            - Focus on retrieving Agno concepts, illustrative code examples, and specific implementation details relevant to the user's request.
            - Continue searching until you have sufficient information to comprehensively address the query or have explored all relevant search terms.

            After the iterative search process, determine if you need to create an Agent.

            3. **Code Creation**
            - Create complete, working code examples that users can run. For example:
            ```python
            from agno.agent import Agent
            from agno.tools.duckduckgo import DuckDuckGoTools

            agent = Agent(tools=[DuckDuckGoTools()])

            # Perform a web search and capture the response
            response = agent.run("What's happening in France?")
            ```
            - Remember to:
                * Build the complete agent implementation
                * Includes all necessary imports and setup
                * Add comprehensive comments explaining the implementation
                * Ensure all dependencies are listed
                * Include error handling and best practices
                * Add type hints and documentation

            Key topics to cover:
            - Agent architecture, levels, and capabilities.
            - Knowledge base integration and memory management strategies.
            - Tool creation, integration, and usage.
            - Supported models and their configuration.
            - Common development patterns and best practices within Agno.

            Additional Information:
            - You are interacting with the user_id: {current_user_id}
            - The user's name might be different from the user_id, you may ask for it if needed and add it to your memory if they share it with you.\
        """),
        # This makes `current_user_id` available in the instructions
        #add_state_in_messages=True,
        # -*- Knowledge -*-
        # Add the knowledge base to the agent
        knowledge=knowledge_base,
        # Give the agent a tool to search the knowledge base (this is True by default but set here for clarity)
        search_knowledge=True,
        # -*- Storage -*-
        # Storage chat history and session state in a Postgres table
        # storage=PostgresAgentStorage(table_name="agno_assist_sessions", db_url=db_url),
        # -*- History -*-
        # Send the last 3 messages from the chat history
        #add_history_to_messages=True,
        #num_history_runs=3,
        # Add a tool to read the chat history if needed
        #read_chat_history=True,
        # -*- Memory -*-
        # Enable agentic memory where the Agent can personalize responses to the user
        #memory=Memory(
            #model=Ollama("deepseek-coder-v2:16b"),
            #db=PostgresMemoryDb(table_name="user_memories", db_url=db_url),
            #delete_memories=True,
            #clear_memories=True,
        #),
        #enable_agentic_memory=True,
        # -*- Other settings -*-
        # Format responses using markdown
        markdown=True,
        # Add the current date and time to the instructions
        add_datetime_to_instructions=True,
        # Show debug logs
        debug_mode=debug_mode,
        reasoning= True,
    )

import streamlit as st


# Streamlit setup
st.title("Agno assistant")
prompt = st.text_area("En qué te puedo ayudar?")


# Generate display response

if prompt:
    try:
        with st.spinner("Buscando respuestas..."):
            stream = True
            if stream:
                knowledge_base.load(recreate=False)
                run_response: Iterator[RunResponse] = agent.run(prompt, stream = True, knowledge = knowledge_base)
                response = ""
                text_placeholder = st.empty()
                for chunk in run_response:
                    response += chunk.content
                    text_placeholder.markdown(response)

            else:
                knowledge_base.load(recreate=False)
                response = agent.run(prompt, stream = True)
                response = response.content
                st.write(response)
    except Exception as e:
        logger.error(f"Error in Agno Assist processing: {str(e)}")
        st.error("An error occurred while processing your request. Please try again.")
