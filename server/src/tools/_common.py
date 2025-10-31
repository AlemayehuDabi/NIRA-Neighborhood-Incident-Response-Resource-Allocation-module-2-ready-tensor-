import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import asyncio

DEFAULT_TIMEOUT = 12.0

async_client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)

# A generic async retry decorator for network calls
def retry_network(**tenacity_kwargs):
    # default: 3 attempts with exponential backoff
    kwargs = {
        "stop": stop_after_attempt(3),
        "wait": wait_exponential(multiplier=1, min=1, max=10),
        "retry": retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError)),
    }
    kwargs.update(tenacity_kwargs)
    return retry(**kwargs)
