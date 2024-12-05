# pylint: disable=unused-import,unused-argument
from collections import namedtuple
import pytest
import mock
from virtualenvrunner.runner import Runner
from fixtureresources.fixtures import create_patch, mock_randomchoice
from crl.devutils._tmpindex import _TmpIndex
from crl.devutils.doccreator import DocCreator
from .fixtures import mock_packagehandler


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_run():
    return mock.Mock()


@pytest.fixture(scope='function')
def tmpindex(mock_packagehandler,
             mock_run):
    return _TmpIndex(run=mock_run,
                     packagehandler=mock_packagehandler,
                     clientarg=' clientarg')


@pytest.fixture(scope='function')
def mock_create_index(request):
    return create_patch(mock.patch(
        'crl.devutils.devpiindex.DevpiIndex.create_index'), request)


@pytest.fixture(scope='function')
def mock_delete_index(request):
    return create_patch(mock.patch(
        'crl.devutils.devpiindex.DevpiIndex.delete_index'), request)


@pytest.fixture(scope='function')
def mock_use_index(request):
    return create_patch(mock.patch(
        'crl.devutils.devpiindex.DevpiIndex.use_index'), request)


@pytest.fixture(scope='function')
def mock_os_path_isdir(request):
    return create_patch(mock.patch('os.path.isdir', return_value=True),
                        request)


@pytest.fixture(scope='function')
def mock_index_exists(request):
    return create_patch(mock.patch(
        'crl.devutils.devpiindex.DevpiIndex.index_exists',
        return_value=False), request)


MockVirtualenvrunner = namedtuple('MocVirtualenvrunner', ['init', 'handle'])


@pytest.fixture(scope='function')
def mock_virtualenvrunner(request):
    m = mock.MagicMock(spec_set=Runner)
    m.__enter__.return_value = mock.Mock(spec_set=Runner)
    mpatch = mock.patch(
        'crl.devutils._tmpindex.virtualenvrunner.runner.Runner',
        return_value=m)
    return MockVirtualenvrunner(init=create_patch(mpatch, request),
                                handle=m.__enter__.return_value)


@pytest.fixture(scope='function')
def mock_doccreator(request):
    m = mock.MagicMock(spec_set=DocCreator)
    create_patch(mock.patch(
        'crl.devutils._tmpindex.DocCreator',
        return_value=m), request)
    return m


def test_test_run_without_docs(mock_run,
                               tmpindex,
                               mock_packagehandler,
                               mock_os_path_isdir):
    mock_os_path_isdir.return_value = False
    mock_packagehandler.name = 'name'
    tmpindex.test()
    assert mock_run.mock_calls == [
        mock.call('devpi upload{clientarg}'.format(
            clientarg=tmpindex.clientarg)),
        mock.call('devpi test name==0.1{clientarg}'.format(
            clientarg=tmpindex.clientarg))]


def _get_pip_install_calls(pip_index_url):
    return [
        mock.call('pip install crl.devutils'
                  ' -i {pip_index_url}'.format(pip_index_url=pip_index_url)),
        mock.call('pip install name==version'
                  ' -i {pip_index_url}'.format(pip_index_url=pip_index_url))]


def _get_run_calls(novirtualenv, pip_index_url):
    calls = [] if novirtualenv else _get_pip_install_calls(pip_index_url)
    calls.append(mock.call('devpi upload --no-vcs --only-docsclientarg'))
    return calls


@pytest.mark.parametrize('novirtualenv, index_name', [
    (True, None), (False, 'index')])
def test_test_with_docs(mock_run,
                        mock_packagehandler,
                        mock_os_path_isdir,
                        mock_virtualenvrunner,
                        mock_doccreator,
                        mock_index_exists,
                        novirtualenv,
                        index_name):
    mock_packagehandler.name = 'name'
    mock_packagehandler.version = 'version'
    mock_packagehandler.novirtualenv = novirtualenv

    with _TmpIndex(run=mock_run,
                   packagehandler=mock_packagehandler,
                   baseindex='base/index',
                   baseurl='https://host',
                   username='username',
                   index_name=index_name,
                   clientarg='clientarg') as t:
        t.test()
    index = index_name if index_name else ''
    pip_index_url = 'https://host/username/' + index + '/+simple/'
    if not novirtualenv:
        mock_virtualenvrunner.init.assert_called_once_with(
            pip_index_url=pip_index_url,
            run=mock_run)
    run = mock_run if novirtualenv else mock_virtualenvrunner.handle.run
    expected_calls = _get_run_calls(novirtualenv, pip_index_url)
    if novirtualenv:
        assert expected_calls[0] in expected_calls
    else:
        assert run.mock_calls == expected_calls

    assert mock_doccreator.create_robotdocs.call_count == 1


def test_create_index(mock_randomchoice, tmpindex):
    tmpindex.create_index()
    tmpindex.run.assert_called_once_with(
        'devpi index -c tmp_abcdefghij clientarg')
    assert tmpindex.index == 'tmp_abcdefghij'


def test_use_index(mock_randomchoice, tmpindex):
    tmpindex.use_index()
    tmpindex.run.assert_called_once_with(
        'devpi use tmp_abcdefghij clientarg')
    assert tmpindex.index == 'tmp_abcdefghij'


def test_delete_index(mock_randomchoice, tmpindex):
    tmpindex.delete_index()
    tmpindex.run.assert_called_once_with(
        'devpi index -y --delete tmp_abcdefghij clientarg')


@pytest.mark.parametrize('index_name', [None, 'abcd'])
def test_tmpindex_with_non_existing_index_name(mock_create_index,
                                               mock_delete_index,
                                               mock_use_index,
                                               mock_index_exists,
                                               mock_run,
                                               mock_packagehandler,
                                               index_name):
    with _TmpIndex(run=mock_run,
                   index_name=index_name,
                   packagehandler=mock_packagehandler,
                   clientarg='clientarg') as tmpindex:
        assert mock_create_index.call_count == 1
        assert mock_use_index.call_count == 1
        assert mock_delete_index.call_count == 0
        assert tmpindex.run == mock_run
        assert tmpindex.packagehandler == mock_packagehandler
        assert tmpindex.clientarg == 'clientarg'
        assert tmpindex.index == index_name if index_name else 'tmp_abcdefghij'
        # pylint: disable=protected-access
        assert tmpindex._default_cleanup == (not bool(index_name))

    assert mock_create_index.call_count == 1
    assert mock_use_index.call_count == 1
    assert mock_delete_index.call_count == (0 if index_name else 1)


def test_tmpindex_with_existing_index(mock_create_index,
                                      mock_delete_index,
                                      mock_use_index,
                                      mock_index_exists,
                                      mock_run,
                                      mock_packagehandler):
    mock_index_exists.return_value = True
    with _TmpIndex(run=mock_run,
                   index_name='index',
                   packagehandler=mock_packagehandler,
                   clientarg='clientarg') as tmpindex:
        assert mock_create_index.call_count == 0
        assert mock_use_index.call_count == 1
        assert mock_delete_index.call_count == 0
        assert tmpindex.run == mock_run
        assert tmpindex.packagehandler == mock_packagehandler
        assert tmpindex.clientarg == 'clientarg'
        assert tmpindex.index == 'index'

    assert mock_create_index.call_count == 0
    assert mock_use_index.call_count == 1
    assert mock_delete_index.call_count == 0


def test_push(tmpindex):
    spec = '{name}=={version}'.format(name=tmpindex.packagehandler.name,
                                      version=tmpindex.packagehandler.version)
    tmpindex.push(spec, 'index')
    tmpindex.run.assert_called_once_with(
        'devpi push name==0.1 index clientarg')


def test_publish(tmpindex):
    tmpindex.publish('index')
    tmpindex.run.assert_called_once_with(
        'devpi push name==0.1 index clientarg')


def test_create_index_with_baseindex(mock_run,
                                     mock_packagehandler,
                                     mock_randomchoice,
                                     mock_index_exists):
    with _TmpIndex(run=mock_run,
                   packagehandler=mock_packagehandler,
                   baseindex='user/index',
                   clientarg=' clientarg'):
        # Testing only context manager side-effects
        pass

    assert (mock_run.mock_calls[0] == mock.call('devpi index'
                                                ' -c tmp_abcdefghij'
                                                ' bases=user/index'
                                                ' clientarg'))
