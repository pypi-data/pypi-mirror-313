import os
import re
import time
import errno
from contextlib import contextmanager
from crl.devutils import utils


__copyright__ = 'Copyright (C) 2019, Nokia'


class VersionFileNotFound(Exception):
    pass


class MultipleVersionFilesFound(Exception):
    pass


class FailedToCreateVersionFile(Exception):
    pass


class FailedToWriteVersion(Exception):
    pass


class FailedToWriteGithash(Exception):
    pass


class InvalidVersionValue(Exception):
    pass


class VersionHandler(object):
    """
    Version handler for ./src/crl/<libname>/_version.py`.

    Version can have these values:
    - Actual version number to use. See below for supported formats.
    - String 'dev' to update version to latest development version (e.g. 2.8
    -> 2.8.1.dev, 2.8.1 -> 2.8.2.dev, 2.8a1 -> 2.8.dev) with the current
    date added or updated.

    Given version must be in one of these PEP-440 compatible formats:
    - Stable version in 'X.Y' or 'X.Y.Z' format (e.g. 2.8, 2.8.6)
    - Pre-releases with 'aN', 'bN' or 'rcN' postfix (e.g. 2.8a1, 2.8.6rc2)
    - Development releases with '.devYYYYMMDD' postfix (e.g.
    2.8.6.dev20141001) or with '.dev' alone (e.g. 2.8.6.dev) in which case
    date is added automatically.

    Args:
      libname: Name of the library.
      pathtoversionfile: Relative path to the version file.
    """

    VERSION_FILE_TEMPLATE = ("VERSION = '{version}'\n"
                             "GITHASH = ''\n"
                             "\n\n"
                             "def get_version():\n"
                             "    return VERSION\n"
                             "\n\n"
                             "def get_githash():\n"
                             "    return GITHASH\n")

    VERSION_RE = re.compile('^((\d+\.\d+)(\.\d+)?)((a|b|rc|.dev)(\d+))?$')

    def __init__(self, libname=None, pathtoversionfile=None):
        self.libname = libname
        self.pathtoversionfile = pathtoversionfile

    @property
    def version(self):
        return self._run_version_file_function('get_version')

    @property
    def version_file(self):
        if self.pathtoversionfile:
            return self.pathtoversionfile
        return self._get_version_file()

    def _run_version_file_function(self, function_name):
        namespace = {}
        utils.execfile(self.version_file, namespace)
        return namespace[function_name]()

    @property
    def githash(self):
        return self._run_version_file_function('get_githash')

    def set_githash(self, githash):
        self._update_file(self.version_file, "GITHASH = '.*'", githash)
        self._verify_githash(githash, FailedToWriteGithash)

    def _verify_githash(self, githash, exception):
        if githash != self.githash:
            raise exception(
                "Githash should be '{githash}'"
                " but it is '{selfgithash}'".format(
                    githash=githash, selfgithash=self.githash))

    def set_version(self, version):
        if version != 'keep':
            self._write_version_file_and_verify(
                self._validate_and_update(version))

    def _validate_and_update(self, version):
        if version == 'dev':
            version = self._get_dev_version()
        if version.endswith('.dev'):
            version += time.strftime('%Y%m%d')
        self.validate_version(version)
        return version

    def validate_version(self, version):
        if not self.VERSION_RE.match(version):
            raise InvalidVersionValue("Invalid version '{}'.".format(version))

    def _get_dev_version(self):
        major, minor, pre = self.VERSION_RE.match(self.version).groups()[1:4]
        if not pre:
            minor = '.{}'.format(int(minor[1:]) + 1 if minor else 1)
        if not minor:
            minor = ''
        return '{}{}.dev'.format(major, minor)

    def _write_version_file_and_verify(self, version):
        self._write_version_file(version)
        self._verify_version(version, FailedToWriteVersion)

    def _verify_version(self, version, exception):
        if version != self.version:
            raise exception(
                "Version should be '{version}'"
                " but it is '{selfversion}'".format(
                    version=version, selfversion=self.version))

    def _write_version_file(self, version):
        try:
            with self.__ioerror_handling():
                self._update_file(self.version_file,
                                  "VERSION = '.*'", version)
        except VersionFileNotFound:
            self._create_initial_version_file(version)

    @staticmethod
    @contextmanager
    def __ioerror_handling():
        try:
            yield None
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise FailedToCreateVersionFile(str(e))
            raise VersionFileNotFound

    @staticmethod
    def _update_file(path, pattern, replacement):
        replacement = pattern.replace('.*', replacement)
        with open(path) as version_file:
            content = ''.join(re.sub(pattern, replacement, line)
                              for line in version_file)
        with open(path, 'w') as version_file:
            version_file.write(content)

    def _create_initial_version_file(self, version):
        with open(self._get_new_version_file(), 'w') as vsf:
            vsf.write(self.VERSION_FILE_TEMPLATE.replace('{version}', version))

    def _get_version_file(self):
        return (self._try_to_get_version_file_for_subdir(self.libname)
                if self.libname else
                self._try_to_get_version_file())

    def _get_new_version_file(self):
        return (self._try_to_get_version_file_for_subdir(self.libname)
                if self.libname else
                self._get_default_version_file())

    def _try_to_get_version_file(self):
        vsf = self._get_all_existing_version_files()
        vslen = len(vsf)
        if vslen == 0:
            raise VersionFileNotFound()
        if vslen == 1:
            return vsf[0]
        raise MultipleVersionFilesFound('Candidates are: {vsf}.'.format(
            vsf=vsf))

    def _get_all_existing_version_files(self):
        return [v for v in self._get_all_version_files() if os.path.isfile(v)]

    def _get_all_version_files(self):
        return [self._get_version_file_for_subdir(n)
                for n in self._get_crl_subdirs()]

    def _get_default_version_file(self):
        return self._get_version_file_for_subdir(self.get_default_lib())

    def _try_to_get_version_file_for_subdir(self, subdir):
        vfile = self._get_version_file_for_subdir(subdir)
        if os.path.isfile(vfile):
            return vfile
        raise VersionFileNotFound()

    def _get_version_file_for_subdir(self, subdir):
        return os.path.abspath(
            os.path.join(self._get_crl_path(),
                         subdir, '_version.py'))

    def get_default_lib(self):
        return self._get_crl_subdirs()[0]

    def _get_crl_subdirs(self):
        return next(os.walk(self._get_crl_path()))[1]

    @staticmethod
    def _get_crl_path():
        return os.path.join('src', 'crl')
