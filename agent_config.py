from langchain_experimental.agents import create_pandas_dataframe_agent 
from logger_helper import get_logger
import streamlit as st

@st.cache_resource
def initialize_agent(llm, df):
    """Initialize a Pandas DataFrame Agent with logging and error handling."""
    logger = get_logger("agent_config.log")
    
    try:
        logger.info("Initializing Pandas DataFrame Agent...")

        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=False,
            allow_dangerous_code=True,  # The allow_dangerous_code=True is necessary for the agent to work, but you should implement additional security layers around it
            agent_executor_kwargs={"handle_parsing_errors": True},
            return_intermediate_steps=True,
        )

        logger.info("Pandas DataFrame Agent initialized successfully")
        return agent

    except Exception as e:
        logger.exception("Failed to initialize Pandas DataFrame Agent")
        raise