import click

from ..utils.printer import print_result
import typing

if typing.TYPE_CHECKING:
    from ..client import Primitive


@click.group()
@click.pass_context
def cli(context):
    """Daemon"""
    pass


@cli.command("install")
@click.pass_context
def install_daemon_command(context):
    """Install the full primitive daemon"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.daemons.install()
    print_result(message=result, context=context)


@cli.command("uninstall")
@click.pass_context
def uninstall_daemon_command(context):
    """Uninstall the full primitive Daemon"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.daemons.uninstall()
    print_result(message=result, context=context)


@cli.command("stop")
@click.pass_context
def stop_daemon_command(context):
    """Stop primitive Daemon"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.daemons.stop()
    message = "stopping primitive daemon"
    if context.obj["JSON"]:
        message = result
    print_result(message=message, context=context)


@cli.command("start")
@click.pass_context
def start_daemon_command(context):
    """Start primitive Daemon"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.daemons.start()
    message = "starting primitive daemon"
    if context.obj["JSON"]:
        message = result
    print_result(message=message, context=context)


@cli.command("logs")
@click.pass_context
def log_daemon_command(context):
    """Logs from primitive Daemon"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    result = primitive.daemons.logs()
    print_result(message=result, context=context)
