import typing
from time import sleep

from primitive.graphql.relay import from_base64

if typing.TYPE_CHECKING:
    pass

from typing import List, Optional

from gql import gql

from primitive.utils.actions import BaseAction

from ..utils.auth import guard
from .graphql.mutations import reservation_create_mutation, reservation_release_mutation
from .graphql.queries import reservation_query, reservations_query


class Reservations(BaseAction):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @guard
    def get_reservations(
        self,
        status: str = "in_progress",
    ):
        query = gql(reservations_query)

        filters = {}
        if status:
            filters["status"] = {"exact": status}

        variables = {
            "filters": filters,
        }
        result = self.primitive.session.execute(
            query, variable_values=variables, get_execution_result=True
        )
        return result

    @guard
    def get_reservation(self, reservation_id: str):
        query = gql(reservation_query)

        variables = {
            "id": reservation_id,
        }

        result = self.primitive.session.execute(
            query, variable_values=variables, get_execution_result=True
        )
        return result

    @guard
    def create_reservation(
        self,
        reason: str,
        requested_hardware_ids: Optional[List[str]] = None,
        organization_id: Optional[str] = None,
        hardware_identifier: Optional[str] = None,
    ):
        mutation = gql(reservation_create_mutation)

        if hardware_identifier and not requested_hardware_ids:
            hardware = self.primitive.hardware.get_hardware_from_slug_or_id(
                hardware_identifier=hardware_identifier
            )
            requested_hardware_ids = [hardware["id"]]

        if not organization_id:
            whoami_result = self.primitive.auth.whoami()
            default_organization = whoami_result.data["whoami"]["defaultOrganization"]
            organization_id = default_organization["id"]

        input = {
            "requestedHardwareIds": requested_hardware_ids,
            "reason": reason,
            "organizationId": organization_id,
        }

        variables = {"input": input}
        result = self.primitive.session.execute(
            mutation, variable_values=variables, get_execution_result=True
        )
        return result

    @guard
    def release_reservation(self, reservation_or_hardware_identifier: str):
        mutation = gql(reservation_release_mutation)
        try:
            # check if it is a base64 encoded id
            type_name, _id = from_base64(reservation_or_hardware_identifier)
            if type_name == "Reservation":
                reservation_id = reservation_or_hardware_identifier
            elif type_name == "Hardware":
                hardware = self.primitive.hardware.get_hardware_from_slug_or_id(
                    hardware_identifier=reservation_or_hardware_identifier
                )
                reservation_id = hardware["activeReservation"]["id"]
        except ValueError:
            # if not, its a string and check for it here
            hardware = self.primitive.hardware.get_hardware_from_slug_or_id(
                hardware_identifier=reservation_or_hardware_identifier
            )
            reservation_id = hardware["activeReservation"]["id"]

        input = {
            "reservationId": reservation_id,
        }
        variables = {"input": input}
        result = self.primitive.session.execute(
            mutation, variable_values=variables, get_execution_result=True
        )
        return result

    @guard
    def wait_for_reservation_status(self, reservation_id: str, desired_status: str):
        reservation_result = self.get_reservation(reservation_id=reservation_id)
        reservation = reservation_result.data["reservation"]
        current_status = reservation["status"]

        sleep_amount = 1
        while current_status != desired_status:
            reservation_result = self.get_reservation(reservation_id=reservation_id)
            reservation = reservation_result.data["reservation"]
            current_status = reservation["status"]
            if current_status == desired_status:
                break
            sleep(sleep_amount)
            sleep_amount += 1

        return reservation
