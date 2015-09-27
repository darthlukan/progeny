import os
import sys
import argparse
import requests
import platform
import subprocess
if int(platform.python_version_tuple()[0]) == 3:
    import configparser
else:
    import ConfigParser as configparser


def _open_config_file(HOME):
    config = configparser.SafeConfigParser()

    try:
        f = open('{0}/.config/progeny/progenyrc'.format(HOME))
        config.readfp(f)
        print('Have config first try')
    except (IOError, configparser.ParsingError):
        print('Caught IOError')
        try:
            f = open('{0}/.progenyrc'.format(HOME))
            config.readfp(f)
            print('Have config second try')
        except (IOError, configparser.ParsingError):
            print('Config is None')
            config = None
    print(config.sections())
    return config


__HOME = os.getenv('HOME')
__config = _open_config_file(__HOME)
print('config: {0}'.format(__config.items('Project Defaults')))
_required = ['name', 'language', 'parent']
_error_conditions = [None, '', 0]
_license_urls = {
    'gpl2': 'http://www.gnu.org/licenses/gpl-2.0.txt',
    'gpl3': 'http://www.gnu.org/licenses/gpl-3.0.txt',
    'agpl3': 'http://www.gnu.org/licenses/agpl-3.0.txt',
    'lgpl2': 'http://www.gnu.org/licenses/lgpl-2.1.txt',
    'lgpl3': 'http://www.gnu.org/licenses/lgpl-2.1.txt',
    'wtfpl': 'http://www.wtfpl.net/txt/copying/'
}
_footprints_lookup_dirs = {
    'default': '/usr/share/progeny/footprints',
    'alternate': '{0}/.config/progeny/footprints'.format(__HOME),
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


class ValidationError(BaseException):
    def __init__(self, msg, originator):
        self.message = '''{0} failed validation with the following reason: {1}
        '''.format(originator, msg)


class Project(object):
    def __init__(self, name, language, parent, footprint=None, config=None,
                 ptype=None, author=None, email=None, license=None, vcs=None):

        self.name = name
        print('config: {0}'.format(config))

        # TODO: This should really be in the validators....
        if config:
            if config.has_section('Project Defaults'):
                if config.has_option('Project Defaults', 'type'):
                    self.ptype = config.get('Project Defaults', 'type')
                if config.has_option('Project Defaults', 'license'):
                    self.license = config.get('Project Defaults', 'license')
                if config.has_option('Project Defaults', 'language'):
                    self.language = config.get('Project Defaults', 'language')
                if config.has_option('Project Defaults', 'author'):
                    self.author = config.get('Project Defaults', 'author')
                if config.has_option('Project Defaults', 'email'):
                    self.email = config.get('Project Defaults', 'email')
                if config.has_option('Project Defaults', 'vcs'):
                    self.vcs = config.get('Project Defaults', 'vcs')
            if config.has_section('Paths'):
                if config.has_option('Paths', 'parent'):
                    self.parent = config.get('Paths', 'parent')
                if config.has_option('Paths', 'footprints'):
                    self._footprints_path = config.get('Paths', 'footprints')
                else:
                    self._footprints_path = None

        self.ptype = ptype
        self.license = license
        self.language = language
        self.parent = parent
        self.author = author
        self.email = email
        self.vcs = vcs

        self._app_base = '{0}/{1}'.format(self.parent, self.name)
        self._footprint = footprint
        self._errors = []

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
        # TODO: Is this the best way? Probably not. Profile string append
        # versus template string -> replace to see which is fastest.
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
            readme = open('{0}/README.md'.format(self._app_base), 'w')
            readme.write(readme_string)
            readme.close()
            return True
        except IOError as e:
            self._errors.append(e)

        return False

    def _license_gen(self):
        print('License: "{0}"'.format(self.license))
        if self.license in _license_urls:
            resp = requests.get(_license_urls[self.license])
            if resp.status_code == 200:
                try:
                    license = open('{0}/LICENSE'.format(self._app_base), 'w')
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
                    '{0}/{1}/{2}'.format(paths[i], self.language, self.ptype)))
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
            path = '{0}/{1}'.format(self._app_base, line)
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


def _check_footprint_required(args, footprint=None):
    if footprint is not None:
        for req in _required:
            if not args.__contains__(req):
                raise ValidationError(
                    'Missing required arg \'{0}\''.format(req), req)

        name = args.name
        # TODO: Language and Parent should honor config if present
        language = args.language
        parent = args.parent
        return Project(name, language, parent, footprint=footprint,
                       config=__config)
    return None


def validate_args(args):
    from pprint import pprint
    pprint(args)
    if args.footprint and args.footprint not in _error_conditions:
        footprint = open_file(args.footprint)
        if footprint is not None:
            return _check_footprint_required(args, footprint=footprint)
        return None

    try:
        name = args.name
        language = args.language
        parent = args.parent
        ptype = args.ptype
    except AttributeError:
        raise RuntimeError('''Progeny requires name, language, parent, and
                              ptype arguments at a minimum if no footprint is
                           supplied via the command line. You provided: {0}
                           '''.format(args))

    license = args.license
    author = args.author
    email = args.email
    vcs = args.vcs

    return Project(name=name, language=language, parent=parent, config=__config,
                   footprint=None, ptype=ptype, license=license, author=author,
                   email=email, vcs=vcs)


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
    project = validate_args(args)
    if project:
        project_state = project.generate()
        print(project_state)
        print(project._errors)
        if project_state:
            print('clean exit')
            return exit(0)
    return exit(1)


if __name__ == '__main__':
    main()
