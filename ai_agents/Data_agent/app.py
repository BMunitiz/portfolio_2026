"""
Data Analyst Application using Pandas AI and LLMs
================================================

This application allows users to upload CSV files and ask questions about the data.
It uses Pandas AI and LLMs to analyze the data and provide insights.
"""

import streamlit as st
import pandas as pd
import pandasai as pai
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
from langchain_groq.chat_models import ChatGroq
import os
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_llm() -> Optional[ChatGroq]:
    """Initialize the language model with proper error handling."""
    try:
        # Check if API key is available
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY environment variable not set")
            st.error("GROQ_API_KEY environment variable not set. Please configure your API key.")
            return None

        #llm = Ollama(model = "gpt-oss:20b", temperature = 0)
        llm = ChatGroq(model_name='llama-3.3-70b-versatile', temperature=0.2, api_key=api_key)
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        st.error(f"Failed to initialize the language model: {str(e)}. Please check your API key and connection.")
        return None

st.title("Data analyst powered by Pandas AI")

uploaded_file = st.file_uploader("Upload your file", type="csv")

if uploaded_file is not None:
    try:
        # Validate file type
        if not uploaded_file.name.endswith('.csv'):
            st.error("Please upload a CSV file")
            st.stop()

        # Read CSV file with error handling
        data = pd.read_csv(uploaded_file, low_memory=False)

        # Validate data
        if data.empty:
            st.warning("The uploaded file is empty")
            st.stop()

        st.write(data.head(5))

        # Initialize SmartDataframe with error handling
        df = SmartDataframe(data, config={"llm": llm})

        prompt = st.text_area("Qué quieres saber?")
        if st.button("Generar"):
            if prompt:
                with st.spinner("Analizando"):
                    try:
                        response = df.chat(prompt)
                        if response is not None:
                            # Check if response is an image path or text
                            if isinstance(response, str) and response.lower().endswith(('.png', '.jpg', '.jpeg')):
                                st.image(response)
                            else:
                                st.write(response)
                        else:
                            st.warning("No response generated. Please try a different query.")
                    except Exception as e:
                        logger.error(f"Error during chat processing: {str(e)}")
                        st.error("An error occurred while processing your request. Please try again.")
            else:
                st.warning("Introduce tu consulta")

    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or invalid")
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Please check the file format.")
    except Exception as e:
        logger.error(f"Error processing uploaded file: {str(e)}")
        st.error("An error occurred while processing the file. Please try again.")
else:
    st.info("Please upload a CSV file to begin analysis")



