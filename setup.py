from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='trello_things3_sync',
   version='1.0',
   description='Module for syncing tasks across Trello and Things 3',
   license="MIT",
   long_description=long_description,
   author='Ben Hylak',
   author_email='bhylak@gmail.com',
   url="http://www.benhylak.com/",
   packages=['trello_things3_sync'],  # same as name
   install_requires=['py-trello', 'pyobjc'],  # external packages as dependencies
   scripts=[
            'scripts/cool',
            'scripts/skype',
           ]
)
