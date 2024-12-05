from contextlib import contextmanager
from crl.devutils.tmpdir import TmpDir


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


class MismatchOfTagAndVersionfileVersion(Exception):
    pass


class MismatchOfTagAndSetupVersion(Exception):
    pass


class VersionTagInWrongBranch(Exception):
    pass


class PackageHandler(object):
    """
    A handler for handling operations on a package.

    Args:
      versionhandler: An instance of VersionHandler.
      setuphandler: An instance of SetupHandler.
      changehandler: An instance of ChnageHandler.
      githandler: An instance of GitHandler.
      novirtualenv: If or not virtualenv must be used.
    """
    def __init__(self,
                 versionhandler,
                 setuphandler,
                 changehandler,
                 githandler,
                 novirtualenv=False):
        self.versionhandler = versionhandler
        self.setuphandler = setuphandler
        self.changehandler = changehandler
        self.githandler = githandler
        self.devpihandler = None
        self._novirtualenv = novirtualenv

    def set_devpihandler(self, devpihandler):
        self.devpihandler = devpihandler

    def verify_clean(self):
        """
        Verifies the cleanliness/readyness of the package before any
        actions are performed on the package. Following are checked
        1. Version file consistency.
        2. Change file consistency.
        3. Clean working directory.
        4. Tag existence and its branch.

        Raises:
          VersionTagInWrongBranch: Tag found in wrong branch.
          MismatchOfTagAndSetupVersion: Tag and setup version are different.
          InvalidVersionValue: Version in incorrect format.
          ChangeFileNotFound: Change file doesn't exist.
          MultipleChangeFilesFound: More than one change files are found.
          ChangeFileVersionCheckFailed: Change file's latest version
            is not same as package's setup version.
          UncleanGitRepository: Working directory is unclean.
        """
        self.versionhandler.validate_version(self.version)
        self.changehandler.verify(self.version)
        self.githandler.verify_clean()
        self._verify_git_versus_setup()

    def _verify_git_versus_setup(self):
        if self.githandler.tag != self.setuphandler.version:
            raise MismatchOfTagAndSetupVersion(
                'Tag in git ({tag}) differs'
                ' from setup version ({version})'.format(
                    tag=self.githandler.tag,
                    version=self.setuphandler.version))

    def _prepare_package(self):
        self.versionhandler.set_githash(self.githandler.hash)

    def _finalize_package(self):
        self.githandler.checkout(self.versionhandler.version_file)

    def _is_version_in_index(self, index):
        pypiver = self.devpihandler.latest_pypi_version(
            pkg_name=self.name, pypi_index=index)
        if self.version == pypiver:
            return True
        return False

    def tag_release(self, version, push):
        """
        Updates the version file and tags with the specified version
        and optionally pushes to the remote git repository.

        Args:
          version: Version with which the version file must be updated
            and remote git tag must be created.
          push: If TRUE, commits version file and pushes the tag to git.

        Raises:
          ChangeFileVersionCheckFailed: Change file version doesn't
            match with the package version.
        """
        self.changehandler.verify(version)
        self.update_version(version, push)
        self.githandler.tag_release(self.versionhandler.version,
                                    push=push)

    def tag_setup_version(self):
        """Tags with the version in setup if needed.
        """
        self.githandler.tag_release(self.version, push=True)

    def update_version(self, version, push):
        """
        Updates the version file with the specified version and optionally
        commits and pushes the file to the remote git repository.

        Args:
          version: Version with which the version file must be updated.
          push: If TRUE, commits and pushes the version file to git.
        """
        self.versionhandler.set_version(version)
        self.githandler.update_version(self.versionhandler.version,
                                       self.versionhandler.version_file,
                                       push=push)

    @property
    def version(self):
        return self.setuphandler.version

    @property
    def name(self):
        return self.setuphandler.name

    @property
    def novirtualenv(self):
        return self._novirtualenv

    @contextmanager
    def _prepared_package(self):
        try:
            self._prepare_package()
            yield None
        finally:
            self._finalize_package()

    def test(self,
             base_index,
             test_index=None,
             credentials_file=None,
             save_tests_to=None,
             toxargs=None,
             select=None):
        """
        Runs tests and uploads the results and docs to a given index.
        If no index is given, a temporary index which is created for
        running tests is later deleted.

        Args:
          base_index: Index to be used as a base for the test index,
            specified as http[s]://host/user/index.
          test_index: Name of the index created for testing,
            specified as NAME.
          credentials_file: User credentials to use.
          save_tests_to: If given, copies the temporary files
            generated during testing to this path.
          toxargs: Extra command line arguments passsed to tox, e.g.
            "--parallel all"
          select: Selector for release files to be tested. This is
            a regular expression passed to 'devpi test' as '--seclect'
            argument, for example "(-py3-none-any.whl|.tar.gz)"

        Raises:
          ChangeFileVersionCheckFailed: Change file version doesn't
            match with the package version.
        """
        self.changehandler.verify(self.version)
        with TmpDir(copytree_to=save_tests_to):
            self.devpihandler.set_index(base_index)
            if credentials_file:
                self.devpihandler.set_credentials_file(credentials_file)
            with self._prepared_package():
                self.devpihandler.test(test_index, toxargs, select)

    def publish(self,
                srcindex,
                destindex,
                credentials_file=None,
                tag_if_needed=False,
                tag_branch='master'):
        """
        Performs pre-checks and prepares for package version to be published
        from a given index to another.

        Args:
          srcindex: Index from where to find the package version.
          destindex: Index to publish the package version.
          credentials_file: User credentials to use.
          tag_if_needed: If or not to tag the version, if not tagged already.
          tag_branch: Alternative git branch where the tag must be found.

        Return:
          bool: True, if publish was successful and False if publish was
            skipped as package version was already published to destindex.

        Raises:
          VersionTagInWrongBranch: Tag was found in a different branch.
          ChangeFileVersionCheckFailed: Change file version doesn't
            match with the package version.
          UncleanGitRepository: If the working directory is found unclean.
          MismatchOfTagAndSetupVersion: If there is a mismatch in
            tag and setup versions.
        """
        self.devpihandler.set_index(srcindex)
        if credentials_file:
            self.devpihandler.set_credentials_file(credentials_file)

        if not self._is_version_in_index(destindex):
            if tag_if_needed:
                self.githandler.tag_release(self.version, push=True)

            self._verify_tag_branch(tag_branch)
            self.verify_clean()
            self.devpihandler.publish(destindex)
            return True
        return False

    def _verify_tag_branch(self, tag_branch):
        git_branch = self.githandler.get_branch_of_tag(self.version)
        if git_branch != tag_branch:
            raise VersionTagInWrongBranch(
                "Version tag ({version}) is in branch '{git_branch}'"
                " but should be in '{tag_branch}'".format(
                    version=self.version,
                    git_branch=git_branch,
                    tag_branch=tag_branch))
