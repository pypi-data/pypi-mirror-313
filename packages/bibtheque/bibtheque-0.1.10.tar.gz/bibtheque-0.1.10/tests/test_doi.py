#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibtheque.doi as doi
import tests.test_vars as test_vars

# ──────────────────────────────────────────────────────────────────────────
# test functions

def test_is_doi():
    assert doi.is_doi(test_vars.doi_url) == True
    assert doi.is_doi(test_vars.doi_str) == True


def test_doi_to_bib():
    assert doi.doi_to_bib(test_vars.doi_url) == test_vars.doi_bib
    assert doi.doi_to_bib(test_vars.doi_str) == test_vars.doi_bib
