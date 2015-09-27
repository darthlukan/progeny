import os
import sys
import argparse
import requests
import platform
import subprocess

import validators


if os.name == 'nt':
    sys.exit('\nWindows not supported!\n')

if int(platform.python_version_tuple()[0]) == 3:
    import configparser
else:
    import ConfigParser as configparser


def _open_config_file(HOME):
    config = configparser.SafeConfigParser()

    try:
        f = open(os.path.join(HOME, '.config', 'progeny', 'progenyrc'))
        config.readfp(f)
    except (IOError, configparser.ParsingError):
        try:
            f = open(os.path.join(HOME, '.progenyrc'))
            config.readfp(f)
        except (IOError, configparser.ParsingError):
            config = None
    return config


__HOME = os.getenv('HOME')
__config = _open_config_file(__HOME)
_required = ['name', 'language', 'parent']
_error_conditions = [None, '', 0]
_license_urls = {
    'gpl2': 'http://www.gnu.org/licenses/gpl-2.0.txt',
    'gpl3': 'http://www.gnu.org/licenses/gpl-3.0.txt',
    'agpl3': 'http://www.gnu.org/licenses/agpl-3.0.txt',
    'lgpl2': 'http://www.gnu.org/licenses/lgpl-2.1.txt',
    'lgpl3': 'http://www.gnu.org/licenses/lgpl-2.1.txt',
    'wtfpl': 'http://www.wtfpl.net/txt/copying/',
    'mit': 'http://www.mit-license.org'
}
_footprints_lookup_dirs = {
    'default': os.path.join('usr', 'share', 'progeny', 'footprints'),
    'alternate': os.path.join(__HOME, '.config', 'progeny', 'footprints')
}
exit_states = {
    'clean': 0,
    'error': 1
}


def exit(status=None):
    if status not in _error_conditions:
        state = exit_states['error']
    else:
        state = exit_states['clean']

    return sys.exit(state)


def open_file(path, mode=None):
    try:
        if mode and isinstance(mode, str):
            return open(path, mode)
        return open(path, 'r')
    except IOError as e:
        return e.message


class Project(object):
    def __init__(self, name, language, parent, footprint=None, config=None,
                 ptype=None, author=None, email=None, license=None, vcs=None):

        self.name = name
        self.language = language
        self.parent = parent
        self.config = config
        self.ptype = ptype
        self.author = author
        self.email = email
        self.license = license
        self.vcs = vcs
        self._app_base = os.path.join(self.parent, self.name)
        self._footprint = footprint
        self._errors = []
        if self.config:
            try:
                self._footprints_path = config.get('Paths', 'footprints')
            except (AttributeError, configparser.Error) as e:
                self._errors.append(e.message)
                self._footprints_path = None
        else:
            self._footprints_path = None

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode('<Project {0}>'.format(self.name))

    def _mkdir(self, path):
        d = subprocess.Popen('mkdir -p {0}'.format(path), shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = d.communicate()
        if stderr and stderr not in _error_conditions:
            self._errors.append(OSError(stderr))
            return False
        return True

    def _touch(self, file):
        f = subprocess.Popen('touch {0}'.format(file), shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = f.communicate()
        if stderr and stderr not in _error_conditions:
            self._errors.append(OSError(stderr))
            return False
        return True

    def _readme_gen(self):
        readme_string = ''
        readme_string += '# {0}\n\n'.format(self.name)
        if self.author is not None:
            readme_string += '> {0} '.format(self.author)
            if self.email is not None:
                readme_string += '<{0}>\n\n'.format(self.email)
            else:
                readme_string += '\n\n'

        readme_string += '## Description\n\n'
        readme_string += '> Insert {0} description here.\n\n'.format(self.name)
        readme_string += '# LICENSE\n\n'
        if self.license is not None:
            readme_string += '> {0}, see LICENSE file.'.format(self.license)
        else:
            readme_string += '> Currently undecided.'

        try:
            readme = open(os.path.join(self._app_base, 'README.md'), 'w')
            readme.write(readme_string)
            readme.close()
            return True
        except IOError as e:
            self._errors.append(e)

        return False

    def _license_gen(self):
        if self.license in _license_urls:
            resp = requests.get(_license_urls[self.license])
            if resp.status_code == 200:
                try:
                    license = open(os.path.join(self._app_base, 'LICENSE'),
                                   'w')
                    license.write(resp.text)
                    license.close()
                    return True
                except IOError as e:
                    self._errors.append(e)
            self._errors.append(RuntimeWarning(
                '{0} license response not 200.'.format(self.license)))
        else:
            self._errors.append(NotImplementedError(
                'License {0} is not currently known by Progeny.'.format(
                    self.license)))

        return False

    def _footprint_check(self, footprint):
        if isinstance(footprint, str):
            return None
        return footprint

    def _find_footprint(self, language, ptype):
        paths = [self._footprints_path, _footprints_lookup_dirs['alternate'],
                 _footprints_lookup_dirs['default']]

        footprint = None
        if self._footprint is None:
            for i in xrange(0, 3):
                footprint = self._footprint_check(open_file(
                    os.path.join(paths[i], self.language, self.ptype)))
                if footprint is not None:
                    return footprint
            return None

        footprint = self._footprint_check(open_file(self._footprint))
        return footprint

    def generate(self):
        if self._footprint is None:
            footprint = self._find_footprint(self.language, self.ptype)
        elif isinstance(self._footprint, str):
            footprint = open_file(self._footprint)
        else:
            footprint = self._footprint

        if footprint is None:
            return False

        success = self._mkdir(self._app_base)
        if not success:
            raise self._errors[-1]

        for line in footprint:
            line = line.strip('\n').strip()
            path = os.path.join(self._app_base, line)
            if path.endswith('/'):
                success = self._mkdir(path)
            else:
                success = self._touch(path)

            if not success:
                    raise self._errors[-1]

        lsuccess = self._license_gen()
        if not lsuccess:
            print(self._errors[-1].message)

        rsuccess = self._readme_gen()
        if not rsuccess:
            print(self._errors[-1].message)

        return True


def validate(args):
    valid, switches = validators.validate_args(args, __config)
    if not valid:
        return None
    if 'footprint' in switches.keys():
        return Project(name=switches['name'], language=switches['language'],
                       parent=switches['parent'], config=__config,
                       footprint=switches['footprint'], ptype=switches['type'],
                       author=switches['author'], email=switches['email'],
                       license=switches['license'], vcs=switches['vcs'])

    return Project(name=switches['name'], language=switches['language'],
                   parent=switches['parent'], config=__config,
                   ptype=switches['type'], author=switches['author'],
                   email=switches['email'], license=switches['license'],
                   vcs=switches['vcs'])


def main():
    parser = argparse.ArgumentParser(
        description='''Generate project directory structures based on templates
        or supplied args.''')
    parser.add_argument('-n', '--name', type=str, action='store', dest='name',
                        help='Your app\'s/project\'s name.')
    parser.add_argument('-a', '--author', type=str, action='store',
                        dest='author', help='Your name.')
    parser.add_argument('-e', '--email', type=str, action='store',
                        dest='email', help='Your email address.')
    parser.add_argument('-l', '--license', type=str, action='store',
                        dest='license', help='License shortname e.g. gpl2.')
    parser.add_argument('-lang', '--language', type=str, action='store',
                        dest='language', help='The project language.')
    parser.add_argument('-t', '--type', type=str, action='store', dest='ptype',
                        help='The ptype of project e.g. cli, web.')
    parser.add_argument('-vcs', '--version-control-system', type=str,
                        action='store', dest='vcs', help='Version Control')
    parser.add_argument('-p', '--parent-dir', type=str, action='store',
                        dest='parent',
                        help='The parent directory e.g. ~/projects.')
    parser.add_argument('-f', '--footprint', type=str, action='store',
                        dest='footprint',
                        help='Provide a custom footprint.')

    args = parser.parse_args()
    project = validate(args)
    if project:
        project_state = project.generate()
        if project_state:
            return exit(0)
    # TODO: Error handling would help...
    print('\nErrors were encountered, please see "progeny -h"\n')
    print(parser.print_help())
    return exit(1)


if __name__ == '__main__':
    main()
