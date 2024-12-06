import uuid
import numpy as np
import click

#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibtheque.doi as doi
import bibtheque.isbn as isbn
import bibtheque.bibtex as bibtex

#  ──────────────────────────────────────────────────────────────────────────

doc_fields = ['bib',
              'file_text',
              'file_path',
              'annotated_path',
              'supplemental_path',
              'tags',
              'notes',
              'synopsis',
              ]

# ──────────────────────────────────────────────────────────────────────────

def determine_standard(standard):
    """
    takes: document standard identifier; DOI or ISBN
    returns: dict or None
    """

    if doi.is_doi(standard):
        doi_bib = doi.doi_to_bib(standard)
        doi_bib_dict = bibtex.bib_to_dict(doi_bib)

        return doi_bib_dict

    elif isbn.is_isbn(standard):
        isbn13 = isbn.get_isbn13(standard)
        isbn_bib = isbn.isbn_to_bib(isbn13)
        isbn_bib_dict = bibtex.bib_to_dict(isbn_bib)

        return isbn_bib_dict

    else:
        raise click.ClickException('Given ID is invalid')


def generate_id(standard):
    """Generate UUID with random salt from the document standard identifier.
    """
    namespace = uuid.UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8') # namespace for objective identifiers

    salt = str(np.random.random()) # randomized salt

    return uuid.uuid5(namespace, salt + standard).hex


def build_doc(bib_dict, file_text=None, file_path="", annotated_path="", supplemental_path="", tags=[], notes="", synopsis=""):
    """
    Builds doc dict from the bib dict and user supplied things.
    returns: dict
    """

    doc = {}

    doc['bib'] = bib_dict

    # if file_text:
        # doc['file_text'] = file_text

    doc['file_path'] = file_path
    doc['annotated_path'] = annotated_path
    doc['supplemental_path'] = supplemental_path

    # if len(tags) > 0:
    doc['tags'] = tags

    doc['notes'] = notes
    doc['synopsis'] = synopsis

    return doc


def build_bib(bib_dict, bibkey=None):
    """Build the BibTeX string with the given Bibkey.

    Builds a BibTeX string from a BibTex dictionary.

    Generates a Bibkey based off the BibTeX dictionary if no Bibkey is provided.

    Parameters
    ----------
    bib_dict : dict
        BibTeX dictionary of a document.
    bibkey : str
        Unique Bibkey string for the BibTeX string. Defaults to None.

    Returns
    -------
    bib : str
        BibTeX string.
    """

    if bibkey:
        bib_dict['key'] = bibkey

    else:
        bibkey = build_bibkey(bib_dict)

        if not bibkey:
            print("Bibkey not provided and unable to be generated. Please provide a Bibkey.")
            return

        bib_dict['key'] = bibkey
    
    bib = bibtex.build_bib(bib_dict)

    return bib


def lastname(bib_dict):
    """Returns first author's lastname.
    """

    authors = bib_dict['author'].split(' and ')

    first_author = authors[0]
    first_author_lastname = bibtex.author_lastname(first_author)

    return first_author_lastname


def build_bibkey(bib_dict):
    """Builds a unique Bibkey based on the BibTeX dictionary information.

    Fails if the BibTeX dictionary doesn't have an author or year of publication.

    Parameters
    ----------
    bib_dict : dict
        BibTeX dictionary of a document.

    Returns
    -------
    bibkey : str
        Unique Bibkey or None, if generation fails.
    """

    bibkey_list = []
    
    if 'author' in bib_dict:
        bibkey_list.append(lastname(bib_dict))
    
    if 'year' in bib_dict:
        bibkey_list.append(bib_dict['year'])
    
    bibkey = ''.join(bibkey_list)

    if len(bibkey) > 0:
        return bibkey
    else:
        return None

# ──────────────────────────────────────────────────────────────────────────
# print

def et_al(bib_dict):
    """Returns an 'et al.' variant of the authors if there's more than one author.
    """

    if 'author' in bib_dict:
        authors = bib_dict['author'].split(' and ')

        first_author = authors[0]
        first_author_lastname = bibtex.author_lastname(first_author)

        if len(authors) > 1:
            return first_author_lastname + ' et al.'
        else:
            return first_author_lastname

    else:
        return None
