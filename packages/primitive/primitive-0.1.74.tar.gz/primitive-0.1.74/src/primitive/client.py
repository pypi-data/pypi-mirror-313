import sys

from gql import Client
from loguru import logger

from .agent.actions import Agent
from .auth.actions import Auth
from .daemons.actions import Daemons
from .exec.actions import Exec
from .files.actions import Files
from .git.actions import Git
from .hardware.actions import Hardware
from .jobs.actions import Jobs
from .organizations.actions import Organizations
from .projects.actions import Projects
from .provisioning.actions import Provisioning
from .reservations.actions import Reservations
from .utils.config import read_config_file

logger.disable("primitive")


class Primitive:
    def __init__(
        self,
        host: str = "api.primitive.tech",
        DEBUG: bool = False,
        JSON: bool = False,
        token: str = None,
        transport: str = None,
    ) -> None:
        self.host: str = host
        self.session: Client = None
        self.DEBUG: bool = DEBUG
        self.JSON: bool = JSON

        if self.DEBUG:
            logger.enable("primitive")
            logger.remove()
            logger.add(
                sink=sys.stderr,
                serialize=self.JSON,
                catch=True,
                backtrace=True,
                diagnose=True,
            )

        # Generate full or partial host config
        if not token and not transport:
            # Attempt to build host config from file
            try:
                self.get_host_config()
            except KeyError:
                self.host_config = {}
        else:
            self.host_config = {"username": "", "token": token, "transport": transport}

        self.auth: Auth = Auth(self)
        self.organizations: Organizations = Organizations(self)
        self.projects: Projects = Projects(self)
        self.jobs: Jobs = Jobs(self)
        self.files: Files = Files(self)
        self.reservations: Reservations = Reservations(self)
        self.hardware: Hardware = Hardware(self)
        self.agent: Agent = Agent(self)
        self.git: Git = Git(self)
        self.daemons: Daemons = Daemons(self)
        self.exec: Exec = Exec(self)
        self.provisioning: Provisioning = Provisioning(self)

    def get_host_config(self):
        self.full_config = read_config_file()
        self.host_config = self.full_config.get(self.host)

        if not self.host_config:
            raise KeyError(f"Host {self.host} not found in config file.")
