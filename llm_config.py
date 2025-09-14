# llm_config.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from logger_helper import get_logger

from dotenv import load_dotenv
load_dotenv()

def initialize_llm():
    """Initialize ChatGoogleGenerativeAI with environment variable for API key."""
    logger = get_logger("llm_config.log")
    
    try:
        # Get API key from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable not found")
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        logger.info("ChatGoogleGenerativeAI initialized successfully")
        return llm
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
        
    except Exception as e:
        logger.exception("Failed to initialize ChatGoogleGenerativeAI")
        raise
