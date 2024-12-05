import shutil
import sys
from time import sleep

from loguru import logger

from primitive.__about__ import __version__
from primitive.utils.actions import BaseAction

from ..utils.cache import get_sources_cache
from .runner import AgentRunner
from .uploader import Uploader


class Agent(BaseAction):
    def execute(
        self,
    ):
        logger.enable("primitive")
        logger.info(" [*] primitive")
        logger.info(f" [*] Version: {__version__}")

        # Create cache dir if it doesn't exist
        cache_dir = get_sources_cache()

        # Create uploader
        uploader = Uploader(primitive=self.primitive)

        # self.primitive.hardware.update_hardware_system_info()
        try:
            self.primitive.hardware.check_in_http(is_available=True, is_online=True)
        except Exception as ex:
            logger.error(f"Error checking in hardware: {ex}")
            sys.exit(1)

        try:
            active_reservation_id = None
            active_reservation_pk = None

            while True:
                logger.debug("Scanning for files to upload...")
                uploader.scan()

                hardware = self.primitive.hardware.get_own_hardware_details()
                if hardware["activeReservation"]:
                    if (
                        hardware["activeReservation"]["id"] != active_reservation_id
                        or hardware["activeReservation"]["pk"] != active_reservation_pk
                    ):
                        logger.warning("New reservation for this hardware.")
                        active_reservation_id = hardware["activeReservation"]["id"]
                        active_reservation_pk = hardware["activeReservation"]["pk"]
                        logger.debug("Active Reservation:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")

                        logger.debug("Running pre provisioning steps for reservation.")
                        self.primitive.provisioning.add_reservation_authorized_keys(
                            reservation_id=active_reservation_id
                        )
                else:
                    if (
                        hardware["activeReservation"] is None
                        and active_reservation_id is not None
                        and hardware["isAvailable"]
                    ):
                        logger.debug("Previous Reservation is Complete:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")
                        logger.debug(
                            "Running cleanup provisioning steps for reservation."
                        )
                        self.primitive.provisioning.remove_reservation_authorized_keys(
                            reservation_id=active_reservation_id
                        )
                        active_reservation_id = None
                        active_reservation_pk = None

                if not active_reservation_id:
                    self.primitive.hardware.check_in_http(
                        is_available=True, is_online=True
                    )
                    sleep_amount = 5
                    logger.debug(
                        f"No active reservation found... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                job_runs_result = self.primitive.jobs.get_job_runs(
                    status="pending", first=1, reservation_id=active_reservation_id
                )

                pending_job_runs = [
                    edge["node"] for edge in job_runs_result.data["jobRuns"]["edges"]
                ]

                if not pending_job_runs:
                    sleep_amount = 5
                    logger.debug(
                        f"Waiting for Job Runs... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                for job_run in pending_job_runs:
                    logger.debug("Found pending Job Run")
                    logger.debug(f"Job Run ID: {job_run['id']}")
                    logger.debug(f"Job Name: {job_run['job']['name']}")

                    git_repo_full_name = job_run["gitCommit"]["repoFullName"]
                    git_ref = job_run["gitCommit"]["sha"]
                    logger.debug(
                        f"Downloading repository {git_repo_full_name} at ref {git_ref}"
                    )

                    github_access_token = (
                        self.primitive.jobs.github_access_token_for_job_run(
                            job_run["id"]
                        )
                    )

                    downloaded_git_repository_dir = (
                        self.primitive.git.download_git_repository_at_ref(
                            git_repo_full_name=git_repo_full_name,
                            git_ref=git_ref,
                            github_access_token=github_access_token,
                            destination=cache_dir,
                        )
                    )

                    source_dir = downloaded_git_repository_dir.joinpath(
                        job_run["jobSettings"]["rootDirectory"]
                    )

                    try:
                        # Initialize Runner
                        runner = AgentRunner(
                            primitive=self.primitive,
                            source_dir=source_dir,
                            job_id=job_run["id"],
                            job_slug=job_run["job"]["slug"],
                            max_log_size=500 * 1024,
                        )
                    except Exception as e:
                        # Log Error
                        logger.error(f"Error initializing agent runner: {e}")
                    else:
                        # Execute job
                        runner.execute()
                    finally:
                        # Clean up
                        shutil.rmtree(path=downloaded_git_repository_dir)

                sleep(5)
        except KeyboardInterrupt:
            logger.info(" [*] Stopping primitive...")
            self.primitive.hardware.check_in_http(is_available=False, is_online=False)
            sys.exit()
