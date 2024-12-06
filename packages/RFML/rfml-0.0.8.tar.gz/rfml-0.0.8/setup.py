from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RFML',  # name of packe which will be package dir below project
    version='0.0.8',
    author_email='rbimrose@gmail.com',
    description='RapidFire ML Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'flask',
        'spacy',
        'torch',
        'nltk',
        'pyTelegramBotAPI'
    ],
)

# from setuptools import setup, find_packages
# setup(
#     name='RFML',
#     version='0.1',
#     packages=find_packages(),
#     long_description=open('./README.md').read(),
#     long_description_content_type='text/markdown',
# )
