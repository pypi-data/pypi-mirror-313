import subprocess
from pathlib import Path
import click

#  ──────────────────────────────────────────────────────────────────────────

class Database():

    def __init__(self, config, version, initialize=False):
        self.version = version
        self.config = config['database']
        self.path = Path(self.config['path']).expanduser()
        self.host = self.config['host']
        self.cache = Path(self.config['cache']).expanduser()
        self.cache_port = self.config['cache_port']

        if initialize:
            self.init()


    def init(self):
        # make remote store

        # annotated
        command = ['ssh', self.host, 'mkdir -p', self.path / Path('annotated') ]
        subprocess.run(command)

        # supplemental
        command = ['ssh', self.host, 'mkdir -p', self.path / Path('supplemental') ]
        subprocess.run(command)

        # make docker-compose template

        docker_init = r"""version: '3'

services:
    server:
        image: dkllrjr/bibtheque_server:""" + self.version + r"""
        restart: unless-stopped
        volumes:
          - ./files:/bibtheque/files
        ports:
          - "2340:2340"
"""

        docker_init_path = Path('/tmp/docker-compose.yml')
        docker_init_path.open('w').write(docker_init)

        command = ['rsync', '--ignore-existing']
        command += [docker_init_path, self.host + ':' + str(self.path / Path('..'))]
        subprocess.run(command)

        # make local cache
        try:
            # annotated
            cache_path = self.cache / Path('annotated')
            cache_path.mkdir(parents=True)

            # supplemental
            cache_path = self.cache / Path('supplemental')
            cache_path.mkdir(parents=True)

        except:
            click.echo('Cache already exists')


    def write(self, local_file_path, remote_file_path, force=False):

        command = ['rsync']
        
        if force:
            command += ['-I']

        # copying to remote store
        command += [Path(local_file_path).resolve(), self.host + ':' + str(self.path / Path(remote_file_path))]
        subprocess.run(command)

        # moving to local cache
        Path(local_file_path).rename(self.cache / Path(remote_file_path))


    def delete(self, remote_file_path):
        command = ['ssh', self.host, 'rm', self.path / Path(remote_file_path)]
        subprocess.run(command)


    def move(self, old_remote_file_path, new_remote_file_path):
        # moving remote store
        command = ['ssh', self.host, 'mv', self.path / Path(old_remote_file_path), self.path / Path(new_remote_file_path)]
        subprocess.run(command)

        # moving cached version if it exists
        if (self.cache / Path(old_remote_file_path)).exists():
            (self.cache / Path(old_remote_file_path)).rename(self.cache / Path(new_remote_file_path))


    def available(self):
        try:
            command = ['ssh', self.host, 'echo', '"test"', '>', '/tmp/bibtheque_ping']
            subprocess.run(command)
            return True
        except:
            return False


    def clear_cache(self):
        cache_paths = sorted(self.cache.rglob('*.pdf'))
        for path in cache_paths:
            path.unlink()



