# core/__init__.py
"""
Core package for the Data Cleaning Tool.

This package provides:
- file_handler: File reading and validation utilities.
- preprocessing: Data cleaning and type handling utilities.
- visualization: Professional plotting utilities (dark theme).
"""

from . import file_handler, preprocessing, visualization

__all__ = ["file_handler", "preprocessing", "visualization"]