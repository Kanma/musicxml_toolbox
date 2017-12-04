==================
 musicxml_toolbox
==================

.. image:: https://travis-ci.org/Kanma/musicxml_toolbox.svg?branch=v0.1.0
    :target: https://travis-ci.org/Kanma/musicxml_toolbox


Tools to process a MusicXML file.



Installation
============

To install this package, do::

    $ pip install musicxml_toolbox



Usage
=====

musicxml-add-empty-measures
---------------------------

Add empty measures at the beginning of a MusicXML file

::

    $ musicxml-add-empty-measures [-h] [--nb NB] src_file dst_file

    positional arguments:
      src_file    Path to the input MusicXML file
      dst_file    Path to the output MusicXML file

    optional arguments:
      -h, --help  show this help message and exit
      --nb NB     The number of measures to add (default: 2)


musicxml-add-fingering
----------------------

Add fingering to given staff of a MusicXML file

::

    $ musicxml-add-fingering [-h] src_file staff dst_file

    positional arguments:
      src_file    Path to the input MusicXML file
      staff       The staff to add the fingering to, in the form: "part:staff"
      dst_file    Path to the output MusicXML file

    optional arguments:
      -h, --help  show this help message and exit


musicxml-annotate-chords
------------------------

Annotate the chords found in a MusicXML file

::

    $ musicxml-annotate-chords [-h] [--staff STAFF] src_file dst_file

    positional arguments:
      src_file       Path to the input MusicXML file
      dst_file       Path to the output MusicXML file

    optional arguments:
      -h, --help     show this help message and exit
      --staff STAFF  The staff to annotate, in the form: "part:staff" (by default,
                     all parts are processed)


musicxml-expand-repeats
-----------------------

Expand the repeats of a MusicXML file

::

    $ musicxml-expand-repeats [-h] src_file dst_file

    positional arguments:
      src_file    Path to the input MusicXML file
      dst_file    Path to the output MusicXML file

    optional arguments:
      -h, --help  show this help message and exit


musicxml-info
-------------

Display informations about a MusicXML file

::

    $ musicxml-info [-h] file

    positional arguments:
      file        Path to the MusicXML file

    optional arguments:
      -h, --help  show this help message and exit


musicxml-remove-key-signature
-----------------------------

Remove the key signatures found in a MusicXML file, and ensure that all
accidentals are correctly displayed

::

    $ musicxml-remove-key-signature [-h] [--part PART] src_file dst_file

    positional arguments:
      src_file     Path to the input MusicXML file
      dst_file     Path to the output MusicXML file

    optional arguments:
      -h, --help   show this help message and exit
      --part PART  The name of the part to process (by default, all parts are
                   processed)


musicxml-simplify
-----------------

Simplify a MusicXML file, by replacing chords by their root note

::

    $ musicxml-simplify [-h] [--staff STAFF] src_file dst_file

    positional arguments:
      src_file       Path to the input MusicXML file
      dst_file       Path to the output MusicXML file

    optional arguments:
      -h, --help     show this help message and exit
      --staff STAFF  The staff to simplify, in the form: "part:staff" (by default,
                     all parts are processed)


musicxml-to-yousician
---------------------

Convert a MusicXML file in a Yousician-friendly format (for Piano)

::

    $ usage: musicxml-to-yousician [-h] src_file dst_file

    positional arguments:
      src_file    Path to the input MusicXML file
      dst_file    Path to the output MusicXML file

    optional arguments:
      -h, --help  show this help message and exit



Running tests
=============

In the source package, do::

    $ python setup.py test



License
=======

*musicxml_toolbox* is is made available under the MIT License. The text of the license
is in the file "LICENSE.txt".

Under the MIT License you may use *musicxml_toolbox* for any purpose you wish, without
warranty, and modify it if you require, subject to one condition:

    "The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software."

In practice this means that whenever you distribute your application, whether as binary
or as source code, you must include somewhere in your distribution the text in the file
"LICENSE.txt". This might be in the printed documentation, as a file on delivered media,
or even on the credits / acknowledgements of the runtime application itself; any of
those would satisfy the requirement.

Even if the license doesn't require it, please consider to contribute your modifications
back to the community.
