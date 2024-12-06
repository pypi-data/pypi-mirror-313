import subprocess
from pathlib import Path
import click

# FIX need to check for rsync and ssh

#  ──────────────────────────────────────────────────────────────────────────

class Cache():

    def __init__(self, config, initialize):
        self.config = config['cache']
        self.path = Path(self.config['path'])

        if initialize:
            self.init()


    def init(self):
        command = ['mkdir -p', self.path / Path('annotated') ]
        subprocess.run(command)


    def write(self, local_file_path, remote_file_path, force=False):

        command = ['rsync']
        
        if force:
            command += ['-I']

        command += [Path(local_file_path).resolve(), self.host + ':' + str(self.path / Path(remote_file_path))]
        subprocess.run(command)


    def delete(self, remote_file_path):
        command = ['ssh', self.host, 'rm', self.path / Path(remote_file_path)]
        click.echo(command)
        subprocess.run(command)


    def move(self, old_remote_file_path, new_remote_file_path):
        command = ['ssh', self.host, 'mv', self.path / Path(old_remote_file_path), self.path / Path(new_remote_file_path)]
        click.echo(command)
        subprocess.run(command)
