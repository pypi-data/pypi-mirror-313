#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibtheque.isbn as isbn
import tests.test_vars as test_vars

# ──────────────────────────────────────────────────────────────────────────
# test functions

def test_is_isbn():
    assert isbn.is_isbn(test_vars.isbn10) == True


def test_get_isbn13():
    assert isbn.get_isbn13(test_vars.isbn10) == test_vars.isbn13


def test_isbn_to_bib():
    assert isbn.isbn_to_bib(test_vars.isbn13) == test_vars.isbn_bib
