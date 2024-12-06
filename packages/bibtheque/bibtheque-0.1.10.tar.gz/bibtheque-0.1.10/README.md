# PyBibthèque

Command line program to organize and manage a bibliography or references.

## Notes

Connects to mongodb database via a URI.
The details are in the config at `.config/bibtheque.toml`
Run tests with `pytest`


Still need to come up with a universal id system. I like doi and isbn but that doesn't work when a paper or book doesn't have that (like for a manual entry). I'm considering making a hash to id idea but I'm not sure if that's the best. I need to investigate particular hashes.

I need to implement the side of bibtheque that outputs bibtex strings to a bib file with correct ids for use in an article 

Fill out the argument parser help doc.

Integrate tags and notes in the cli.py

## running

`pip install -e <path>` to install and run

## bibtex

https://www.bibtex.com/format/

## setup

library
|- database.json
|- raw/
|- annotated/
|- .gitignore

### initialize

bibtheque init

- make library folder and folder structure
- make database.json
- make default config at .config/bibtheque.yml
- make .gitignore with raw/ and annotated/ in it


### insert files

insert files with `insert -f` ? (f flag for file?)

original filename is stored
file is renamed according to uuid given to it and moved
when entry is called, original file is returned (uuid.pdf renamed original.pdf)

### versioning

use git for database.json and config

## BibTeX

### entry types

article
book
booklet
conference (same as inproceedings)
inbook
incollection
inproceedings
manual
mastersthesis
misc
phdthesis
proceedings
techreport
unpublished

#### required and optional fields

type
- required
- optional

article
- author, title, journal, year, volume
- number, pages, month, doi, note, key

book
- author or editor, title, publisher, year
- volume or number, series, address, edition, month, note, key, url

booklet
- title
- author, howpublished, address, month, year, note, key

conference (see inproceedings)

inbook
- author or editor, title, chapter or pages, publisher, year
- volume or number, series, type, address, edition, month, note, key

incollection
- author, title, booktitle, publisher, year
- editor, volume or number, series, type, chapter, pages, address, edition, month, note, key

inproceedings
- author, title, booktitle, year
- editor, volume or number, series, pages, address, month, organization, publisher, note, key

manual
- title
- author, organization, address, edition, month, year, note, key

mastersthesis
- author, title, school, year
- type, address, month, note, key

misc
- 
- author, title, howpublished, month, year, note, key

phdthesis
- author, title, school, year
- type, address, month, note, key

proceedings
- title, year
- editor, volume or number, series, address, month, publisher

techreport
- author, title, institution, year
- type, number, address, month, note, key

unpublished
- author, title, note
- month, year, key

### fields

address
annote
author
booktitle
Email
chapter
crossref
doi
edition
editor
howpublished
institution
journal
key
month
note
number
organization
pages
publisher
school
series
title
type
volume
year

## database

all bibtex fields
read flag
tags
organization tags
synopsis
annotations
raw_path
annotated_path

###
 
doc_dict
- bib_dict (dict) -> doc_dict['bib']
    - fields (str)
- read flag (bool)
- tags (list) -> including project labels
- synopsis (str)
- notes (str)
- path_dict (dict) -> doc_dict['path']
    - raw_path (str)
    - annotated_path (str)

## database

- type
    - alphabetical order of required fields

Connect:

```
mongosh "mongodb://144.44.44.44" --username root --password pass
```


    doc = {}

    doc['bib'] = bib_dict

    if file_text:
        doc['file_text'] = file_text

    if file_path:
        doc['file_path'] = file_path

    if annotated_path:
        doc['annotated_path'] = annotated_path

    # if len(tags) > 0:
    doc['tags'] = tags

    if notes:
        doc['notes'] = notes

    if synopsis:
        doc['synopsis'] = synopsis
