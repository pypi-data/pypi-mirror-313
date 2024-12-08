import os
from datetime import datetime
from loguru import logger
import sys
from logtail import LogtailHandler
from functools import wraps
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Remove the default handler first
logger.remove()

# 1. Handler for console output - less verbose output
logger.add(
    sys.stderr,
    level="INFO",
    backtrace=False,  # Don't show traceback
    diagnose=False    # Don't show variables
)

# 2. Handler for system storage - keep full details for debugging
logs_dir = "logs/"
os.makedirs(logs_dir, exist_ok=True)
logger.add(
    os.path.join(logs_dir, "bjarkan_{time:YYYY-MM-DD}.log"),
    level="INFO",
    rotation="00:00",
    retention="7 days",
    backtrace=True,   # Keep full traceback in file
    diagnose=True     # Keep variables in file
)

# 3. Add the Better Stack logger
token = os.getenv("BETTERSTACK_TOKEN")
handler = LogtailHandler(token)
logger.add(
    handler,
    format="{message}",
    level="INFO",
    backtrace=True,
    diagnose=True
)


# Decorator for error catching (supports both sync and async functions)
def catch_exception(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {str(e)}")
            raise

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {str(e)}")
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# Initialize logger with basic info
logger.info("Bjarkan SDK Logger initialized")
