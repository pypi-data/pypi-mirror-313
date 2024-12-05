# pylint: disable=unused-argument
from builtins import str
import subprocess
import mock
import pytest
from crl.devutils.runner import Result, run, Failure


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_popen(request):
    ms = mock.Mock()
    ms.communicate = mock.Mock(return_value=('out', 'err'))
    ms.returncode = 0
    mpatch = mock.patch('subprocess.Popen', return_value=ms)
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


def test_run(mock_popen):
    r = run('cmd')
    mock_popen.assert_called_once_with('cmd',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
    assert r.returncode == 0
    assert r.stdout == 'out'
    assert r.stderr == 'err'
    assert (str(r) ==
            'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 0')


def test_run_replaced_output(mock_popen):
    r = run(cmd='cmd', replaced_output='replaced_output')
    assert r.returncode == 0
    assert r.cmd == 'replaced_output'
    assert r.stdout == ''
    assert r.stderr == ''
    assert (str(r) ==
            'cmd: replaced_output\nstdout:\n\nstderr:\n\nreturncode: 0')


def test_run_ignore_codes(mock_popen):
    mock_popen.return_value.returncode = 2
    r = run(cmd='cmd', ignore_codes=[2, 20, 123])
    assert r.returncode == 2
    assert r.cmd == 'cmd'
    assert r.stdout == 'out'
    assert r.stderr == 'err'
    assert (str(r) ==
            'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 2')


def test_run_ignore_codes_raises(mock_popen):
    mock_popen.return_value.returncode = 2
    with pytest.raises(Failure) as excinfo:
        run('cmd', ignore_codes=[1])
    r = excinfo.value.args[0]
    assert r.cmd == 'cmd'
    assert r.stdout == 'out'
    assert r.stderr == 'err'
    assert str(r) == 'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 2'


def test_run_return_stdout_and_stderr_is_unicode(mock_popen):
    mock_popen.return_value.communicate.return_value = (b'out', b'err')
    r = run('cmd')
    assert isinstance(r.stdout, str)
    assert isinstance(r.stderr, str)


def test_result_output_type():
    result = Result('cmd', 0, b'out', b'err')
    assert isinstance(result.stdout, str)
    assert isinstance(result.stderr, str)


def test_result_false(mock_popen):
    mock_popen.return_value.returncode = 1
    with pytest.raises(Failure) as excinfo:
        run('cmd')
    r = excinfo.value.args[0]
    assert r.cmd == 'cmd'
    assert r.stdout == 'out'
    assert r.stderr == 'err'
    assert str(r) == 'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 1'


def test_result_string():
    assert (str(Result('cmd', 0, 'out', 'err')) ==
            'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 0')


def test_verbose(capsys, mock_popen):
    run(cmd='cmd', verbose=True)
    out, _ = capsys.readouterr()
    assert out == 'cmd: cmd\nstdout:\nout\nstderr:\nerr\nreturncode: 0\n'


def test_verbose_replaced_output(capsys, mock_popen):
    run(cmd='cmd', verbose=True, replaced_output='replaced_output')
    out, _ = capsys.readouterr()
    assert out == 'cmd: replaced_output\nstdout:\n\nstderr:\n\nreturncode: 0\n'


@pytest.mark.parametrize('shell', [True, False])
def test_run_shell(mock_popen, shell):
    run(cmd='cmd', shell=shell)
    mock_popen.assert_called_once_with('cmd',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=shell)


def test_run_env(mock_popen):
    run('cmd', env={'name': 'value'})
    mock_popen.assert_called_once_with('cmd',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True,
                                       env={'name': 'value'})
