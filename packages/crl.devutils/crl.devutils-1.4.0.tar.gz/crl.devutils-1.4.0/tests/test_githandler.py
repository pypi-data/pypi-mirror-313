# pylint: disable=unused-argument,protected-access
import pytest
import mock
from crl.devutils.githandler import GitHandler, UncleanGitRepository
from crl.devutils.runner import Failure
from .fixtures import (
    mock_response,
    mock_run,
    create_mpatch)


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_commit(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.commit'), request)


@pytest.fixture(scope='function')
def mock_update_version(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.update_version'), request)


@pytest.fixture(scope='function')
def mock_add_tag(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler._add_tag'), request)


@pytest.fixture(scope='function')
def mock_is_clean_status(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler._is_clean_status'), request)


@pytest.fixture(scope='function')
def mock_is_tag_present(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler._is_tag_present'), request)


@pytest.fixture(scope='function')
def mock_is_clean(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.is_clean',
        return_value=False), request)


@pytest.fixture(scope='function')
def mock_update(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.update'), request)


@pytest.fixture(scope='function')
def mock_clone(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.clone'), request)


@pytest.fixture(scope='function')
def mock_status(request):
    return create_mpatch(mock.patch(
        'crl.devutils.githandler.GitHandler.status'), request)


@pytest.fixture(scope='function')
def mock_os_getcwd(request):
    return create_mpatch(mock.patch('os.getcwd', return_value='cwd'), request)


@pytest.fixture(scope='function')
def mock_os_chdir(request):
    return create_mpatch(mock.patch('os.chdir'), request)


@pytest.fixture(scope='function')
def mock_os_path_isdir(request):
    return create_mpatch(mock.patch('os.path.isdir'), request)


@pytest.mark.parametrize('paths,expected', [
    ('a', 'git add a'),
    (['a', 'b'], 'git add a b')])
def test_git_add(mock_run, paths, expected):
    assert GitHandler(run=mock_run).add(paths)
    mock_run.assert_called_once_with(expected)


@pytest.mark.parametrize('paths,expected_runs', [
    ('a', [mock.call("git add a"),
           mock.call("git commit -m 'm' a")]),
    (['a', 'b'], [mock.call("git add a b"),
                  mock.call("git commit -m 'm' a b")])])
def test_git_commit_no_push(mock_run,
                            paths,
                            expected_runs,
                            mock_is_clean):
    assert GitHandler(run=mock_run).commit(paths, 'm')
    assert mock_run.mock_calls == expected_runs


@pytest.mark.parametrize('run,expected_runs,expected_return', [
    (mock.MagicMock(side_effect=[True, True, True]),
     [mock.call("git add filename"),
      mock.call("git commit -m 'message' filename"),
      mock.call("git push")], True),
    (mock.MagicMock(side_effect=[True, True, Failure]),
     [mock.call("git add filename"),
      mock.call("git commit -m 'message' filename"),
      mock.call("git push")], False),
    (mock.MagicMock(side_effect=[True, Failure, True]),
     [mock.call("git add filename"),
      mock.call("git commit -m 'message' filename")], False),
    (mock.MagicMock(side_effect=[Failure, True, True]),
     [mock.call("git add filename")], False)])
def test_git_commit_push(run,
                         expected_runs,
                         expected_return,
                         mock_is_clean):

    try:
        assert GitHandler(run=run).commit(
            'filename', 'message', push=True) == expected_return
    except Failure:
        assert not expected_return

    assert run.mock_calls == expected_runs


@pytest.mark.parametrize('is_clean_status,expected_runs', [
    (False, [mock.call("git add filename"),
             mock.call("git commit -m 'message' filename")]),
    (True, [mock.call("git add filename")])])
def test_commit_with_clean_status(is_clean_status,
                                  expected_runs,
                                  mock_run,
                                  mock_is_clean_status):
    mock_is_clean_status.return_value = is_clean_status
    GitHandler(run=mock_run).commit('filename', 'message', push=False)
    assert mock_run.mock_calls == expected_runs


@pytest.mark.parametrize('is_clean_status,expected_result', [
    (True, True),
    (False, False)])
def test_is_clean(mock_is_clean_status,
                  mock_run,
                  is_clean_status,
                  expected_result,):
    mock_is_clean_status.return_value = is_clean_status
    assert GitHandler(run=mock_run).is_clean() == expected_result


@pytest.mark.parametrize('run_response,expected_return', [
    (mock_response(stdout='a'), False),
    (mock_response(stdout=''), True),
    (mock_response(stdout='\n'), True)])
def test_is_clean_status(mock_run, run_response, expected_return):
    mock_run.return_value = run_response
    assert GitHandler(run=mock_run)._is_clean_status() == expected_return
    assert mock_run.mock_calls == [
        mock.call('git status --porcelain')]


def test_status(mock_run):
    mock_run.return_value = mock_response(stdout='stdout\n')
    assert GitHandler(run=mock_run).status() == 'stdout'
    mock_run.assert_called_once_with('git status')


@pytest.mark.parametrize('is_clean_return', [
    False,
    pytest.param(True,
                 marks=pytest.mark.xfail)])
def test_clean_raises(mock_is_clean,
                      is_clean_return,
                      mock_status,
                      mock_os_getcwd):
    mock_is_clean.return_value = is_clean_return
    mock_status.return_value = 'status'
    with pytest.raises(UncleanGitRepository) as excinfo:
        GitHandler(run=mock_run).verify_clean()
    assert (excinfo.value.args[0] ==
            'git repository in cwd is unclean:\n'
            'status')


@pytest.mark.parametrize('push,run,expected_runs,expected_return', [
    (True, mock.MagicMock(side_effect=[True, True]),
     [mock.call("git tag -a 0.1 -m 'm'"),
      mock.call("git push --tags")], True),
    (False, mock.MagicMock(side_effect=[True, Failure]),
     [mock.call("git tag -a 0.1 -m 'm'")], True),
    (False, mock.MagicMock(side_effect=[Failure, Failure]),
     [mock.call("git tag -a 0.1 -m 'm'")], False)])
def test_add_tag(run, push, expected_runs, expected_return):
    try:
        assert (GitHandler(run=run)._add_tag('0.1', 'm', push=push) ==
                expected_return)
    except Failure:
        pass
    finally:
        assert run.mock_calls == expected_runs


@pytest.mark.parametrize('push,commit_return,expected_return', [
    (True, True, True),
    (True, False, False),
    (False, True, True)])
def test_update_version(push,
                        commit_return,
                        expected_return,
                        mock_run,
                        mock_commit):
    mock_commit.return_value = commit_return
    assert GitHandler(run=mock_run).update_version(
        '0.1', 'version_file', push=push) == expected_return
    mock_commit.assert_called_once_with('version_file',
                                        'Updated version to 0.1', push=push)


@pytest.mark.parametrize('push,tag_exists', [
    (True, True), (False, True),
    (False, False), (True, False)])
def test_tag_release(mock_run,
                     mock_add_tag,
                     mock_is_tag_present,
                     push,
                     tag_exists):
    mock_is_tag_present.return_value = tag_exists
    assert GitHandler(
        run=mock_run).tag_release(
            '0.1', push=push)
    mock_is_tag_present.assert_called_once_with('0.1')
    if not tag_exists:
        mock_add_tag.assert_called_once_with('0.1', 'Release 0.1', push=push)
        assert mock_run.mock_calls == [
            mock.call('git push') for _ in range(push)]


def test_tag(mock_run):
    mock_run.return_value = mock_response('tag\n')
    assert GitHandler(run=mock_run).tag == 'tag'
    mock_run.assert_called_once_with('git describe --tags')


def test_hash(mock_run):
    mock_run.return_value = mock_response('hash\n')
    assert GitHandler(run=mock_run).hash == 'hash'
    mock_run.assert_called_once_with('git rev-parse --verify HEAD')


def test_checkout(mock_run):
    mock_run.return_value = 'return_value'
    assert GitHandler(run=mock_run).checkout('filename') == 'return_value'
    mock_run.assert_called_once_with('git checkout filename')


@pytest.mark.parametrize('stdout', [
    'branch', ' branch', ' branch\n', '* branch\n'])
def test_get_branch_of_tag(mock_run, stdout):
    mock_run.return_value = mock_response(stdout)
    assert GitHandler(run=mock_run).get_branch_of_tag('0.1') == 'branch'
    mock_run.assert_called_once_with('git branch --contains 0.1')


def test_clone(mock_run, mock_os_getcwd, mock_os_chdir):
    GitHandler(run=mock_run).clone('git@host:group/gitrepo.git', 'version')
    assert mock_run.mock_calls == [
        mock.call('git clone git@host:group/gitrepo.git'),
        mock.call('git checkout version')]
    assert mock_os_chdir.mock_calls == [mock.call('gitrepo'), mock.call('cwd')]


def test_update(mock_run,
                mock_os_getcwd,
                mock_os_chdir,
                mock_is_clean_status):
    GitHandler(run=mock_run).update('git@host:group/gitrepo.git', 'version')
    assert mock_os_chdir.mock_calls == [mock.call('gitrepo'), mock.call('cwd')]
    assert mock_is_clean_status.called
    assert mock_run.mock_calls == [
        mock.call('git fetch --all'),
        mock.call('git checkout version')]


@pytest.mark.parametrize('isdir,expected_clone_calls,expected_update_calls', [
    (True, [], [mock.call('git@host:group/gitrepo.git', 'version')]),
    (False, [mock.call('git@host:group/gitrepo.git', 'version')], [])])
def test_clone_or_update(mock_update,
                         mock_clone,
                         mock_run,
                         mock_os_path_isdir,
                         isdir,
                         expected_clone_calls,
                         expected_update_calls):
    mock_os_path_isdir.return_value = isdir

    GitHandler(run=mock_run).clone_or_update(
        'git@host:group/gitrepo.git', 'version')
    assert mock_update.mock_calls == expected_update_calls
    assert mock_clone.mock_calls == expected_clone_calls
