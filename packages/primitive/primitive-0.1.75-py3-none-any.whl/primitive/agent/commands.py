import click
import typing

if typing.TYPE_CHECKING:
    from ..client import Primitive


@click.command("agent")
@click.pass_context
def cli(context):
    """agent"""
    primitive: Primitive = context.obj.get("PRIMITIVE")
    primitive.agent.execute()
