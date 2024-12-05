from __future__ import print_function
import os
import shutil
import sys
from collections import namedtuple
from contextlib import contextmanager
from invoke import task
from invoke.main import program
from crl.devutils import (
    versionhandler,
    githandler,
    packagehandler,
    setuphandler,
    changehandler,
    devpihandler,
    doccreator)
from crl.devutils.runner import run, Failure
from crl.devutils.versionhandler import (
    VersionFileNotFound,
    MultipleVersionFilesFound,
    InvalidVersionValue,
    FailedToCreateVersionFile,
    FailedToWriteVersion,
    FailedToWriteGithash)
from crl.devutils.changehandler import (
    ChangeFileNotFound,
    MultipleChangeFilesFound,
    ChangeFileVersionCheckFailed)
from crl.devutils.packagehandler import (
    MismatchOfTagAndVersionfileVersion,
    MismatchOfTagAndSetupVersion,
    VersionTagInWrongBranch)
from crl.devutils.githandler import UncleanGitRepository
from crl.devutils.doccreator import FailedToCreateDocs


__copyright__ = 'Copyright (C) 2019-2024, Nokia'

MODULEDIR = os.path.dirname(os.path.abspath(__file__))
SETUP_TEMPLATE = """
import os
import imp
from setuptools import setup, find_packages

VERSIONFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'src', 'crl', '{libname}', '_version.py')

def get_version():
    return imp.load_source('_version', VERSIONFILE).get_version()

setup(
    name='crl.{libname}',
    version=get_version(),
    author='n/a',
    author_email='n/a',
    description='n/a',
    install_requires=[],
    long_description='n/a',
    license='n/a',
    keywords='n/a',
    url='n/a',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['crl'],
)
"""

GitRepoItem = namedtuple('GitRepoItem', ['dirname', 'repo', 'version'])


def get_verboserun(verbose):
    def verboserun(cmd, **kwargs):
        kwargs_copy = kwargs.copy()
        kwargs_copy['verbose'] = verbose
        return run(cmd, **kwargs_copy)

    return verboserun


def create_packagehandler(libname=None,
                          pathtoversionfile=None,
                          verbose=False,
                          novirtualenv=False):
    verboserun = get_verboserun(verbose)
    kwargs = {'novirtualenv': True} if novirtualenv else {}
    ph = packagehandler.PackageHandler(
        versionhandler=versionhandler.VersionHandler(
            libname=libname,
            pathtoversionfile=pathtoversionfile),
        setuphandler=setuphandler.SetupHandler(run=verboserun),
        changehandler=changehandler.ChangeHandler(run=verboserun),
        githandler=githandler.GitHandler(run=verboserun),
        **kwargs)
    ph.set_devpihandler(devpihandler.DevpiHandler(
        run=verboserun, packagehandler=ph))
    return ph


def create_doccreator(verbose=False, robotdocs_root_folders='robotdocs'):
    return doccreator.DocCreator(robotdocs_root_folders=robotdocs_root_folders,
                                 run=get_verboserun(verbose))


def create_devpihandler(verbose=False):
    verboserun = get_verboserun(verbose)
    return devpihandler.DevpiHandler(
        run=verboserun,
        packagehandler=create_packagehandler(verbose=verbose))


@task(default=True)
def help():
    """Show help, basically an alias for --help.

    This task can be removed once the fix to this issue is released:
    https://github.com/pyinvoke/invoke/issues/180
    """
    print(run(
        'invoke -r {moduledir} --help'.format(moduledir=MODULEDIR)).stdout)


@task
def tag_release(version, libname=None, push=True, verbose=False,
                pathtoversionfile=None):
    """Tag specified release.

    Updates version using `set_version`, creates tag, and pushes changes.
    Args:
        version:   Version to use. See above for supported values and formats.
        libname:   Name of the directory under ./src/crl where version
                   file (_version.py) is located. By default the first
                   directory name is used.
        push:      Push updated version file and tag to the remote.
        pathtoversionfile: Alternative relative path to version file.
        verbose:   Display task execution in more detail.
    """
    ph = create_packagehandler(libname=libname,
                               pathtoversionfile=pathtoversionfile,
                               verbose=verbose)
    ph.tag_release(version, push=push)
    print('Version: {version}'.format(version=ph.version))


@task
def tag_setup_version(verbose=False):
    """Tag specified release.

    Creates tag of version in setup and pushes changes.
    Args:
        verbose:   Display task execution in more detail.
    """
    ph = create_packagehandler(verbose=verbose)
    ph.tag_setup_version()


@task
def set_version(version, push=False, libname=None,
                pathtoversionfile=None, verbose=False):
    """Set version in ./src/crl/<libname>/_version.py`.

    Version can have these values:
    - Actual version number to use. See below for supported formats.
    - String 'dev' to update version to latest development version
      (e.g. 2.8 -> 2.8.1.dev, 2.8.1 -> 2.8.2.dev, 2.8a1 -> 2.8.dev) with
      the current date added or updated.
    - String 'keep' to keep using the previously set version.

    Given version must be in one of these PEP-440 compatible formats:
    - Stable version in 'X.Y' or 'X.Y.Z' format (e.g. 2.8, 2.8.6)
    - Pre-releases with 'aN', 'bN' or 'rcN' postfix (e.g. 2.8a1, 2.8.6rc2)
    - Development releases with '.devYYYYMMDD' postfix (e.g. 2.8.6.dev20141001)
      or with '.dev' alone (e.g. 2.8.6.dev) in which case date is added
      automatically.

    Args:
        version:  Version to use. See above for supported values and formats.
        push:     Commit and push changes to the remote repository.
        libname:  Name of the directory under ./src/crl where version
                  file (_version.py) is located. By default the first
                  directory name is used.
        pathtoversionfile: Alternative relative path to version file.
        verbose:  display task execution in more detail.
    """
    ph = create_packagehandler(libname=libname,
                               pathtoversionfile=pathtoversionfile,
                               verbose=verbose)
    ph.update_version(version, push=push)
    print('Version: {version}'.format(version=ph.version))


@task
def clean(remove_dist=True, create_dirs=False):
    """Clean workspace.

    By default deletes 'dist' directory and removes '*.pyc'
    and '$py.class' files.

    Args:
        create_dirs:  Re-create 'dist' after removing it.
    """
    with error_handling():
        directories = ['dist']
        for name in directories:
            if os.path.isdir(name) and (name != 'dist' or remove_dist):
                shutil.rmtree(name)
            if create_dirs and not os.path.isdir(name):
                os.mkdir(name)
        for directory, _, files in os.walk('.'):
            for name in files:
                if name.endswith(('.pyc', '$py.class')):
                    os.remove(os.path.join(directory, name))


@task
def sdist(deploy=False, remove_dist=False):
    """Create source distribution.

    Args:
        deploy:       Register and upload sdist to PyPI.
        remove_dist:  Control is 'dist' directory initially removed or not.
    """
    clean(remove_dist=remove_dist, create_dirs=True)
    run('python setup.py sdist' + (' register upload' if deploy else ''))
    announce()


def announce():
    print()
    print('Distributions:')
    for name in os.listdir('dist'):
        print(os.path.join('dist', name))


@task
def create_setup(libname=None, add_to_git=True):
    """Create initial setup.py into current directory from library name.
    The module setup will define path to version file
    by joining it with src/crl/libname/_version.py.
    The new file is added and committed by default to git.

    Args:
         libname: Name of the library. If not given first directory under
                  src/crl is used as library name
         add_to_git: If True, add the setup.py to git.
    """
    setupp = get_setup_path()
    if os.path.isfile(setupp):
        raise Exception('The module setup.py already exists.')
    with open(setupp, 'w') as setup_file:
        setup_file.write(SETUP_TEMPLATE.replace(
            '{libname}', libname or
            versionhandler.VersionHandler().get_default_lib()))
    if add_to_git:
        githandler.GitHandler(run).add(setupp)


def get_setup_path():
    return os.path.join(os.getcwd(), 'setup.py')


@task
def create_index(index, baseindex, additional_index=None,
                 credentials_file=None, verbose=False):
    """
    Create an index with given bases

    Args:
        index: Name of the index to create
        baseindex: URL of devpi PyPI index to be used as base index.
               Format: http[s]://host:user/indexname.
        additional_index: Other additional indices to use as base.
               Format: 'user/index1,user/index2'
        credentials_file: /full/path/to/credentials/file with plain text
                          content  username:password. In case no
                          credentials_file given, the default devpi clientdir
                          authorization token is used.
        verbose: Display task execution in more detail.
    """
    dh = create_devpihandler(verbose=verbose)
    dh.create_index(name=index, baseindex=baseindex,
                    otherbase=additional_index,
                    credentials_file=credentials_file)
    print(
        'Successfully created {index} for user {user}'.format(
            index=index, user=dh.username))


@task
def delete_index(index, credentials_file=None, verbose=False):
    """
    Delete an index

    Args:
        index: URL of the devpi PyPI index to delete.
                Format: http[s]://host:user/indexname
        credentials_file: /full/path/to/credentials/file with plain text
                          content  username:password. In case no
                          credentials_file given, the default devpi clientdir
                          authorization token is used.
        verbose: Display task execution in more detail.
    """
    dh = create_devpihandler(verbose=verbose)
    dh.delete_index(index=index, credentials_file=credentials_file)
    print(
        'Successfully deleted {index} for user {user}'.format(
            index=index, user=dh.username))


@task
def test(baseindex, testindex=None, credentials_file=None,  # pylint: disable=too-many-arguments
         save_tests_to=None, virtualenv=True,
         pathtoversionfile=None, verbose=False,
         toxargs=None, select=None):
    """ Uploads contents of current workspace to devpi and runs tox tests.

    Args:
        baseindex: URL of devpi PyPI index to be used as base index.
               Format: http[s]://host:user/indexname.
        testindex: Name of the index to be used for running tests.
                   If the given index doesn't exist, it is created.
                   If not specified, uses a temporary index.
        credentials_file: /full/path/to/credentials/file with plain text
                          content  username:password. In case no
                          credentials_file given, the default devpi clientdir
                          authorization token is used.
        save_tests_to: Copy tests temporary directory to this new not yet
                       existing directory.
        virtualenv: Create and run the task in a new temporary virtualenv.
        pathtoversionfile: Alternative relative path to version file.
        verbose: Display task execution in more detail.
        toxargs: Extra command line arguments for tox. e.g.
                 --toxargs="--parallel all"
        select: Selector for release files to be tested. This is
                a regular expression passed to 'devpi test' as '--select'
                argument, for example "(-py3-none-any.whl|.tar.gz)"
    """
    kwargs = {} if virtualenv else {'novirtualenv': True}
    ph = create_packagehandler(verbose=verbose,
                               pathtoversionfile=pathtoversionfile,
                               **kwargs)
    ph.test(base_index=baseindex, test_index=testindex,
            credentials_file=credentials_file,
            save_tests_to=save_tests_to,
            toxargs=toxargs,
            select=select)


@task
def publish(srcindex, destindex, credentials_file=None, tag_if_needed=False,
            tag_branch='master', verbose=False):
    """*DEPRECATED* Publish version from a given index to another index.

    Args:
        srcindex: URL of devpi PyPI index from where to find the new version.
                Format http[s]://host:user/indexname.
        destindex: URL(short format) of devpi PyPI index to publish to.
                Format: user/indexname.
        tag_if_needed: Tags using the package's version if not found tagged.
        credentials_file: /full/path/to/credentials/file with plain text
                          content  username:password. In case no
                          credentials_file given, the default devpi clientdir
                          authorization token is used.
        tag_branch: Alternative git branch where the tag must be.
        verbose: Display task execution in more detail.
    """
    ph = create_packagehandler(verbose=verbose)
    success = ph.publish(srcindex=srcindex, destindex=destindex,
                         credentials_file=credentials_file,
                         tag_if_needed=tag_if_needed, tag_branch=tag_branch)
    if success:
        print(
            'Published successfully {version} of {name} to {index}'.format(
                version=ph.version, name=ph.name, index=destindex))
    else:
        print(
            'Skipping. {ver} of {name} already published to {index}'.format(
                ver=ph.version, name=ph.name, index=destindex))


@task
def create_docs(robotdocs_root_folders='robotdocs', verbose=False):
    """ Create both Robot Framework and Sphinx documentation.

    If 'robotdocsconf.py' exists in root folders then Robot
    Framework test libraries and resource files documentation
    is generated and integrated with Sphinx documentation.
    'robotdocsconf.py' is searched from robotdocs_root_folders
     recursively.

    Example 1 'robotdocsconf.py' for python library documentation:

    module_name = "RunnerExecutor Libraries"
    output_file = "RunnerExecutor.rst"

    robotdocs = {
    'RunnerExecutor.remoterunnerexecutor.RemoteRunnerExecutor': {
        'args': ['None', 'None', 'False'],
        'docformat': 'robot',
        'synopsis': ('Command executor in the remote target shell.')},
    'RunnerExecutor.remoterunnerexecutor.SftpTransfer': {
        'args': ['False'],
        'docformat': 'robot',
        'synopsis': ('Command executor in the remote target shell.')}

    Example 2 'robotdocsconf.py' for robot resource file documentation:
    module_name = "Deployment Helpers"
    output_file = "Framework_deployment.rst"

    robotdocs = {
    'resources/framework/deployment/_deployment_helper.robot': {
        'docformat': 'robot'
        }
    }

    Robotdocsconf.py's output_file will be the name of the generated
    'sphinxdocs/.........rst' file. A good practice is to name it so that
    library's identification is easy. If output_file is missing then
    robotdocs.rst will be the file name.  Robotdocsconf.py's module_name will
    be written to rst file header. Header text will be: 'Robot Framework Test
    Libraries' if the module name is missing.

    Sphinx documentation is generated according to 'sphinxdocs/conf.py'.

    Args:
        robotdocs_root_folders: folders list with relative or
        absolute path separated by ':',
        robotdocsconf.py is searched from these root folders recursively
        verbose: Display task execution in more detail.

    Example:
        crl create_docs -r library_root_folder1:library_root_folder2 -v
    """
    create_doccreator(verbose=verbose,
                      robotdocs_root_folders=robotdocs_root_folders).create()


@task
def create_robotdocs(robotdocs_root_folders='robotdocs', verbose=False):
    """ Create only Robot Framework ReST documentation.

    If 'robotdocsconf.py' exists in root folders then Robot
    Framework test libraries and resource files documentation
    is generated and integrated with Sphinx documentation.
    'robotdocsconf.py' is searched from robotdocs_root_folders
     recursively.

    Example 1 'robotdocsconf.py' for python library documentation:

    module_name = "RunnerExecutor Libraries"
    output_file = "RunnerExecutor.rst"

    robotdocs = {
    'RunnerExecutor.remoterunnerexecutor.RemoteRunnerExecutor': {
        'args': ['None', 'None', 'False'],
        'docformat': 'robot',
        'synopsis': ('Command executor in the remote target shell.')},
    'RunnerExecutor.remoterunnerexecutor.SftpTransfer': {
        'args': ['False'],
        'docformat': 'robot',
        'synopsis': ('Command executor in the remote target shell.')}

    Example 2 'robotdocsconf.py' for robot resource file documentation:
    module_name = "Deployment Helpers"
    output_file = "Framework_deployment.rst"

    robotdocs = {
    'resources/framework/deployment/_deployment_helper.robot': {
        'docformat': 'robot'
        }
    }

    Robotdocsconf.py's output_file will be the name of the generated
    'sphinxdocs/.........rst' file. A good practice is to name it so that
    library's identification is easy. If output_file is missing then
    robotdocs.rst will be the file name.  Robotdocsconf.py's module_name will
    be written to rst file header. Header text will be: 'Robot Framework Test
    Libraries' if the module name is missing.

    Sphinx documentation is generated according to 'sphinxdocs/conf.py'.

    Args:
        robotdocs_root_folders: folders list with relative or
        absolute path separated by ':',
        robotdocsconf.py is searched from these root folders recursively
        verbose: Display task execution in more detail.

    Example:
        crl create_robotdocs -r library_root_folder1:library_root_folder2 -v
    """
    create_doccreator(
        verbose=verbose,
        robotdocs_root_folders=robotdocs_root_folders).create_robotdocs()


@contextmanager
def error_handling():
    try:
        yield None
    except Failure as e:
        result = e.args[0]
        print('{excname}: {result}'.format(excname=e.__class__.__name__,
                                           result=result))
        sys.exit(result.returncode)  # pylint: disable=no-member
    except (
            ChangeFileNotFound,
            MultipleChangeFilesFound,
            ChangeFileVersionCheckFailed,
            VersionFileNotFound,
            MultipleVersionFilesFound,
            MismatchOfTagAndVersionfileVersion,
            MismatchOfTagAndSetupVersion,
            VersionTagInWrongBranch,
            InvalidVersionValue,
            UncleanGitRepository,
            FailedToCreateVersionFile,
            FailedToWriteVersion,
            FailedToWriteGithash,
            FailedToCreateDocs,
            IOError,
            OSError) as e:
        print('{excname}{message}'.format(
            excname=e.__class__.__name__,
            message='' if str(e) == '' else ': ' + str(e)))
        sys.exit(1)


def main():
    # Hack sys.argv because invoke.Program is not working as a library in
    # version 0.12. See discussion in
    # https://github.com/pyinvoke/invoke/pull/285.
    with error_handling():
        sys.argv = ['invoke', '-r', MODULEDIR] + sys.argv[1:]
        program.run()
