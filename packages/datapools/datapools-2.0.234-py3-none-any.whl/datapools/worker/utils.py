import logging
import ctypes
import platform
import gc
from urllib.parse import urlunparse, urlparse

from ..common.queues import QueueMessageType

logger = logging.getLogger(__name__)


def get_worker_storage_invalidation_routing_key(worker_id):
    return f"worker_{worker_id}"


def canonicalize_url(url: str):
    # Normalize the URL to a standard form
    p = urlparse(url.strip())
    # logger.info(f"canonicalize_url {url=} {p=}")
    return urlunparse((p.scheme, p.netloc, p.path if p.path != "/" else "", p.params, p.query, ""))

if platform.system() == 'Darwin':
    libc = ctypes.CDLL('libSystem.dylib')
else:
    libc = ctypes.CDLL('libc.so.6')

def freemem():
    gc.collect()
    libc.malloc_trim(0)
