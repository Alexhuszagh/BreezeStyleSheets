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

GITIGNORE_ENTRIES = [
    # Comments
    '# NOTE: this file is auto-generated via `git.py`',
    '# DO NOT MANUALLY EDIT THIS FILE.',
    # Ignore all compiled bytecode.
    '__pycache__',
    '*.pyc',
    # Ignore all resource files except `breeze.qrc`.
    '*.qrc',
    '!breeze.qrc'
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


def call(command):
    '''Call subprocess command (ignoring output but checking code).'''

    return subprocess.check_call(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
    )


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
        file.write('\n'.join(entries) + '\n')


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
    gitignore_entries = list(GITIGNORE_ENTRIES)
    if args.no_track_dist:
        gitignore_entries += ['dist/', 'breeze_resources.py']
    write_gitignore(gitignore_entries)

    # Manage any distribution file extras here.
    def update_dist_index(file):
        '''Update the index of a file'''

        exists = os.path.exists(f'{home}/{file}')
        if args.no_track_dist and exists:
            assume_unchanged(git, file)
        elif args.track_dist and exists:
            no_assume_unchanged(git, file)

    dist_files = ['breeze_resources.py']
    for root, dirs, files in os.walk(f'{home}/dist'):
        relpath = os.path.relpath(root, home)
        for file in files:
            dist_files.append(f'{relpath}/{file}')
    for file in dist_files:
        update_dist_index(file)

    return 0

if __name__ == '__main__':
    sys.exit(main())
