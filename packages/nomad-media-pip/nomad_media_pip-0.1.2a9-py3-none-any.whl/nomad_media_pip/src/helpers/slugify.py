"""
This module contains a function to slugify text.

Functions:
    _slugify: Slugifies text.
"""

import re
import unicodedata


def _slugify(text: str) -> str:
    """
    Slugifies text.

    Args:
        text (str): The text to slugify.

    Returns:
        str: The slugified text.
    """

    if not text or len(text.strip()) == 0:
        return ""

    text = str(text)
    text = unicodedata.normalize("NFD", text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.lower()
    text = text.strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w-]+', '', text)
    text = re.sub(r'--+', '-', text)
    return text
