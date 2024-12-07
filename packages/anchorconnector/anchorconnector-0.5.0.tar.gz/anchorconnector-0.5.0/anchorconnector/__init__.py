"""
This package allows you to fetch data from the inofficial Anchor Podcast API.
The API is not documented and may change at any time. Use at your own risk.
"""

from .connector import AnchorConnector

__all__ = ["AnchorConnector"]
