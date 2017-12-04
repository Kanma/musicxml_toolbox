from setuptools import setup, find_packages
from codecs import open
import os


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# Package version
version = '0.1.0'


setup(
    name = 'musicxml_toolbox',
    version = version,

    description = 'Tools to process a MusicXML file',
    long_description = long_description,

    url = 'https://github.com/Kanma/musicxml_toolbox',
    download_url = 'https://github.com/Kanma/musicxml_toolbox/archive/v%s.tar.gz' % version,

    author = 'Philip Abbet',
    author_email = 'philip.abbet@gmail.com',

    license='MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia',
        'Intended Audience :: Developers',
    ],

    keywords = ['piano', 'music', 'musicxml'],

    packages = [
        'musicxml_toolbox',
        'musicxml_toolbox.musicxml',
        'musicxml_toolbox.scripts',
        'musicxml_toolbox.test',
    ],

    install_requires = [
        'music21',
        'piano_fingering',
    ],
    extras_require = {},

    entry_points = {
        'console_scripts': [
            'musicxml-info=musicxml_toolbox.scripts.info:main',
            'musicxml-add-empty-measures=musicxml_toolbox.scripts.add_empty_measures:main',
            'musicxml-add-fingering=musicxml_toolbox.scripts.add_fingering:main',
            'musicxml-annotate-chords=musicxml_toolbox.scripts.annotate_chords:main',
            'musicxml-expand-repeats=musicxml_toolbox.scripts.expand_repeats:main',
            'musicxml-remove-key-signature=musicxml_toolbox.scripts.remove_key_signature:main',
            'musicxml-simplify=musicxml_toolbox.scripts.simplify:main',
            'musicxml-to-yousician=musicxml_toolbox.scripts.to_yousician:main',
        ],
    },

    test_suite = 'musicxml_toolbox.test',
)
