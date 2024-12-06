from habanero import cn

# ──────────────────────────────────────────────────────────────────────────
# functions

def is_doi(url):
    """Check if a URL is a DOI URL or string.

    Parameters
    ----------
    url : str
        Potential DOI URL or string.

    Returns
    -------
    bool
        True if it is a DOI URL, False if not.
    """

    try:
        cn.content_negotiation(ids=url)
        return True

    except:
        return False


def doi_to_bib(doi):
    """Retrieves the BibTeX citation for a document with a given DOI.

    Parameters
    ----------
    doi : str
        The DOI string of the desired document.

    Returns
    -------
    bib : str
        The BibTeX citation of the given DOI.
    """
    
    try:
        doi_bib = cn.content_negotiation(ids=doi, format='bibtex').strip()

    except:
        raise

    return doi_bib
