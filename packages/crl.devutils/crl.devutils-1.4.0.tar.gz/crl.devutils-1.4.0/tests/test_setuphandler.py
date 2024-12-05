# pylint: disable=unused-import
from crl.devutils.setuphandler import SetupHandler
from .fixtures import mock_response, mock_run


__copyright__ = 'Copyright (C) 2019, Nokia'


def test_version(mock_run):
    mock_run.return_value = mock_response('0.1\n')
    assert SetupHandler(run=mock_run).version == '0.1'
    mock_run.assert_called_once_with('python setup.py --version')


def test_name(mock_run):
    mock_run.return_value = mock_response('name\n')
    assert SetupHandler(run=mock_run).name == 'name'
    mock_run.assert_called_once_with('python setup.py --name')
