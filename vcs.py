'''
    vcs
    ===

    Track/untrack distribution files.
'''

__version__ = '0.1.0'

import argparse
import errno
import os
import shutil
import subprocess
import sys

home = os.path.dirname(os.path.realpath(__file__))

# Based off of:
#   https://github.com/github/gitignore/blob/main/Python.gitignore
PYTHON_GITIGNORE = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
'''

# Based off of:
#   https://github.com/github/gitignore/blob/main/C%2B%2B.gitignore
CPP_GITIGNORE = '''
# Prerequisites
*.d

# Compiled Object files
*.slo
*.lo
*.o
*.obj

# Precompiled Headers
*.gch
*.pch

# Compiled Dynamic libraries
*.so
*.dylib
*.dll

# Fortran module files
*.mod
*.smod

# Compiled Static libraries
*.lai
*.la
*.a
*.lib

# Executables
*.exe
*.out
*.app
'''

EXTRAS_GITIGNORE = [
    # Comments
    '# NOTE: this file is auto-generated via `git.py`',
    '# DO NOT MANUALLY EDIT THIS FILE.',
    # extra entries
    'TODO.md',
]


def parse_args(argv=None):
    '''Parse the command-line options.'''

    parser = argparse.ArgumentParser(description='Git configuration changes.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    dist = parser.add_mutually_exclusive_group()
    dist.add_argument(
        '--track-dist',
        help='track changes to distribution files',
        action='store_true',
    )
    dist.add_argument(
        '--no-track-dist',
        help='do not track changes to distribution files',
        action='store_true',
    )
    gitignore = parser.add_mutually_exclusive_group()
    gitignore.add_argument(
        '--track-gitignore',
        help='track changes to `.gitignore`',
        action='store_true',
    )
    gitignore.add_argument(
        '--no-track-gitignore',
        help='do not track changes to `.gitignore`',
        action='store_true',
    )

    return parser.parse_args(argv)


def call(command, ignore_errors=True):
    '''Call subprocess command (ignoring output but checking code).'''

    try:
        return subprocess.check_output(
            command,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            shell=False,
        )
    except subprocess.CalledProcessError as error:
        if b'Unable to mark file' not in error.stderr or not ignore_errors:
            raise


def assume_unchanged(git, file):
    '''Assume a version-controlled file is unchanged.'''

    return call([
        git,
        'update-index',
        '--assume-unchanged',
        file,
    ])


def no_assume_unchanged(git, file):
    '''No longer assume a version-controlled file is unchanged.'''

    return call([
        git,
        'update-index',
        '--no-assume-unchanged',
        file,
    ])


def write_gitignore(entries):
    '''Write to ignore ignore file using the provided entries.'''

    with open(os.path.join(home, '.gitignore'), 'w') as file:
        file.write(f'{"\n".join(entries)}\n{PYTHON_GITIGNORE}\n{CPP_GITIGNORE}\n')


def main(argv=None):
    '''Configuration entry point'''

    # Validate and parse our arguments.
    if len(sys.argv) == 1:
        raise ValueError('Must provide at least one command.')
    args = parse_args(argv)

    # Must be in the project home, or git won't work.
    os.chdir(home)

    # Find our git executable. Go to the in case on
    # Windows `.py` is added to valid suffixes so
    # we don't recursively call this file.
    git = shutil.which('git')
    if git is None:
        raise FileNotFoundError(errno.ENOENT, "No such file or directory: 'git'")

    # Determine if we need to assume unchanged gitignore,
    # and then update our track dist. This is since normally
    # we assume tracking/untracking dist should ignore
    # our gitignore file.
    if args.track_gitignore:
        no_assume_unchanged(git, '.gitignore')
    else:
        assume_unchanged(git, '.gitignore')

    # Determine if we need to update our gitignore.
    update_keys = ['track_dist', 'no_track_dist']
    update_gitignore = any(getattr(args, i) for i in update_keys)
    if not update_gitignore:
        return 0

    # Update our gitignore entries, and write to file.
    gitignore_entries = list(EXTRAS_GITIGNORE)
    if args.no_track_dist:
        gitignore_entries += ['dist/', 'resources/']
    write_gitignore(gitignore_entries)

    # Manage any distribution file extras here.
    def update_dist_index(file):
        '''Update the index of a file'''

        exists = os.path.exists(f'{home}/{file}')
        if args.no_track_dist and exists:
            assume_unchanged(git, file)
        elif args.track_dist and exists:
            no_assume_unchanged(git, file)

    dist_files = []
    dist_dirs = [f'{home}/dist', f'{home}/resources']
    for dist_dir in dist_dirs:
        for root, dirs, files in os.walk(dist_dir):
            relpath = os.path.relpath(root, home)
            for file in files:
                dist_files.append(f'{relpath}/{file}')
    for file in dist_files:
        update_dist_index(file)

    return 0


if __name__ == '__main__':
    sys.exit(main())
