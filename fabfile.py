from fabric.api import local, settings, abort, run, cd, env, prefix
from fabric.contrib.console import confirm
from contextlib import contextmanager
from datetime import datetime

env.hosts = ['root@verbalite.com']


# CONTEXT MANAGERS #

@contextmanager
def project_home():
    with cd("~/mimicme"):
        yield

@contextmanager
def virtualenv():
    with project_home():
        with prefix("workon mimicme"):
            yield

# GIT HELPERS #

def remote_latest_commit():
    with project_home(): 
        run("git log HEAD^..HEAD")

def remote_pull():
    with project_home():
        run("git pull")


# DJANGO HELPERS #

def remote_syncdb():
    with virtualenv():
        run("./manage.py syncdb")

def remote_collectstatic():
    with virtualenv():
        run("./manage.py collectstatic --noinput")


# DEPLOY HELPERS #

def remote_reload_django():
    run("ps ux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -HUP")


# BACKUPS #

def now_filename_str():
    return datetime.now().strftime("%Y-%m-%d-%H.%M.%S")

#def backup_everything():
#    run("mkdir -p ~/backups")
#    with virtualenv():
#        filename = "~/backups/prepfly-all-%s.json" % now_filename_str()
#        run("./manage.py dumpdata > %s" % filename)


def get_uploads():
    local("rm uploadedmedia/*")
    local("scp root@verbalite.com:~/mimicme/uploadedmedia/* uploadedmedia/")
    with virtualenv():
        run("./manage.py dumpdata > ~/temp/dump.json")
    local("scp root@verbalite.com:~/temp/dump.json ~/temp/dump.json")
    local("./manage.py loaddata ~/temp/dump.json")


# SCRIPTS #

def remote_redeploy():
    remote_pull()
    remote_collectstatic()
    remote_syncdb()
    remote_reload_django()

