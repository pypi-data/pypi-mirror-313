"""
Langchain Loaders.

Basic Documents Loaders, adapted to be used in Flowtask Tasks.
"""
from .docx import MSWordLoader

__all__ = (
    'MSWordLoader',
)
