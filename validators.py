PROJECT_DEFAULTS = 'Project Defaults'
PATHS = 'Paths'

_from_config = {
    'author': None,
    'email': None,
    'license': None,
    'language': None,
    'type': None,
    'parent': None,
    'vcs': None,
    'footprints': None
}

_from_args = {
    'name': None,
    'author': None,
    'email': None,
    'license': None,
    'language': None,
    'type': None,
    'parent': None,
    'vcs': None,
    'footprint': None
}


def load_args(args):
    from_args = _from_args.copy()
    keys = _from_args.keys()
    for key in keys:
        if args.__contains__(key):
            from_args[key] = args.__getattribute__(key)
    return from_args


def load_config(config):
    from_config = _from_config.copy()
    keys = _from_config.keys()
    if config:
        if config.has_section(PROJECT_DEFAULTS):
            for key in keys:
                if config.has_option(PROJECT_DEFAULTS, key):
                    from_config[key] = config.get(PROJECT_DEFAULTS, key)
        if config.has_section(PATHS):
            for key in keys:
                if config.has_option(PATHS, key):
                    from_config[key] = config.get(PATHS, key)
    return from_config


def merge_configged_argged(configged, argged):
    merged = configged.copy()
    for key in argged.keys():
        if True in [key == k for k in configged.keys()]:
            # We only care about a None val if the key exists in configged
            # this will overwrite the config so that args take percedence
            if argged[key] is not None:
                merged[key] = argged[key]
        else:
            # If the key is not already here, then it must be 'footprint', in
            # which case we definitely want to include it since that is our
            # highest priority and requires less args to generate a project
            merged[key] = argged[key]

    return merged


def footprint_requires(merged):
    required = ['name', 'parent']
    passed = 0
    pass_requires = len(required)
    for r in required:
        if r in merged.keys():
            if merged[r] is not None:
                passed += 1
    return passed == pass_requires


def solo_args_requires(args):
    required = ['name', 'parent', 'language', 'type']
    passed = 0
    pass_requires = len(required)
    for r in required:
        if r in args.keys():
            if args[r] is not None:
                passed += 1
    return passed == pass_requires


def validate_args(args, config):
    if config is not None:
        configged = load_config(config)
        argged = load_args(args)
        merged = merge_configged_argged(configged, argged)
        # If footprint is provided, we only need name and parent
        if merged['footprint'] is not None:
            return footprint_requires(merged), merged
        # If no footprint, we need name, parent, language, and type to perform
        # footprint lookups
        if None not in [merged['name'], merged['parent'], merged['language'],
                        merged['type']]:
            return True, merged
        return False, merged

    argged = load_args(args)
    return solo_args_requires(argged), argged
