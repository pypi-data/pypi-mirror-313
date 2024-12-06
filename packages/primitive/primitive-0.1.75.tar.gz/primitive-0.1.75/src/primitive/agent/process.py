from subprocess import Popen, PIPE
import shlex
import selectors
from loguru import logger


class Process:
    def __init__(
        self,
        cmd,
        env,
        workdir: str = ".",
    ):
        self.cmd = shlex.split(cmd)
        self.env = env
        self.workdir = workdir
        self.process = None
        self.stdout_thread = None
        self.stderr_thread = None
        self._errors = 0

    def start(self):
        # Start the process
        self.sel = selectors.DefaultSelector()
        self.process = Popen(
            self.cmd,
            env=self.env,
            cwd=self.workdir,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )

        self.sel.register(self.process.stdout, selectors.EVENT_READ)
        self.sel.register(self.process.stderr, selectors.EVENT_READ)

    def log(self):
        for key, _ in self.sel.select():
            data = key.fileobj.readline()
            if not data:
                continue

            if key.fileobj is self.process.stdout:
                raw_data = data.rstrip()
                if "error" in raw_data.lower():
                    logger.error(raw_data)
                    self._errors += 1
                elif "warning" in raw_data.lower():
                    logger.warning(raw_data)
                else:
                    logger.info(raw_data)
            elif key.fileobj is self.process.stderr:
                logger.error(data.rstrip())
                self._errors += 1

    def wait(self):
        while True:
            self.log()
            if not self.is_running():
                break

        return self.finish()

    def run(self):
        """Start and wait for the process."""
        self.start()
        return self.wait()

    def is_running(self):
        """Check if the process is still running."""
        return self.process and self.process.poll() is None

    def finish(self):
        """Make sure that logging finishes"""
        if self.process:
            self.sel.unregister(self.process.stdout)
            self.sel.unregister(self.process.stderr)
            self.process.stdout.close()
            self.process.stderr.close()

            return self.process.poll()

    def terminate(self):
        """Terminate the process."""
        if self.process:
            self.process.terminate()

    def kill(self):
        """Kill the process."""
        if self.process:
            self.process.kill()

    @property
    def errors(self) -> int:
        return self._errors
