from bibtexparser import loads
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import splitname, convert_to_unicode

# ──────────────────────────────────────────────────────────────────────────
# functions

def bib_to_dict(bib):
    """Returns a dictionary from the given BibTeX citation.

    Parameters
    ----------
    bib : str
        The BibTeX citation string for the desired work.

    Returns
    -------
    bib_dict : dict
        A dictionary containing the BibTeX citation.
    """

    def translator_from_bibtexparser(bib_dict):

        translation_dict = {'ID': 'key', 'ENTRYTYPE': 'type'}
        fields = list(bib_dict.keys())

        for field in fields:
            if field in translation_dict.keys():
                bib_dict[translation_dict[field]] = bib_dict[field]

        for field in fields:
            if field in translation_dict.keys():
                del bib_dict[field]

        return bib_dict


    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_dict = loads(bib, parser=parser).entries[0]
    bib_dict = translator_from_bibtexparser(bib_dict)

    return bib_dict


def author_lastname(author_str):
    """Returns author's lastname, given a string containing the author's full name.

    Parameters
    ----------
    author_str : str
        String of the author's name.

    Returns
    -------
    lastname : str
        String of the lastname of the author. 
    """

    name_dict = splitname(author_str)
    lastname = name_dict['last'][0]
    
    return lastname


def build_bib(bib_dict):
    """Generates a BibTeX string from a given dictionary of BibTeX field values.

    Parameters
    ----------
    bib_dict : dict
        Dictionary with all the BibTeX fields.

    Returns
    -------
    bib : str
        BibTeX string of the given dictionary.
    """

    bib = ["@" + bib_dict['type'].lower() + "{" + bib_dict['key'],]

    for field in bib_dict.keys():
        bib += [field + " = " + "{" + bib_dict[field] + "}"]

    bib = ",\n\t".join(bib) + "\n}"

    return bib
