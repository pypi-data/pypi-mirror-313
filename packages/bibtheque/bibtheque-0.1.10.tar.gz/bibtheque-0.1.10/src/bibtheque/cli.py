import click
import sys
import importlib.metadata
import json
from pathlib import Path
import subprocess
from shutil import which
import http.server
import socketserver

#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibtheque.document as document
import bibtheque.index as index
import bibtheque.database as database
from bibtheque.config import config

#  ──────────────────────────────────────────────────────────────────────────
# global variables

bibtheque_version = importlib.metadata.version('bibtheque')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def handle_tags(tags):
    """Handle comma delimited tag string"""
    tag_list = tags.split(',')
    tags = []
    for tag in tag_list:
        tags.append(tag.strip())
    return sorted(set(tags))

#  ──────────────────────────────────────────────────────────────────────────
# global options

file_option = click.option('-f', '--file', 'file', default="", help='PDF file path', type=str)
annotated_option = click.option('-a', '--annotated', 'annotated', default="", help='Annotated PDF file path', type=str)
supplemental_option = click.option('-si', '--supplemental', 'supplemental', default="", help='Supplemental PDF file path', type=str)
tags_option = click.option('-t', '--tags', 'tags', default='', help="Comma delimited tags; e.g. 'tag0, tag1, tag2'")
force_option = click.option('--force', is_flag=True, default=False, show_default=True, help='Force command', type=bool)
dry_run_option = click.option('--dry-run', 'dry_run', is_flag=True, default=False, show_default=True, help='Dry run of command')

#  ──────────────────────────────────────────────────────────────────────────
# global arguments

doc_id_arg = click.argument('doc_id', type=str)

#  ──────────────────────────────────────────────────────────────────────────

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(bibtheque_version)
@click.option('--config', type=dict, default=config, help='Configuration')
@click.option('--debug', type=int, default=1, help='Debug traceback level; higher prints more: e.g. 3 prints 3 levels of traceback; a negative value prints all traceback')
@click.option('--init', is_flag=True, default=False, help='Init')
@click.pass_context
def bibtheque(ctx, config, debug, init):
    """A tool to manage bibliographic items, particularily for research.
    """

    # check if rsync and ssh are available
    if which('rsync') and which('ssh'):
        pass
    else:
        raise click.ClickException('rsync and ssh not found')

    # setting debug traceback; value of None prints all
    if debug < 0:
        debug = None

    sys.tracebacklimit = debug

    if init and click.confirm('Initializing an existing Bibtheque index will delete it. Are you sure you want to continue?'):
        pass
    else:
        init = False

    # getting configuration
    ctx.obj = {'index': index.Index(config, initialize=init), 'database': database.Database(config, bibtheque_version, initialize=init), 'config': config}

    # initializing git
    if init:
        ctx.invoke(git, git_commands=['init'])
        ctx.invoke(git, git_commands=['add', ctx.obj['index'].path])
        ctx.invoke(git, git_commands=['commit', '-m', '"Initialization"'])

#  ──────────────────────────────────────────────────────────────────────────
# Insert

@click.command()
@file_option
@annotated_option
@supplemental_option
@tags_option
@click.option('-n', '--notes', 'notes', default='', help='Additional notes', type=str)
@click.option('-s', '--synopsis', 'synopsis', default='', help='Synopsis of the work', type=str)
@force_option
@dry_run_option
@click.argument('standard', type=str)
@click.pass_context
def insert(ctx, file, annotated, supplemental, tags, notes, synopsis, force, dry_run, standard):
    """Insert a document into the database."""

    # build doc dict and id
    doc_bib_dict = document.determine_standard(standard)
    doc_id = document.generate_id(standard)

    # regenerating if index already exists
    while ctx.obj['index'].exists(doc_id):
        doc_id = document.generate_id(standard)

    # adding pdf file text and path
    if file:
        # check if file exists
        with click.open_file(file) as _:
            pass

        # file_text = ctx.obj['index'].read_pdf(file) # DISABLING FOR NOW; NEED TO MAKE ADDITIONAL COMMAND TO EXTRACT PDF TEXT AND PLACE IN REPOSITORY AS SEPARATE FILE
        file_text = ""
        file_path = doc_id + '.pdf'
    else:
        file_text = ""
        file_path = ""

    # adding annotated file path
    if annotated:
        # check if annotated file exists
        with click.open_file(annotated) as _:
            pass

        annotated_path = 'annotated/' + doc_id + '.pdf'
    else:
        annotated_path = ""

    # adding supplemental file path
    if supplemental:
        # check if supplemental file exists
        with click.open_file(supplemental) as _:
            pass

        supplemental_path = 'supplemental/' + doc_id + '.pdf'
    else:
        supplemental_path = ""

    # listifying tags
    if tags:
        tags = handle_tags(tags)
    else:
        tags = []

    # build doc
    doc = document.build_doc(doc_bib_dict, file_text=file_text, file_path=file_path, annotated_path=annotated_path, supplemental_path=supplemental_path, tags=tags, notes=notes, synopsis=synopsis)

    # dry run exit point
    if dry_run:
        dry_run_doc = json.dumps(doc, indent=4)
        click.echo(click.style(doc_id, bold=True) + '\n' + dry_run_doc)

        if click.confirm('Do you wish to insert?'):
            pass
        else:
            return

    # inserting into index
    ctx.obj['index'].insert(doc_id, doc, force=force)

    # writing to index and database
    if (file or annotated or supplemental) and ctx.obj['database'].available(): # checking connectivity

        # adding file to file repository
        if file:
            ctx.obj['database'].write(file, file_path, force=force)

        if annotated:
            ctx.obj['database'].write(annotated, annotated_path, force=force)

        if supplemental:
            ctx.obj['database'].write(supplemental, supplemental_path, force=force)

    else:
        raise click.ClickException('Cannot connect to database')

    # complete write when all else passes
    ctx.obj['index'].write()

    # git adding insert
    ctx.invoke(git, git_commands=['add', ctx.obj['index'].path])
    ctx.invoke(git, git_commands=['commit', '-m', '"Inserted ' + doc_id + '"'])

    # confirmation
    click.echo(click.style('Inserted: ', bold=True) + doc_id)

bibtheque.add_command(insert)

#  ──────────────────────────────────────────────────────────────────────────
# Manually (Insert)

# FIXXXX

@click.command()
@file_option
@annotated_option
@supplemental_option
@tags_option
@click.option('-n', '--notes', 'notes', default='', help='Additional notes', type=str)
@click.option('-s', '--synopsis', 'synopsis', default='', help='Synopsis of the work', type=str)
@force_option
@dry_run_option
@click.argument('standard', type=str)
@click.pass_context
def manual(ctx, file, annotated, supplemental, tags, notes, synopsis, force, dry_run, standard):
    """Manually insert a document into the database."""

    # build doc dict and id
    doc_bib_dict = document.determine_standard(standard)
    doc_id = document.generate_id(standard)

    # regenerating if index already exists
    while ctx.obj['index'].exists(doc_id):
        doc_id = document.generate_id(standard)

    # adding pdf file text and path
    if file:
        # check if file exists
        with click.open_file(file) as _:
            pass

        # file_text = ctx.obj['index'].read_pdf(file) # DISABLING FOR NOW; NEED TO MAKE ADDITIONAL COMMAND TO EXTRACT PDF TEXT AND PLACE IN REPOSITORY AS SEPARATE FILE
        file_text = ""
        file_path = doc_id + '.pdf'
    else:
        file_text = ""
        file_path = ""

    # adding annotated file path
    if annotated:
        # check if annotated file exists
        with click.open_file(annotated) as _:
            pass

        annotated_path = 'annotated/' + doc_id + '.pdf'
    else:
        annotated_path = ""

    # adding supplemental file path
    if supplemental:
        # check if supplemental file exists
        with click.open_file(supplemental) as _:
            pass

        supplemental_path = 'supplemental/' + doc_id + '.pdf'
    else:
        supplemental_path = ""

    # listifying tags
    if tags:
        tags = handle_tags(tags)
    else:
        tags = []

    # build doc
    doc = document.build_doc(doc_bib_dict, file_text=file_text, file_path=file_path, annotated_path=annotated_path, supplemental_path=supplemental_path, tags=tags, notes=notes, synopsis=synopsis)

    # dry run exit point
    if dry_run:
        dry_run_doc = json.dumps(doc, indent=4)
        click.echo(click.style(doc_id, bold=True) + '\n' + dry_run_doc)

        if click.confirm('Do you wish to insert?'):
            pass
        else:
            return

    # inserting into index
    ctx.obj['index'].insert(doc_id, doc, force=force)

    # writing to index and database
    if (file or annotated or supplemental) and ctx.obj['database'].available(): # checking connectivity

        # adding file to file repository
        if file:
            ctx.obj['database'].write(file, file_path, force=force)

        if annotated:
            ctx.obj['database'].write(annotated, annotated_path, force=force)

        if supplemental:
            ctx.obj['database'].write(supplemental, supplemental_path, force=force)

    else:
        raise click.ClickException('Cannot connect to database')

    # complete write when all else passes
    ctx.obj['index'].write()

    # git adding insert
    ctx.invoke(git, git_commands=['add', ctx.obj['index'].path])
    ctx.invoke(git, git_commands=['commit', '-m', '"Inserted ' + doc_id + '"'])

    # confirmation
    click.echo(click.style('Inserted: ', bold=True) + doc_id)

bibtheque.add_command(manual)

#  ──────────────────────────────────────────────────────────────────────────
# Modify

@click.command()
@file_option
@annotated_option
@supplemental_option
@tags_option
@force_option
@doc_id_arg
@click.pass_context
def modify(ctx, file, annotated, supplemental, tags, force, doc_id):
    """Opens the default text editor to edit the document with the given DOC_ID."""

    # adding file
    if file:
        attr = 'file_path'
        overwrite = False
        if attr in ctx.obj['index'].index[doc_id]:
            if force or click.confirm('Are you sure you want overwrite the current file path?'):
                overwrite = True
        else:
            overwrite = True

        if overwrite:
            file_text = ctx.obj['index'].read_pdf(file)
            file_path = doc_id + '.pdf'
            ctx.obj['index'].index[doc_id][attr] = file_path
            ctx.obj['index'].write()
            ctx.obj['database'].write(file, file_path, force=force)

        return

    # adding annotated file
    if annotated:
        attr = 'annotated_path'
        overwrite = False
        if attr in ctx.obj['index'].index[doc_id]:
            if force or click.confirm('Are you sure you want overwrite the current annotated file path?'):
                overwrite = True
        else:
            overwrite = True

        if overwrite:
            annotated_path = 'annotated/' + doc_id + '.pdf'
            ctx.obj['index'].index[doc_id][attr] = annotated_path
            ctx.obj['index'].write()
            ctx.obj['database'].write(annotated, annotated_path, force=force)

        return

    # adding supplemental file
    if supplemental:
        attr = 'supplemental_path'
        overwrite = False
        if attr in ctx.obj['index'].index[doc_id]:
            if force or click.confirm('Are you sure you want overwrite the current supplemental file path?'):
                overwrite = True
        else:
            overwrite = True

        if overwrite:
            supplemental_path = 'supplemental/' + doc_id + '.pdf'
            ctx.obj['index'].index[doc_id][attr] = supplemental_path
            ctx.obj['index'].write()
            ctx.obj['database'].write(supplemental, supplemental_path, force=force)

        return

    # adding tags
    if tags:
        attr = 'tags'
        old_tags = ctx.obj['index'].index[doc_id][attr]
        old_tags = ','.join(old_tags)
        tags = handle_tags(tags + ',' + old_tags)
        ctx.obj['index'].index[doc_id][attr] = tags
        ctx.obj['index'].write()

        return

    old, diff = ctx.obj['index'].modify(doc_id)
    ctx.obj['index'].write()
    
    # handling changes in file and annotated file paths without adding a new file
    if diff:
        for attr in ['file_path', 'annotated_path']:
            if attr in diff:
                if force or click.confirm('Are you sure you want to change the file or annotated file path?'):
                    ctx.obj['database'].move(old[attr], diff[attr])

    # git adding delete
    ctx.invoke(git, git_commands=['add', ctx.obj['index'].path])
    ctx.invoke(git, git_commands=['commit', '-m', '"Modified ' + doc_id + '"'])

    # confirmation
    click.echo(click.style('Modified: ', bold=True) + doc_id)

bibtheque.add_command(modify)

#  ──────────────────────────────────────────────────────────────────────────
# Delete

@click.command()
@force_option
@doc_id_arg
@click.pass_context
def delete(ctx, force, doc_id):
    """Deletes the document with the given DOC_ID."""

    if click.confirm('Are you sure you want to delete this document?'):

        # deleting file
        if ctx.obj['index'].file_exists(doc_id):
            ctx.obj['database'].delete(ctx.obj['index'].index[doc_id]['file_path'])

        # deleting annotated file
        if ctx.obj['index'].file_exists(doc_id, other='annotated'):
            ctx.obj['database'].delete(ctx.obj['index'].index[doc_id]['annotated_path'])

        # deleting supplemental file
        if ctx.obj['index'].file_exists(doc_id, other='supplemental'):
            ctx.obj['database'].delete(ctx.obj['index'].index[doc_id]['annotated_path'])
        
        # deleting index entry; must be deleted last
        ctx.obj['index'].delete(doc_id)
        ctx.obj['index'].write()

        # git adding delete
        ctx.invoke(git, git_commands=['add', ctx.obj['index'].path])
        ctx.invoke(git, git_commands=['commit', '-m', '"Deleted ' + doc_id + '"'])

        # confirmation
        click.echo(click.style('Deleted: ', bold=True) + doc_id)

bibtheque.add_command(delete)

#  ──────────────────────────────────────────────────────────────────────────
# Search

# fields? need to add fields to only search through
@click.command()
@click.option('-o', '--output', 'output', default='counts', type=click.Choice(['minimal', 'counts', 'json', 'pretty']), help='Option that changes the output format.')
@click.option('-p', '--pager', 'pager', default=False, is_flag=True, help='Enters pager mode to page through results.')
@click.option('-b', '--bib', '--bibtex', 'bib', default=False, is_flag=True, help='Outputs documents found from the search in BiBTeX string format.')
@click.argument('regex', type=str, default="") # add bibtex output and handle tags by specifying tag?
@click.pass_obj # passes object directly without context
def search(db, output, pager, bib, regex):
    """Searches the database with REGEX_TEXT.
    """

    def print_results(hits, output='simple', pager=False):
        """
        'minimal', 'counts', 'json', 'pretty'
        """

        results_json = {}

        for doc_id in hits:

            if output == 'minimal':
                click.echo(doc_id)
                continue

            counts = [] # for counts output
            result_json = {} # for json output
            pretty = [] # for pretty output

            for attr in hits[doc_id]:
                if attr == 'bib':
                    result_json[attr] = {}

                    for field in hits[doc_id][attr]:

                        tmp_pretty = ''
                        for i, match in enumerate(hits[doc_id][attr][field]):
                            result_json[attr][field] = match.string # just overwriting the same string

                            # pretty handling
                            match_span = match.span()
                            match_str = match.string

                            if i == 0:
                                prefix = match_str[0:match_span[0]]
                                tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                                prior_match_span = match_span
                            else:
                                prefix = match_str[prior_match_span[1]:match_span[0]]
                                tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                                prior_match_span = match_span

                        tmp_pretty += match_str[match_span[1]:]
                        pretty.append(attr + ': ' + field + ': ' + tmp_pretty)
                        counts.append(attr + ': ' + field + ': ' + str(i+1))

                elif attr == 'tags':
                    result_json[attr] = []

                    for tag in hits[doc_id][attr]:
                        result_json[attr].append(tag)

                        tmp_pretty = ''
                        for i, match in enumerate(hits[doc_id][attr][tag]):

                            # pretty handling
                            match_span = match.span()
                            match_str = match.string

                            if i == 0:
                                prefix = match_str[0:match_span[0]]
                                tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                                prior_match_span = match_span
                            else:
                                prefix = match_str[prior_match_span[1]:match_span[0]]
                                tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                                prior_match_span = match_span

                        tmp_pretty += match_str[match_span[1]:]
                        pretty.append(attr + ': ' + tag + ': ' + tmp_pretty)

                        counts.append(attr + ': ' + tag + ': ' + str(i+1))

                else:
                    tmp_pretty = ''
                    for i, match in enumerate(hits[doc_id][attr]):
                        result_json[attr] = match.string

                        # pretty handling
                        match_span = match.span()
                        match_str = match.string

                        if i == 0:
                            prefix = match_str[0:match_span[0]]
                            tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                            prior_match_span = match_span
                        else:
                            prefix = match_str[prior_match_span[1]:match_span[0]]
                            tmp_pretty += prefix + click.style(match_str[match_span[0]:match_span[1]], bold=True)
                            prior_match_span = match_span

                    tmp_pretty += match_str[match_span[1]:]
                    pretty.append(attr + ': ' + tmp_pretty)

                    counts.append(attr + ': ' + str(i+1))

            results_json[doc_id] = result_json

            if output == 'counts':
                output_str = click.style(doc_id + '\n', bold=True)

                attr = 'bib'
                try:
                    output_str += db['index'].index[doc_id][attr]['title'] + '\n'
                except:
                    pass

                try:
                    output_str += click.style(db['index'].index[doc_id][attr]['author'] + '\n', italic=True)
                except:
                    pass

                output_str += '\n'.join(counts)
                if pager:
                    click.echo_via_pager(output_str)
                else:
                    click.echo(output_str)

            if output == 'pretty':
                output_str = click.style(doc_id + '\n', bold=True, underline=True)

                attr = 'bib'
                try:
                    output_str += db['index'].index[doc_id][attr]['title'] + '\n'
                except:
                    pass

                try:
                    output_str += click.style(db['index'].index[doc_id][attr]['author'] + '\n', italic=True)
                except:
                    pass

                output_str += '\n'.join(pretty) + '\n'
                if pager:
                    click.echo_via_pager(output_str)
                else:
                    click.echo(output_str)
                
        results_json['search'] = regex

        if output == 'json':
            if pager:
                click.echo_via_pager(output_str)
            else:
                click.echo(output_str)


    def print_bib(hits):
        keys = []
        for doc_id in hits:
            attr = 'bib'
            doc_bib = db['index'].index[doc_id][attr]

            field = 'key'
            key = doc_bib[field]
            tmp_key = key
            i = 97 # ascii a
            while tmp_key in keys:
                tmp_key = key + chr(i)
                i += 1

            keys.append(tmp_key)
            doc_bib[key] = tmp_key

            click.echo(document.build_bib(doc_bib, bibkey=tmp_key))


    hits = db['index'].search(regex)

    if bib:
        print_bib(hits)
    else:
        print_results(hits, output=output, pager=pager)

bibtheque.add_command(search)

#  ──────────────────────────────────────────────────────────────────────────
# git command

CONTEXT_SETTINGS_git = CONTEXT_SETTINGS.copy()
CONTEXT_SETTINGS_git['ignore_unknown_options'] = True

@click.command('git', short_help='Git manage the index', context_settings=CONTEXT_SETTINGS_git)
@click.argument('git_commands', type=click.UNPROCESSED, nargs=-1)
@click.pass_context
def git(ctx, git_commands):
    """Git command to manage the bibtheque git repository."""

    command = ['git', '-C', ctx.obj['index'].path.parent]

    for arg in git_commands:
        command.append(arg)

    subprocess.run(command)

bibtheque.add_command(git)

#  ──────────────────────────────────────────────────────────────────────────
# cache command

@click.command('cache', short_help='Manage local cache')
@click.option('-c', '--clear', 'clear', is_flag=True, default=False, help='Clear local cache')
@click.option('-s', '--serve', 'serve', is_flag=True, default=False, help='Locally serve the local cache')
@click.pass_context
def cache(ctx, clear, serve):
    """Local cache management."""
    if clear:
        ctx.obj['database'].clear_cache()

    if serve:

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=ctx.obj['database'].cache, **kwargs)

        handler = Handler

        with socketserver.TCPServer(("", ctx.obj['database'].cache_port), handler) as httpd:
            click.echo('Serving the cache at: locahost:' + str(ctx.obj['database'].cache_port))
            httpd.serve_forever()

bibtheque.add_command(cache)
