# implements a decentralized routines worker
# connects to worker pool
# broadcast heartbeat
# listen to commands

import os
import sys
import psutil
import time
import subprocess
import threading
from subprocess import DEVNULL
from threading import Thread

import pandas as pd
import numpy as np
from pathlib import Path

from SharedData.Logger import Logger


def upsert_routine(newroutine,routines):
    updated = False
    for routine in routines:
        if ('pid' in routine):
            if newroutine['pid'] == routine['pid']:
                routine.update(newroutine)
                updated = True

        elif ('repo' in newroutine) & ('repo' in routine['command']):
            if (routine['command']['repo'] == newroutine['repo']):
                if ('routine' in newroutine) & ('routine' in routine['command']):
                    if (routine['command']['routine'] == newroutine['routine']):
                        routine.update(newroutine)
                        updated = True
    if not updated:
        routines.append(newroutine)


def update_routines(routines):

    source_path = Path(os.environ['SOURCE_FOLDER'])
    if os.name == 'posix':
        python_path = 'venv/bin/python'
    else:
        python_path = 'venv/Scripts/python.exe'

    processes = []
    for processes in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            if processes.info['cmdline'] and processes.info['cmdline'][0].startswith(str(source_path)):
                proc = processes.info
                if len(proc['cmdline']) >= 2:
                    idx = np.array(proc['cmdline']) == '-m'
                    if np.any(idx):
                        i = np.argmax(idx)
                        if 'SharedData' in proc['cmdline'][i+1]:
                            routine = {}
                            routine['pid'] = proc['pid']
                            routine['process'] = psutil.Process(routine['pid'])
                            routine['command'] = {}
                            routine['command']['repo'] = 'SharedData'
                            routine['command']['routine'] = proc['cmdline'][i+1].replace('SharedData.', '')
                            if len(proc['cmdline']) >= i+3:
                                routine['command']['args'] = proc['cmdline'][i+2]
                            upsert_routine(routine,routines)
                    else:
                        idx = [str(source_path) in s for s in proc['cmdline']]
                        if np.any(idx):
                            i = np.argmax(idx)
                            for cmd in proc['cmdline'][i+1:]:
                                i=i+1
                                if str(source_path) in cmd:
                                    routinestr = cmd.replace(str(source_path), '')
                                    if routinestr.startswith(os.sep):
                                        routinestr = routinestr[1:]
                                    cmdsplit = routinestr.split(os.sep)
                                    routine = {}
                                    routine['pid'] = proc['pid']
                                    routine['process'] = psutil.Process(routine['pid'])
                                    routine['command'] = {}
                                    routine['command']['repo'] = cmdsplit[0]
                                    routine['command']['routine'] = os.sep.join(cmdsplit[1:])
                                    # if len(cmdsplit) >= i+3:
                                    #     routine['command']['args'] = cmdsplit[i+2]
                                    upsert_routine(routine,routines)
                                    break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def process_command(command,routines):

    if command['job'] == 'command':
        start_time = time.time()
        routine = {
            'command': command,
            'thread': None,
            'process': None,
            'subprocess': None,
            'start_time': start_time,
        }
        thread = Thread(target=send_command,args=(command['command'],))
        routine['thread'] = thread
        routines.append(routine)
        thread.start()

    elif command['job'] == 'install':
        if not isrunning(command,routines):
            start_time = time.time()
            routine = {
                'command': command,
                'thread': None,
                'start_time': start_time,
            }
            thread = Thread(target=install_repo,
                            args=(command, routine))
            routine['thread'] = thread
            routines.append(routine)
            thread.start()
        else:
            Logger.log.info(
                'Already installing %s!' % (str(command)))

    elif command['job'] == 'routine':
        # expects command:
        # command = {
        #     "sender" : "MASTER",
        #     "target" : user,
        #     "job" : "routine",
        #     "repo" : routine.split('/')[0],
        #     "routine" : '/'.join(routine.split('/')[1:])+'.py',
        #     "branch" : branch,
        # }
        if not isrunning(command,routines):
            start_time = time.time()
            routine = {
                'command': command,
                'thread': None,
                'process': None,
                'subprocess': None,
                'start_time': start_time,
            }
            thread = Thread(target=run_routine,
                            args=(command, routine))
            routine['thread'] = thread
            routines.append(routine)
            thread.start()
        else:
            Logger.log.info('Already running %s!' %
                            (str(command)))

    elif command['job'] == 'kill':
        kill_routine(command,routines)

    elif command['job'] == 'restart':
        kill_routine(command,routines)
        
        time.sleep(5)
        
        start_time = time.time()
        routine = {
            'command': command,
            'thread': None,
            'process': None,
            'subprocess': None,
            'start_time': start_time,
        }
        thread = Thread(target=run_routine,
                        args=(command, routine))
        routine['thread'] = thread
        routines.append(routine)
        thread.start()

    elif command['job'] == 'stop':
        # TODO: implement a stop command
        pass

    elif command['job'] == 'status':

        Logger.log.info('Status: %i process' % (len(routines)))
        n = 0
        for routine in routines:
            n += 1
            if 'repo' in routine['command']:
                statusstr = 'Status %i: running %s' % (n, routine['command']['repo'])

            if 'routine' in routine['command']:
                statusstr = '%s/%s' % (statusstr,
                                       routine['command']['routine'])
            if 'args' in routine['command']:
                statusstr = '%s/%s' % (statusstr,
                                       routine['command']['args'])
            if 'start_time' in routine:
                statusstr = '%s %.2fs' % (
                    statusstr, time.time()-routine['start_time'])
            Logger.log.info(statusstr)

    elif command['job'] == 'restart worker':
        restart_program()

    elif command['job'] == 'ping':
        Logger.log.info('pong')

    elif command['job'] == 'pong':
        Logger.log.info('ping')


installed_repos = {}


def install_repo(command, routine=None):

    install = False
    if not command['repo'] in installed_repos:
        installed_repos[command['repo']] = {}
        installed_repo = installed_repos[command['repo']]
        installed_repo['isinstalling'] = True
        installed_repo['ts'] = time.time()
        install = True
    else:
        installed_repo = installed_repos[command['repo']]
        while installed_repo['isinstalling']:
            time.sleep(1)
        installage = time.time() - installed_repo['ts']
        if installage > 300:
            install = True

    if not install:
        return True
    if install:
        installed_repo['ts'] = time.time()
        installed_repo['isinstalling'] = True

        Logger.log.info('Installing %s...' % (command['repo']))
        runroutine = False
        if ('GIT_USER' not in os.environ) | \
            ('GIT_TOKEN' not in os.environ) |\
                ('GIT_ACRONYM' not in os.environ):
            Logger.log.error('Installing repo %s ERROR missing git parameters'
                             % (command['repo']))
        else:

            hasbranch, requirements_path, repo_path, python_path, env = get_env(command)

            repo_exists = repo_path.is_dir()
            venv_exists = python_path.is_file()
            install_requirements = not python_path.is_file()

            # GIT_URL=os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_USER']+':'+os.environ['GIT_TOKEN']+'@'\
            #     +os.environ['GIT_SERVER']+'/'+os.environ['GIT_ACRONYM']+'/'+command['repo']
            GIT_URL = os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_SERVER']+'/' +\
                os.environ['GIT_ACRONYM']+'/'+command['repo']

            # GIT PULL OR GIT CLONE
            if repo_exists:
                Logger.log.info('Pulling repo %s' % (command['repo']))
                requirements_lastmod = 0
                if requirements_path.is_file():
                    requirements_lastmod = os.path.getmtime(
                        str(requirements_path))

                # pull existing repo
                if hasbranch:
                    cmd = ['git', '-C', str(repo_path),
                           'pull', GIT_URL, command['branch']]
                else:
                    cmd = ['git', '-C', str(repo_path), 'pull', GIT_URL]

                if not send_command(cmd):
                    Logger.log.error('Pulling repo %s ERROR!' %
                                     (command['repo']))
                    runroutine = False
                else:
                    if requirements_path.is_file():
                        install_requirements = os.path.getmtime(
                            str(requirements_path)) != requirements_lastmod
                        runroutine = True
                        Logger.log.info('Pulling repo %s DONE!' %
                                        (command['repo']))
                    else:
                        install_requirements = False
                        runroutine = False
                        Logger.log.error(
                            'Pulling repo %s ERROR: requirements.txt not found!' % (command['repo']))

            else:
                Logger.log.info('Cloning repo %s...' % (command['repo']))
                if hasbranch:
                    cmd = ['git', '-C', str(repo_path.parents[0]), 'clone',
                           '-b', command['branch'], GIT_URL, str(repo_path)]
                else:
                    cmd = ['git', '-C',
                           str(repo_path.parents[0]), 'clone', GIT_URL]
                if not send_command(cmd):
                    Logger.log.error('Cloning repo %s ERROR!' %
                                     (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    if requirements_path.is_file():
                        install_requirements = True
                        Logger.log.info('Cloning repo %s DONE!' %
                                        (command['repo']))
                    else:
                        install_requirements = False
                        Logger.log.error(
                            'Cloning repo %s ERROR: requirements.txt not found!' % (command['repo']))

            # TODO: ALLOW FOR PYTHON VERSION SPECIFICATION
            # CREATE VENV
            if (runroutine) & (not venv_exists):
                Logger.log.info('Creating venv %s...' % (command['repo']))
                if not send_command(['python', '-m', 'venv', str(repo_path/'venv')]):
                    Logger.log.error('Creating venv %s ERROR!' %
                                     (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    if requirements_path.is_file():
                        install_requirements = True
                        Logger.log.info('Creating venv %s DONE!' %
                                        (command['repo']))
                    else:
                        install_requirements = False
                        Logger.log.error(
                            'Creating venv %s ERROR: requirements.txt not found!' % (command['repo']))

            # INSTALL REQUIREMENTS
            if (runroutine) & (install_requirements):
                Logger.log.info('Installing requirements %s...' %
                                (command['repo']))
                if not send_command([str(python_path), '-m', 'pip', 'install', '-r', str(requirements_path)], env=env):
                    Logger.log.error(
                        'Installing requirements %s ERROR!' % (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    Logger.log.info('Installing requirements %s DONE!' %
                                    (command['repo']))

        if runroutine:
            Logger.log.info('Installing %s DONE!' % (command['repo']))
        else:
            Logger.log.error('Installing %s ERROR!' % (command['repo']))

        installed_repo['ts'] = time.time()
        installed_repo['isinstalling'] = False
        return runroutine


def run_routine(command, routine):
    Logger.log.info('Running routine %s/%s' %
                    (command['repo'], command['routine']))

    installed = True
    if command['repo'] != 'SharedData':
        installed = install_repo(command)

    if installed:
        # RUN ROUTINE
        Logger.log.info('Starting process %s/%s...' %
                        (command['repo'], command['routine']))

        hasbranch, requirements_path, repo_path, python_path, env = get_env(
            command)

        if command['repo'] == 'SharedData':
            cmd = [str(python_path), '-m',
                   str('SharedData.'+command['routine'])]
        else:
            cmd = [str(python_path), str(repo_path/command['routine'])]

        if 'args' in command:
            cmd += [command['args']]

        routine['subprocess'] = subprocess.Popen(cmd, env=env)
        routine['pid'] = routine['subprocess'].pid
        routine['process'] = psutil.Process(routine['pid'])

        Logger.log.info('Starting process %s/%s DONE!' %
                        (command['repo'], command['routine']))
    else:
        Logger.log.error(
            'Aborting routine %s, could not install repo' % (command['routine']))


def kill_routine(command, routines):
    routines_to_remove = []

    success = True
    if command['repo'] == 'ALL':
        Logger.log.info('Kill: ALL...')
        for routine in routines:
            if 'process' in routine:
                try:
                    if routine['process'].is_running():
                        routine['process'].kill()
                except:
                    success = False
                routines_to_remove.append(routine)
        Logger.log.info('Kill: ALL DONE!')
    else:
        reponame = command['repo']
        if ('branch' in command) and (command['branch'] != ''):
            reponame += '#' + command['branch']
        for routine in routines:
            kill = False
            if 'repo' in routine['command']:
                routine_reponame = routine['command']['repo']
                if ('branch' in routine['command']) and (routine['command']['branch'] != ''):
                    routine_reponame += '#' + routine['command']['branch']
                
                if (routine_reponame == reponame):
                    if 'routine' in command:
                        if (routine['command']['routine'] == command['routine']):
                            kill = True
                    else:
                        kill = True

            if (kill) & ('process' in routine):
                try:
                    if routine['process'].is_running():
                        routine['process'].kill()
                        Logger.log.info('Kill: %s/%s %.2fs DONE!' %
                                        (routine['command']['repo'], routine['command']['routine'],
                                         time.time()-routine['start_time']))
                except:
                    success = False
                    Logger.log.error('Failed to kill %s/%s!' %
                                     (command['repo'], command['routine']))
                routines_to_remove.append(routine)

    for routine in routines_to_remove:
        routines.remove(routine)

    return success


def remove_finished_routines(routines):
    new_routines = []
    for routine in routines:
        remove_routine = False
        
        if 'process' in routine and routine['process'] is not None:
            is_running = False
            try:
                if 'subprocess' in routine:
                    exit_code = routine['subprocess'].poll()
                    if (not exit_code is None) and (exit_code != 0):
                        Logger.log.error('Routine %s/%s exited with code %s' %
                                         (routine['command']['repo'], routine['command']['routine'], exit_code))
                is_running = routine['process'].is_running()
            except:
                pass
            if not is_running:
                remove_routine = True

        elif 'thread' in routine and not routine['thread'].is_alive():
            remove_routine = True

        if not remove_routine:
            new_routines.append(routine)

    return new_routines


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    Logger.log.info('restarting worker...')
    try:
        p = psutil.Process(os.getpid())
        children = p.children(recursive=True)
        for child in children:
            child.kill()

    except Exception as e:
        Logger.log.error('restarting worker ERROR!')
        Logger.log.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def read_stdout(stdout):
    try:
        while True:
            out = stdout.readline()
            if out:
                out = out.replace('\n', '')
                if (out != ''):
                    Logger.log.debug('<-' + out)
            else:
                break
    except:
        pass


def read_stderr(stderr):
    try:
        while True:
            err = stderr.readline()
            if err:
                err = err.replace('\n', '')
                if (err != ''):
                    if ('INFO' in err):
                        Logger.log.info('<-'+err)
                    elif ('WARNING' in err):
                        Logger.log.warning('<-'+err)
                    elif ('ERROR' in err):
                        Logger.log.error('<-'+err)
                    elif ('CRITICAL' in err):
                        Logger.log.critical('<-'+err)
                    else:
                        Logger.log.debug('<-'+err)
            else:
                break
    except:
        pass


def send_command(command, env=None, blocking=True):
    if isinstance(command, (list, tuple)):
        _command = ' '.join(command)
    else:
        _command = command
    
    Logger.log.debug('->%s' % _command)
    
    if env is None:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True)
    else:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True, env=env)

    stdout_thread = threading.Thread(
        target=read_stdout, args=([process.stdout]))
    stderr_thread = threading.Thread(
        target=read_stderr, args=([process.stderr]))
    stdout_thread.start()
    stderr_thread.start()

    if blocking:
        process.wait()  # block until process terminated

    stdout_thread.join()
    stderr_thread.join()

    rc = process.returncode
    success = rc == 0
    if success:
        Logger.log.debug('DONE!->%s' % (_command))
        return True
    else:
        Logger.log.error('ERROR!->%s' % (_command))
        return False


def list_process():
    source_path = Path(os.environ['SOURCE_FOLDER'])
    procdict = {}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=None)
            if len(pinfo['cmdline']) > 0:
                if str(source_path) in pinfo['cmdline'][0]:
                    procdict[proc.pid] = {'proc': proc, 'pinfo': pinfo}
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return procdict


def get_env(command):
    hasbranch = False
    if 'branch' in command:
        if command['branch'] != '':
            hasbranch = True

    if command['repo'] == 'SharedData':
        repo_path = Path(os.environ['SOURCE_FOLDER'])
    elif hasbranch:
        repo_path = Path(os.environ['SOURCE_FOLDER']) / \
            (command['repo']+'#'+command['branch'])
    else:
        repo_path = Path(os.environ['SOURCE_FOLDER'])/command['repo']

    requirements_path = repo_path/'requirements.txt'
    if os.name == 'posix':
        python_path = repo_path/'venv/bin/python'
    else:
        python_path = repo_path/'venv/Scripts/python.exe'

    env = os.environ.copy()
    env['VIRTUAL_ENV'] = str(repo_path/'venv')
    env['PATH'] = str(repo_path/'venv')+';' + \
        str(python_path.parents[0])+';'+env['PATH']
    env['PYTHONPATH'] = str(repo_path/'venv')+';'+str(python_path.parents[0])
    env['GIT_TERMINAL_PROMPT'] = "0"

    return hasbranch, requirements_path, repo_path, python_path, env


def start_schedules(schedule_names):
    # run logger
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "IO.ReadLogs",
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'subprocess': None,
        'start_time': start_time,
    }
    run_routine(command, routine)

    # run scheduler
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "Routines.Scheduler",
        "args": schedule_names,
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'subprocess': None,
        'start_time': start_time,
    }
    run_routine(command, routine)


def isrunning(command,routines):
    isrunning = False
    for routine in routines:
        if ('repo' in command) & ('repo' in routine['command']):
            if (routine['command']['repo'] == command['repo']):
                if ('routine' in command) & ('routine' in routine['command']):
                    if (routine['command']['routine'] == command['routine']):
                        isrunning = True
                        break
                else:
                    isrunning = True
                    break
    return isrunning
