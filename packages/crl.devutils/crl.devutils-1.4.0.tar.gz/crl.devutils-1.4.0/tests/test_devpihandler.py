# pylint: disable=unused-argument,protected-access
import os
from collections import namedtuple
import pytest
import mock
from crl.devutils._tmpindex import _TmpIndex
from crl.devutils.devpihandler import DevpiHandler, MalformedURL
from .fixtures import (  # pylint: disable=unused-import
    mock_packagehandler,
    mock_devpiindex,
    mock_randomchoice,
    mock_gettempdir,
    devpihandler,
    create_mpatch,
    mock_response)
from .mockfile import MockFile


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


@pytest.fixture(scope='function')
def randomtmpdir():
    return os.path.join('tmp', 'username_abcdefghij')


@pytest.fixture(scope='function')
def mock_run():
    return mock.Mock(return_value='return_value')


@pytest.fixture(scope='function')
def mock_login(request):
    mpatch = mock.patch(
        'crl.devutils.devpihandler.DevpiHandler._login')
    return create_mpatch(mpatch, request)


@pytest.fixture(scope='function')
def mock_logoff(request):
    mpatch = mock.patch(
        'crl.devutils.devpihandler.DevpiHandler._logoff')
    return create_mpatch(mpatch, request)


MockTmpIndex = namedtuple('MockTmpIndex', ['init', 'handle'])
MockDevpiIndex = namedtuple('MockDevpiIndex', ['create', 'handler'])


@pytest.fixture(scope='function')
def mock_tmpindex(request):
    m = mock.MagicMock(spec_set=_TmpIndex)
    m.__enter__.return_value = mock.Mock(spec_set=_TmpIndex)
    mpatch = mock.patch('crl.devutils.devpihandler._TmpIndex',
                        return_value=m)
    return MockTmpIndex(init=create_mpatch(mpatch, request),
                        handle=m.__enter__.return_value)


@pytest.fixture(scope='function')
def mock_create_devpiindex(request, mock_devpiindex):
    mpatch = mock.patch('crl.devutils.devpihandler.DevpiIndex',
                        return_value=mock_devpiindex)
    return MockDevpiIndex(create=create_mpatch(mpatch, request),
                          handler=mock_devpiindex)


@pytest.fixture(scope='function')
def mock_credentials_file(request):
    cf = MockFile(filename='creds', content='username:password')
    cf.start()
    request.addfinalizer(cf.stop)
    return cf


@pytest.fixture(scope='function')
def mock_credentials_file_enoent(mock_credentials_file):
    def raise_io_error():
        raise IOError('message')
    mock_credentials_file.set_side_effect(raise_io_error)
    return mock_credentials_file


@pytest.fixture(scope='function')
def mock_rmtree(request):
    return create_mpatch(mock.patch('shutil.rmtree'), request)


@pytest.mark.parametrize('publishindex', [
    'https://host/otheruser/otherindex',
    'otheruser/otherindex'])
def test_publish(devpihandler,
                 mock_login,
                 mock_logoff,
                 mock_create_devpiindex,
                 mock_credentials_file,
                 randomtmpdir,
                 publishindex):
    devpihandler.set_index('https://host/user/index')
    devpihandler.publish(publishindex)
    assert mock_login.call_count == 1
    assert mock_logoff.call_count == 1
    mock_create_devpiindex.create.assert_called_once_with(
        run=devpihandler.run,
        baseindex='user/index',
        baseurl='https://host',
        index_name='index',
        username='username',
        clientarg=' --clientdir {expected_clientdir}'.format(
            expected_clientdir=randomtmpdir))
    mock_create_devpiindex.handler.push.assert_called_once_with(
        'name==0.1', 'otheruser/otherindex')


@pytest.mark.parametrize('index', [None, 'index'])
def test_test(devpihandler,
              mock_login,
              mock_logoff,
              mock_tmpindex,
              mock_credentials_file,
              randomtmpdir,
              index):
    devpihandler.set_index('https://host/user/index')
    devpihandler.test(index)
    assert mock_login.call_count == 1
    assert mock_logoff.call_count == 1
    mock_tmpindex.init.assert_called_once_with(
        run=devpihandler.run,
        packagehandler=devpihandler.packagehandler,
        baseindex='user/index',
        baseurl='https://host',
        username='username',
        index_name=index,
        clientarg=' --clientdir {expected_clientdir}'.format(
            expected_clientdir=randomtmpdir))
    mock_tmpindex.handle.test.assert_called_once_with(
        toxargs=None, select=None)


@pytest.mark.parametrize('index,expected_url', [
    ('https://host/user/index', 'https://host'),
    ('http://host/user/index', 'http://host')])
def test_login(index,
               expected_url,
               devpihandler,
               mock_credentials_file,
               randomtmpdir):
    devpihandler.set_index(index)
    devpihandler._login()
    assert devpihandler.run.mock_calls == [
        mock.call(
            'devpi use {expected_url} --clientdir {expected_clientdir}'.format(
                expected_url=expected_url,
                expected_clientdir=randomtmpdir)),
        mock.call(
            ['devpi', 'login', 'username', '--password', 'password',
             '--clientdir', '{expected_clientdir}'.format(
                 expected_clientdir=randomtmpdir)],
            replaced_output='devpi login username',
            shell=False)]


@pytest.mark.parametrize('index,expected_url', [
    ('https://host/user/index', 'https://host'),
    ('http://host/user/index', 'http://host')])
def test_login_without_credentials_file(index,
                                        expected_url,
                                        devpihandler,
                                        mock_credentials_file):
    devpihandler.set_index(index)
    devpihandler.set_credentials_file(None)
    devpihandler._login()
    devpihandler.run.assert_called_once_with(
        'devpi use {expected_url}'.format(expected_url=expected_url))


@pytest.mark.parametrize('index', [
    'ftp://host/user/index',
    'https://host',
    'https://host/user'])
def test_set_index_raises_malformedurl(index,
                                       devpihandler):
    with pytest.raises(MalformedURL) as excinfo:
        devpihandler.set_index(index)

    assert excinfo.value.args[0] == (
        "URL '{index}' not in form 'http[s]://host/user/indexname'".format(
            index=index))


def test_logoff(devpihandler,
                mock_credentials_file,
                mock_rmtree,
                randomtmpdir):
    devpihandler._logoff()
    assert devpihandler.run.mock_calls == [
        mock.call('devpi logoff'
                  ' --clientdir {expected_clientdir}'.format(
                      expected_clientdir=randomtmpdir))]
    mock_rmtree.assert_called_once_with(randomtmpdir)


def test_logoff_without_credentials_file(devpihandler,
                                         mock_credentials_file,
                                         mock_rmtree):
    devpihandler.set_credentials_file(None)
    devpihandler._logoff()
    assert not devpihandler.run.called
    assert not mock_rmtree.called


def test_set_index(devpihandler):
    devpihandler.set_index('https://host/user/index')
    assert devpihandler.index == 'https://host/user/index'


def test_set_credentials_file(devpihandler):
    devpihandler.set_credentials_file('creds')
    assert devpihandler.credentials_file == 'creds'


@pytest.mark.parametrize('devpi_user', [
    'https://host/username:\n',
    'http://host/username:\n',
    'https://host/username:\nemail: email.example.com\n'])
def test_username_no_credentialsfile(mock_run,
                                     mock_packagehandler,
                                     devpi_user):
    mock_run.return_value = mock_response(devpi_user)

    assert DevpiHandler(
        run=mock_run,
        packagehandler=mock_packagehandler).username == 'username'

    mock_run.assert_called_once_with('devpi user')


@pytest.mark.parametrize('pkgname,output,version', [
    ('name', 'name (1.0.1) - text \n name1 (0.0.1) - xyz', '1.0.1'),
    ('name', '/pkg/name (1.0.1b2) (abc) \n /names (0.1.0)', '1.0.1b2'),
    ('name', '/abc/nome (0.1.0) \n /nome (0.0.1)', ''),
    ('name', '', '')])
def test_latest_pypi_version(mock_run,
                             devpihandler,
                             pkgname,
                             output,
                             version):
    mock_run.return_value = mock_response(output)
    index = 'https://host/user/index'
    devpihandler.packagehandler.name = pkgname
    devpihandler.set_index(index)

    assert devpihandler.latest_pypi_version() == version
    mock_run.assert_called_once_with('pip search {pkgname} -i {index}'.format(
        pkgname=devpihandler.packagehandler.name,
        index=index if index.endswith('/') else index + '/'),
        ignore_codes=[23])


@pytest.mark.parametrize('index', [
    'https://host/user1/index1', 'user2/index2'])
def test_latest_pypi_version_with_long_short_urls(mock_run,
                                                  devpihandler,
                                                  index):
    mock_run.return_value = mock_response('out')
    devpihandler.packagehandler.name = 'name'
    devpihandler.set_index('https://host/user/index')
    devpihandler.latest_pypi_version('name', index)
    long_index = index if index.startswith('https') else 'https://host/' + index  # noqa: E501
    mock_run.assert_called_once_with('pip search name -i {index}'.format(
        index=long_index if long_index.endswith('/') else long_index + '/'),
        ignore_codes=[23])


@pytest.mark.parametrize('index', [
    'https://host/user1/index1', 'user2/index2'])
def test_get_long_url(devpihandler, index):
    devpihandler.set_index('https://host/user/index')
    long_index = index if index.startswith('https') else 'https://host/' + index  # noqa: E501
    assert devpihandler._get_long_url(index) == long_index


@pytest.mark.parametrize('index', [
    'https://host/user1/index1', 'user2/index2'])
def test_get_short_url(devpihandler, index):
    devpihandler.set_index('https://host/user/index')
    short_index = index if not index.startswith('https') else index.replace(
        'https://host/', '')
    assert devpihandler._get_short_url(index) == short_index


@pytest.mark.parametrize('otherbases, index_exists', [
    ('user1/index1', True), ('user1/index1,user2/index2', True),
    ('user1/index1', False), ('user1/index1,user2/index2', False)])
def test_create_index(devpihandler, mock_login, mock_logoff,
                      mock_create_devpiindex, mock_credentials_file,
                      randomtmpdir, otherbases, index_exists):
    mock_create_devpiindex.handler.index_exists.return_value = index_exists
    devpihandler.create_index('newindex', 'https://host/user/index',
                              otherbase=otherbases)
    assert mock_login.call_count == 1
    assert mock_logoff.call_count == 1
    mock_create_devpiindex.create.assert_called_once_with(
        run=devpihandler.run,
        baseindex='user/index' + ',' + otherbases,
        baseurl='https://host',
        index_name='newindex',
        username='username',
        clientarg=' --clientdir {expected_clientdir}'.format(
            expected_clientdir=randomtmpdir))
    assert mock_create_devpiindex.handler.create_index.called == (
        not index_exists)
    assert mock_create_devpiindex.handler.index_exists.called
    assert mock_create_devpiindex.handler.use_index.called


def test_delete_index(devpihandler, mock_login, mock_logoff,
                      mock_create_devpiindex, mock_credentials_file,
                      randomtmpdir):
    devpihandler.delete_index('https://host/user/index')
    assert mock_login.call_count == 1
    assert mock_logoff.call_count == 1
    mock_create_devpiindex.create.assert_called_once_with(
        run=devpihandler.run,
        baseindex='user/index',
        baseurl='https://host',
        index_name='index',
        username='username',
        clientarg=' --clientdir {expected_clientdir}'.format(
            expected_clientdir=randomtmpdir))
    assert mock_create_devpiindex.handler.delete_index.called
    assert mock_create_devpiindex.handler.index_exists.called
