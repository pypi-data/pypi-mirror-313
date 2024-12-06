from pypdf import PdfReader
import click
import json
import re
from pathlib import Path

#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibtheque.fields as fields
import bibtheque.document as document
import bibtheque.strings as strings

#  ──────────────────────────────────────────────────────────────────────────

class Index():

    def __init__(self, config, initialize=False):
        self.config = config['index']
        self.path = Path(self.config['path']).expanduser()

        # handling initialization
        if initialize:
            self.init()
        else:
            self.read()


    def init(self):
        """Initializes the index.json file"""
        if not self.path.exists():
            self.path.parent.mkdir(parents=True)

        with click.open_file(self.path, 'w') as file:
            json.dump({}, file)


    def read(self):
        """Reads the index.json file"""
        with click.open_file(self.path, 'r') as file:
            self.index = json.load(file)


    def write(self):
        """Write changes to index file"""
        with click.open_file(self.path, 'w') as file:
            json.dump(self.index, file)


    def exists(self, doc_id):
        if doc_id in self.index:
            return True
        else:
            return False


    def insert(self, doc_id, doc, force=False):
        """Inserts document into the index"""

        # looking for duplicates
        ignore_common_bib_fields = list(set(fields.all_fields) - set(['publisher', 'url', 'type', 'month', 'year', 'number', 'volume']))
        duplicates = self.find_duplicates(doc, bib_fields=ignore_common_bib_fields)

        if force or not duplicates:
            self.index[doc_id] = doc
        else:
            doc_str = json.dumps(doc, indent=4)
            json_str = json.dumps(duplicates, indent=4)
            raise click.ClickException(click.style('Duplicates found:\n', bold=True) + click.style('Submitted:\n', bold=True) + click.style(doc_str) + click.style('\nDuplicates:\n', bold=True) + click.style(json_str))


    def modify(self, doc_id):
        if self.exists(doc_id):
            old = self.index[doc_id]

            tmp = json.dumps(self.index[doc_id])
            tmp = click.edit(tmp, extension='.json')

            if tmp: # if changes are made, return the differences or return Nones
                self.index[doc_id] = json.loads(tmp) # index modified here

                # getting differences
                tmp = json.loads(tmp)
                diff = {}
                for attr in tmp:
                    if attr == 'bib':

                        diff[attr] = {}
                        for field in tmp[attr]:
                            if field not in old[attr] or tmp[attr][field] != old[attr][field]:
                                diff[attr][field] = tmp[attr][field]

                        if not diff[attr]:
                            del diff[attr]

                    elif attr == 'tags':
                        diff[attr] = []
                        for tag in tmp[attr]:
                            if tag not in old[attr]:
                                diff[attr].append(tag)

                        if not diff[attr]:
                            del diff[attr]

                    else:
                        if attr not in old or tmp[attr] != old[attr]:
                            diff[attr] = tmp[attr]

                if diff:
                    return old, diff
                else:
                    return None, None
            else:
                return None, None

        else:
            raise click.ClickException('Doc not found')


    def delete(self, doc_id):
        """Delete doc from the index"""
        if self.exists(doc_id):
            del self.index[doc_id]


    def search(self, regex):
        """Search through index with regex"""
        hits = {}

        for doc_id in self.index:

            hit = {}

            for attr in self.index[doc_id]:

                # search through
                if attr == 'bib':

                    hit[attr] = {}

                    for field in self.index[doc_id][attr]:
                        if re.search(regex, self.index[doc_id][attr][field]):
                            hit[attr][field] = re.finditer(regex, self.index[doc_id][attr][field])

                    if not hit[attr]:
                        del hit[attr]

                elif attr == 'tags':

                    hit[attr] = {}

                    for tag in self.index[doc_id][attr]:
                        if re.search(regex, tag):
                            hit[attr][tag] = re.finditer(regex, tag)

                    if not hit[attr]:
                        del hit[attr]

                else:
                    if re.search(regex, self.index[doc_id][attr]):
                        hit[attr] = re.finditer(regex, self.index[doc_id][attr])

            if hit:
                hits[doc_id] = hit
        
        return hits


    def find_duplicates(self, doc, search_docs=None, doc_fields=None, bib_fields=None, duplicate_threshold=None, length_threshold=None):
        """Searches docs by field for duplicate fields"""

        def _find(self, doc, search_docs, doc_fields, bib_fields, duplicate_threshold, length_threshold):
            """Searches docs by field for duplicate fields: ACTUAL LOGIC"""

            duplicates = {}
            for doc_id in search_docs:

                duplicate_doc = {}

                # search doc_fields
                for doc_field in doc_fields:

                    if doc_field in doc and doc_field in search_docs[doc_id]:

                        # search by bib_fields
                        if doc_field == 'bib':

                            duplicate_doc[doc_field] = {}

                            for bib_field in bib_fields:
                                if bib_field in doc[doc_field] and bib_field in search_docs[doc_id][doc_field]:
                                    if 0 < len(doc[doc_field][bib_field]) < length_threshold and 0< len(search_docs[doc_id][doc_field][bib_field]) < length_threshold:
                                        if strings.matching(doc[doc_field][bib_field], search_docs[doc_id][doc_field][bib_field], duplicate_threshold):
                                            duplicate_doc[doc_field][bib_field] = search_docs[doc_id][doc_field][bib_field]

                            # removing if no duplicates in bib_fields are found
                            if not duplicate_doc[doc_field]:
                                del duplicate_doc[doc_field]

                        # ignore tags
                        elif doc_field == 'tags':
                            pass

                        # search everything else normally

                        elif 0 < len(doc[doc_field]) < length_threshold and 0 < len(search_docs[doc_id][doc_field]) < length_threshold:
                            if strings.matching(doc[doc_field], search_docs[doc_id][doc_field], duplicate_threshold):
                                duplicate_doc[doc_field] = search_docs[doc_id][doc_field]

                if duplicate_doc:
                    duplicates[doc_id] = duplicate_doc

            return duplicates


        def _search_fields(search_fields, all_fields):
            """Setting search fields"""

            if not search_fields:
                search_fields = all_fields
            else:
                for field in search_fields:
                    if field not in all_fields:
                        click.echo(field, 'not an allowable field') # FIX
                        raise click.Abort

            return search_fields


        # setting search_docs to all docs by default
        if not search_docs:
            search_docs = self.index

        # set doc_fields to search through
        doc_fields = _search_fields(doc_fields, document.doc_fields)

        # sets bib_fields to all if none are specified
        bib_fields = _search_fields(bib_fields, fields.all_fields)

        # setting default threshold from config
        if not duplicate_threshold:
            duplicate_threshold = self.config['duplicate_threshold']

        # setting length threshold from config
        if not length_threshold:
            length_threshold = self.config['length_threshold']

        duplicates = _find(self, doc, search_docs, doc_fields, bib_fields, duplicate_threshold, length_threshold)

        return duplicates


    def find_all_duplicates(self):
        """Find all duplicates in the index"""

        all_duplicates = {}

        for pivot_doc_id in self.index:

            search_docs = {}

            for searchable_doc_id in self.index:
                if pivot_doc_id != searchable_doc_id:
                    search_docs[searchable_doc_id] = self.index[searchable_doc_id]

            all_duplicates[pivot_doc_id] = self.find_duplicates(self.index[pivot_doc_id], search_docs=search_docs)

        return all_duplicates


    def read_pdf(self, pdf_path):
        """Extracts text from PDF"""

        if Path(pdf_path).suffix == '.pdf':

            # extracting text
            readpdf = PdfReader(pdf_path)
            pdf_text = ''
            for page in readpdf.pages:
                pdf_text += page.extract_text()

            return pdf_text

        else:
            click.echo('Not a pdf')
            return None


    def file_exists(self, doc_id, other=False):
        """other is either ['annotated', 'supplemental']"""
        if other:
            if other in ['annotated', 'supplemental']:
                path_name = other + '_path'
            else:
                click.echo(other + ' not an allowable field')
                return None

        else:
            path_name = 'file_path'

        if self.index[doc_id][path_name]:
            return True
        else:
            return False
