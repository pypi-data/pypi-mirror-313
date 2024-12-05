import re
import os
import tempfile
import shutil
from contextlib import contextmanager
from crl.devutils.devpiindex import DevpiIndex
from crl.devutils._tmpindex import _TmpIndex
from crl.devutils.utils import get_randomstring


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


class MalformedURL(Exception):
    pass


class DevpiHandler(object):
    """
    A handler for handling all devpi related actions.

    Args:
      run: Reference to a function capable of running shell commands.
      packagehandler: An instance of PackageHandler object
      credentials_file: User login information in a file.
    """
    _index_re = re.compile('^(http[s]*://[^/]+)/([^/]+/[^/]+)[/]*$')
    _user_re = re.compile('^(http[s]*://[^/]+)/([^:]+):')
    _user_index_re = re.compile('^([^/]+)/([^/]+)*$')

    def __init__(self,
                 run,
                 packagehandler,
                 credentials_file=None):
        self.run = run
        self.packagehandler = packagehandler
        self._index = None
        self.credentials_file = credentials_file
        self._clientdir = None
        self._username = None

    @property
    def index(self):
        """
        Currently used PyPI index.
        """
        return self._index

    def set_index(self, index):
        """
        Set the given index as the current index.

        Args:
          index: Index, specified as http[s]://host/user/index.

        Raises:
          MalformedURL: If index URL is in wrong format.
        """
        self._index = index
        self._validate_index_url_format(index)

    def _validate_index_url_format(self, index):
        match = self._index_re.match(index)
        if not match or len(match.groups()) < 2:
            raise MalformedURL(
                "URL '{index}' not in form"
                " 'http[s]://host/user/indexname'".format(
                    index=index))

    def _get_short_url(self, index):
        short_name = index
        try:
            self._validate_index_url_format(index)
            short_name = self._index_re.match(index).groups()[1]
        except MalformedURL:
            self._validate_user_index_url_format(index)
        return short_name

    def _get_long_url(self, index):
        try:
            self._validate_index_url_format(index)
            long_name = index
        except MalformedURL:
            self._validate_user_index_url_format(index)
            long_name = "{url}/{userindex}".format(
                url=self.url, userindex=index)
        return long_name

    def _validate_user_index_url_format(self, index):
        match = self._user_index_re.match(index)
        if not match or len(match.groups()) < 2:
            raise MalformedURL(
                "URL '{index}' not in form"
                " 'user/indexname'".format(
                    index=index))

    def set_credentials_file(self, credentials_file):
        self.credentials_file = credentials_file

    def publish(self, index):
        """
        Publish a version of package from current index to given index.

        Args:
          index: PYPI Index to publish to.
        """
        with self._session():
            self._publish(index)

    def test(self, test_index=None, toxargs=None, select=None):
        """
        Test and upload results and docs to the given index.
        If no index is specified, uses a temporary index.

        Args:
          test_index: Index name to use for testing, specified as NAME.
          toxargs: extra command line arguments for tox.
          select: Selector for the tests to run.
        """
        with self._session():
            self._test_via_tmpindex(test_index, toxargs, select)

    def create_index(self, name, baseindex, otherbase=None,
                     credentials_file=None):
        """
        Create a new index for the current user with given bases.

        Args:
          name: Name of the index to create, specified as NAME.
          baseindex: URL of index from which the new index will inherit.
          otherbase: Name of other indices (specified as USER/NAME) to use.
          credentials_file: File containing the users credentials.
        """
        def _combined(base, otherbase=None):
            base = base.split()
            if otherbase:
                base.extend(otherbase.split(','))
            return ','.join(base)

        self.set_index(baseindex)
        if credentials_file:
            self.set_credentials_file(credentials_file)

        with self._session():
            index = DevpiIndex(run=self.run,
                               baseindex=_combined(self.userindex, otherbase),
                               baseurl=self.url,
                               index_name=name,
                               username=self.username,
                               clientarg=self._clientarg)
            if not index.index_exists():
                index.create_index()
            index.use_index()

    def delete_index(self, index, credentials_file=None):
        """
        Delete the given index.

        Args:
          index: Index to delete, specified as http[s]://host/user/index.
        """
        self.set_index(index)
        if credentials_file:
            self.set_credentials_file(credentials_file)

        with self._session():
            indexname = self.userindex.split('/')[-1]
            index = DevpiIndex(run=self.run,
                               baseindex=self.userindex,
                               baseurl=self.url,
                               index_name=indexname,
                               username=self.username,
                               clientarg=self._clientarg)
            if index.index_exists():
                index.delete_index()

    @contextmanager
    def _session(self):
        try:
            self._login()
            yield None
        finally:
            self._logoff()

    @property
    def _clientarg(self):
        return (' --clientdir {clientdir}'.format(clientdir=self.clientdir)
                if self.credentials_file else '')

    @property
    def clientdir(self):
        if not self._clientdir and self.credentials_file:
            self._clientdir = self._get_tmpdir()
        return self._clientdir

    def _get_tmpdir(self):
        return os.path.join(
            tempfile.gettempdir(),
            '{username}_{randomstring}'.format(
                username=self.username,
                randomstring=get_randomstring(length=10)))

    @property
    def username(self):
        """
        Currently logged in username. If no user is logged in,
        uses credentials from a file.
        """
        if self.credentials_file:
            self._username = self._get_credentials()[0]
        else:
            self._username = self._get_login_user()
        return self._username

    @property
    def _password(self):
        return self._get_credentials()[1].rstrip('\n')

    def _get_credentials(self):
        with open(self.credentials_file) as creds:
            return creds.read().split(':', 1)

    def _get_login_user(self):
        return self._user_re.match(self.run('devpi user').stdout).groups()[1]

    @property
    def url(self):
        """
        The base URL of the PYPI server, specified as http[s]://host
        """
        return self._index_re.match(self.index).groups()[0]

    @property
    def userindex(self):
        """
        Current user index, specified as user/indexname
        """
        return self._index_re.match(self.index).groups()[1]

    def _pip_search_pkg(self, pkgname, index):
        return self.run('pip search {pkg_name} -i {index}'.format(
            pkg_name=pkgname,
            index=index if index.endswith('/') else index + '/'),
            ignore_codes=[23]).stdout.split('\n')

    def latest_pypi_version(self, pkg_name=None, pypi_index=None):
        """
        Returns latest version of a package from the given index.

        Args:
          pkg_name: Name of the package, if different from the current package.
          pypi_index: Name of the index, if different from the current index.
        """
        version = ''
        pkgname = pkg_name if pkg_name else self.packagehandler.name
        index = self._get_long_url(pypi_index) if pypi_index else self.index
        results = self._pip_search_pkg(pkgname, index)

        for result in results:
            pkg_details = result.split()
            if pkg_details and pkgname in pkg_details[0].split('/'):
                version = re.search(r'\((.*?)\)', pkg_details[1]).group(1)
        return version

    def _login(self):
        self.run('devpi use {url}{clientarg}'.format(
            url=self.url, clientarg=self._clientarg))
        if self.credentials_file:
            self.run(
                ['devpi', 'login', self.username, '--password', self._password,
                 '--clientdir', self.clientdir],
                replaced_output='devpi login {username}'.format(
                    username=self.username),
                shell=False)

    def _logoff(self):
        if self.credentials_file:
            self.run('devpi logoff{clientarg}'.format(
                clientarg=self._clientarg))
            shutil.rmtree(self.clientdir)

    def _publish(self, index):
        short_index_name = self._get_short_url(index)
        indexname = self.userindex.split('/')[1]
        pkgspec = '{name}=={version}'.format(
            name=self.packagehandler.name, version=self.packagehandler.version)

        index = DevpiIndex(run=self.run,
                           baseindex=self.userindex,
                           baseurl=self.url,
                           index_name=indexname,
                           username=self.username,
                           clientarg=self._clientarg)
        index.use_index()
        index.push(pkgspec, short_index_name)

    def _test_via_tmpindex(self, index, toxargs, select):
        with _TmpIndex(run=self.run,
                       packagehandler=self.packagehandler,
                       baseindex=self.userindex,
                       baseurl=self.url,
                       index_name=index,
                       username=self.username,
                       clientarg=self._clientarg) as tmpindex:
            tmpindex.test(toxargs=toxargs, select=select)
