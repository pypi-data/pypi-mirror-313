# pylint: disable=protected-access
from collections import namedtuple
import pytest
import mock
from crl.devutils.packagehandler import (
    PackageHandler,
    MismatchOfTagAndSetupVersion,
    VersionTagInWrongBranch)
from crl.devutils.versionhandler import (
    VersionHandler,
    InvalidVersionValue)
from crl.devutils.changehandler import (
    ChangeFileNotFound,
    MultipleChangeFilesFound,
    ChangeFileVersionCheckFailed)
from crl.devutils.githandler import UncleanGitRepository
from .fixtures import (  # pylint: disable=unused-import
    mock_initial_version_file,
    mock_os_walk,
    mock_os_path_isfile,
    mock_os_path_abspath,
    versionfilename,
    mock_execfile_with_mock_file,
    mock_setuphandler,
    mock_githandler,
    mock_changehandler,
    mock_devpihandler,
    create_mpatch)


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


@pytest.fixture(scope='function')
def mock_prepare_package(request):
    return create_mpatch(mock.patch(
        'crl.devutils.packagehandler.PackageHandler._prepare_package'),
        request)


@pytest.fixture(scope='function')
def mock_finalize_package(request):
    return create_mpatch(mock.patch(
        'crl.devutils.packagehandler.PackageHandler._finalize_package'),
        request)


@pytest.fixture(scope='function')
def mock_verify_clean(request):
    return create_mpatch(mock.patch(
        'crl.devutils.packagehandler.PackageHandler.verify_clean'),
        request)


@pytest.fixture(scope='function')
def packagehandler(mock_initial_version_file,  # pylint:disable=unused-argument
                   mock_githandler,
                   mock_setuphandler,
                   mock_changehandler,
                   mock_devpihandler):
    ph = PackageHandler(versionhandler=VersionHandler(),
                        changehandler=mock_changehandler,
                        githandler=mock_githandler,
                        setuphandler=mock_setuphandler)
    ph.set_devpihandler(mock_devpihandler)
    return ph


MockTmpDir = namedtuple('MockTmpDir', ['init', 'handle'])


@pytest.fixture(scope='function')
def mock_tmpdir(request):
    m = mock.MagicMock()
    m.__enter__.return_value = mock.Mock()
    mpatch = mock.patch('crl.devutils.packagehandler.TmpDir',
                        return_value=m)
    return MockTmpDir(init=create_mpatch(mpatch, request),
                      handle=m.__enter__.return_value)


@pytest.mark.parametrize('novirtualenv', [True, False])
def test_novirtualenv(novirtualenv):
    kwargs = {'novirtualenv': True} if novirtualenv else {}
    ph = PackageHandler(versionhandler=mock.Mock(),
                        setuphandler=mock.Mock(),
                        changehandler=mock.Mock(),
                        githandler=mock.Mock(),
                        **kwargs)

    assert ph.novirtualenv == novirtualenv


def test_verify_clean_ok(packagehandler):
    packagehandler.verify_clean()
    assert packagehandler.githandler.verify_clean.call_count == 1
    assert packagehandler.changehandler.verify.call_count == 1


def test_verify_mismatch_tag_and_setup(packagehandler):
    type(packagehandler.setuphandler).version = mock.PropertyMock(
        return_value='0.2')
    with pytest.raises(MismatchOfTagAndSetupVersion) as excinfo:
        packagehandler.verify_clean()
    assert (str(excinfo.value) ==
            'Tag in git (0.1) differs from setup version (0.2)')


def test_prepare_package(packagehandler):
    packagehandler._prepare_package()
    assert packagehandler.versionhandler.githash == 'githash'


def test_finalize_package(versionfilename, packagehandler):
    packagehandler._finalize_package()
    packagehandler.githandler.checkout.assert_called_once_with(
        versionfilename)


@pytest.mark.parametrize('push', [True, False])
def test_tag_release(versionfilename, packagehandler, push):
    packagehandler.tag_release('0.2', push)
    packagehandler.githandler.update_version.assert_called_once_with(
        '0.2', versionfilename, push=push)
    packagehandler.githandler.tag_release.assert_called_once_with(
        '0.2', push=push)
    packagehandler.changehandler.verify.assert_called_once_with('0.2')
    assert packagehandler.versionhandler.version == '0.2'


def test_tag_setup_version(packagehandler):
    packagehandler.tag_setup_version()
    packagehandler.githandler.tag_release.assert_called_once_with(
        packagehandler.setuphandler.version, push=True)


@pytest.mark.parametrize('push', [True, False])
def test_update_version(versionfilename, packagehandler, push):
    packagehandler.update_version('0.2', push=push)
    packagehandler.githandler.update_version.assert_called_once_with(
        '0.2', versionfilename, push=push)
    assert packagehandler.versionhandler.version == '0.2'


def test_version(packagehandler):
    assert packagehandler.version == '0.1'


def test_name(packagehandler):
    type(packagehandler.setuphandler).name = mock.PropertyMock(
        return_value='name')
    assert packagehandler.name == 'name'


def test_test_with_credentials_file(packagehandler,
                                    mock_prepare_package,
                                    mock_finalize_package,
                                    mock_verify_clean):
    packagehandler.test(base_index='index', credentials_file='creds')
    packagehandler.devpihandler.set_index.assert_called_once_with('index')
    packagehandler.devpihandler.set_credentials_file.assert_called_once_with(
        'creds')
    assert packagehandler.devpihandler.test.call_count == 1
    assert mock_prepare_package.call_count == 1
    assert mock_verify_clean.call_count == 0
    assert mock_finalize_package.call_count == 1


def test_test_without_credentials_file(packagehandler,
                                       mock_prepare_package,
                                       mock_finalize_package,
                                       mock_verify_clean):
    packagehandler.test(base_index='index')
    packagehandler.devpihandler.set_index.assert_called_once_with('index')
    assert not packagehandler.devpihandler.set_credentials_file.called
    assert packagehandler.devpihandler.test.call_count == 1
    assert mock_prepare_package.call_count == 1
    assert mock_verify_clean.call_count == 0
    assert mock_finalize_package.call_count == 1


@pytest.mark.parametrize('save_tests_to', [True, False])
def test_test_save_tests_to(packagehandler,
                            mock_tmpdir,
                            save_tests_to):
    packagehandler.test(base_index='index', save_tests_to=save_tests_to)
    mock_tmpdir.init.assert_called_once_with(copytree_to=save_tests_to)
    assert mock_tmpdir.init.return_value.__enter__.called
    assert mock_tmpdir.init.return_value.__exit__.called


@pytest.mark.parametrize('test_index', [None, 'abcd'])
def test_test_with_index_name(packagehandler,
                              mock_prepare_package,
                              mock_finalize_package,
                              mock_verify_clean,
                              test_index):
    packagehandler.test(base_index='index', test_index=test_index)
    packagehandler.devpihandler.test.assert_called_once_with(test_index, None, None)
    assert packagehandler.devpihandler.test.call_count == 1
    assert mock_prepare_package.call_count == 1
    assert mock_verify_clean.call_count == 0
    assert mock_finalize_package.call_count == 1


@pytest.mark.parametrize('exception', [UncleanGitRepository,
                                       InvalidVersionValue,
                                       ChangeFileNotFound,
                                       MultipleChangeFilesFound,
                                       ChangeFileVersionCheckFailed])
def test_publish_verify_clean_fails(packagehandler,
                                    mock_verify_clean,
                                    exception):
    mock_verify_clean.side_effect = exception
    with pytest.raises(exception):
        packagehandler.publish('srcindex', 'destindex')


@pytest.mark.parametrize('exception', [ChangeFileNotFound,
                                       MultipleChangeFilesFound,
                                       ChangeFileVersionCheckFailed])
def test_tag_release_fails(packagehandler, exception):
    packagehandler.changehandler.verify.side_effect = exception

    with pytest.raises(exception):
        packagehandler.tag_release('0.5', True)


def test_publish_with_credentials_file(packagehandler,
                                       mock_verify_clean):
    packagehandler.publish(srcindex='srcindex', destindex='destindex',
                           credentials_file='creds')
    packagehandler.devpihandler.set_index.assert_called_once_with('srcindex')
    packagehandler.devpihandler.publish.assert_called_once_with(
        'destindex')
    packagehandler.devpihandler.set_credentials_file.assert_called_once_with(
        'creds')
    assert packagehandler.devpihandler.latest_pypi_version.call_count == 1
    assert packagehandler.githandler.tag_release.call_count == 0
    assert mock_verify_clean.call_count == 1


@pytest.mark.parametrize('tag_if_needed', [True, False])
def test_publish_with_tag_if_needed(packagehandler,
                                    mock_verify_clean,
                                    tag_if_needed):
    packagehandler.devpihandler.latest_pypi_version.return_value = '1.0'
    packagehandler.publish(srcindex='srcindex', destindex='destindex',
                           tag_if_needed=tag_if_needed)
    packagehandler.devpihandler.set_index.assert_called_once_with('srcindex')
    packagehandler.devpihandler.publish.assert_called_once_with('destindex')
    assert packagehandler.devpihandler.latest_pypi_version.call_count == 1
    assert packagehandler.githandler.tag_release.call_count == (
        1 if tag_if_needed else 0)
    assert mock_verify_clean.call_count == 1


def test_publish_with_published_tag(packagehandler,
                                    mock_verify_clean):
    packagehandler.devpihandler.latest_pypi_version.return_value = '0.1'
    packagehandler.publish(srcindex='srcindex', destindex='destindex')
    packagehandler.devpihandler.set_index.assert_called_once_with('srcindex')
    assert packagehandler.devpihandler.latest_pypi_version.called
    assert not packagehandler.devpihandler.publish.called
    assert not packagehandler.githandler.tag_release.called
    assert not mock_verify_clean.called


def test_publish_without_credentials_file(packagehandler,
                                          mock_verify_clean):
    packagehandler.publish(srcindex='srcindex', destindex='destindex')
    packagehandler.devpihandler.set_index.assert_called_once_with('srcindex')
    assert not packagehandler.devpihandler.set_credentials_file.called
    assert packagehandler.devpihandler.publish.call_count == 1
    assert mock_verify_clean.call_count == 1


@pytest.mark.parametrize('tag_branch', ['branch1', 'branch2'])
def test_publish_verify_branch_ok(packagehandler, tag_branch):
    packagehandler.githandler.get_branch_of_tag.return_value = tag_branch
    packagehandler.publish(srcindex='srcindex', destindex='destindex',
                           tag_branch=tag_branch)
    packagehandler.githandler.get_branch_of_tag.assert_called_once_with('0.1')


def test_publich_verify_branch_raises(packagehandler):
    packagehandler.githandler.get_branch_of_tag.return_value = 'git_branch'
    with pytest.raises(VersionTagInWrongBranch) as excinfo:
        packagehandler.publish(srcindex='srcindex', destindex='destindex',
                               tag_branch='tag_branch')
    assert (excinfo.value.args[0] ==
            "Version tag (0.1) is in branch 'git_branch' but should be in"
            " 'tag_branch'")


def set_wrong_version(packagehandler, version, versionfilename):
    type(packagehandler.githandler).tag = mock.PropertyMock(
        return_value=version)
    type(packagehandler.setuphandler).version = mock.PropertyMock(
        return_value=version)
    with open(versionfilename) as f:
        content = f.read()
    with open(versionfilename, 'w') as f:
        f.write(content.replace('0.1', version))


@pytest.mark.parametrize('version', [
    '0.dev',
    'dev',
    'b1',
    '0.1dev1',
    '0.2dev1',
    '0.1.2.3'])
def test_wrong_version_format(packagehandler, version, versionfilename):
    set_wrong_version(packagehandler, version, versionfilename)
    with pytest.raises(InvalidVersionValue) as excinfo:
        packagehandler.verify_clean()

    assert excinfo.value.args[0] == "Invalid version '{version}'.".format(
        version=version)


@pytest.mark.parametrize('verify_side_effect', [Exception, None])
def test_with_prepared_package(packagehandler,
                               mock_prepare_package,
                               mock_finalize_package,
                               mock_verify_clean,
                               verify_side_effect):
    mock_verify_clean.side_effect = verify_side_effect
    try:
        packagehandler.test('index')
    except Exception:  # pylint: disable=broad-except
        assert not mock_prepare_package.called
        assert not mock_finalize_package.called
    else:
        assert mock_prepare_package.called
        assert mock_finalize_package.called


@pytest.mark.parametrize('pypiver,tag_if_needed', [
    ('1.0', True), ('0.1', True), ('0.1', False), ('', True)])
def test_publish_tags_if_tag_needed_and_version_not_in_index(
        packagehandler, pypiver, tag_if_needed):

    packagehandler.devpihandler.latest_pypi_version.return_value = pypiver
    packagehandler.publish('index1', 'index2', tag_if_needed=tag_if_needed)
    tag_called = pypiver != packagehandler.version and tag_if_needed
    assert packagehandler.githandler.tag_release.call_count == (
        1 if tag_called else 0)


@pytest.mark.parametrize('pypiver', ['0.1', '1.0'])
def test_is_version_in_index(packagehandler, pypiver):
    packagehandler.devpihandler.latest_pypi_version.return_value = pypiver
    expected_is_version_in_index = pypiver == packagehandler.version
    actual_is_version_in_index = packagehandler._is_version_in_index('index')
    assert actual_is_version_in_index == expected_is_version_in_index
