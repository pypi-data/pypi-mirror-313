import io
import mock
try:
    import __builtin__
    builtins_module = __builtin__.__name__
except ImportError:
    import builtins
    builtins_module = builtins.__name__

# Heuristics for I/O stream selection for text files
# BytesIO works better in 2.7 while in 3.4 StringIO works better
try:
    io.StringIO('')
    SavedIOBase = io.StringIO
except TypeError:
    SavedIOBase = io.BytesIO


__copyright__ = 'Copyright (C) 2019, Nokia'


class SavedIO(SavedIOBase):

    def __init__(self, content='', saver=None, mode=None):
        super(SavedIO, self).__init__(self.get_updated_content(content, mode))
        self._saver = saver
        if mode is not None and mode.startswith('a'):
            self.seek(0, 2)

    @staticmethod
    def get_updated_content(content, mode):
        if mode is not None:
            content = '' if mode.startswith('w') else content
        return content

    def __exit__(self, *args, **kwargs):
        if self._saver:
            self._saver(self.getvalue())
        super(SavedIO, self).__exit__(*args, **kwargs)


class MockFile(object):
    """ Simple mock for a file to be used via __builtin__.open
        Please note that only one file can be mocked at a time with
        this implementation.
    """

    def __init__(self,
                 filename=None,
                 content='',
                 side_effect=None,
                 args=None):
        self.filename = None
        self.content = None
        self.side_effect = None
        self.set_filename(filename)
        self.set_content(content)
        self.set_side_effect(side_effect)
        self.args = args
        self.mocked_open = None
        self.mock_open = None
        self.saver = self.set_content

    def set_filename(self, filename):
        self.filename = filename

    def set_content(self, content):
        self.content = content

    def set_side_effect(self, side_effect):
        self.side_effect = side_effect

    def set_saver(self, saver):
        self.saver = saver

    def mock_open_file(self, *args):
        if args[0] == self.filename:
            f = SavedIO(content=self.content,
                        saver=self.saver,
                        mode=args[1] if len(args) > 1 else None)
            f.name = self.filename
            if self.side_effect:
                self.side_effect(*args)
        else:
            self.mocked_open.stop()
            f = open(*args)
            self.mocked_open.start()
        return f

    def start(self):
        if self.mock_open is None:
            self.mocked_open = mock.patch(
                '{module}.open'.format(module=builtins_module),
                self.mock_open_file)
            self.mock_open = self.mocked_open.start()

    def stop(self):
        if self.mock_open is not None:
            self.mocked_open.stop()
            self.mock_open = None

    def __enter__(self):
        self.start()
        return self.mock_open_file(self.filename, self.args)

    def __exit__(self, *args):
        self.stop()
