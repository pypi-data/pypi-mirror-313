import typing

import click

from ..utils.printer import print_result

if typing.TYPE_CHECKING:
    from ..client import Primitive


@click.group()
@click.pass_context
def cli(context):
    """Hardware"""
    pass


@cli.command("systeminfo")
@click.pass_context
def systeminfo_command(context):
    """Get System Info"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    message = primitive.hardware.get_system_info()
    print_result(message=message, context=context)


@cli.command("register")
@click.pass_context
def register_command(context):
    """Register Hardware with Primitive"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.hardware.register()
    color = "green" if result else "red"
    if result.data.get("registerHardware"):
        message = "Hardware registered successfully"
    else:
        message = (
            "There was an error registering this device. Please review the above logs."
        )
    print_result(message=message, context=context, fg=color)


@cli.command("checkin")
@click.pass_context
def checkin_command(context):
    """Checkin Hardware with Primitive"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    check_in_http_result = primitive.hardware.check_in_http()
    if messages := check_in_http_result.data.get("checkIn").get("messages"):
        print_result(message=messages, context=context, fg="yellow")
    else:
        message = "Hardware checked in successfully"
        print_result(message=message, context=context, fg="green")


@cli.command("list")
@click.pass_context
def list_command(context):
    """List Hardware"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    get_hardware_list_result = primitive.hardware.get_hardware_list()
    message = get_hardware_list_result.data
    print_result(message=message, context=context)
