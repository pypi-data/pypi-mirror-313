import os
from typing import Optional
from nornir.core.inventory import Host
from nornir.core import Nornir


def load_credentials(
    host: Host,
    username: Optional[str] = None,
    password: Optional[str] = None,
    platform: Optional[str] = None,
) -> None:
    """
    load_credentials is an transform_functions to add credentials to every host.
    Environment variables `NORNIR_USERNAME` and `NORNIR_PASSWORD` or arguments can be used.
    Args:
        username: Device username
        password: Device password
        platform: Device platform
    """
    username = username if username is not None else os.getenv("NORNIR_USERNAME")
    if username is not None:
        host.username = username
    password = password if password is not None else os.getenv("NORNIR_PASSWORD")
    if password is not None:
        host.password = password
    if platform is not None:
        host.platform = platform


def transform_consolidate_fact_commands(nr: Nornir) -> Nornir:
    """this is an inventory transform function that adds a new Host inventory attribute: consolidated_fact_commands
    This attribute has all the fact commands that should be run for this host and is derived from
    the host + group "cmd_facts" extended data

    Commands starting with a ^ will not be executed for this host
    """
    for host in nr.inventory.hosts.values():
        fact_commands = [cmd for cmd in host.extended_data().get("cmd_facts", [])]

        for grp in host.groups:
            fact_commands += [cmd for cmd in grp.extended_data().get("cmd_facts", [])]

        fact_commands = list(set(fact_commands))

        do_not_execute_commands = [cmd for cmd in fact_commands if cmd.startswith("^")]

        fact_commands = [
            cmd
            for cmd in fact_commands
            if not cmd.startswith("^") and f"^{cmd}" not in do_not_execute_commands
        ]

        host["consolidated_fact_commands"] = fact_commands

    return nr
