__copyright__ = 'Copyright (C) 2019, Nokia'


class DevpiIndex(object):
    def __init__(self,
                 run,
                 baseindex=None,
                 baseurl=None,
                 index_name=None,
                 username=None,
                 clientarg=None):
        self.run = run
        self.baseindex = baseindex
        self.baseurl = baseurl
        self.username = username
        self.clientarg = clientarg
        self._index = index_name

    @property
    def index(self):
        return self._index

    @property
    def pypiurl(self):
        return '{baseurl}/{username}/{index}/+simple/'.format(
            baseurl=self.baseurl,
            username=self.username,
            index=self.index)

    def create_index(self):
        self.run('devpi index -c {index}{bases}{clientarg}'.format(
            index=self.index,
            bases=' bases={baseindex}'.format(
                baseindex=self.baseindex) if self.baseindex else '',
            clientarg=self.clientarg))

    def use_index(self):
        self.run('devpi use {index}{clientarg}'.format(
            index=self.index, clientarg=self.clientarg))

    def delete_index(self):
        self.run('devpi index -y --delete {index}{clientarg}'.format(
            index=self.index, clientarg=self.clientarg))

    def push(self, pkgspec, index):
        self.run('devpi push {spec} {index}{clientarg}'.format(
            spec=pkgspec, index=index, clientarg=self.clientarg))

    def indices(self):
        return self.run('devpi index -l{clientarg}'.format(
            clientarg=self.clientarg)).stdout.split('\n')

    def index_exists(self):
        index = '{username}/{index}'.format(
            username=self.username, index=self.index)
        if index in self.indices():
            return True
        return False
