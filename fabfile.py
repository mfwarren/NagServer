# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

from fabric.api import sudo, run, env, hide, cd, task, put, local
from fabric.contrib.files import append
from fabric.utils import puts
from fabric.colors import red, green

project = "NagServer"
REPO = 'https://github.com/mfwarren/NagServer.git'

# the user to use for the remote commands
env.user = 'root'
env.password = ''
# the servers where the commands are executed
env.hosts = ['192.168.1.80']


def clone_project():
    run('mkdir /var/www/')
    with cd('/var/www/'):
        run('git clone %s' % REPO)

def pull_project():
    with cd('/var/www/%s' % project):
        run('git pull')

def initialize_python3():
    """
    Compile from source takes a while
    """
    local('curl -O https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz')
    put('Python-3.4.2.tgz')
    run('tar zxvf Python-3.4.2.tgz')
    with cd('Python-3.4.2'):
        run('./configure;make;make install')

@task
def prepare_server():
    initialize_python3()
    clone_project()


@task
def deploy():
    """
    Install everything
    """
    puts(green("Starting deploy"))
    create_remote_git
