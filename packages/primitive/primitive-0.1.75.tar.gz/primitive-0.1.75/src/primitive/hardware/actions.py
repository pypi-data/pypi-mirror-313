import csv
import io
import json
import platform
import subprocess
import typing
from shutil import which
from typing import Dict, List, Optional

import click
from aiohttp import client_exceptions
from gql import gql
from loguru import logger

from primitive.graphql.relay import from_base64
from primitive.utils.memory_size import MemorySize

from ..utils.auth import guard
from ..utils.config import update_config_file
from .graphql.mutations import (
    hardware_checkin_mutation,
    hardware_update_mutation,
    register_hardware_mutation,
)
from .graphql.queries import hardware_list

if typing.TYPE_CHECKING:
    pass


from primitive.utils.actions import BaseAction


class Hardware(BaseAction):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.previous_state = {
            "isHealthy": False,
            "isQuarantined": False,
            "isAvailable": False,
            "isOnline": False,
        }

    def _get_darwin_system_profiler_values(self) -> Dict[str, str]:
        system_profiler_hardware_data_type = subprocess.check_output(
            ["system_profiler", "SPHardwareDataType", "-json"]
        )
        system_profiler_hardware_data = json.loads(system_profiler_hardware_data_type)
        data_type = system_profiler_hardware_data.get("SPHardwareDataType")[0]
        return {
            "apple_model_name": data_type.get("machine_model"),
            "apple_model_identifier": data_type.get("machine_name"),
            "apple_model_number": data_type.get("model_number"),
            "physical_memory": data_type.get("physical_memory"),
            "apple_serial_number": data_type.get("serial_number"),
        }

    def _get_supported_metal_device(self) -> int | None:
        """
        Checks if metal hardware is supported. If so, the index
        of the supported metal device is returned
        """
        supported_metal_device = None
        is_system_profiler_available = bool(which("system_profiler"))
        if is_system_profiler_available:
            system_profiler_display_data_type_command = (
                "system_profiler SPDisplaysDataType -json"
            )
            try:
                system_profiler_display_data_type_output = subprocess.check_output(
                    system_profiler_display_data_type_command.split(" ")
                )
            except subprocess.CalledProcessError as exception:
                message = f"Error running system_profiler: {exception}"
                logger.error(message)
                return supported_metal_device

            try:
                system_profiler_display_data_type_json = json.loads(
                    system_profiler_display_data_type_output
                )
            except json.JSONDecodeError as exception:
                message = f"Error decoding JSON: {exception}"
                logger.error(message)
                return supported_metal_device

            # Checks if any attached displays have metal support
            # Note, other devices here could be AMD GPUs or unconfigured Nvidia GPUs
            for index, display in enumerate(
                system_profiler_display_data_type_json["SPDisplaysDataType"]
            ):
                if "spdisplays_mtlgpufamilysupport" in display:
                    supported_metal_device = index
                    return supported_metal_device

        return supported_metal_device

    def _get_gpu_config(self) -> List:
        """
        For Nvidia based systems, nvidia-smi will be used to profile the gpu/s.
        For Metal based systems, we will gather information from SPDisplaysDataType.
        """
        gpu_config = []

        # Check nvidia gpu availability
        is_nvidia_smi_available = bool(which("nvidia-smi"))
        if is_nvidia_smi_available:
            nvidia_smi_query_gpu_csv_command = "nvidia-smi --query-gpu=gpu_name,driver_version,memory.total --format=csv"  # noqa
            try:
                nvidia_smi_query_gpu_csv_output = subprocess.check_output(
                    nvidia_smi_query_gpu_csv_command.split(" "),
                )
            except subprocess.CalledProcessError as exception:
                message = f"Command {nvidia_smi_query_gpu_csv_command} failed with exception: {exception}"  # noqa
                logger.error(message)
                raise exception

            try:
                nvidia_smi_query_gpu_csv_decoded = (
                    nvidia_smi_query_gpu_csv_output.decode("utf-8")
                    .replace("\r", "")
                    .replace(", ", ",")
                    .lstrip("\n")
                )
            except UnicodeDecodeError as exception:
                message = f"Error decoding: {exception}"
                logger.error(message)
                raise exception

            nvidia_smi_query_gpu_csv_dict_reader = csv.DictReader(
                io.StringIO(nvidia_smi_query_gpu_csv_decoded)
            )

            for gpu_info in nvidia_smi_query_gpu_csv_dict_reader:
                # Refactor key into B
                memory_total_in_mebibytes = gpu_info.pop("memory.total [MiB]")
                memory_size = MemorySize(memory_total_in_mebibytes)
                gpu_info["memory_total"] = memory_size.to_bytes()

                gpu_config.append(gpu_info)

        if platform.system() == "Darwin":
            # Check Metal gpu availability
            supported_metal_device = self._get_supported_metal_device()
            if supported_metal_device is not None:
                # Since Apple's SoC contains Metal,
                # we query the system itself for total memory
                system_profiler_hardware_data_type_command = (
                    "system_profiler SPHardwareDataType -json"
                )

                try:
                    system_profiler_hardware_data_type_output = subprocess.check_output(
                        system_profiler_hardware_data_type_command.split(" ")
                    )
                except subprocess.CalledProcessError as exception:
                    message = f"Error running {system_profiler_hardware_data_type_command}: {exception}"  # noqa
                    logger.error(message)
                    raise exception

                try:
                    system_profiler_hardware_data_type_json = json.loads(
                        system_profiler_hardware_data_type_output
                    )
                except json.JSONDecodeError as exception:
                    message = f"Error decoding JSON: {exception}"  # noqa
                    logger.error(message)
                    raise exception

                metal_device_json = system_profiler_hardware_data_type_json[
                    "SPHardwareDataType"
                ][supported_metal_device]

                gpu_info = {}
                gpu_info["name"] = metal_device_json.get("chip_type")

                # Refactor key into B
                physical_memory = metal_device_json.get("physical_memory")
                memory_size = MemorySize(physical_memory)
                gpu_info["memory_total"] = memory_size.to_bytes()

                gpu_config.append(gpu_info)

        return gpu_config

    def _get_windows_computer_service_product_values(self) -> Dict[str, str]:
        windows_computer_service_product_csv_command = (
            "cmd.exe /C wmic csproduct get Name, Vendor, Version, UUID /format:csv"
        )
        windows_computer_service_product_csv_output = subprocess.check_output(
            windows_computer_service_product_csv_command.split(" "),
            stderr=subprocess.DEVNULL,
        )
        windows_computer_service_product_csv_decoded = (
            windows_computer_service_product_csv_output.decode("utf-8")
            .replace("\r", "")
            .lstrip("\n")
        )
        windows_computer_service_product_dict = csv.DictReader(
            io.StringIO(windows_computer_service_product_csv_decoded)
        )
        csp_info = list(windows_computer_service_product_dict)[0]
        return {
            "windows_model_name": csp_info.get("Name", ""),
            "windows_model_vendor": csp_info.get("Vendor", ""),
            "windows_model_version": csp_info.get("Version", ""),
            "windows_model_uuid": csp_info.get("UUID", ""),
        }

    def _get_windows_cpu_values(self) -> Dict[str, str]:
        windows_cpu_csv_command = (
            "cmd.exe /C wmic cpu get Name, MaxClockSpeed /format:csv"  # noqa
        )
        windows_cpu_csv_output = subprocess.check_output(
            windows_cpu_csv_command.split(" "),
            stderr=subprocess.DEVNULL,
        )
        windows_cpu_csv_decoded = (
            windows_cpu_csv_output.decode("utf-8").replace("\r", "").lstrip("\n")
        )
        windows_cpu_dict = csv.DictReader(io.StringIO(windows_cpu_csv_decoded))
        cpu_info = list(windows_cpu_dict)[0]
        return {
            "cpu_brand": cpu_info.get("Name", "").strip(),
            "cpu_max_clock_speed": cpu_info.get("MaxClockSpeed", ""),
        }

    def _get_ubuntu_values(self) -> Dict[str, str]:
        get_machine_id_command = "cat /etc/machine-id"
        machine_id = subprocess.check_output(
            get_machine_id_command.split(" "),
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")
        if machine_id:
            return {"linux_machine_id": machine_id}
        return {}

    def get_system_info(self):
        os_family = platform.system()
        system_info = {}
        if os_family == "Darwin":
            system_info = {**system_info, **self._get_darwin_system_profiler_values()}
            system_info["cpu_brand"] = (
                subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
                .strip()
                .decode("utf-8")
            )
            system_info["apple_mac_os_version"] = platform.mac_ver()[0]
        elif os_family == "Linux":
            # Support for Linux-based VMs in Windows
            if "WSL2" in platform.platform():
                system_info = {
                    **system_info,
                    **self._get_windows_computer_service_product_values(),
                    **self._get_windows_cpu_values(),
                }
            else:
                system_info = {**system_info, **self._get_ubuntu_values()}
        elif os_family == "Windows":
            system_info = {
                **system_info,
                **self._get_windows_computer_service_product_values(),
                **self._get_windows_cpu_values(),
            }

        system_info["name"] = platform.node()
        system_info["os_family"] = os_family
        system_info["os_release"] = platform.release()
        system_info["os_version"] = platform.version()
        system_info["platform"] = platform.platform()
        system_info["processor"] = platform.processor()
        system_info["machine"] = platform.machine()
        system_info["architecture"] = platform.architecture()[0]
        system_info["cpu_cores"] = str(platform.os.cpu_count())  # type: ignore exits
        system_info["gpu_config"] = self._get_gpu_config()
        return system_info

    @guard
    def register(self):
        system_info = self.get_system_info()
        mutation = gql(register_hardware_mutation)
        input = {"systemInfo": system_info}
        variables = {"input": input}
        result = self.primitive.session.execute(
            mutation, variable_values=variables, get_execution_result=True
        )
        if messages := result.data.get("registerHardware").get("messages"):
            for message in messages:
                logger.enable("primitive")
                if message.get("kind") == "ERROR":
                    logger.error(message.get("message"))
                else:
                    logger.debug(message.get("message"))
            return False

        fingerprint = result.data.get("registerHardware").get("fingerprint")

        self.primitive.host_config["fingerprint"] = fingerprint
        self.primitive.full_config[self.primitive.host] = self.primitive.host_config
        update_config_file(new_config=self.primitive.full_config)

        # then check in that the hardware, validate that it is saved correctly
        # and headers are set correctly
        self.primitive.get_host_config()
        self.check_in_http(is_healthy=True)
        return result

    @guard
    def update_hardware_system_info(self):
        """
        Updates hardware system information and returns the GraphQL response.

        Returns:
            dict: GraphQL response
        Raises:
            Exception: If no fingerprint is found or an error occurs
        """

        fingerprint = self.primitive.host_config.get("fingerprint", None)
        if not fingerprint:
            message = (
                "No fingerprint found. Please register: primitive hardware register"
            )
            raise Exception(message)

        system_info = self.get_system_info()
        new_state = {
            "systemInfo": system_info,
        }

        mutation = gql(hardware_update_mutation)

        input = new_state
        variables = {"input": input}
        try:
            result = self.primitive.session.execute(
                mutation, variable_values=variables, get_execution_result=True
            )
        except client_exceptions.ClientConnectorError as exception:
            message = " [*] Failed to update hardware system info! "
            logger.error(message)
            raise exception

        message = " [*] Updated hardware system info successfully! "
        logger.info(message)

        return result

    @guard
    def check_in_http(
        self,
        is_healthy: bool = True,
        is_quarantined: bool = False,
        is_available: bool = False,
        is_online: bool = True,
    ):
        fingerprint = self.primitive.host_config.get("fingerprint", None)
        if not fingerprint:
            message = (
                "No fingerprint found. Please register: primitive hardware register"
            )
            raise Exception(message)

        new_state = {
            "isHealthy": is_healthy,
            "isQuarantined": is_quarantined,
            "isAvailable": is_available,
            "isOnline": is_online,
        }

        mutation = gql(hardware_checkin_mutation)
        input = new_state
        variables = {"input": input}
        try:
            result = self.primitive.session.execute(
                mutation, variable_values=variables, get_execution_result=True
            )
            checkin_success = result.data.get("checkIn").get("lastCheckIn")
            if messages := result.data.get("checkIn").get("messages"):
                for message in messages:
                    logger.enable("primitive")
                    if message.get("kind") == "ERROR":
                        logger.error(message.get("message"))
                    else:
                        logger.debug(message.get("message"))

            if checkin_success:
                previous_state = self.previous_state
                self.previous_state = new_state.copy()

                message = " [*] Checked in successfully: "
                for key, value in new_state.items():
                    if value != previous_state.get(key, None):
                        if value is True:
                            message = (
                                message
                                + click.style(f"{key}: ")
                                + click.style("💤")
                                + click.style(" ==> ✅ ", fg="green")
                            )
                        else:
                            message = (
                                message
                                + click.style(f"{key}: ")
                                + click.style("✅")
                                + click.style(" ==> 💤 ", fg="yellow")
                            )
                logger.info(message)
            else:
                message = "Failed to check in!"
                raise Exception(message)
            return result
        except client_exceptions.ClientConnectorError as exception:
            message = " [*] Failed to check in! "
            logger.error(message)
            raise exception

    @guard
    def get_hardware_list(
        self, fingerprint: Optional[str] = None, slug: Optional[str] = None
    ):
        query = gql(hardware_list)

        filters = {}
        if fingerprint:
            filters["fingerprint"] = {"exact": fingerprint}
        if slug:
            filters["slug"] = {"exact": slug}

        variables = {
            "first": 1,
            "filters": filters,
        }
        result = self.primitive.session.execute(
            query, variable_values=variables, get_execution_result=True
        )
        return result

    def get_own_hardware_details(self):
        hardware_list_result = self.get_hardware_list(
            fingerprint=self.primitive.host_config.get("fingerprint")
        )
        hardware = (
            hardware_list_result.data.get("hardwareList").get("edges")[0].get("node")
        )
        return hardware

    def get_hardware_from_slug_or_id(self, hardware_identifier: str):
        is_id = False
        is_slug = False
        # first check if the hardware_identifier is a slug or ID
        try:
            type_name, id = from_base64(hardware_identifier)

            is_id = True
            if type_name == "Hardware":
                is_hardware_type = True
            else:
                raise Exception(
                    f"ID was not for Hardware, you supplied an ID for a {type_name}"
                )

        except ValueError:
            is_slug = True

        hardware = None

        if is_id and is_hardware_type:
            hardware_list_result = self.get_hardware_list(slug=hardware_identifier)
            if edges := hardware_list_result.data["hardwareList"]["edges"]:
                hardware = edges[0]["node"]
            else:
                raise Exception(f"No hardware found with slug {hardware_identifier}")
        elif is_slug:
            hardware_list_result = self.get_hardware_list(slug=hardware_identifier)
            if edges := hardware_list_result.data["hardwareList"]["edges"]:
                hardware = edges[0]["node"]
            else:
                raise Exception(f"No hardware found with slug {hardware_identifier}")

        return hardware
