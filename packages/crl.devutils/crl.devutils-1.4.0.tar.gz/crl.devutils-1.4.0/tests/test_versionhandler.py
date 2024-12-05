# pylint: disable=unused-argument,protected-access
import errno
from collections import namedtuple
import mock
import pytest
from crl.devutils.versionhandler import (
    VersionHandler,
    MultipleVersionFilesFound,
    VersionFileNotFound,
    FailedToCreateVersionFile,
    FailedToWriteVersion,
    FailedToWriteGithash,
    InvalidVersionValue)
from crl.devutils import utils
from .mockfile import MockFile
from .fixtures import (  # pylint: disable=unused-import
    mock_initial_version_file,
    mock_execfile_with_mock_file,
    mock_version_file_not_found,
    mock_os_walk,
    mock_os_path_isfile,
    mock_os_path_abspath,
    mock_walk_gen,
    versionfilename,
    create_mpatch,
    raise_io_error)


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def versionhandler_with_lib():
    return VersionHandler('libname')


@pytest.fixture(scope='function')
def versionhandler_without_lib():
    return VersionHandler()


@pytest.fixture(scope='function')
def mock_strftime(request):
    return create_mpatch(mock.patch('time.strftime', return_value='0000'),
                         request)


@pytest.fixture(scope='function')
def mock_write_version_file_and_verify(request):
    return create_mpatch(mock.patch(
        'crl.devutils.versionhandler.VersionHandler'
        '._write_version_file_and_verify'), request)


@pytest.fixture(scope='function')
def mock_create_initial_version_file(request):
    return create_mpatch(mock.patch(
        'crl.devutils.versionhandler.VersionHandler'
        '._create_initial_version_file'), request)


@pytest.fixture(scope='function')
def mock_update_file(request):
    return create_mpatch(mock.patch(
        'crl.devutils.versionhandler.VersionHandler'
        '._update_file'), request)


@pytest.fixture(scope='function')
def mock_version_file(request):
    return create_mpatch(mock.patch(
        'crl.devutils.versionhandler.VersionHandler.version_file',
        new_callable=mock.PropertyMock,
        return_value='file'), request)


@pytest.fixture(scope='function')
def versionhandler_with_mocked_version_file(mock_version_file):
    return VersionHandler('libname')


MockExecFile = namedtuple('MockExecFile',
                          ['mock_execfile', 'mock_get_version'])


@pytest.fixture(scope='function')
def mock_get_version():
    return mock.Mock(return_value='1')


@pytest.fixture(scope='function')
def mock_execfile(request, mock_get_version):

    m = mock.Mock()

    def mock_execfile_inner(filename, namespace):
        m(filename, dict(namespace))
        namespace['get_version'] = mock_get_version

    mpatch = mock.patch(
        'crl.devutils.versionhandler.utils.execfile',
        mock_execfile_inner)
    mpatch.start()
    request.addfinalizer(mpatch.stop)
    return MockExecFile(m, mock_get_version)


@pytest.fixture(scope='function')
def mpatch_version_file(request):
    return create_mpatch(mock.patch(
        'crl.devutils.versionhandler.VersionHandler.version_file',
        new_callable=mock.PropertyMock), request)


def test_init_empty(versionhandler_without_lib):
    assert versionhandler_without_lib.libname is None


def test_init_with_libname(versionhandler_with_lib):
    assert versionhandler_with_lib.libname == 'libname'


def test_version(versionhandler_with_mocked_version_file,
                 mock_execfile):
    assert versionhandler_with_mocked_version_file.version == '1'
    mock_execfile.mock_execfile.assert_called_once_with('file', {})


def test_versionfile_with_pathtoversionfile():
    assert VersionHandler(
        pathtoversionfile='path').version_file == 'path'


def test_set_version_keep(mock_write_version_file_and_verify):
    VersionHandler().set_version('keep')
    assert not mock_write_version_file_and_verify.called, (
        "set_version('keep') shall not call write")


def test_set_version_invalid(mock_write_version_file_and_verify,
                             mock_execfile):
    with pytest.raises(InvalidVersionValue):
        VersionHandler().set_version('1.1.1.invalid')


@pytest.mark.parametrize("version_in_file,version_input,version_expected", [
    (None, '1.1.1', '1.1.1'),
    ('1.1', 'dev', '1.1.1.dev0000'),
    ('1.1.1', 'dev', '1.1.2.dev0000'),
    ('1.1a1', 'dev', '1.1.dev0000'),
    (None, '1.1.1.dev', '1.1.1.dev0000')])
def test_set_version_parametrized(mock_write_version_file_and_verify,
                                  mock_execfile,
                                  mock_strftime,
                                  mock_version_file,
                                  version_in_file,
                                  version_input,
                                  version_expected):
    if version_in_file is not None:
        mock_execfile.mock_get_version.return_value = version_in_file
    VersionHandler().set_version(version_input)
    mock_write_version_file_and_verify.assert_called_once_with(
        version_expected)


def test_write_version_file_create(mock_initial_version_file):
    assert VersionHandler().version == '0.1'


@pytest.mark.parametrize("versionhandler", [
    VersionHandler(),
    VersionHandler('lib')])
def test_write_version_file_update(mock_initial_version_file,
                                   versionhandler):
    versionhandler.set_version('0.2')
    assert versionhandler.version == '0.2'


def test_write_version_file_not_found(mock_version_file_not_found,
                                      mock_create_initial_version_file):
    VersionHandler()._write_version_file('0.1')
    mock_create_initial_version_file.assert_called_once_with('0.1')


def test_write_version_file_permission_denied(
        mock_version_file_not_found,
        mock_create_initial_version_file):
    mock_version_file_not_found.set_side_effect(
        lambda *args: raise_io_error(errno=errno.EACCES))
    with pytest.raises(FailedToCreateVersionFile) as excinfo:
        VersionHandler()._write_version_file('0.1')

    assert 'message' in excinfo.value.args[0]
    assert not mock_create_initial_version_file.called


def test_write_version_file_write_failed(mock_initial_version_file,
                                         mock_create_initial_version_file,
                                         mock_update_file):

    with pytest.raises(FailedToWriteVersion) as excinfo:
        VersionHandler()._write_version_file_and_verify('0.2')
    assert excinfo.value.args[0] == "Version should be '0.2' but it is '0.1'"


def test_version_file_not_found(mpatch_version_file,
                                mock_create_initial_version_file):
    mpatch_version_file.side_effect = VersionFileNotFound
    VersionHandler()._write_version_file('0.1')
    mock_create_initial_version_file.assert_called_once_with('0.1')


def test_try_get_version_file_raises_multiple_versions(mock_os_walk,
                                                       mock_os_path_isfile,
                                                       mock_os_path_abspath):
    mock_os_walk.return_value = mock_walk_gen(['a', 'b'])
    with pytest.raises(MultipleVersionFilesFound):
        VersionHandler()._try_to_get_version_file()


def test_try_to_get_version_file_raises_file_not_found(mock_os_walk,
                                                       mock_os_path_isfile,
                                                       mock_os_path_abspath):
    mock_os_walk.return_value = mock_walk_gen([])
    with pytest.raises(VersionFileNotFound):
        VersionHandler()._try_to_get_version_file()


def test_try_to_get_version_file_subdir_raises_not_found(mock_os_path_isfile,
                                                         mock_os_walk):
    with pytest.raises(VersionFileNotFound):
        mock_os_path_isfile.return_value = False
        VersionHandler()._try_to_get_version_file_for_subdir('lib')


def test_execfile():
    with MockFile(filename='a.py', content="a = 0"):
        namespace = {}
        utils.execfile('a.py', namespace)
        assert namespace['a'] == 0


def test_githash(mock_initial_version_file):
    VersionHandler().set_githash('githash')
    assert VersionHandler().githash == 'githash'


def test_githash_githash_write_failed(mock_initial_version_file):
    mock_initial_version_file.set_saver(None)
    with pytest.raises(FailedToWriteGithash) as excinfo:
        VersionHandler().set_githash('githash')
    assert excinfo.value.args[0] == "Githash should be 'githash' but it is ''"


def test_no_recreation_of_versionfile(mock_initial_version_file,
                                      versionfilename):
    with open(versionfilename, 'a') as f:
        f.write("\n\ntest = 'test'\n")
    VersionHandler().set_version('0.2')
    assert VersionHandler().version == '0.2'
    namespace = {}
    utils.execfile(versionfilename, namespace)
    assert namespace['test'] == 'test'
