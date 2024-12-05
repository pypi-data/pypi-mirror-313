.. Copyright (C) 2019-2024, Nokia

CHANGES
=======

1.4.0
-----

- Support selecting release files for which 'crl test' is running tests via new CLI
  argument '--select'. This makes possible testing of non-universal wheels besides
  source distributions or selecting only one of them.

1.3.1
-----

- Support running 'crl test' in Python 3.10 environment

1.3.0
-----

- Support parallel test execution via new CLI argument for 'crl test': '--toxargs'.
  This is replacing old solution based on 'detox'

1.2.6
-----

- Support for Python versions 3.8, 3.9 and 3.10
- Use importlib in setup.py for Python 3.x (instead of deprecated imp module)
- Require Jinja2==3.0.3 to avoid errors caused by removal of 'contextfunction'
- Require pytest-flake8==1.0.7 and lazy-object-proxy==1.6.0 for Python 2.7 tests

1.2.5
-----

- Require check-manifest==0.41 to avoid 'devpi upload' error caused
  by backwards incompatible change

1.2.4
-----

- Pinned dependencies for python 2
- Changed the usage of pep8 and flakes to flake8
- Added python 3.7 as a test environment

1.2.3
-----

 - Add contribution guide and list of libraries developed by crl.devutils

1.2.2
-----

 - Integrate with Read The Docs


1.2.1
-----

 - Correct syntax error in mock_exec_file_with_exec

1.2
---

 - Add task for creating Robot Framework documentation only

1.1
---

 - Add initial content


