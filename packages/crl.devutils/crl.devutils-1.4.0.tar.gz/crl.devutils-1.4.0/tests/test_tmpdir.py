import os
from collections import namedtuple
import pytest
import mock
from crl.devutils.tmpdir import TmpDir
from .fixtures import (  # pylint: disable=unused-import
    create_mpatch,
    mock_randomchoice,
    randomtmpdir)


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_gettempdir(request):
    return create_mpatch(
        mock.patch('tempfile.gettempdir', return_value='tmp'), request)


@pytest.fixture(scope='function')
def mock_makedirs(request):
    return create_mpatch(
        mock.patch('os.makedirs'), request)


@pytest.fixture(scope='function')
def mock_rmtree(request):
    return create_mpatch(
        mock.patch('shutil.rmtree'), request)


@pytest.fixture(scope='function')
def mock_copytree(request):
    return create_mpatch(
        mock.patch('shutil.copytree'), request)


@pytest.fixture(scope='function')
def mock_isdir(request):
    return create_mpatch(
        mock.patch('os.path.isdir', return_value=True), request)


def get_tmpdir():
    return (os.environ['TMPDIR']
            if 'TMPDIR' in os.environ
            else None)


# TODO: Use directly pytest.mark.paramterize if
# https://github.com/pytest-dev/pytest/issues/349 is corrected
TmpDirArgs = namedtuple('TmpDirArgs', ['tmpdir',
                                       'copytree_to',
                                       'expected_copytree_calls'])


@pytest.fixture(params=[
    'empty',
    'tmpdir',
    'copytree_to'])
def tmpdir_args(request, randomtmpdir):

    return {'empty': TmpDirArgs(None, None, []),
            'tmpdir': TmpDirArgs('tmpdir', None, []),
            'copytree_to': TmpDirArgs(
                None, 'copytree_to', [mock.call(
                    randomtmpdir, 'copytree_to')])}[request.param]


def test_tmpdir(  # pylint: disable=unused-argument
        mock_gettempdir,
        mock_randomchoice,
        mock_makedirs,
        mock_rmtree,
        mock_copytree,
        tmpdir_args,
        randomtmpdir,
        monkeypatch):

    if tmpdir_args.tmpdir:
        monkeypatch.setenv('TMPDIR', tmpdir_args.tmpdir)
    else:
        monkeypatch.delenv('TMPDIR', raising=False)
    with TmpDir(copytree_to=tmpdir_args.copytree_to) as tdir:
        mock_makedirs.assert_called_once_with(randomtmpdir)
        assert tdir.path == randomtmpdir
        assert get_tmpdir() == randomtmpdir

    assert tmpdir_args.tmpdir == get_tmpdir()
    assert mock_copytree.mock_calls == tmpdir_args.expected_copytree_calls
    mock_rmtree.assert_called_once_with(randomtmpdir)


def add_noaccess_content_under_path(filepath):
    rodir = os.path.join(filepath, 'rodir')
    os.makedirs(rodir)
    rofile = os.path.join(filepath, 'rofile')
    rodirfile = os.path.join(rodir, 'rofile')
    for path in [rofile, rodirfile]:
        with open(path, 'w') as f:
            f.write('content')
        os.chmod(path, 0000)
    os.chmod(rodir, 0000)


@pytest.mark.parametrize('copytree_to', [True, False])
def test_tmpdir_with_readonly_files(copytree_to):
    paths = []
    with TmpDir() as outer:
        paths.append(outer.path)
        args = [os.path.join(outer.path, 'new')] if copytree_to else []
        with TmpDir(*args) as inner:
            paths.append(inner.path)
            add_noaccess_content_under_path(inner.path)

    for path in paths:
        assert not os.path.exists(path)
