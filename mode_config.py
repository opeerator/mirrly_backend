#!/usr/bin/env python3

import subprocess


class ModeManager(object):
    """This is a class to control the robot's modes."""
    
    # Different modes will initiate their specific module.
    mode_list = {
        "collision_avoidance": {"script": "collision_control.py", "server": True},
        "head_follow": {"script": "head_follow_control.py", "server": True},
        "demo": {"script": "demo_control.py", "server": True},
        "study": {"script": "study_control.py", "server": True},
        "full_control": {"script": "full_control.py", "server": True},
        "start_motion": {"script": "start_motion.py", "server": True}
    }

    def __init__(self):
        # Lists to keep every running process.
        self.active_processes = {}

    def is_running(self, mode_name = None):
        """Checks if a process is running and send's states."""
        if self.active_processes == {}:
            return True
        if mode_name != None:
            if mode_name in self.active_processes:
                return True
            else:
                return False
        else:
            return True

    def run(self, mode_name):
        """Initiate a subprocess to run robotic behaviour."""
        if mode_name not in self.active_processes:
            script = self.mode_list[mode_name]['script']
            self.active_processes.push[mode_name] = subprocess.Popen(["python3", script])
        else:
            pass

    def stop(self, mode_name = None):
        """Stopping a subprocess."""
        if mode_name != None:
            if self.is_running(mode_name):
                self.active_processes.send_signal(subprocess.signal.SIGINT)
                self.active_processes.pop(mode_name)
            else:
                pass
        else:
            if self.is_running():
                self.active_processes.send_signal(subprocess.signal.SIGINT)
                self.active_processes = {}

    def should_redirect(self, mode_name):
        return self.mode_config[mode_name].get('server') is True and self.is_running()
