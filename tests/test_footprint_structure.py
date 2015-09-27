import os
import pytest


EXPECTED_FILES_PYTHON = ('__init__.py', 'README.md', 'LICENSE')

# Footprints folders
footprints_folder = 'footprints'
footprints_folder_python = os.path.join(footprints_folder, 'python')
footprints_python = os.listdir(footprints_folder_python)


@pytest.mark.parametrize('footprint', footprints_python)
def test_essential_files(footprint):
    ''' Test essential files

        Checks that essential files are present in the footprint files

        :param footprint: py.test fixture to parametrize the name of the
                          footprints in the given folder

        :author: Jean Cruypenynck
        :contact: filaton@me.com
    '''
    with open(os.path.join(footprints_folder_python, footprint)) as fp:
        lines = fp.read().splitlines()

    issues = []
    for exp_file in EXPECTED_FILES_PYTHON:
        if lines.count(exp_file) != 1:
            msg = 'The file {0} was expected 1 time but was found {1} times'\
                   .format(exp_file, lines.count(exp_file))
            issues.append(msg)

    assert len(issues) == 0, '\n'.join(issues)


def test_folders_only():
    ''' Test folders only

        Checks that the root footprints folder contains only folders, each one
        corresponding to a programming language

        :author: Jean Cruypenynck
        :contact: filaton@me.com
    '''
    root_dir_content = os.listdir(footprints_folder)

    for item in root_dir_content:
        item_path = os.path.join(footprints_folder, item)
        assert os.path.isfile(item_path) is False, 'A file was found in the \
            root footprints folder. Only folders should be there.'
