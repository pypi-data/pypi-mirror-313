from click.testing import CliRunner
import subprocess

#  ──────────────────────────────────────────────────────────────────────────
# local imports

from bibtheque.config import config
from bibtheque.cli import bibtheque
from bibtheque.doi import doi_to_bib
from bibtheque.bibtex import bib_to_dict
import bibtheque.database as database
import tests.test_vars as test_vars

#  ──────────────────────────────────────────────────────────────────────────

config['mongo_db_name'] = 'test_db'

#  ──────────────────────────────────────────────────────────────────────────
# running tests

def test_insert():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'insert', '--file', 'test.pdf', '-n', 'test notes for test pdf', '--tags', 'test, tags, here', '--force', '--print', test_vars.doi_url])
    # print(result.output)
    assert result.exit_code == 0


def test_search():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'search', 'notes'])
    # print(result.output)
    assert result.exit_code == 0


def test_search_all():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'search'])
    # print(result.output)
    assert result.exit_code == 0


def test_regex():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'regex', '--fields', 'tags', 'here'])
    # print(result.output)
    assert result.exit_code == 0


def test_clean():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'clean'])
    assert result.exit_code == 0


def test_bib():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'bib', 'test'])

    result_dict = bib_to_dict(result.output)
    doi_dict = bib_to_dict(test_vars.doi_bib)

    del result_dict['key']
    del doi_dict['key']

    assert result_dict == doi_dict
    assert result.exit_code == 0


def test_write():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'insert', '--file', 'test.pdf', '-n', 'test notes for test pdf', '--tags', 'test, tags, here', '--force', '--print', test_vars.doi_url])
    doc_id = result.output.strip('\n')
    result = runner.invoke(bibtheque, ['--config', config, 'write', doc_id])
    subprocess.run(['rm', doc_id + '.pdf'])
    # print(result.output)
    result = runner.invoke(bibtheque, ['--config', config, 'delete', '--test', doc_id])
    assert result.exit_code == 0


def test_modify():
    runner = CliRunner()
    result = runner.invoke(bibtheque, ['--config', config, 'insert', '--file', 'test.pdf', '-n', 'test notes for test pdf', '--tags', 'test, tags, here', '--force', '--print', test_vars.doi_url])
    doc_id = result.output.strip('\n')
    result = runner.invoke(bibtheque, ['--config', config, 'modify', '--test', doc_id])
    result = runner.invoke(bibtheque, ['--config', config, 'delete', '--test', doc_id])
    assert result.exit_code == 0

#  ──────────────────────────────────────────────────────────────────────────
# cleaning test database

def clean(config):
    DB = database.Database(config)
    DB.delete()

clean(config)
