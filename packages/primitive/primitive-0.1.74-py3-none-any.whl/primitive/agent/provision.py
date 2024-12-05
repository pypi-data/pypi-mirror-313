import sys
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Dict
from ..utils.shell import env_string_to_dict


class ProvisionPython:
    def __init__(self, source_dir: Path, requirements_path: Path):
        self.source_dir = source_dir
        self.requirements_path = requirements_path

    def create_env(self) -> Dict:
        cmd = f"{sys.executable} -m ensurepip"
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, text=True)
        proc.wait()

        cmd = f"{sys.executable} -m pip install virtualenv"
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, text=True)
        proc.wait()

        cmd = f"{sys.executable} -m virtualenv venv"
        proc = Popen(
            cmd, cwd=self.source_dir, stdout=PIPE, stderr=PIPE, shell=True, text=True
        )
        proc.wait()

        cmd = "source venv/bin/activate && env"
        proc = Popen(
            cmd, cwd=self.source_dir, stdout=PIPE, stderr=PIPE, shell=True, text=True
        )
        proc.wait()

        # Read the output and decode it
        output, _ = proc.communicate()

        # Split the output into lines and parse it into a dictionary
        env_vars = env_string_to_dict(output)

        cmd = f"python -m pip install -r {self.requirements_path}"
        proc = Popen(
            cmd,
            cwd=self.source_dir,
            env=env_vars,
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
            text=True,
        )
        proc.wait()

        return env_vars
