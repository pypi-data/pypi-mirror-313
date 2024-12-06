import isbnlib
from isbnlib.registry import bibformatters
import bibtexparser

# ──────────────────────────────────────────────────────────────────────────
# functions

def is_isbn(url):
    """Check if the given URL has an ISBN

    Parameters
    ----------
    url : str
        URL with potential ISBN.

    Returns
    -------
    bool
        True if there is an ISBN, False if not.
    """

    return not isbnlib.notisbn(url)


def get_isbn13(isbn_gen_str):
    """Returns a clean ISBN number if one exists in the given argument.

    Parameters
    ----------
    isbn_gen_str : str
        Potentially "dirty" string containing an ISBN number, possibly embedded in an URL.

    Returns
    -------
    isbn13 : str
        ISBN 13 number
    """

    isbn_like = isbnlib.get_isbnlike(isbn_gen_str, level='loose')[-1]  # Get ISBN from a URL or ISBN string.
    clean_isbn_like = isbnlib.clean(isbn_like)

    if isbnlib.is_isbn10(clean_isbn_like):  # Check if the ISBN is ISBN10 and changing it to ISBN13 if it is.
        isbn13 = isbnlib.to_isbn13(clean_isbn_like)
    else:
        isbn13 = clean_isbn_like

    return isbn13


def isbn_to_bib(isbn13):
    """Retrieves the BibTeX citation for a document with a given ISBN-13.

    Parameters
    ----------
    isbn : str
        The ISBN-13 number of the desired document.

    Returns
    -------
    bib : str
        The BibTeX citation of the given ISBN-13.
    """
    
    try:
        isbn_dict = isbnlib.meta(isbn13)
        isbn_bib = bibformatters['bibtex'](isbn_dict)

    except:
        raise

    return isbn_bib


