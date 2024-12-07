import importlib.metadata

__version__ = importlib.metadata.version("mem302ai")

from mem302ai.client.main import MemoryClient, AsyncMemoryClient  # noqa
from mem302ai.memory.main import Memory  # noqa
