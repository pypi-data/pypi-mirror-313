"""
Tests for the anchorconnector.pagination module
"""

import pytest

from anchorconnector.pagination import number_of_pages


@pytest.mark.parametrize(
    # Calculates the number of pages for a given number of items and items per page.
    # E.g. 20 items, 15 items per page = 2 pages (ceil division)
    "number_of_items, items_per_page, expected_number_of_pages",
    [
        (20, 15, 2),
        (20, 20, 1),
        (20, 10, 2),
        (20, 5, 4),
        (20, 1, 20),
        (0, 1, 0),
        (0, 0, 0),
        (0, 10, 0),
        (1, 0, 0),
        (1, 1, 1),
        (1, 2, 1),
        (1, 10, 1),
        (1, 100, 1),
        (100, 1, 100),
    ],
)
def test_number_of_pages(number_of_items, items_per_page, expected_number_of_pages):
    """
    Test the number_of_pages function
    """
    assert number_of_pages(number_of_items, items_per_page) == expected_number_of_pages
