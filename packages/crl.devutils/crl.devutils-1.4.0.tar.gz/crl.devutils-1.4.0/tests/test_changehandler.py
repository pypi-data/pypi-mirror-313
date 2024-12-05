from __future__ import print_function
import subprocess
import os
import pytest
import mock
from crl.devutils.changehandler import ChangeHandler
from crl.devutils.changehandler import (
    MultipleChangeFilesFound,
    ChangeFileNotFound,
    ChangeFileVersionCheckFailed)
from crl.devutils.runner import Failure
from .fixtures import (  # pylint: disable=unused-import
    mock_glob_changes,
    create_mpatch,
    mock_run)


__copyright__ = 'Copyright (C) 2019, Nokia'

changefile_contents = """
CHANGES
=======

0.1
---
- feature1

0.1b
----
- feature1 beta-version

"""

singlechangefile = """
CHANGES
=======

0.1
---

- feature 1
"""


@pytest.fixture(scope='function')
def tmpsinglechange(tmpdir):
    changes = tmpdir.join('CHANGES.rst')
    changes.write(singlechangefile)
    return tmpdir


@pytest.fixture(scope='function')
def tmpemptychange(tmpdir):
    changes = tmpdir.join('CHANGES.rst')
    changes.write('')
    return tmpdir


@pytest.fixture(scope='function')
def mock_read(request):
    return create_mpatch(mock.patch(
        'crl.devutils.changehandler.ChangeHandler._read'),
        request)


@pytest.fixture(scope='function')
def changefile_at_tmpdir(tmpdir):
    cf = tmpdir.mkdir('tmp').join('CHANGES.rst')
    cf.write(changefile_contents)
    return os.path.join(cf.dirname, cf.basename)


def test_verify(tmpsinglechange, mock_run, mock_read):
    with tmpsinglechange.as_cwd():
        ch = ChangeHandler(run=mock_run)
        mock_read.return_value = changefile_contents

        ch.verify('0.1')
        mock_run.assert_called_once_with('rstcheck %s' % ch.change_file)
        assert ch.change_file == 'CHANGES.rst'
        assert ch.latest_version == '0.1'


def test_verify_changefile_at_tmpdir(mock_run, changefile_at_tmpdir):
    ch = ChangeHandler(run=mock_run, pathtochangefile=changefile_at_tmpdir)
    ch.verify('0.1')
    mock_run.assert_called_once_with('rstcheck %s' % ch.change_file)
    assert ch.change_file == changefile_at_tmpdir
    assert ch.latest_version == '0.1'


def test_verify_raises_with_wrong_synatx(mock_run, changefile_at_tmpdir):
    mock_run.side_effect = Failure
    ch = ChangeHandler(run=mock_run, pathtochangefile=changefile_at_tmpdir)

    with pytest.raises(Failure):
        ch.verify('0.1')

    mock_run.assert_called_once_with('rstcheck %s' % ch.change_file)
    assert ch.change_file == changefile_at_tmpdir


def test_verify_raises_with_wrong_version(mock_run, changefile_at_tmpdir):
    ch = ChangeHandler(run=mock_run, pathtochangefile=changefile_at_tmpdir)

    with pytest.raises(ChangeFileVersionCheckFailed) as excinfo:
        ch.verify('1.0')

    assert excinfo.value.args[0] == "Latest version in %s is %s" \
        " and not 1.0" % (ch.change_file, ch.latest_version)

    mock_run.assert_called_once_with('rstcheck %s' % ch.change_file)
    assert ch.change_file == changefile_at_tmpdir
    assert ch.latest_version != '1.0'


def test_verify_fails_with_empty_file_contents(tmpemptychange,
                                               mock_run,
                                               mock_read):
    with tmpemptychange.as_cwd():
        ch = ChangeHandler(run=mock_run)
        mock_read.return_value = ''

        with pytest.raises(ChangeFileVersionCheckFailed) as excinfo:
            ch.verify('1.0')

        assert excinfo.value.args[0] == "Latest version in %s is %s" \
            " and not 1.0" % (ch.change_file, ch.latest_version)

        mock_run.assert_called_once_with('rstcheck %s' % ch.change_file)
        assert ch.change_file == 'CHANGES.rst'
        assert ch.latest_version == ''


@pytest.mark.parametrize('return_value', [
    ['changes.st', 'CHANGES.rstd', 'changes.yml'],
    ['changes.mdl', 'changes.xml', 'CHANGES.txt']])
def test_change_file_raises_if_file_not_present(mock_run,
                                                mock_glob_changes,
                                                return_value):
    mock_glob_changes.return_value = return_value
    ch = ChangeHandler(run=mock_run)
    with pytest.raises(ChangeFileNotFound):
        print(ch.change_file)

    assert mock_glob_changes.call_count == 1


@pytest.mark.parametrize('return_value', [
    ['changes.md', 'CHANGES.rst'],
    ['changes.rst', 'CHANGES.md']])
def test_change_file_raises_if_multiple_files(mock_run,
                                              mock_glob_changes,
                                              return_value):
    mock_glob_changes.return_value = return_value
    ch = ChangeHandler(run=mock_run)
    with pytest.raises(MultipleChangeFilesFound):
        print(ch.change_file)

    assert mock_glob_changes.call_count == 1


def test_single_change_in_changefile(tmpsinglechange):
    with tmpsinglechange.as_cwd():
        ch = ChangeHandler(run=subprocess.check_call)
        assert ch.latest_version == '0.1'
