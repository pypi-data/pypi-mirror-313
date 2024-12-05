from contextlib import contextmanager
import os
import re
from six import string_types


__copyright__ = 'Copyright (C) 2019, Nokia'


class UncleanGitRepository(Exception):
    pass


class GitHandler(object):
    """
    A handler responsible for handling all git related actions.

    Args:
      run: Reference to a function capable of running shell commands.
    """
    def __init__(self, run):
        self.run = run

    def tag_release(self, version, push):
        """
        Tags a given version if not already tagged and optionally pushes
        all tags to remote.

        Args:
          version: Version to tag.
          push: If or not to push the tags to remote.

        Returns:
          bool: True, if all commands succeded, False, if any of them failed.
        """
        calls = list()
        if not self._is_tag_present(version):
            calls.append(
                lambda: self._add_tag(version, 'Release {version}'.format(
                    version=version), push=push))
            if push:
                calls.append(self._push)
        return self._call_list(calls)

    @property
    def tag(self):
        return self.run('git describe --tags').stdout.rstrip('\n')

    @property
    def hash(self):
        return self.run('git rev-parse --verify HEAD').stdout.rstrip('\n')

    def add(self, paths):
        return self.run('git add {paths}'.format(
            paths=self._get_flattened_paths(paths)))

    def remotes(self):
        return self.run('git remote').stdout.split('\n')

    @staticmethod
    def _get_flattened_paths(paths):
        return (paths
                if isinstance(paths, string_types) else
                ' '.join(paths))

    def commit(self, paths, message, push=False):
        """
        Commits given file with given message and optionally pushes to remote.

        Args:
          paths: Path of file(s) to be committed.
          message: Commit message.
          push: If or not to push the commit to remote.

        Returns:
          bool: True, if all commands succeded
        """
        calls = [lambda: self.add(paths)]
        if not self.is_clean():
            self._add_commit(calls, paths, message)
        if push:
            calls.append(self._push)
        return self._call_list(calls)

    def _add_commit(self, calls, paths, message):
        calls.append(lambda: self.run(
            "git commit -m '{message}' {paths}".format(
                message=message, paths=self._get_flattened_paths(paths))))

    def _push(self):
        return self.run('git push')

    @staticmethod
    def _call_list(calls):
        ret = True
        for c in calls:
            ret = c()
        return ret

    def verify_clean(self):
        """
        Checks if or not, the current working dirctory is clean.

        Raises:
          UncleanGitRepository: If the current working directory is unclean.
        """
        if not self.is_clean():
            raise UncleanGitRepository(
                'git repository in {cwd} is unclean:\n'
                '{status}'.format(
                    cwd=os.getcwd(),
                    status=self.status()))

    def is_clean(self):
        """
        Checks if current working directory is clean.

        Returns:
          bool: True, if directory is clean.
        """
        return self._is_clean_status()

    def _is_clean_status(self):
        out = self.run('git status --porcelain').stdout.rstrip('\n')
        return not out or out == ''

    def _is_tag_present(self, tag):
        remotes = self.remotes()
        try:
            self.run(
                'git ls-remote --exit-code --tags {remote} {tag}'.format(
                    remote=remotes[0] if remotes else 'origin',
                    tag=tag)).returncode
        except Exception:  # pylint: disable=broad-except
            return False
        return True

    def status(self):
        return self.run('git status').stdout.rstrip('\n')

    def _add_tag(self, tag, message, push):
        calls = [lambda: self.run("git tag -a {tag} -m '{message}'".format(
            tag=tag, message=message))]
        if push:
            calls.append(lambda: self.run("git push --tags"))
        return self._call_list(calls)

    def update_version(self, version, version_file, push):
        """
        Updates the given version file with a given version,
        commits and optionally pushes to the remote.

        Args:
          version: Version to update.
          version_file: Name or Path of the version file.
          push: If or not to push the commit to remote.
        """
        return self.commit(version_file, 'Updated version to {version}'.format(
            version=version), push=push)

    def checkout(self, filename):
        """
        Checks out the given filename

        Args:
          filename: Name of the file to checkout.
        """
        return self.run('git checkout {filename}'.format(filename=filename))

    def get_branch_of_tag(self, tag):
        """
        Get the branch which contains the given tag.

        Args:
          tag: Tag to look for.
        """
        return self.run('git branch --contains {tag}'.format(
            tag=tag)).stdout.rstrip('\n').split(' ', 1)[-1:][0]

    def clone(self, gitrepo, version):
        """
        Clone and checkout the given version of git repository.

        Args:
          gitrepo: URL of the git project.
          version: Git version to checkout.
        """
        self.run('git clone {gitrepo}'.format(gitrepo=gitrepo))
        with self._run_in_clone_repo_dir(gitrepo):
            return self.checkout(version)

    @contextmanager
    def _run_in_clone_repo_dir(self, gitrepo):
        current_dir = os.getcwd()
        os.chdir(self._get_clone_directory_name(gitrepo))
        try:
            yield None
        finally:
            os.chdir(current_dir)

    @staticmethod
    def _get_clone_directory_name(repo):
        return re.sub('\.git$', '', os.path.basename(repo))

    def update(self, gitrepo, version):
        """
        Update the local working directory with the given version
        if the local working directory is clean.

        Args:
          gitrepo: URL of the git project.
          version: Git version to checkout.
        """
        with self._run_in_clone_repo_dir(gitrepo):
            self.verify_clean()
            self.run('git fetch --all')
            self.checkout(version)

    def clone_or_update(self, gitrepo, version):
        """
        If not already cloned, clones the version to a local directory.
        If cloned already, updates the local directory with given version.

        Args:
          gitrepo: URL of the git project.
          version: Git version to clone or update.
        """
        if os.path.isdir(self._get_clone_directory_name(gitrepo)):
            return self.update(gitrepo, version)
        return self.clone(gitrepo, version)
