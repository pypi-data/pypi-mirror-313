"""
# ΦωΦ (pronounced owega)

ΦωΦ is a command-line interface for conversing with GPT models (from OpenAI),
Mistral API, and chub.ai API.
"""
from . import owega, utils
from .changelog import OwegaChangelog as _oc

__version__ = _oc.version
__all__ = ['owega', 'utils', "__version__"]
