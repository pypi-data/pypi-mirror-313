import os
from contextlib import contextmanager
import virtualenvrunner.runner
from crl.devutils.utils import get_randomstring
from crl.devutils.doccreator import DocCreator
from crl.devutils.devpiindex import DevpiIndex


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


class _TmpIndex(DevpiIndex):

    def __init__(self,
                 run,
                 packagehandler,
                 baseindex=None,
                 baseurl=None,
                 index_name=None,
                 username=None,
                 clientarg=None):
        super(_TmpIndex, self).__init__(self)
        self.run = run
        self.packagehandler = packagehandler
        self.baseindex = baseindex
        self.baseurl = baseurl
        self.username = username
        self.clientarg = clientarg
        self._index = index_name
        self._set_default_cleanup(not bool(index_name))

    @property
    def index(self):
        if not self._index:
            self._index = 'tmp_{random}'.format(random=get_randomstring(10))
        return self._index

    def _set_default_cleanup(self, cleanup):
        self._default_cleanup = cleanup

    def __enter__(self):
        if not self.index_exists():
            self.create_index()
        self.use_index()
        return self

    def __exit__(self, *args):
        if self._default_cleanup:
            self.delete_index()

    def test(self, toxargs=None, select=None):
        self._upload()
        self.run('devpi test {spec}{clientarg}{toxargs}{select}'.format(
            spec=self.spec,
            clientarg=self.clientarg,
            toxargs=self._get_formatted_toxargs(toxargs),
            select=self._get_formatted_select(select)))

    @staticmethod
    def _get_formatted_toxargs(toxargs):
        if toxargs is None:
            return ''
        return ' --tox-args "{toxargs}"'.format(toxargs=toxargs)

    @staticmethod
    def _get_formatted_select(select):
        if select is None:
            return ''
        return ' --select "{select}"'.format(select=select)

    def _upload(self):
        self.run('devpi upload{clientarg}'.format(
            clientarg=self.clientarg))

        if self._is_docs:
            with self._docsrunnercontext() as runner:
                self._generate_robotdocs(runner)
                self._upload_only_docs(runner)

    def publish(self, index):
        self.push(self.spec, index)

    def _docsrunnercontext(self):

        @contextmanager
        def _runner():
            yield self

        return (_runner()
                if self.packagehandler.novirtualenv else
                virtualenvrunner.runner.Runner(pip_index_url=self.pypiurl,
                                               run=self.run))

    @property
    def _is_docs(self):
        return os.path.isdir('sphinxdocs')

    def _generate_robotdocs(self, runner):
        if not self.packagehandler.novirtualenv:
            self._install_docs_requirements(runner)
        DocCreator(robotdocs_root_folders='robotdocs',
                   run=runner.run).create_robotdocs()

    def _install_docs_requirements(self, runner):
        runner.run('pip install crl.devutils -i {pypiurl}'.format(
            pypiurl=self.pypiurl))
        runner.run('pip install {name}=={version} -i {pypiurl}'.format(
            name=self.packagehandler.name,
            version=self.packagehandler.version,
            pypiurl=self.pypiurl))

    def _upload_only_docs(self, runner):
        runner.run('devpi upload --no-vcs --only-docs{clientarg}'.format(
            clientarg=self.clientarg))

    @property
    def spec(self):
        return '{name}=={version}'.format(
            name=self.packagehandler.name,
            version=self.packagehandler.version)
