"""
Simple pagination helper function.
Moved into its own module to make it easier to test.
"""

import math


def number_of_pages(number_of_items: int, items_per_page: int) -> int:
    """
    Calculates the number of pages for a given number of items and items per page.
    E.g. 20 items, 15 items per page = 2 pages (ceil division)
    """
    return math.ceil(number_of_items / items_per_page) if items_per_page else 0
