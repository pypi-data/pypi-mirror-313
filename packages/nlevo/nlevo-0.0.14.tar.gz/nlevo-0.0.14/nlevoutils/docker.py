import os


def is_running_in_docker():
    return False if os.environ.get('is_not_docker') else True
    try:
        folder_path = '/proc'
        folder_list = os.listdir(folder_path)
        if "docker" in folder_list:  # mac os
            return True
        else:  # linux
            with open('/proc/1/cgroup', 'rt') as f:
                return 'docker' in f.read()
    except FileNotFoundError:
        return False
