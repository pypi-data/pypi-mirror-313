__copyright__ = 'Copyright (C) 2019, Nokia'


class SetupHandler(object):
    """
    A handler to retreive information about a package's setup.py

    Args:
      run: Reference to a function capable fo running shell commands.
    """
    def __init__(self, run):
        self.run = run

    @property
    def version(self):
        """
        Version of the package as in setup.py
        """
        return self.run('python setup.py --version').stdout.rstrip('\n')

    @property
    def name(self):
        """
        Name of the package as in setup.py
        """
        return self.run('python setup.py --name').stdout.rstrip('\n')
