import sys
import argparse
import subprocess


_required = ['name', 'language', 'parent']
_error_conditions = [None, '', 0]
exit_states = {
    'clean': 0,
    'error': 1
}


class ValidationError(BaseException):
    def __init__(self, msg, originator):
        self.message = '''{0} failed validation with the following reason: {1}
        '''.format(originator, msg)


def exit(status=None):
    if status not in _error_conditions:
        state = exit_states['error']
    else:
        state = exit_states['clean']

    return sys.exit(state)


def open_file(path):
    try:
        return open(path)
    except IOError as e:
        return e.message


class Project(object):
    def __init__(self, name, language, parent,
                 type=None, author=None, email=None, license=None, vcs=None):
        self.name = name
        self.type = type if type is not None else 'cli'
        self.license = license
        self.language = language
        self.parent = parent
        self.author = author
        self.email = email
        self.vcs = vcs
        self._app_base = '{0}/{1}'.format(self.parent, self.name)
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

    def generate(self):
        errors = []
        try:
            footprint = open_file(
                'footprints/{0}/{1}'.format(self.language, self.type))
        except IOError as e:
            print(e.message)
            return exit(1)

        success = self._mkdir(self._app_base)
        if not success:
            raise self._errors[-1]

        for line in footprint:
            if line.endswith('/'):
                dpath = '{0}/{1}'.format(self._app_base, line.strip('\n'))
                dsuccess = self._mkdir(dpath)
                if not dsuccess:
                    raise self._errors[-1]
            else:
                fpath = '{0}/{1}'.format(self._app_base, line.strip('\n'))
                fsuccess = self._touch(fpath)
                if not fsuccess:
                    raise self._errors[-1]
        print(errors)
        return True


def validate_template(template):
    tmpl = open_file(template)
    if isinstance(tmpl, str):
        raise ValidationError(tmpl, template)

    pre_proj = {}
    for line in tmpl:
        l = line.split('=')
        key = l[0].strip().lower()
        val = l[1].strip().lower()
        if key in _required and val in _error_conditions:
            raise ValidationError(
                'Missing required attribute {0}'.format(key), template)
        pre_proj[key] = val

    name = pre_proj['name']
    language = pre_proj['language']
    parent = pre_proj['parent']

    # TODO: No, seriously, figure out a better way than this.
    try:
        type = pre_proj['type']
    except KeyError:
        type = None

    try:
        license = pre_proj['license']
    except KeyError:
        license = None

    try:
        vcs = pre_proj['vcs']
    except KeyError:
        vcs = None

    try:
        author = pre_proj['author']
    except KeyError:
        author = None

    try:
        email = pre_proj['email']
    except KeyError:
        email = None

    project = Project(name, language, parent, type, author, email, license, vcs)
    return project


def validate_args(args):
    print(args)
    print(args.name)
    if args.template and args.template not in _error_conditions:
        return validate_template(args.template)

    for req in _required:
        if not args.__contains__(req):
            raise ValidationError(
                'Missing required arg \'{0}\''.format(req), req)

    name = args.name
    language = args.language
    parent = args.parent

    # TODO: Make a loop out of this (DRY)
    try:
        type = args.type
    except (AttributeError, IndexError):
        type = None

    try:
        license = args.license
    except (AttributeError, IndexError):
        license = None

    try:
        vcs = args.vcs
    except (AttributeError, IndexError):
        vcs = None

    try:
        author = args.author
    except (AttributeError, IndexError):
        author = None

    try:
        email = args.email
    except (AttributeError, IndexError):
        email = None

    project = Project(name, language, parent, type, author, email, license, vcs)
    return project


def main():
    parser = argparse.ArgumentParser(
        description='''Generate project directory structures based on templates
        or supplied args.''')
    parser.add_argument('-n', '--name', type=str, action='store', dest='name',
                        help='Your app\'s/project\'s name.')
    parser.add_argument('-a', '--author', type=str, action='store',
                        dest='author', help='Your name.')
    parser.add_argument('-e', '--email', type=str, action='store', dest='email',
                        help='Your email address.')
    parser.add_argument('-l', '--license', type=str, action='store',
                        dest='license', help='License shortname e.g. gpl2.')
    parser.add_argument('-lang', '--language', type=str, action='store',
                        dest='language', help='The project language.')
    parser.add_argument('-t', '--type', type=str, action='store', dest='type',
                        help='The type of project e.g. cli, web.')
    parser.add_argument('-vcs', '--version-control-system', type=str,
                        action='store', dest='vcs', help='Version Control')
    parser.add_argument('-p', '--parent-dir', type=str, action='store',
                        dest='parent',
                        help='The parent directory e.g. ~/projects.')
    parser.add_argument('-f', '--template-file', type=str, action='store',
                        dest='template',
                        help='Generate project based on template file.')

    args = parser.parse_args()
    project = validate_args(args)
    project_state = project.generate()
    print(project._errors)
    if project_state:
        return exit(0)
    return exit(1)


if __name__ == '__main__':
    main()
