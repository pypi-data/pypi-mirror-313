# biomapper/__init__.py
"""Biomapper package for biological data harmonization and ontology mapping."""

from .standardization.ramp_client import RaMPClient

__all__ = ["RaMPClient"]
__version__ = "0.1.0"  # Also good to expose version here
