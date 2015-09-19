import sys


class ValidationError(BaseException):
    def __init__(self, msg, originator):
        self.message = '''{0} failed validation with the following reason: {1}
        '''.format(originator, msg)


class Project(object):
    def __init__(self, name, type_p, license, author,
                 email, vcs=None, **kwargs):
        self.name = name
        self.type = type_p
        self.license = license
        self.author = author
        self.email = email
        self.vcs = vcs if vcs != '' else None
        self.additional = kwargs if len(kwargs.keys()) > 0 else None


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


def main():
    print(validate_template(sys.argv[1]))
    return exit()


if __name__ == '__main__':
    main()
