# pylint: disable=unused-argument,protected-access
import os
import pytest
import mock
from fixtureresources.mockfile import MockFile
from fixtureresources.fixtures import create_patch
from crl.devutils.doccreator import DocCreator, FailedToCreateDocs, \
    RobotSphinxDocCreator
from crl.devutils.runner import Result as RunResult


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture(scope='function')
def mock_robotdocsconf(request):
    filename = os.path.join('folder1', 'robotdocsconf.py')
    mfile = MockFile(
        filename=filename,
        content="robotdocs={\n"
                "    'library':\n"
                "        {'args': ['arg'], 'docformat': 'docformat'}}")
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_robotdocsconf_with_outputfile(request):
    filename = os.path.join('folder2', 'robotdocsconf.py')
    mfile = MockFile(
        filename=filename,
        content="output_file=\"module1.rst\"\n\n"
                "robotdocs={\n"
                "    'library':\n"
                "        {'args': ['arg1', 'arg2'],"
                " 'docformat': 'docformat'}}")
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_robotdocsconf_with_modulename(request):
    filename = os.path.join('folder3', 'robotdocsconf.py')
    mfile = MockFile(
        filename=filename,
        content="module_name=\"module libraries\"\n\n"
                "robotdocs={\n"
                "    'library':\n"
                "        {'args': ['arg1', 'arg2'],"
                " 'docformat': 'docformat'}}")
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_robotdocsconf_multiargs(mock_robotdocsconf):
    mock_robotdocsconf.set_content(
        "robotdocs={\n"
        "    'library':\n"
        "        {'args': ['arg1', 'arg2'], 'docformat': 'docformat'}}")
    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsconf_no_docformat(mock_robotdocsconf):
    mock_robotdocsconf.set_content(
        "robotdocs={\n"
        "    'library':\n"
        "        {'args': ['arg']}}")

    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsconf_synopsis(mock_robotdocsconf):
    mock_robotdocsconf.set_content(
        "robotdocs={\n"
        "    'library':\n"
        "        {'synopsis': 'synopsis'}}")

    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsconf_multilibrary(mock_robotdocsconf):
    mock_robotdocsconf.set_content(
        "robotdocs={\n"
        "    'library1': {},\n"
        "    'library2': {}}")

    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsconf_with_resource_file(mock_robotdocsconf):
    mock_robotdocsconf.set_content(
        "robotdocs={\n"
        "    'resources/subfolder1/subfolder2/resource_file.robot': \n"
        "       {'docformat': 'robot'}}")
    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsconf_raises_ioerror(mock_robotdocsconf):
    def raise_ioerror(*args):
        raise IOError('message')

    mock_robotdocsconf.set_side_effect(raise_ioerror)
    return mock_robotdocsconf


@pytest.fixture(scope='function')
def mock_sphinxdocsconf(request):
    filename = os.path.join('sphinxdocs', 'conf.py')
    template = "html_static_path = ['_static']\n" \
               "html_extra_path = ['{path}']\n"
    content = template.format(path=os.path.join(os.pardir, 'robotdocs'))
    mfile = MockFile(
        filename=filename,
        content=content)
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_sphinxdocsconf_no_html_extra_path(mock_sphinxdocsconf):
    mock_sphinxdocsconf.set_content(
        "html_static_path = ['_static']\n")
    return mock_sphinxdocsconf


@pytest.fixture(scope='function')
def mock_robotdocsrst(request):
    mfile = MockFile(filename=os.path.join('sphinxdocs',
                                           'robotdocs.rst'))
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_module1rst(request):
    mfile = MockFile(filename=os.path.join('sphinxdocs',
                                           'module1.rst'))
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_module2rst(request):
    mfile = MockFile(filename=os.path.join('sphinxdocs',
                                           'module2.rst'))
    create_patch(mfile, request)
    return mfile


@pytest.fixture(scope='function')
def mock_run():
    return mock.Mock()


runresult_robotlib_kwd_list_nokwds = RunResult(
    'python -m robot.libdoc library list',
    0, stdout='')

runresult_robotlib_kwd_list_2kwds = RunResult(
    'python -m robot.libdoc library list',
    0, stdout='Keyword One{linesep}Keyword Two{linesep}'.format(
        linesep=os.linesep))

runresult_robotlib_kwd_list_2kwds_as_binary = RunResult(
    'python -m robot.libdoc library list',
    0, stdout='Keyword One{linesep}Keyword Two{linesep}'.format(
        linesep=os.linesep).encode('ascii'))


class MockIsdir(object):
    def __init__(self, path, ispath):
        self.path = path
        self.orig_isdir = os.path.isdir
        self.ispath = ispath

    def isdir(self, path):
        return self.ispath if path == self.path else self.orig_isdir(path)


@pytest.fixture(scope='function')
def mock_os_path_isdir_no_sphinxdocs(request):
    mock_is_dir = MockIsdir(path='sphinxdocs', ispath=False)
    create_patch(mock.patch(
        'os.path.isdir',
        side_effect=mock_is_dir.isdir), request)
    return mock_is_dir


@pytest.fixture(scope='function')
def mock_os_path_isdir_sphinxdocs(mock_os_path_isdir_no_sphinxdocs):
    mock_os_path_isdir_no_sphinxdocs.ispath = True
    return mock_os_path_isdir_no_sphinxdocs


@pytest.fixture()
def mock_search_for_robotdocsconf():
    with mock.patch(
            'crl.devutils.doccreator.DocCreator.search_for_robotdocsconf')\
            as p:
        yield p


robotdoc_generation_call = ('python'
                            ' -m robot.libdoc'
                            ' -f html'
                            ' -F docformat'
                            ' library::arg'
                            ' {}'.format(os.path.join('robotdocs',
                                                      'library.html')))

sphinxdocs_generation_call = ('sphinx-build'
                              ' -b html'
                              ' sphinxdocs'
                              ' build_dir')

robotdoc_kwd_list_call = 'python -m robot.libdoc library::arg list'


robotdocs_rst_header = ('.. Generated by crl.devutils\n\n'
                        'Robot Framework Test Libraries\n'
                        '==============================\n\n')

modul_rst_header = ('.. Generated by crl.devutils\n\n'
                    'module libraries\n'
                    '================\n\n')


def robotdocs_rst_library_section(libname='library', synopsis=None):
    return (
        '.. index::\n'
        '   single: Robot Framework Library; {library}\n\n'
        '* `{library} <{librarypath}.html>`_{synopsis}\n\n'
        '   Keywords: '
        '`Keyword One <{librarypath}.html#Keyword%20One>`__, '
        '`Keyword Two <{librarypath}.html#Keyword%20Two>`__'
    ).format(library=libname,
             librarypath=os.path.basename(libname),
             synopsis='' if not synopsis else ' - ' + synopsis)


def robotdocs_rst_expected_content(
        header=robotdocs_rst_header,
        library_sections=None):
    if library_sections is None:
        library_sections = [robotdocs_rst_library_section()]
    return (
        '{robotdocs_rst_header}'
        '{library_sections}'.format(
            robotdocs_rst_header=header,
            library_sections='\n\n'.join(library_sections),
        ))


@pytest.mark.usefixtures("mock_robotdocsconf",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_one_robotdocsconf(mock_run,
                                  mock_robotdocsrst,
                                  mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    assert mock_robotdocsrst.content == robotdocs_rst_expected_content()
    assert mock_run.mock_calls[0] == mock.call(robotdoc_generation_call)
    assert mock_run.mock_calls[1] == mock.call(robotdoc_kwd_list_call)
    assert mock_run.mock_calls[2] == mock.call(sphinxdocs_generation_call)


@pytest.mark.usefixtures("mock_robotdocsconf_with_outputfile",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_outputfile_included(mock_run,
                                    mock_module1rst,
                                    mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder2']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    assert mock_module1rst.content == robotdocs_rst_expected_content()


@pytest.mark.usefixtures("mock_robotdocsconf_with_modulename",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_module_name_included(mock_run,
                                     mock_robotdocsrst,
                                     mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder3']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    assert mock_robotdocsrst.content == robotdocs_rst_expected_content(
        header=modul_rst_header)


@pytest.mark.usefixtures("mock_robotdocsconf",
                         "mock_robotdocsconf_with_outputfile",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_multiple_robotdocsconf(mock_run,
                                       mock_robotdocsrst,
                                       mock_module1rst,
                                       mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0),
                            RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1', 'folder2']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    assert mock_robotdocsrst.content == robotdocs_rst_expected_content()
    assert mock_module1rst.content == robotdocs_rst_expected_content()


@pytest.mark.usefixtures("mock_robotdocsconf",
                         "mock_os_path_isdir_no_sphinxdocs")
def test_create_no_sphinxdocs(mock_run,
                              mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()

    mock_run.assert_called_once_with(robotdoc_generation_call)


@pytest.mark.usefixtures("mock_os_path_isdir_sphinxdocs")
def test_create_without_robotdocs(mock_run):
    mock_run.side_effect = [RunResult(sphinxdocs_generation_call, 0)]
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    mock_run.assert_called_with(sphinxdocs_generation_call)


@pytest.mark.usefixtures("mock_robotdocsconf",
                         "mock_robotdocsrst",
                         "mock_os_path_isdir_sphinxdocs",
                         "mock_sphinxdocsconf_no_html_extra_path")
def test_create_with_robotdocs_but_no_html_extra_path(
        mock_run,
        mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    with pytest.raises(FailedToCreateDocs) as excinfo:
        DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()

    message = "Incorrect configuration found in {sphinx_conf}"
    message = message.format(sphinx_conf=os.path.join('sphinxdocs', 'conf.py'))
    assert message in str(excinfo.value)


@pytest.mark.usefixtures("mock_robotdocsconf_synopsis",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_generate_robotdocs_rst_synopsis(mock_run,
                                                mock_robotdocsrst,
                                                mock_search_for_robotdocsconf):
    mock_search_for_robotdocsconf.return_value = ['folder1']
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()
    assert mock_robotdocsrst.content == robotdocs_rst_expected_content(
        library_sections=[robotdocs_rst_library_section(synopsis='synopsis')])


@pytest.mark.usefixtures("mock_robotdocsconf_multilibrary",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_robotdocs_rst_multilibrary(mock_run,
                                           mock_robotdocsrst,
                                           mock_search_for_robotdocsconf):
    mock_search_for_robotdocsconf.return_value = ['folder1']
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()

    assert (mock_robotdocsrst.content == robotdocs_rst_expected_content(
        library_sections=[robotdocs_rst_library_section(libname='library1'),
                          robotdocs_rst_library_section(libname='library2')]))


@pytest.mark.usefixtures("mock_robotdocsconf_with_resource_file",
                         "mock_robotdocsrst",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_from_resource_file(mock_run,
                                   mock_robotdocsrst,
                                   mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    DocCreator(robotdocs_root_folders='folder1', run=mock_run).create()

    assert (mock_run.mock_calls[0] ==
            mock.call('python'
                      ' -m robot.libdoc'
                      ' -f html'
                      ' -F robot'
                      ' resources/subfolder1/subfolder2/resource_file.robot'
                      ' {}'.format(
                          os.path.join('robotdocs',
                                       'resource_file.robot.html'))))

    assert (mock_robotdocsrst.content == robotdocs_rst_expected_content(
        library_sections=[robotdocs_rst_library_section(
            libname='resources/subfolder1/subfolder2/resource_file.robot')]))


@pytest.mark.usefixtures("mock_robotdocsconf_multiargs",
                         "mock_robotdocsrst",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_multiargs(mock_run,
                          mock_search_for_robotdocsconf):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    DocCreator(robotdocs_root_folders='folder1', run=mock_run).create()

    assert (mock_run.mock_calls[0] ==
            mock.call('python'
                      ' -m robot.libdoc'
                      ' -f html'
                      ' -F docformat'
                      ' library::arg1::arg2'
                      ' {}'.format(
                          os.path.join('robotdocs',
                                       'library.html'))))


@pytest.mark.parametrize('content', [
    ("robotdocs={\n"
     "    'library':\n"
     "        {'docformat': 'docformat'}}"),
    ("robotdocs={\n"
     "    'library':\n"
     "        {'args': [], 'docformat': 'docformat'}}")])
@pytest.mark.usefixtures("mock_robotdocsrst",
                         "mock_sphinxdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_noargs(mock_run,
                       mock_robotdocsconf,
                       mock_search_for_robotdocsconf,
                       content):
    mock_robotdocsconf.set_content(content)
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult_robotlib_kwd_list_2kwds,
                            RunResult(sphinxdocs_generation_call, 0)]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    DocCreator(robotdocs_root_folders='robotdocs', run=mock_run).create()

    assert (mock_run.mock_calls[0] ==
            mock.call('python'
                      ' -m robot.libdoc'
                      ' -f html'
                      ' -F docformat'
                      ' library'
                      ' {}'.format(
                          os.path.join('robotdocs',
                                       'library.html'))))


@pytest.mark.parametrize('runresult', [
    runresult_robotlib_kwd_list_2kwds,
    runresult_robotlib_kwd_list_2kwds_as_binary])
@pytest.mark.usefixtures("mock_robotdocsconf",
                         "mock_os_path_isdir_sphinxdocs")
def test_create_robotdocs(mock_run,
                          mock_robotdocsrst,
                          mock_search_for_robotdocsconf,
                          runresult):
    mock_run.side_effect = [RunResult(robotdoc_generation_call, 0),
                            runresult]
    mock_search_for_robotdocsconf.return_value = ['folder1']
    dc = DocCreator(robotdocs_root_folders='robotdocs',
                    run=mock_run)
    dc.create_robotdocs()

    assert mock_run.mock_calls[0] == mock.call(robotdoc_generation_call)
    assert mock_run.mock_calls[1] == mock.call(robotdoc_kwd_list_call)
    assert mock_robotdocsrst.content == robotdocs_rst_expected_content()


@pytest.mark.usefixtures("mock_sphinxdocsconf")
def test_sphinxdocsconfig(mock_run):
    sphinxdocsconf = RobotSphinxDocCreator(robotdocs_folder='robotdocs',
                                           run=mock_run).sphinxdocsconfig
    expected_path = os.path.join(os.pardir, 'robotdocs')
    assert sphinxdocsconf['html_extra_path'] == [expected_path]


@pytest.mark.usefixtures("mock_sphinxdocsconf_no_html_extra_path")
def test_sphinxdocsconfig_missing_var(mock_run):
    sphinxdocsconf = RobotSphinxDocCreator(robotdocs_folder='robotdocs',
                                           run=mock_run).sphinxdocsconfig
    assert 'html_extra_path' not in sphinxdocsconf


@pytest.mark.parametrize(
    "mock_run_return_value,library,library_args_dict,"
    "expected_libdoc_call,expected_kwd_list",
    [
        (runresult_robotlib_kwd_list_nokwds, 'library', {},
         'python -m robot.libdoc library list', []),
        (runresult_robotlib_kwd_list_2kwds, 'library', {},
         'python -m robot.libdoc library list',
         ['Keyword One', 'Keyword Two']),
        (runresult_robotlib_kwd_list_2kwds, 'library', {'args': ['arg']},
         'python -m robot.libdoc library::arg list',
         ['Keyword One', 'Keyword Two']),
        (runresult_robotlib_kwd_list_2kwds, 'library',
         {'args': ['arg1', 'arg2']},
         'python -m robot.libdoc library::arg1::arg2 list',
         ['Keyword One', 'Keyword Two'])
    ])
def test_get_robot_lib_keywords(mock_run,
                                mock_run_return_value, library,
                                library_args_dict,
                                expected_libdoc_call,
                                expected_kwd_list):
    mock_run.return_value = mock_run_return_value
    kw_list = RobotSphinxDocCreator(
        robotdocs_folder='robotdocs', run=mock_run).\
        _get_robot_lib_keywords(library, library_args_dict)
    mock_run.assert_called_once_with(expected_libdoc_call)
    assert kw_list == expected_kwd_list
