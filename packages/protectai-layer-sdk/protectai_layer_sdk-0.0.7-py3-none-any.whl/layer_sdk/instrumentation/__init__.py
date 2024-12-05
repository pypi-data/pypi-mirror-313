"""Instrumentation module for the SDK."""
from typing import Dict, Callable

from ._base import BaseInstrumentor
from ._openai import OpenAIInstrumentation

instrumentor_instances: Dict[str, Callable] = {
    'openai': OpenAIInstrumentation
}

__all__ = ["BaseInstrumentor", "instrumentor_instances"]
