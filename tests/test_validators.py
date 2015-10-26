import argparse
from .. import validators


parser = argparse.ArgumentParser()
good_args = parser.parse_args()
good_args.parent = 'parent'
good_args.name = 'name'
good_args.footprint = 'footprint'
good_args.language = 'lang'
good_args.type = 'type'

bad_args = parser.parse_args()
bad_args.name = 'name'
bad_args.parent = 'parent'


def test_load_args():
    good = validators.load_args(good_args)
    assert 'name' in good and good['name'] == good_args.name
    assert 'parent' in good and good['parent'] == good_args.parent
    assert 'footprint' in good and good['footprint'] == good_args.footprint
    assert 'language' in good and good['language'] == good_args.language
    assert 'type' in good and good['type'] == good_args.type

    bad = validators.load_args(bad_args)
    assert 'name' in bad and bad['name'] == bad_args.name
    assert 'parent' in bad and bad['parent'] == bad_args.parent
    assert 'footprint' in bad and bad['footprint'] is None


def test_solo_args_requires():
    args = validators.load_args(good_args)
    good = validators.solo_args_requires(args)
    assert good is True

    args = validators.load_args(bad_args)
    bad = validators.solo_args_requires(args)
    assert bad is False


def test_footprint_requires():
    parser = argparse.ArgumentParser()
    good_args = parser.parse_args()
    good_args.name = 'name'
    good_args.parent = 'parent'
    gooder_args = validators.load_args(good_args)
    good = validators.footprint_requires(gooder_args)
    assert good is True

    bad_args = parser.parse_args()
    bad_args.name = 'name'
    badder_args = validators.load_args(bad_args)
    bad = validators.footprint_requires(badder_args)
    assert bad is False

