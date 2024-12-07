import os
import subprocess


def subprocess_start(bec_path: str, config_path: str, services: dict):
    processes = []
    for ii, service_info in enumerate(services.items()):
        service, service_config = service_info
        service_path = service_config["path"].substitute(base_path=bec_path)
        # service_config adds a subdirectory to each path, here we do not want the subdirectory
        cwd = os.path.abspath(os.path.join(service_path, ".."))
        if config_path:
            processes.append(
                subprocess.Popen((service_config["command"], "--config", config_path), cwd=cwd)
            )
        else:
            processes.append(subprocess.Popen((service_config["command"],), cwd=cwd))
    return processes


def subprocess_stop():
    # do nothing for now... would require pid files or something to keep track
    # of the started processes
    ...
