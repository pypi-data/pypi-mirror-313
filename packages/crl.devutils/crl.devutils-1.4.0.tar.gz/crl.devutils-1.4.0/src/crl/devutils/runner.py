from __future__ import print_function
import subprocess


__copyright__ = 'Copyright (C) 2019, Nokia'


class Failure(Exception):
    pass


class Result(object):
    def __init__(self, cmd, returncode, stdout='', stderr=''):
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = _bytes_to_unicode(stdout)
        self.stderr = _bytes_to_unicode(stderr)

    def __str__(self):
        return ('cmd: {cmd}\n'
                'stdout:\n{stdout}\n'
                'stderr:\n{stderr}\n'
                'returncode: {returncode}'.format(
                    cmd=self.cmd,
                    stdout=self.stdout,
                    stderr=self.stderr,
                    returncode=self.returncode))


def run(cmd, replaced_output=None, shell=True,
        verbose=False, env=None, ignore_codes=None):
    """
    Run shell command and return Result object.

    Args:
        cmd: Command to be executed.
        replaced_output:
            Replace stdout with replaced_output and return empty stderr.
        shell:
            If or not, the given command must be executed through the shell.
        verbose: If or not, task execution must be displayed in more detail.
        env: Environment defining any variables needed for the new process.
        ignore_codes: A list of exit codes that the command must ignore.

    Raises:
        Failure: If the command exited with exit code greater than zero
                 and it is not in list of ignore codes.
    """
    if ignore_codes is None:
        ignore_codes = []

    kwargs = {'stdout': subprocess.PIPE,
              'stderr': subprocess.PIPE,
              'shell': shell}
    if env:
        kwargs['env'] = env
    s = subprocess.Popen(cmd,
                         **kwargs)
    out, err = s.communicate()
    result = (Result(cmd=replaced_output, returncode=s.returncode)
              if replaced_output else
              Result(cmd, s.returncode, out, err))
    if verbose:
        print(result)
    if result.returncode and result.returncode not in ignore_codes:
        raise Failure(result)
    return result


def _bytes_to_unicode(x):
    try:
        return x.decode('utf-8')
    except AttributeError:
        return x
