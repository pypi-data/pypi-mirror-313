.. Copyright (C) 2019, Nokia

.. image:: https://travis-ci.org/nokia/crl-devutils.svg?branch=master
    :target: https://travis-ci.org/nokia/crl-devutils

##################################################################
Guide for developing Common Robot Libraries (CRL) via crl.devutils
##################################################################


Documentation
=============

Documentation for crl.devutils can be found from `Read The Docs`_.

.. _Read the Docs: http://crl-devutils.readthedocs.io/


Setup
=====

First, install crl.devutils.

.. code:: bash

    $ pip install crl.devutils

Now, there is available *crl* development command line:

.. code:: bash

    $ crl -l

    Available tasks:

      clean               Clean workspace.
      create_docs         Create both Robot Framework and Sphinx documentation.
      create_index        Create an index with given bases
      create_setup        Create initial setup.py into current directory from library name.
      delete_index        Delete an index
      help                Show help, basically an alias for --help.
      publish             *DEPRECATED* Publish version from a given index to another index.
      sdist               Create source distribution.
      set_version         Set version in ./src/crl/<libname>/_version.py`.
      tag_release         Tag specified release.
      tag_setup_version   Tag specified release.
      test                Uploads contents of current workspace to devpi and runs tox tests.



**NOTE that some of the commands have been deprecated and should not be used.**

This tool is based on invoke 3rd party Python module and more details can be
found by running command *crl help*. Please use *crl* instead of *invoke* even
though the help shows this differently.

The *crl* tasks glue the git tags and the package distribution versions
together behind the scenes.


Using the CRL devpi server
--------------------------

For using the test command you need the devpi server. If you do not have devpi,
you need to install and configure it. See instructions on how to `Configure
Devpi`_.

Before using the test command you should also configure the devpi index that is
to be used as the base index of the library.

Here devpi is configured to use the imaginary
https://example.devpi.com/user/index simple index.

.. code:: bash

    $ devpi use https://example.devpi.com/user/index/+simple --set-cfg
    current devpi index: https://example.devpi.com/crl/prod (logged in as <username>)
    ~/.pydistutils.cfg     : https://example.devpi.com/user/index/+simple/
    ~/.pip/pip.conf        : https://example.devpi.com/user/index/+simple/
    ~/.buildout/default.cfg: https://example.devpi.com/user/index/+simple/
    always-set-cfg: no


Using the Test Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

If there is a [testenv:test] in the library's tox.ini, you can use this to
test your work. This runs the same tests as tox, but also uploads the current
workspace contents to a development index. Also, this is the way tests are
run in CI, so you might want to simulate the CI run to avoid problems later.

If the library's tox.ini doesn't have the test environment, it can be added
easily by adding the following lines into the tox.ini file:

.. code:: bash

    [testenv:test]
    changedir = {toxinidir}
    deps=
         crl.devutils
    commands= crl test --no-virtualenv {posargs}

.. warning::
    Dependency package list to this test environment may vary according
    to the library's needs.

First, login to the devpi server. Now you can load development indexes under
your personal user index.

.. code:: bash

    $ PYPI=https://example.devpi.com/user/index
    $ tox -e test -- -b ${PYPI} -t <test-indexname> --verbose

The above command saves the tests and contents to
https://example.devpi.com/<username>/<test-indexname>.


Working without the *crl* namespace
-----------------------------------

If the library shall not be in *crl* namespace, then the version file path has
to be given relatively.

For example:

.. code:: bash

    $ tox -e test -i ${PYPI}/+simple -- \
        -t CRL-92 \
        -p src/examplelib/_version.py \
        -s https://example.devpi.com/<username>/<srcindexname> \
        -d https://example.devpi.com/<username>/<destindexname>

The tagging of the version commmand has to also contain the path to version
file. For example:

.. code:: bash

    $ crl tag_release \
         --pathtoversionfile src/examplelib/_version.py 0.6.10.dev201612050621


Creating a new CRL library
==========================

Creating a new CRL library is done with a dedicated Jenkins job `Create New CRL
Library`_. The job creates the library structure from a template and generates
all the needed Jenkins jobs for the library.

Creating Documentation
======================

The *crl* tool provides two alternatives for the documentation of the test
library: *crl create_docs* and *crl publish*.

Now, the *crl create_docs* is a standalone tool for generating documentation
during the development. If documentation is done so that a *sphinxdocs*
directory exists, *crl publish* tool automatically uploads the documentation
more or less the same produced by *crl create_docs* tool. It is recommended
that *crl create_docs* will be integrated to *tox* in order to verify
documentation generation, as well as producing it in the CI e.g. via Jenkins
jobs for each commit to git.

Adding docs environment for tox.ini. Remember to add the docs environment to
the *envlist*.

.. code:: bash

    [testenv:docs]
    deps =
        sphinx
        crl.devutils
        robotframework
    commands = crl create_docs -v

.. warning::
    Dependency package list for docs environment may vary according to the
    library's needs

In order to generate documentation for your library with robot.libdoc you
should:

* create *robotdocs/robotdocsconf.py*, with content like below:

.. code:: python

        robotdocs={
            'crl.examplelib.examplelib':
                {'docformat': 'rest',
                 'synopsis': 'Example of test library functions.'},
            'crl.examplelib.examplelib.Example':
                {'args':['example'],
                 'docformat': 'rest',
                 'synopsis': 'Example of test library class.'}}

* add relative path of your *robotdocs* directory to 'html_extra_path' in
  *sphinxdocs/conf.py*:

.. code:: python

       html_extra_path = ['../robotdocs']

* it is also recommended to set page width to 90% in 'html_theme_options' in
  *sphinxdocs/conf.py*

.. code:: python

        html_theme_options = {'page_width': '90%'}

Libraries using crl.devutils process
====================================

Libraries providing Robot Framework test libraries
--------------------------------------------------

======================== ================================================================
Library                  Description
======================== ================================================================
crl-interactivesessions_ Remote command and file management via pexpect
------------------------ ----------------------------------------------------------------
crl-remotescript_        Remote command and file management via paramiko and trilead-ssh
------------------------ ----------------------------------------------------------------
crl-remotesession_       Wrapper of crl-interactivesessions_ and crl-remotescript_
======================== ================================================================

.. _crl-interactivesessions: https://github.com/nokia/crl-interactivesessions
.. _crl-remotescript: https://github.com/nokia/crl-remotescript
.. _crl-remotesession: https://github.com/nokia/crl-remotesession

Robot Framework robot command wrappers
--------------------------------------

======================== ================================================================
Library                  Description
======================== ================================================================
crl-rfcli_               Python path setter and parser of test target file
------------------------ ----------------------------------------------------------------
crl-threadverify_        Robot run verifier for hanging threads
======================== ================================================================

.. _crl-rfcli: https://github.com/nokia/crl-rfcli
.. _crl-threadverify: https://github.com/nokia/crl-threadverify

Development libraries
----------------------

======================== ================================================================
Library                  Description
======================== ================================================================
crl-devutils_            Development tools for CRL
------------------------ ----------------------------------------------------------------
crl-examplelib_          Example library template for CRL
======================== ================================================================

.. _crl-devutils: https://github.com/nokia/crl-devutils
.. _crl-examplelib: https://github.com/nokia/crl-examplelib

Generic helper libraries
------------------------

======================== ================================================================
Library                  Description
======================== ================================================================
fixtureresources_        Pytest fixtures
------------------------ ----------------------------------------------------------------
sphinx-invoke_           Sphinx extension for invoke tasks
------------------------ ----------------------------------------------------------------
virtualenvrunner_        Python Virtualenv creator and command executor
======================== ================================================================

.. _fixtureresources: https://github.com/nokia/fixtureresources
.. _sphinx-invoke: https://github.com/nokia/sphinx-invoke
.. _virtualenvrunner: https://github.com/nokia/virtualenvrunner

Useful Links
============

* `Configure Devpi`_
* `Create New CRL Library`_

.. _`Configure Devpi`: https://doc.devpi.net
.. _`Create New CRL Library`: https://github.com/nokia/cookiecutter-crl-template


Contributing
============

Please see contributing_ for development and contribution practices.

The code_ and the issues_ are hosted on GitHub.

The project is licensed under BSD-3-Clause_.

.. _contributing: https://github.com/nokia/crl-devutils/blob/master/CONTRIBUTING.rst
.. _code: https://github.com/nokia/crl-devutils
.. _issues: https://github.com/nokia/crl-devutils/issues
.. _BSD-3-Clause:  https://github.com/nokia/crl-devutils/blob/master/LICENSE
