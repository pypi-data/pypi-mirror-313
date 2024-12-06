import click
from genopen.commands.create import create_command
from genopen.commands.add import add_command
from genopen.commands.build import build_command


@click.group()
def cli():
    """
    Genopen CLI - A blog generator.
    """
    pass


cli.add_command(create_command)
cli.add_command(add_command)
cli.add_command(build_command)

if __name__ == "__main__":
    cli()
