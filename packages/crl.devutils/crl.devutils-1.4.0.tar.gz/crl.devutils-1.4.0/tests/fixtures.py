# pylint: disable=unused-argument
import os
import errno
import pytest
import mock
from crl.devutils.versionhandler import VersionHandler
from crl.devutils.devpihandler import DevpiHandler
from crl.devutils.packagehandler import PackageHandler
from crl.devutils.setuphandler import SetupHandler
from crl.devutils.changehandler import ChangeHandler
from crl.devutils.githandler import GitHandler
from crl.devutils.devpiindex import DevpiIndex
from crl.devutils.runner import Result
from .mockfile import MockFile


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_packagehandler():
    m = mock.Mock(spec_set=PackageHandler)
    m.name = 'name'
    m.version = '0.1'
    return m


@pytest.fixture(scope='function')
def mock_setuphandler():
    m = mock.Mock(spec_set=SetupHandler)
    m.version = '0.1'
    return m


@pytest.fixture(scope='function')
def mock_changehandler():
    m = mock.Mock(spec_set=ChangeHandler)
    m.latest_version = '0.1'
    m.change_file = 'CHANGES.rst'
    return m


@pytest.fixture(scope='function')
def mock_githandler():
    m = mock.Mock(spec_set=GitHandler)
    m.tag = '0.1'
    m.hash = 'githash'
    m.get_branch_of_tag.return_value = 'master'
    return m


@pytest.fixture(scope='function')
def mock_devpihandler():
    m = mock.Mock(spec_set=DevpiHandler)
    m.index = 'index'
    m.username = 'user'
    return m


@pytest.fixture(scope='function')
def mock_devpiindex():
    m = mock.Mock(spec_set=DevpiIndex)
    m.index = 'index'
    m.pypiurl = 'https://host/user/index/+simple'
    return m


class MockSystemRandom(object):
    def __init__(self):
        self.count = 0

    def choice(self, choices):
        ret = choices[self.count % len(choices)]
        self.count += 1
        return ret


@pytest.fixture(scope='function')
def mock_randomchoice(request):
    m = MockSystemRandom()
    mpatch = mock.patch('random.SystemRandom', return_value=m)
    return create_mpatch(mpatch, request)


class MockExecFileWithMockFile(object):

    def __init__(self, request):
        self._request = request
        self.mock_open = None
        self.mock_file = MockFile()
        self.setup_mocks()

    def setup_mocks(self):
        self._setup_open_mock()
        self._setup_execfile_mock()

    def _setup_open_mock(self):
        self.mock_file.start()
        self._request.addfinalizer(self.mock_file.stop)

    def _setup_execfile_mock(self):
        epatch = mock.patch(
            'crl.devutils.versionhandler.utils.execfile',
            self._mock_execfile_with_exec)
        epatch.start()
        self._request.addfinalizer(epatch.stop)

    def _mock_execfile_with_exec(self, filename, namespace):
        exec(self.mock_file.content, namespace)


@pytest.fixture(scope='function')
def mock_execfile_with_mock_file(request):
    return MockExecFileWithMockFile(request)


def mock_walk_gen(subdirs):
    for _ in range(10):
        yield '', subdirs, []


@pytest.fixture(scope='function')
def mock_os_walk(request):
    mpatch = mock.patch('os.walk', return_value=mock_walk_gen(['lib']))
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def mock_glob_changes(request):
    mpatch = mock.patch('glob.glob', return_value=['CHANGES.rst'])
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def mock_os_path_isfile(request):
    mpatch = mock.patch('os.path.isfile', return_value=True)
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def mock_os_remove(request):
    mpatch = mock.patch('os.remove', return_value=True)
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def mock_os_path_abspath(request):

    def mock_abspath(path):
        return os.path.join('abspath', path)

    mpatch = mock.patch('os.path.abspath', mock_abspath)
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def versionfilename():
    return os.path.join('abspath', 'src', 'crl', 'lib', '_version.py')


@pytest.fixture(scope='function')
def mock_initial_version_file(mock_os_path_isfile,
                              mock_execfile_with_mock_file,
                              mock_os_path_abspath,
                              mock_os_walk,
                              versionfilename):
    mock_execfile_with_mock_file.mock_file.set_filename(versionfilename)
    # pylint: disable=protected-access
    VersionHandler()._create_initial_version_file('0.1')
    mock_os_path_isfile.return_value = True
    return mock_execfile_with_mock_file.mock_file


def raise_io_error(errno):
    e = IOError('message')
    e.errno = errno
    raise e


@pytest.fixture(scope='function')
def mock_version_file_not_found(request,
                                mock_os_path_isfile,
                                mock_os_path_abspath,
                                mock_os_walk,
                                versionfilename):
    m = MockFile(filename=versionfilename,
                 side_effect=lambda *args: raise_io_error(errno.ENOENT))
    m.start()
    request.addfinalizer(m.stop)
    return m


def mock_response(stdout='\n'):
    return Result('cmd', 0, stdout, 'stderr')


@pytest.fixture(scope='function')
def mock_run():
    return mock.MagicMock(return_value=mock_response(''))


@pytest.fixture(scope='function')
def mock_gettempdir(request):
    mpatch = mock.patch('tempfile.gettempdir', return_value='tmp')
    return create_mpatch(mpatch, request)


@pytest.fixture(scope='function')
def devpihandler(mock_run,
                 mock_packagehandler,
                 mock_randomchoice,
                 mock_gettempdir):
    return DevpiHandler(run=mock_run,
                        packagehandler=mock_packagehandler,
                        credentials_file='creds')


def create_mpatch(mpatch, request):
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


@pytest.fixture(scope='function')
def randomtmpdir():
    return os.path.join('tmp', 'tmp_abcdefghij')
