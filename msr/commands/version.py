"""Version command

@author Rory Byrne <rory@rory.bio>
"""
import sys
import click
from click._compat import iteritems


@click.command()
def version():
    """Returns the current version of the tool

    Checks all installed packages and finds the msr package, then prints its version.

    Shamelessly adapted from click.version_option()
    """
    module = 'msr'
    ver = None

    try:
        import pkg_resources
    except ImportError:
        pass
    else:
        for dist in pkg_resources.working_set:
            scripts = dist.get_entry_map().get("console_scripts") or {}
            for _, entry_point in iteritems(scripts):
                if entry_point.module_name.startswith(module):
                    ver = dist.version
                    break
    if ver is None:
        raise RuntimeError("Could not determine version")

    print(ver)
