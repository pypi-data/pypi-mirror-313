# Mypy; for the `|` operator purpose
# Remove this __future__ import once the oldest supported Python is 3.10
from __future__ import annotations

import contextlib

from . import exceptions, job_metadata_constants
from .bluequbit_client import BQClient
from .bluequbit_logger import init_logger
from .estimate_result import EstimateResult
from .job_result import JobResult

with contextlib.suppress(ImportError):
    from .qiskit_provider import BlueQubitProvider, EstimatorV2, SamplerV2

from .version import __version__

with contextlib.suppress(ImportError):
    from .__init__private import *  # noqa: F403

__all__ = [
    "BQClient",
    "BlueQubitProvider",
    "EstimateResult",
    "EstimatorV2",
    "JobResult",
    "SamplerV2",
    "__version__",
    "exceptions",
    "job_metadata_constants",
]

logger = init_logger()


def init(api_token: str | None = None) -> BQClient:
    """Returns :class:`BQClient` instance for managing jobs on BlueQubit platform.

    :param api_token: API token of the user. If ``None``, the token will be looked
                      in the environment variable BLUEQUBIT_API_TOKEN.
    """
    return BQClient(api_token)
