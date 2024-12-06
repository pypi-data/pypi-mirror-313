import logging
import os
import shlex
import subprocess
import traceback
from signal import SIGKILL, SIGTERM
from typing import Tuple

logger = logging.getLogger('main')


def get_output(cmd: str) -> str:
    """ 명령에 대한 output을 가져옴. 단, 명령은 수행 후 종료되는 명령이어야 함 """
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as process:
            outputs = process.stdout.read().decode()
            return outputs
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        return ''


def command_generator(command: str, max_count: int = None):
    """
    tail처럼 foreground 상에서 지속되는 명령에 대한 output을 하나씩 yield 하여 가져옴

    Args:
        command (str): command string for shell
        max_count (int, optional): count for yielding output. if None, yield result infinitely

    Yields:
        _type_: _description_
    """
    count = 0
    process = subprocess.Popen(shlex.split(
        command), stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            logger.info('command generator terminated')
            break
        if output:
            ret = output.strip()
            yield ret

            count += 1
            if max_count and count >= max_count:
                break

    rc = process.poll()
    return rc


def get_pid(name: str) -> Tuple[str]:
    if os.name == 'posix':
        pids = get_output(f'pidof {name}').split()
    else:
        pids = None
    return pids


def get_pid_grep(*names: str) -> Tuple[str]:
    if os.name == 'posix':
        grep_cmd = " | grep ".join([f'"{name}"' for name in names])
        pids = get_output(
            f'ps -eaf | grep {grep_cmd} | grep -v grep | awk \'{{print $2}}\'').split()
    else:
        pids = None
    return pids


def get_pid_by_pgrep(command: str) -> Tuple[int]:
    pids = get_output(f'pgrep -f "{command}"').split()
    return [int(el) for el in pids] or []


'''
1 - SIGHUP: Hangup detected on controlling terminal or death of controlling process. Often used to reload configuration files and reopen log files in daemon processes.
2 - SIGINT: Interrupt from keyboard (like pressing Ctrl+C).
3 - SIGQUIT: Quit from keyboard.
9 - SIGKILL: Kill signal. It forces the process to terminate immediately. This signal cannot be caught, blocked, or ignored, making it surefire but also potentially dangerous if not used judiciously.
15 - SIGTERM: Termination signal. This is the default and safest way to kill a process as it allows the process to release resources and perform cleanup operations before shutting down.
'''


def kill_pid(name: str, signal=SIGKILL):
    try:
        pids = get_pid(name)
        if pids is not None:
            for pid in pids:
                os.kill(int(pid), signal)
    except Exception as e:
        print(str(e).encode())


def kill_pid_grep(*names: str, signal=SIGKILL):
    try:
        pids = get_pid_grep(*names)
        if pids is not None:
            for pid in pids:
                os.kill(int(pid), signal)
    except Exception as e:
        print(str(e).encode())


def kill_process_by_command(cmd: str, signal=SIGTERM):
    tcpdump_pids = get_pid_by_pgrep(cmd)
    try:
        for pid in tcpdump_pids:
            os.kill(pid, signal)
    except Exception as e:
        print(str(e).encode())
