# data_loader.py
import pandas as pd
import os
from pandas.errors import EmptyDataError, ParserError
from logger_helper import get_logger  # Import your logger function

def load_csv_data(file_path, log_file="data_loading.log"):
    """
    Load CSV data with comprehensive error handling and logging.
    
    Args:
        file_path (str): Path to the CSV file
        log_file (str): Log file name for logging operations
        
    Returns:
        pd.DataFrame: Loaded dataframe
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        EmptyDataError: If the CSV file is empty
        ParserError: If there are parsing issues
        Exception: For any other unexpected errors
    """
    logger = get_logger(log_file)
    
    try:
        # Check if file exists before attempting to read
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {os.path.abspath(file_path)}")
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
        # Log file info
        file_size = os.path.getsize(file_path)
        logger.info(f"Loading dataset from: {os.path.abspath(file_path)} ({file_size} bytes)")
        
        # Load data
        df = pd.read_csv(file_path)
        
        # Log success with dataset info
        logger.info(f"Dataset loaded successfully:")
        logger.info(f"  - Shape: {df.shape}")
        logger.info(f"  - Columns: {list(df.columns)}")
        logger.info(f"  - Memory usage: {df.memory_usage(deep=True).sum()} bytes")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"Dataset file not found: {file_path}")
        logger.error(f"Current working directory: {os.getcwd()}")
        raise
        
    except EmptyDataError:
        logger.error("The CSV file is empty or contains no parseable data")
        raise
        
    except ParserError as e:
        logger.error(f"CSV parsing error: {e}")
        logger.info("Consider checking file format, delimiters, or using error_bad_lines=False")
        raise
        
    except Exception as e:
        logger.exception(f"Unexpected error loading dataset")
        raise
