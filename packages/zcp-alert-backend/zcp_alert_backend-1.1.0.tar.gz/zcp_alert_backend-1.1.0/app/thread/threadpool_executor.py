# Create a thread pool executor for application
from concurrent.futures import ThreadPoolExecutor
import logging

from app import settings

log = logging.getLogger('appLogger') 

executor = ThreadPoolExecutor(max_workers=settings.MAX_THREAD_COUNT)
log.info(f"Thread pool executor created with max workers: {settings.MAX_THREAD_COUNT}")

def get_executor():
    return executor
