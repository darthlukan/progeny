import sys
import argparse


class ValidationError(BaseException):
    def __init__(self, msg, originator):
        self.message = '''{0} failed validation with the following reason: {1}
        '''.format(originator, msg)


class Project(object):
    def __init__(self, name, language, type, author, email,
                 license, vcs, **kwargs):
        self.name = name
        self.type = type
        self.license = license
        self.language = language
        self.author = author
        self.email = email
        self.vcs = vcs
        self.additional = kwargs if len(kwargs.keys()) > 0 else None

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode('<Project {0}>'.format(self.name))

    def generate(self):
        return


exit_states = {
    'clean': 0,
    'error': 1
}


def exit(status=None):
    if status is not None:
        state = exit_states['error']
    else:
        state = exit_states['clean']

    return sys.exit(state)


def open_file(path):
    try:
        return open(path)
    except IOError as e:
        return e.message


def validate_template(template):
    tmpl = open_file(template)
    if isinstance(tmpl, str):
        raise ValidationError(tmpl, template)

    pre_proj = {}
    for line in tmpl:
        l = line.split('=')
        key = l[0].strip().lower()
        val = l[1].strip().lower()
        pre_proj[key] = val

    try:
        project = Project(
            name=pre_proj['name'], type_p=pre_proj['type'],
            license=pre_proj['license'], author=pre_proj['author'],
            email=pre_proj['email'], vcs=pre_proj['vcs'])
    except (KeyError, AttributeError) as e:
        raise ValidationError(e.message, template)

    attrs = ['name', 'type', 'license', 'author', 'email']
    for attr in attrs:
        a = project.__getattribute__(attr)
        if a is None or a == '':
            raise ValidationError('missing required attribute {0}!'.format(
                attr), template)

    return project


def validate_args(args):
    if args.template and args.template[0] != '':
        return validate_template(args._template[0])
    return args


def main():
    parser = argparse.ArgumentParser(
        description='''Generate project directory structures based on templates
        or supplied args.''')
    parser.add_argument('-n', '--name', nargs=1, type=str, action='store',
                        dest='name', help='Your app\'s/project\'s name.')
    parser.add_argument('-a', '--author', nargs=1, type=str, action='store',
                        dest='author', help='Your name.')
    parser.add_argument('-e', '--email', nargs=1, type=str, action='store',
                        dest='email', help='Your email address.')
    parser.add_argument('-l', '--license', nargs=1, type=str, action='store',
                        dest='license', help='License shortname e.g. gpl2.')
    parser.add_argument('-lang', '--language', nargs=1, type=str,
                        action='store', dest='language',
                        help='The project language.')
    parser.add_argument('-t', '--type', nargs=1, type=str, action='store',
                        dest='type', help='The type of project e.g. cli, web.')
    parser.add_argument('-vcs', '--version-control-system', nargs=1, type=str,
                        action='store', dest='vcs', help='Version Control')
    parser.add_argument('-p', '--parent-dir', nargs=1, type=str,
                        action='store', dest='parent',
                        help='The parent directory e.g. ~/projects.')
    parser.add_argument('-f', '--template-file', nargs=1, type=str,
                        action='store', dest='template',
                        help='Generate project based on template file.')

    args = parser.parse_args()
    print(validate_args(args))
    return exit()


if __name__ == '__main__':
    main()
