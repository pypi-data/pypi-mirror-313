from collections import namedtuple
import pytest
import mock
from fixtureresources.fixtures import create_patch
from crl.devutils.tasks import (
    test,
    publish,
    create_packagehandler,
    create_devpihandler,
    create_doccreator,
    error_handling,
    set_version,
    tag_release,
    tag_setup_version,
    create_index,
    delete_index,
    create_docs,
    create_robotdocs)
from crl.devutils.runner import Failure, Result
from crl.devutils.versionhandler import (
    VersionHandler,
    VersionFileNotFound,
    MultipleVersionFilesFound,
    InvalidVersionValue,
    FailedToCreateVersionFile,
    FailedToWriteVersion,
    FailedToWriteGithash)
from crl.devutils.packagehandler import (
    MismatchOfTagAndVersionfileVersion,
    MismatchOfTagAndSetupVersion,
    VersionTagInWrongBranch)
from crl.devutils.changehandler import (
    ChangeFileNotFound,
    MultipleChangeFilesFound,
    ChangeFileVersionCheckFailed)
from crl.devutils.githandler import UncleanGitRepository
from crl.devutils.doccreator import DocCreator, FailedToCreateDocs
from .fixtures import (  # pylint: disable=unused-import
    mock_packagehandler,
    mock_setuphandler,
    mock_changehandler,
    mock_githandler,
    mock_devpihandler)


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


MockHandlerFactory = namedtuple('MockHandlerFactory', [
    'create', 'handler'])


@pytest.fixture(scope='function')
def mock_create_packagehandler(request, mock_packagehandler):
    return MockHandlerFactory(create_patch(mock.patch(
        'crl.devutils.tasks.create_packagehandler',
        return_value=mock_packagehandler), request), mock_packagehandler)


@pytest.fixture(scope='function')
def mock_create_devpihandler(request, mock_devpihandler):
    return MockHandlerFactory(create_patch(mock.patch(
        'crl.devutils.tasks.create_devpihandler',
        return_value=mock_devpihandler), request), mock_devpihandler)


@pytest.fixture(scope='function')
def mock_doccreator():
    return mock.Mock(spec_set=DocCreator)


@pytest.fixture(scope='function')
def mock_create_doccreator(request, mock_doccreator):
    return MockHandlerFactory(create_patch(mock.patch(
        'crl.devutils.tasks.create_doccreator',
        return_value=mock_doccreator), request), handler=mock_doccreator)


@pytest.fixture(scope='function')
def mpatch_packagehandler(request, mock_packagehandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.packagehandler.PackageHandler',
        return_value=mock_packagehandler), request)


@pytest.fixture(scope='function')
def mock_versionhandler():
    return mock.Mock(spec_set=VersionHandler)


@pytest.fixture(scope='function')
def mpatch_versionhandler(request, mock_versionhandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.versionhandler.VersionHandler',
        return_value=mock_versionhandler), request)


@pytest.fixture(scope='function')
def mpatch_setuphandler(request, mock_setuphandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.setuphandler.SetupHandler',
        return_value=mock_setuphandler), request)


@pytest.fixture(scope='function')
def mpatch_changehandler(request, mock_changehandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.changehandler.ChangeHandler',
        return_value=mock_changehandler), request)


@pytest.fixture(scope='function')
def mpatch_githandler(request, mock_githandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.githandler.GitHandler',
        return_value=mock_githandler), request)


@pytest.fixture(scope='function')
def mpatch_devpihandler(request, mock_devpihandler):
    return create_patch(mock.patch(
        'crl.devutils.tasks.devpihandler.DevpiHandler',
        return_value=mock_devpihandler), request)


@pytest.fixture(scope='function')
def mpatch_doccreator(request, mock_doccreator):
    return create_patch(mock.patch(
        'crl.devutils.tasks.doccreator.DocCreator',
        return_value=mock_doccreator), request)


@pytest.fixture(scope='function')
def mpatch_run(request):
    return create_patch(mock.patch(
        'crl.devutils.tasks.run', return_value='return_value'), request)


class PathToVersionFile(object):
    def __init__(self, path=None):
        self.path = path

    @property
    def expected_kwargs(self):
        return {'pathtoversionfile': self.path}

    @property
    def kwargs(self):
        return {} if self.path is None else {
            'pathtoversionfile': self.path}


@pytest.mark.parametrize('verbose,push,pathtoversionfile', [
    (True, True, PathToVersionFile()),
    (False, True, PathToVersionFile()),
    (False, False, PathToVersionFile('path'))])
def test_tag_release(mock_create_packagehandler,
                     capsys,
                     verbose,
                     push,
                     pathtoversionfile):
    tag_release(version='0.1',
                libname='libname',
                push=push,
                verbose=verbose, **pathtoversionfile.kwargs)
    mock_create_packagehandler.create.assert_called_once_with(
        libname='libname',
        verbose=verbose,
        **pathtoversionfile.expected_kwargs)
    mock_create_packagehandler.handler.tag_release.assert_called_once_with(
        '0.1', push=push)
    out, err = capsys.readouterr()
    assert out == 'Version: 0.1\n'
    assert err == ''


@pytest.mark.parametrize('verbose', [True, False])
def test_tag_setup_version(mock_create_packagehandler,
                           capsys,
                           verbose):
    tag_setup_version(verbose=verbose)
    mock_create_packagehandler.create.assert_called_once_with(verbose=verbose)
    tag_setup = mock_create_packagehandler.handler.tag_setup_version
    tag_setup.assert_called_once_with()
    _, err = capsys.readouterr()
    assert err == ''


@pytest.mark.parametrize('push,pathtoversionfile,verbose', [
    (True, PathToVersionFile(), True),
    (True, PathToVersionFile(), False),
    (False, PathToVersionFile(), True),
    (False, PathToVersionFile('path'), False)])
def test_set_version(mock_create_packagehandler,
                     capsys,
                     push,
                     verbose,
                     pathtoversionfile):
    set_version(version='0.1', push=push, libname='libname', verbose=verbose,
                **pathtoversionfile.kwargs)
    mock_create_packagehandler.create.assert_called_once_with(
        libname='libname', verbose=verbose,
        **pathtoversionfile.expected_kwargs)
    mock_create_packagehandler.handler.update_version.assert_called_once_with(
        '0.1', push=push)
    out, err = capsys.readouterr()
    assert out == 'Version: 0.1\n'
    assert err == ''


@pytest.mark.parametrize('testindex,save_tests_to,pathtoversionfile,toxargs,select',
                         [(None, None, PathToVersionFile(), None, None),
                          ('test', 'save_tests_to',
                           PathToVersionFile('path'), '--parallel all', '-py3-none-any.whl')])
def test_test(mock_create_packagehandler,
              testindex,
              save_tests_to,
              pathtoversionfile,
              toxargs,
              select):
    test(baseindex='index', testindex=testindex, credentials_file='creds',
         save_tests_to=save_tests_to, toxargs=toxargs, select=select,
         **pathtoversionfile.kwargs)
    mock_create_packagehandler.handler.test.assert_called_once_with(
        base_index='index', test_index=testindex, credentials_file='creds',
        save_tests_to=save_tests_to, toxargs=toxargs, select=select)


def test_test_without_virtualenv(mock_create_packagehandler):
    test(baseindex='index', virtualenv=False)
    mock_create_packagehandler.create.assert_called_once_with(
        verbose=False, novirtualenv=True, pathtoversionfile=None)


@pytest.mark.parametrize('verbose', [True, False])
def test_test_with_verbose(mock_create_packagehandler, verbose):
    test(baseindex='index', verbose=verbose)
    mock_create_packagehandler.create.assert_called_once_with(
        verbose=verbose, pathtoversionfile=None)


@pytest.mark.parametrize('tag_needed,verbose', [
    (True, False), (True, True),
    (False, True), (False, False)])
def test_publish(mock_create_packagehandler,
                 capsys, tag_needed, verbose):
    publish(srcindex='index1', destindex='index2',
            tag_if_needed=tag_needed, credentials_file='creds',
            verbose=verbose)
    mock_create_packagehandler.create.assert_called_once_with(
        verbose=verbose)
    mock_create_packagehandler.handler.publish.return_value = True
    mock_create_packagehandler.handler.publish.assert_called_once_with(
        srcindex='index1', destindex='index2',
        tag_if_needed=tag_needed, credentials_file='creds',
        tag_branch='master')
    out, err = capsys.readouterr()
    assert out == 'Published successfully 0.1 of name to index2\n'
    assert err == ''


def test_publish_with_published_tag(mock_create_packagehandler,
                                    capsys):
    mock_create_packagehandler.handler.publish.return_value = False
    publish(srcindex='index1', destindex='index2')
    assert mock_create_packagehandler.create.called
    mock_create_packagehandler.handler.publish.assert_called_once_with(
        srcindex='index1', destindex='index2',
        tag_if_needed=False, credentials_file=None,
        tag_branch='master')
    out, err = capsys.readouterr()
    assert out == 'Skipping. 0.1 of name already published to index2\n'
    assert err == ''


def test_publish_tag_branch(mock_create_packagehandler):
    publish(srcindex='index1', destindex='index2', tag_branch='tag_branch')
    mock_create_packagehandler.handler.publish.assert_called_once_with(
        srcindex='index1', destindex='index2', tag_if_needed=False,
        credentials_file=None, tag_branch='tag_branch')


@pytest.mark.parametrize('kwargs', [
    {}, {'novirtualenv': True}])
def test_create_packagehandler(mpatch_packagehandler,
                               mpatch_versionhandler,
                               mpatch_setuphandler,
                               mpatch_changehandler,
                               mpatch_githandler,
                               mpatch_devpihandler,
                               kwargs):
    create_packagehandler('lib', **kwargs)
    mpatch_packagehandler.assert_called_once_with(
        versionhandler=mpatch_versionhandler.return_value,
        setuphandler=mpatch_setuphandler.return_value,
        changehandler=mpatch_changehandler.return_value,
        githandler=mpatch_githandler.return_value,
        **kwargs)
    ph = mpatch_packagehandler.return_value
    ph.set_devpihandler.assert_called_once_with(
        mpatch_devpihandler.return_value)


# TODO: Use directly pytest.mark.parametrize if
# https://github.com/pytest-dev/pytest/issues/349 is corrected.
@pytest.fixture(params=[
    'mpatch_setuphandler',
    'mpatch_changehandler',
    'mpatch_githandler',
    'mpatch_devpihandler'])
def handler_with_run_arg(request,
                         mpatch_setuphandler,
                         mpatch_changehandler,
                         mpatch_githandler,
                         mpatch_devpihandler):
    return {'mpatch_setuphandler': mpatch_setuphandler,
            'mpatch_changehandler': mpatch_changehandler,
            'mpatch_githandler': mpatch_githandler,
            'mpatch_devpihandler': mpatch_devpihandler}[request.param]


@pytest.mark.parametrize('verbose', [True, False])
def test_create_package_handler_verbose_and_run(handler_with_run_arg,
                                                mpatch_run,
                                                verbose):
    create_packagehandler(verbose=verbose)
    assert handler_with_run_arg.call_args[1]['run'](
        'cmd', replaced_output='replaced_output') == 'return_value'
    mpatch_run.assert_called_once_with('cmd',
                                       replaced_output='replaced_output',
                                       verbose=verbose)
    assert handler_with_run_arg.call_args[1]['run'](
        'cmd', replaced_output='replaced_output',
        shell=False) == 'return_value'


def test_error_handling_failure(capsys):
    with pytest.raises(SystemExit) as excinfo:
        with error_handling():
            raise Failure(Result(cmd='cmd',
                                 returncode=1,
                                 stdout='stdout',
                                 stderr='stderr'))
    out, err = capsys.readouterr()
    assert out == ('Failure: cmd: cmd\nstdout:\nstdout\nstderr:\nstderr\n'
                   'returncode: 1\n')
    assert err == ''
    assert excinfo.value.args[0] == 1


@pytest.mark.parametrize('exception', [
    ChangeFileNotFound,
    MultipleChangeFilesFound,
    ChangeFileVersionCheckFailed,
    VersionFileNotFound,
    MultipleVersionFilesFound,
    MismatchOfTagAndVersionfileVersion,
    MismatchOfTagAndSetupVersion,
    VersionTagInWrongBranch,
    IOError,
    OSError,
    InvalidVersionValue,
    UncleanGitRepository,
    FailedToCreateVersionFile,
    FailedToWriteVersion,
    FailedToWriteGithash,
    FailedToCreateDocs])
def test_error_handling(capsys, exception):
    with pytest.raises(SystemExit):
        with error_handling():
            raise exception('message')
    out, err = capsys.readouterr()
    assert 'message' in out
    assert err == ''


@pytest.mark.parametrize('message,expected_out', [
    ('message', 'VersionFileNotFound: message\n'),
    ('', 'VersionFileNotFound\n')])
def test_error_handling_without_message(capsys, message, expected_out):
    with pytest.raises(SystemExit):
        with error_handling():
            raise VersionFileNotFound(message)
    out, err = capsys.readouterr()
    assert out == expected_out
    assert err == ''


@pytest.mark.parametrize('verbose', [True, False])
def test_create_docs(mock_create_doccreator, verbose):
    create_docs(verbose=verbose, robotdocs_root_folders='robotdocs')

    mock_create_doccreator.create.assert_called_once_with(
        verbose=verbose,
        robotdocs_root_folders='robotdocs')
    assert mock_create_doccreator.handler.create.call_count == 1


@pytest.mark.parametrize('verbose', [True, False])
def test_create_robotdocs(mock_create_doccreator, verbose):
    create_robotdocs(verbose=verbose, robotdocs_root_folders='robotdocs')

    mock_create_doccreator.create.assert_called_once_with(
        verbose=verbose,
        robotdocs_root_folders='robotdocs')
    assert mock_create_doccreator.handler.create_robotdocs.call_count == 1


@pytest.mark.parametrize('verbose', [True, False])
def test_create_doccreator(mpatch_run,
                           mpatch_doccreator,
                           verbose):
    assert create_doccreator(verbose=verbose) == mpatch_doccreator.return_value
    assert mpatch_doccreator.call_args[1]['run'](
        'cmd', replaced_output='replaced_output') == 'return_value'
    mpatch_run.assert_called_once_with('cmd',
                                       replaced_output='replaced_output',
                                       verbose=verbose)


@pytest.mark.parametrize('verbose', [True, False])
def test_create_devpihandler(mpatch_run,
                             mpatch_devpihandler,
                             verbose):
    assert create_devpihandler(verbose) == mpatch_devpihandler.return_value
    assert mpatch_devpihandler.call_args[1]['run'](
        'cmd', replaced_output='replaced_output') == 'return_value'
    mpatch_run.assert_called_once_with('cmd',
                                       replaced_output='replaced_output',
                                       verbose=verbose)
    assert mpatch_devpihandler.call_args[1]['run'](
        'cmd', replaced_output='replaced_output',
        shell=False) == 'return_value'


@pytest.mark.parametrize('verbose', [True, False])
def test_create_index(mock_create_devpihandler, capsys, verbose):
    create_index(index='index', baseindex='base', verbose=verbose)
    mock_create_devpihandler.create.assert_called_once_with(verbose=verbose)
    assert mock_create_devpihandler.handler.create_index.call_count == 1
    mock_create_devpihandler.handler.create_index.assert_called_once_with(
        name='index', baseindex='base',
        otherbase=None, credentials_file=None)
    out, err = capsys.readouterr()
    assert 'Successfully created index for user user\n' in out
    assert err == ''


@pytest.mark.parametrize('verbose', [True, False])
def test_create_index_with_creds(mock_create_devpihandler, capsys, verbose):
    create_index(index='index', baseindex='base',
                 credentials_file='creds', verbose=verbose)
    mock_create_devpihandler.create.assert_called_once_with(verbose=verbose)
    assert mock_create_devpihandler.handler.create_index.call_count == 1
    mock_create_devpihandler.handler.create_index.assert_called_once_with(
        name='index', baseindex='base',
        otherbase=None, credentials_file='creds')
    out, err = capsys.readouterr()
    assert 'Successfully created index for user user\n' in out
    assert err == ''


@pytest.mark.parametrize('verbose', [True, False])
def test_delete_index_with_creds(mock_create_devpihandler, capsys, verbose):
    delete_index(index='index', credentials_file='creds', verbose=verbose)
    mock_create_devpihandler.create.assert_called_once_with(verbose=verbose)
    assert mock_create_devpihandler.handler.delete_index.call_count == 1
    mock_create_devpihandler.handler.delete_index.assert_called_once_with(
        index='index', credentials_file='creds')
    out, err = capsys.readouterr()
    assert 'Successfully deleted index for user user\n' in out
    assert err == ''
