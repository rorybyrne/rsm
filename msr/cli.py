"""Entry point for the CLI

@author Rory Byrne <rory@rory.bio>
"""
import click
from msr.commands.measure import measure
from msr.commands.register import register
from msr.commands.race import race
from msr.commands.version import version


@click.group()
def msr():
    """CLI entry point"""
    pass

msr.add_command(version)
msr.add_command(register)
msr.add_command(measure)
msr.add_command(race)
