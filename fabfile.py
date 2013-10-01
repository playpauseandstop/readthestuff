"""
=======
fabfile
=======

Deploy Read the Stuff to EC2.

"""

import os

from fabric import api


DEFAULT_BRANCH = 'master'
REPO = 'git://github.com/playpauseandstop/readthestuff.git'
PROJECT_DIR = '/home/ubuntu/projects/readthestuff'
api.env.use_ssh_config = True


def bootstrap():
    """
    Bootstrap project on remote server.
    """
    with api.cd(PROJECT_DIR):
        api.run('make bootstrap')


def deploy(branch=None):
    """
    Run full deploy process.
    """
    init()
    pull(branch)
    bootstrap()
    restart('readthestuff')
    restart('nginx')


def init():
    """
    Initialize project dir on remote host if necessary.
    """
    parent = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

    api.run('[ ! -d "{0}" ] && mkdir "{0}" || :'.format(PROJECT_DIR))
    api.run('[ ! -d "{0}" ] && git clone {1} "{0}" || :'.
            format(PROJECT_DIR, REPO))

    with api.cd(PROJECT_DIR):
        api.run('make initdb')


def pull(branch=None):
    """
    Pull updates from Git branch.
    """
    branch = branch or DEFAULT_BRANCH

    with api.cd(PROJECT_DIR):
        with api.settings(warn_only=True):
            status_code = api.run('git status | grep "On branch {0}"'.
                                  format(branch))

        if status_code:
            api.run('git pull')
            api.run('git fetch origin {0}'.format(branch))

        api.run('git pull origin {0}'.format(branch))


def restart(service):
    """
    Restart remote services.
    """
    api.sudo('service {0} restart'.format(service))
