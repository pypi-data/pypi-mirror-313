import os
import stat
import tempfile
import shutil
import logging
from crl.devutils.utils import get_randomstring


__copyright__ = 'Copyright (C) 2019, Nokia'

logger = logging.getLogger(__name__)


class TmpDir(object):
    def __init__(self, copytree_to=None):
        self.copytree_to = copytree_to
        self._tmpdir = None
        self._original_tmpdir = None

    def __enter__(self):
        self._start_tmpdir()
        return self

    def __exit__(self, *args):
        self._stop_tmpdir()

    @property
    def path(self):
        return self._tmpdir

    def _start_tmpdir(self):
        self._set_tmpdir()
        self._mkdir_tmpdir()

    def _set_tmpdir(self):
        self.__set_original_tmpdir()
        self._tmpdir = os.path.join(
            tempfile.gettempdir(), 'tmp_{random}'.format(
                random=get_randomstring(10)))
        os.environ['TMPDIR'] = self.path

    def __set_original_tmpdir(self):
        if self.tmpdir():
            self._original_tmpdir = self.tmpdir()

    def _mkdir_tmpdir(self):
        os.makedirs(self.path)

    def _stop_tmpdir(self):
        try:
            if self.copytree_to is not None:
                self._add_permissions_to_path(
                    stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                shutil.copytree(self.path, self.copytree_to)
        finally:
            if self._original_tmpdir is None:
                del os.environ['TMPDIR']
            else:
                os.environ['TMPDIR'] = self._original_tmpdir
            self._rmtree_with_chmod_allow_all()

    def _rmtree_with_chmod_allow_all(self):
        self._add_permissions_to_path(
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        shutil.rmtree(self.path)

    def _add_permissions_to_path(self, permissions):
        for root, dirs, files in os.walk(self.path):
            self._add_permissions(root, permissions)
            for items in [dirs, files]:
                for item in items:
                    self._add_permissions(os.path.join(root, item),
                                          permissions)

    @staticmethod
    def _add_permissions(path, permissions):
        try:
            logger.debug('Adding permissions %o to %s', permissions, path)
            os.chmod(path, os.stat(path).st_mode | permissions)
        except OSError:
            logger.debug('could not change the permission of %s',
                         path)

    @staticmethod
    def tmpdir():
        return (os.environ['TMPDIR']
                if 'TMPDIR' in os.environ else
                None)
