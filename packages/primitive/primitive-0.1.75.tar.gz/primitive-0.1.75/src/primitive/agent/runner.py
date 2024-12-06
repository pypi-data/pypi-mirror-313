import os
import threading
import typing
import json
from pathlib import Path, PurePath
from time import sleep
from typing import Dict, Iterable, List, Optional, TypedDict, Callable

import yaml
from loguru import logger
from .process import Process
from .provision import ProvisionPython
from ..utils.cache import get_artifacts_cache, get_logs_cache
from ..utils.files import find_files_for_extension

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

if typing.TYPE_CHECKING:
    import primitive.client


class Artifact(TypedDict):
    name: str
    extension: str


class JobStep(TypedDict):
    name: str
    workdir: str
    artifacts: List[Artifact]
    cmd: str


class JobDescription(TypedDict):
    name: str
    provision: str
    steps: List[JobStep]


class AgentRunner:
    def __init__(
        self,
        primitive: "primitive.client.Primitive",
        source_dir: Path,
        job_id: str,
        job_slug: str,
        max_log_size: int = 10 * 1024 * 1024,
        log_to_file: bool = True,
        job: Optional[JobDescription] = None,
    ) -> None:
        self.primitive = primitive
        self.source_dir = source_dir
        self.workdir = "."
        self.job_id = job_id
        self.job_slug = job_slug
        self.max_log_size = max_log_size
        self.log_to_file = log_to_file

        # Enable and configure logger
        logger.enable("primitive")

        if self.log_to_file:
            log_name = f"{self.job_slug}_{self.job_id}_{{time}}.primitive.log"
            logger.add(
                Path(get_logs_cache(self.job_id) / log_name),
                rotation=self.max_log_size,
                format=AgentRunner.log_serializer(),
            )

        # Attempt to load job from file
        if not job:
            logger.info(f"Scanning directory for job file {self.job_slug}")
            yaml_file = Path(self.source_dir / ".primitive" / f"{self.job_slug}.yaml")
            yml_file = Path(self.source_dir / ".primitive" / f"{self.job_slug}.yml")

            if yaml_file.exists() and yml_file.exists():
                logger.error(
                    f"Found two job descriptions with the same slug: {self.job_slug}"
                )
                self.primitive.jobs.job_run_update(
                    self.job_id, status="request_completed", conclusion="failure"
                )
                raise FileExistsError

            if yaml_file.exists():
                self.job = yaml.load(open(yaml_file, "r"), Loader=Loader)
            elif yml_file.exists():
                self.job = yaml.load(open(yml_file, "r"), Loader=Loader)
            else:
                logger.error(
                    f"No job description with matching slug '{self.job_slug}' found"
                )
                self.primitive.jobs.job_run_update(
                    self.job_id, status="request_completed", conclusion="failure"
                )
                raise FileNotFoundError

            logger.info(f"Found job description for {self.job_slug}")
        else:
            self.job = job

    @staticmethod
    def log_serializer() -> Callable:
        def fmt(record):
            step = ""
            if "step" in record["extra"]:
                step = record["extra"]["step"]

            log = {
                "time": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                "utc": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f%z"),
                "level": record["level"].name,
                "message": record["message"],
                "name": record["name"],
                "step": step,
            }

            record["extra"]["serialized"] = json.dumps(log)

            return "{extra[serialized]}\n"

        return fmt

    def name(self) -> str:
        return self.job["name"]

    def steps(self) -> Iterable[JobStep]:
        for step in self.job["steps"]:
            yield step

    def execute(self) -> None:
        logger.info(f"Executing {self.job_slug} job")
        self.primitive.jobs.job_run_update(self.job_id, status="request_in_progress")

        # Initialize the environment with the system
        environment = os.environ
        if "provision" in self.job:
            logger.info(f"Provisioning for {self.job['provision']} environment")
            environment = self.provision()

            if not environment:
                self.primitive.jobs.job_run_update(
                    self.job_id, status="request_completed", conclusion="failure"
                )
                logger.error(f"{self.job_slug} concluded with error(s)")
                return

        total_job_errors = 0
        for step in self.steps():
            logger.info(f"Beginning step {step['name']}")

            with logger.contextualize(step=step["name"]):
                if "workdir" in step:
                    self.workdir = step["workdir"]

                proc = Process(
                    cmd=step["cmd"],
                    workdir=Path(self.source_dir / self.workdir),
                    env=environment,
                )

                try:
                    proc.start()
                except Exception as e:
                    logger.error(f"Error while attempting to run process {e}")
                    self.primitive.jobs.job_run_update(
                        self.job_id, status="request_completed", conclusion="failure"
                    )
                    logger.error(f"{self.job_slug} concluded with error(s)")
                    return

                def status_check():
                    while proc.is_running():
                        # Check job status
                        status = self.primitive.jobs.get_job_status(self.job_id)
                        status_value = status.data["jobRun"]["status"]

                        # TODO: Should probably use request_cancelled or something
                        # once we change it, we'll have to call conclude w/ cancelled status
                        if status_value == "completed":
                            logger.warning("Job cancelled by user")
                            proc.terminate()
                            return

                        sleep(5)

                status_thread = threading.Thread(target=status_check)
                status_thread.start()

                returncode = proc.wait()
                total_job_errors += proc.errors
                status_thread.join()

            self.collect_artifacts(step)

            if returncode > 0:
                self.primitive.jobs.job_run_update(
                    self.job_id, status="request_completed", conclusion="failure"
                )
                logger.error(f"{self.job_slug} concluded with error(s)")
                return

        if total_job_errors > 0:
            self.primitive.jobs.job_run_update(
                self.job_id, status="request_completed", conclusion="failure"
            )
            logger.error(f"{self.job_slug} concluded with error(s)")
            return

        self.primitive.jobs.job_run_update(
            self.job_id, status="request_completed", conclusion="success"
        )
        logger.success(f"Completed {self.job_slug} job")

    def provision(self) -> Optional[Dict]:
        match self.job["provision"]:
            case "python":
                requirements_glob = self.source_dir.rglob("requirements.txt")

                requirements_path = next(requirements_glob, None)

                if not requirements_path:
                    logger.error("Unable to locate requirements.txt")
                    return None

                prov = ProvisionPython(self.source_dir, requirements_path)
                return prov.create_env()

    def collect_artifacts(self, step: JobStep) -> None:
        if "artifacts" not in step:
            return

        for artifact in step["artifacts"]:
            files = find_files_for_extension(self.source_dir, artifact["extension"])

            for file in files:
                # Find path relative to source_dir
                relative_path = PurePath(file).relative_to(self.source_dir)

                # Construct destination to preserve directory structure
                destination = Path(get_artifacts_cache(self.job_id) / relative_path)

                # Create directories if they don't exist
                destination.parent.mkdir(parents=True, exist_ok=True)

                # Move file
                file.rename(destination)
