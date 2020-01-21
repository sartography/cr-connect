import os
import subprocess
from invoke import task, Collection


def is_linux():
    uname_output = subprocess.Popen(["uname", "-a"],
                                    stdout=subprocess.PIPE).communicate()[0]
    if uname_output.decode('utf-8').startswith('Linux'):
        return True
    return False


@task
def stopenv(c):
    """stop the constellation"""
    c.run('docker-compose down')


@task(stopenv)
def clean(c):
    """clean up the repo (NOTE: stops constellation)"""
    if is_linux():
        # _print("*** FIXING PERMISSIONS ***")  # pylint: disable=E1601
        dir_basename = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        c.run(f'sudo chown -R {os.geteuid()}.{os.getegid()} ../{dir_basename}')
    # _print("*** CLEANING UP REPO ***")  # pylint: disable=E1601
    c.run('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')


@task
def prune_docker(c):
    """reclaim space from docker (run often)"""
    c.run('docker system prune -f --volumes')


@task()
def startenv(c):
    """start the constellation"""
    c.run('docker-compose up')


@task(stopenv, startenv)
def restartenv(c):
    pass


@task(clean, help={'name': 'only build for supplied container name'})
def buildenv(c, name=None):
    """build new constellation containers"""
    cmd = 'docker-compose build'
    c.run('{cmd} name' if name else cmd)


@task
def showenv(c):
    """show running constellation containers"""
    c.run('docker-compose ps')


@task
def shell(c):
    """start a shell"""
    os.system('docker-compose run workflow bash')


@task
def dbshell(c):
    """start a dbshell"""
    os.system('docker-compose run workflow psql -h db -U postgres postgres')


@task(help={'filename': 'path to the file containing the test module',
            'substring': 'only run tests that contain the supplied substring'})
def run_tests(c, filename=None, substring=None):
    """run the test suite"""
    env_opts = ''
    dcrun = f'docker-compose run {env_opts} workflow'
    cmd = f'{dcrun} pipenv run py.test -rf'
    if substring:
        cmd += f' -k {substring}'
    if filename:
        cmd += f' {filename}'
    print('RUNNING PYTEST: {}\n'.format(cmd))
    c.run(cmd)


@task
def list_branches(c):
    """list branches in order of last commit"""
    c.run('git branch --sort=committerdate')


@task
def prune_git_branches(c):
    """Clean up outdated references"""
    c.run('git remote prune origin')


@task
def list_git_references(c):
    """List git references"""
    c.run('git branch -r')


# repo maintenance and info
ns_repo = Collection('repo')
ns_repo.add_task(clean)
ns_repo.add_task(list_git_references, 'git-references')
ns_repo.add_task(prune_git_branches, 'git-prune')
ns_repo.add_task(list_branches, 'branches')

# dev constellation admin
ns_dev = Collection('dev')
ns_dev.add_task(startenv, 'start')
ns_dev.add_task(stopenv, 'stop')
ns_dev.add_task(restartenv, 'restart')
ns_dev.add_task(buildenv, 'build')
ns_dev.add_task(showenv, 'show')

# docker maintenance
ns_docker = Collection('docker')
ns_docker.add_task(prune_docker, 'clean')
ns_dev.add_collection(ns_docker)

# crc workflow tasks
ns_workflow = Collection('workflow')
ns_workflow.add_task(shell)
ns_workflow.add_task(run_tests, 'test')
ns_dev.add_collection(ns_workflow)

# database tasks
ns_database = Collection('database')
ns_database.add_task(dbshell, 'shell')
ns_dev.add_collection(ns_database)

# put dev in env namespace
ns_env = Collection('env')
ns_env.add_collection(ns_dev)

# add namespaces to root collection
ns = Collection()
ns.add_collection(ns_repo)
ns.add_collection(ns_env)

