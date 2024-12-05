import os
import abc
import six
from crl.devutils import utils


__copyright__ = 'Copyright (C) 2019, Nokia'


class FailedToCreateDocs(Exception):
    pass


class DocCreator(object):
    def __init__(self, robotdocs_root_folders, run):
        self.run = run
        self.robotdocs_folders = \
            self.search_for_robotdocsconf(robotdocs_root_folders)

    @staticmethod
    def search_for_robotdocsconf(root_folders):
        """
        Search robotdocsconf.py from root folders recursively.
        Args:
            root_folders:folders with relative or absolute path
            separated by ':'

        Returns: list of folders where from robotdocsconf.py is found,
        no duplication
        """
        robotdocs_folders = set()
        root_folders_list = root_folders.split(":")
        for root_folder in root_folders_list:
            for root, _, files in os.walk(root_folder):
                for file in files:
                    if file == "robotdocsconf.py":
                        robotdocs_folders.add(os.path.abspath(root))
        return robotdocs_folders

    def _folder_doc_creators(self):
        if not self.robotdocs_folders:
            yield SphinxDocCreator(self.run)
        else:
            for rfolder in self.robotdocs_folders:
                yield RobotSphinxDocCreator(rfolder, self.run)

    def create(self):
        for fdc in self._folder_doc_creators():
            fdc.create()

    def create_robotdocs(self):
        for fdc in self._folder_doc_creators():
            fdc.create_robotdocs()


@six.add_metaclass(abc.ABCMeta)
class SubDocCreator(object):
    def __init__(self, run):
        self.run = run
        self._sphinxdocsconfig = None

    def create(self):
        """Create all documentation.
        """
        self._create_sphinxdocs()

    @abc.abstractmethod
    def create_robotdocs(self):
        """Create only robotdocs.
        """

    @property
    def sphinxdocsconfig(self):
        if self._sphinxdocsconfig is None:
            self._initialize_sphinxdocs_config()
        return self._sphinxdocsconfig

    def _create_sphinxdocs(self):
        if os.path.isdir('sphinxdocs'):
            self.run('sphinx-build -b html sphinxdocs build_dir')

    def _initialize_sphinxdocs_config(self):
        """
        Fetch some variables of interest from sphinxdocs/conf.py and store
        their values to dictionary self._sphinxdocsconfig
        """
        self._sphinxdocsconfig = {}
        try:
            namespace = {}
            utils.execfile(os.path.join('sphinxdocs', 'conf.py'),
                           namespace)
            for param in ['html_extra_path']:
                if param in namespace:
                    self._sphinxdocsconfig[param] = namespace[param]
        except IOError:
            pass


class SphinxDocCreator(SubDocCreator):

    def create_robotdocs(self):
        pass


class RobotSphinxDocCreator(SubDocCreator):

    def __init__(self, robotdocs_folder, run):
        super(RobotSphinxDocCreator, self).__init__(run)
        self.robotdocs_folder = robotdocs_folder
        self._robotdocsconfig = None

    def create(self):
        self._create_robotdocs()
        super(RobotSphinxDocCreator, self).create()

    def create_robotdocs(self):
        self._create_robotdocs()
        self._generate_robotdocs_rst_if_config()

    def _create_robotdocs(self):

        for library, args in self.robotdocsconfig.items():
            self.run(
                'python'
                ' -m robot.libdoc'
                ' -f html'
                ' -F {docformat}'
                ' {library}{args}'
                ' {librarypath}.html'.format(
                    docformat=self._get_docformat(args),
                    library=library,
                    args=self._get_flattened_args(args),
                    librarypath=os.path.join('robotdocs',
                                             os.path.basename(library))))

    @property
    def robotdocsconfig(self):
        if self._robotdocsconfig is None:
            self._initialize_robotdocs_config()
        return self._robotdocsconfig

    def _get_robot_lib_keywords(self, library_name, args):
        keyword_list = self.run(
            'python -m robot.libdoc {library}{args} list'.format(
                library=library_name,
                args=self._get_flattened_args(args))).stdout
        keyword_list = keyword_list.decode('ascii') if \
            isinstance(keyword_list, bytes) else keyword_list
        return keyword_list.splitlines()

    @staticmethod
    def _get_docformat(args):
        try:
            return args['docformat']
        except KeyError:
            return ''

    @staticmethod
    def _get_flattened_args(args):
        try:
            flattened = format('::'.join(arg for arg in args['args']))
            return '::' + flattened if flattened else ''
        except KeyError:
            return ''

    def _initialize_robotdocs_config(self):
        self._robotdocsconfig = {}
        try:
            namespace = {}
            utils.execfile(os.path.join(self.robotdocs_folder,
                                        'robotdocsconf.py'),
                           namespace)
            try:
                self.module_name = namespace["module_name"]
            except KeyError:
                self.module_name = 'Robot Framework Test Libraries'
            try:
                self.output_file = namespace["output_file"]
            except KeyError:
                self.output_file = "robotdocs.rst"
            self._robotdocsconfig = namespace['robotdocs']
        except IOError:
            pass

    def _create_sphinxdocs(self):
        if os.path.isdir('sphinxdocs'):
            self._generate_robotdocs_rst_if_config()
            self._fail_if_got_robotdocs_but_not_found_in_sphinxdocsconf()
            self.run('sphinx-build -b html sphinxdocs build_dir')

    def _fail_if_got_robotdocs_but_not_found_in_sphinxdocsconf(self):
        if not self.robotdocsconfig:
            return
        robotdocdir = os.path.join(os.pardir, 'robotdocs')
        if (('html_extra_path' not in self.sphinxdocsconfig) or
                (robotdocdir not in self.sphinxdocsconfig['html_extra_path'])):
            msg = "Incorrect configuration found in {sphinx_conf}: " \
                  "'{robotdoc_relpath}' should be listed " \
                  "in 'html_extra_path'," \
                  " otherwise robot library documentation won't be packaged."
            msg = msg.format(sphinx_conf=os.path.join('sphinxdocs', 'conf.py'),
                             robotdoc_relpath=robotdocdir)
            raise FailedToCreateDocs(msg)

    def _generate_robotdocs_rst_if_config(self):
        if self.robotdocsconfig:
            self._generate_robotdocs_rst()

    def _generate_robotdocs_rst(self):
        if not self.output_file:
            self.output_file = "robotdocs.rst"
        with open(os.path.join('sphinxdocs',
                               self.output_file), 'w') as f:
            self._write_robotdocs_rst_header(f)
            f.write('\n\n'.join(
                self._get_robotdocs_rst_library_lines(library, args)
                for library, args in sorted(
                    self.robotdocsconfig.items())
            ))

    def _write_robotdocs_rst_header(self, filehandle):
        filehandle.write('.. Generated by crl.devutils\n\n' +
                         '{}\n{}\n\n'.format(
                             self.module_name, '=' * len(
                                 self.module_name)))

    def _get_robotdocs_rst_library_lines(self, library, args):
        return (
            '{index_spec}'
            '{link_spec}'
            '{kwd_list}').format(
                index_spec=self._get_robotdocs_library_index_spec(library),
                link_spec=self._get_robotdocs_library_link(library, args),
                kwd_list=self._get_robotdocs_library_keywords_list(
                    library, args))

    @staticmethod
    def _get_robotdocs_library_index_spec(library):
        return (
            '.. index::\n'
            '   single: Robot Framework Library; {library}\n\n'
        ).format(library=library)

    def _get_robotdocs_library_link(self, library, args):
        return '* `{library} <{libraryhtml}>`_{synopsis}\n\n'.format(
            library=library,
            synopsis=self._get_synopsis(args),
            libraryhtml='{}.html'.format(os.path.basename(library)))

    def _get_robotdocs_library_keywords_list(self, library, args):
        keyword_list = self._get_robot_lib_keywords(library, args)
        keywords_line = ', '.join(
            ['`{kwd} <{library}.html#{kwd_url_coded}>`__'.format(
                kwd=kwd, library=os.path.basename(library),
                kwd_url_coded=kwd.replace(' ', '%20')
            ) for kwd in keyword_list]
        )
        return '   Keywords: {keywords_line}'.format(
            keywords_line=keywords_line)

    @staticmethod
    def _get_synopsis(args):
        try:
            return ' - {synopsis}'.format(
                synopsis=args['synopsis'])
        except KeyError:
            return ''
