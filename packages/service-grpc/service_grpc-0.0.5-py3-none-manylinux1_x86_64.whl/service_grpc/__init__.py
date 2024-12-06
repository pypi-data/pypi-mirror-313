from typing import Optional

from .sdk import Run, init, finish

from . import calculator_client
from . import proto


name: str = "service_grpc"

run: Optional[Run] = None

__version__ = "0.0.5"

__all__ = ["calculator_client", "proto", "init", "finish"]
