import glob
import xml.etree.ElementTree as etree
from docutils.core import publish_doctree


__copyright__ = 'Copyright (C) 2019, Nokia'


class ChangeFileNotFound(Exception):
    pass


class MultipleChangeFilesFound(Exception):
    pass


class ChangeFileVersionCheckFailed(Exception):
    pass


class ChangeHandler(object):
    """
    Validates the given change file's syntax and parses
    the change file to get the latest documented version.
    If the change file isn't specified, it looks for a file named
    'CHANGES' on the package's root directory and uses it.
    Valid file extensions for change file are '.rst' and '.md'.

    Args:
      run: Reference to a function capable of running shell commands.
      pathtochangefile: Relative path to change file.
    """
    def __init__(self, run, pathtochangefile=None):
        self.run = run
        self.pathtochangefile = pathtochangefile
        self.allowed_extensions = ['.rst', '.md']

    @property
    def latest_version(self):
        """
        The latest version as in Change file.
        """
        return self._latest_version()

    @property
    def change_file(self):
        """
        Name/Relative path of change file in use.
        """
        if self.pathtochangefile:
            return self.pathtochangefile
        return self._get_default_change_file()

    def _available_rst_md_files(self):
        for f in glob.glob('CHANGES.*'):
            if f.endswith(tuple(self.allowed_extensions)):
                yield f

    def _get_default_change_file(self):
        filesgen = self._available_rst_md_files()

        for f in filesgen:
            try:
                next(filesgen)
                raise MultipleChangeFilesFound()
            except StopIteration:
                return f
        raise ChangeFileNotFound()

    def _verify_syntax(self):
        return self.run('rstcheck {changefile}'.format(
            changefile=self.change_file))

    @staticmethod
    def _read(filename):
        with open(filename) as f:
            return f.read()

    def _latest_version(self):
        contents = self._read(self.change_file)
        doctree = etree.fromstring((publish_doctree(contents).asdom()).toxml())
        titles = [title for section in doctree.findall(
            'section') for title in section.findall('title')]
        versions = [title.text for title in titles] or [
            subtitle.text for subtitle in doctree.findall('subtitle')]
        return versions[0] if versions else ''

    def _verify_latest(self, version):
        if self.latest_version != version:
            raise ChangeFileVersionCheckFailed(
                'Latest version in %s is %s and not %s' % (
                    self.change_file, self.latest_version, version))

    def verify(self, version):
        """
        Verify if the given version is the newest version listed in ChangeFile.

        Args:
          version: version to check.

        Raises:
          Failure: Raised if the Change file syntax is incorrect.
          ChangeFileNotFound: Raised if the Change file is not found.
          MultipleChangeFilesFound: Raised if more than one changefile found.
          ChangeFileVersionCheckFailed: Raises if the given version is not the
            newest version listed in the Changefile.
        """
        self._verify_syntax()
        self._verify_latest(version)
