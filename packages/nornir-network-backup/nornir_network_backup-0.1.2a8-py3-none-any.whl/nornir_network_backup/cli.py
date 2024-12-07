import os

import click

from nornir_network_backup.nornir import nr_backup, nr_summary


@click.group
def base():
    """Base entry for click"""


@click.command(name="backup")
@click.option(
    "-u",
    "--user",
    prompt=False,
    default=lambda: os.environ.get("USER", ""),
    type=str,
    required=False,
    help="Username",
)
@click.password_option(
    "-p",
    "--password",
    prompt=False,
    confirmation_prompt=False,
    type=str,
    required=False,
    help="Password",
)
@click.option(
    "--all",
    "all_hosts",
    default=False,
    is_flag=True,
    help="Take a backup of all hosts in the hosts.yaml inventory",
)
@click.option(
    "--host",
    "-h",
    "host_list",
    multiple=True,
    help="Take a backup of one host. This command can be repeated to include multiple hosts. The host has to exist in the inventory.",
)
@click.option(
    "--group",
    "-g",
    "group_list",
    multiple=True,
    help="Take a backup of all the hosts of one group. This command can be repeated to include multiple groups. The group has to exist in the inventory.",
)
@click.option(
    "--regenerate-hosts/--no-regenerate-hosts",
    "regenerate_hosts",
    default=None,
    help="Enable or disable re-generation of hosts.yaml file if the NMAPDiscoveryInventory inventory plugin is installed, this overrides the settings from the main config file",
)
@click.option(
    "--facts/--no-facts",
    "facts",
    default=None,
    help="Disable gathering extra facts, this overrides settings from the main config file",
)
@click.option(
    "--oneaccess",
    "driver",
    flag_value="oneaccess_oneos",
    help="Driver for OneAccess OneOS devices",
)
@click.option(
    "--cisco-ios-xe",
    "driver",
    flag_value="cisco_ios",
    help="Driver for Cisco IOS-XE devices",
)
@click.option(
    "--cisco-ios-xr",
    "driver",
    flag_value="cisco_xr",
    help="Driver for Cisco IOS-XR devices",
)
@click.option(
    "--ciena-saos",
    "driver",
    flag_value="ciena_saos",
    help="Driver for Ciena SAOS devices",
)
@click.option(
    "-c",
    "--config-file",
    default="config-nnb.yaml",
    type=str,
    required=False,
    help="Specifiy the location of main nornir config file, default = config.yaml",
)
@click.option("-v", "--verbose", count=True)
@click.option(
    "--dryrun/--no-dryrun",
    "dryrun",
    default=False,
    help="If enabled then the hosts are printed but the backup process will not start",
)
def backup_command(
    all_hosts,
    host_list,
    group_list,
    user,
    password,
    regenerate_hosts,
    facts,
    driver,
    verbose,
    config_file,
    dryrun,
):
    """Backup many hosts. All hosts HAVE to exist in the hosts.yaml file and filters may be used on existing host or
    groups or you can provide a valid Nornir F() filter string.

    The username and password may be provided but they're not required, then can also be set in one of the configuration
    files or provided via environment variable.

    The hosts.yaml file will be regenerated automatically by default if the NMAPDiscoveryInventory inventory plugin is used.
    """

    if not (all_hosts or host_list or group_list):
        raise click.UsageError(
            "Please provide a host, group or nornir filter or explicitly add the --all parameter\n"
        )

    click.echo("Starting backup process")

    nr_backup(
        user,
        password,
        all_hosts=all_hosts,
        host_list=host_list,
        group_list=group_list,
        regenerate_hostsfile=regenerate_hosts,
        gather_facts=facts,
        config_file=config_file,
        platform=driver,
        verbose=verbose,
        dryrun=dryrun,
    )


# SUMMARY COMMAND
# -----------------
# Generates the summary details of one or more CPE's
# For example for PBXPLUG devices it will give the
# VOIP call details
@click.command(name="summary")
@click.option(
    "-u",
    "--user",
    prompt=True,
    default=lambda: os.environ.get("USER", ""),
    type=str,
    required=True,
    help="Username",
)
@click.password_option(
    "-p",
    "--password",
    prompt=True,
    confirmation_prompt=False,
    type=str,
    required=True,
    help="Password",
)
@click.option(
    "--host",
    "-h",
    "host_list",
    multiple=True,
    help="Generate a summary for one host. This command can be repeated to include multiple hosts. The host has to exist in the inventory.",
)
@click.option(
    "--group",
    "-g",
    "group_list",
    multiple=True,
    help="Take a backup of all the hosts of one group. This command can be repeated to include multiple groups. The group has to exist in the inventory.",
)
@click.option(
    "--oneaccess",
    "driver",
    flag_value="oneaccess_oneos",
    help="Driver for OneAccess OneOS devices",
)
@click.option(
    "--cisco-ios-xe",
    "driver",
    flag_value="cisco_ios",
    help="Driver for Cisco IOS-XE devices",
)
@click.option(
    "--cisco-ios-xr",
    "driver",
    flag_value="cisco_xr",
    help="Driver for Cisco IOS-XR devices",
)
@click.option(
    "--ciena-saos",
    "driver",
    flag_value="ciena_saos",
    help="Driver for Ciena SAOS devices",
)
@click.option(
    "-c",
    "--config-file",
    default="config-nnb.yaml",
    type=str,
    required=False,
    help="Specifiy the location of main nornir config file, default = config.yaml",
)
@click.option("-v", "--verbose", count=True)
@click.option(
    "--dryrun/--no-dryrun",
    "dryrun",
    default=False,
    help="If enabled then the hosts are printed but the backup process will not start",
)
def summary_command(
    host_list,
    group_list,
    user,
    password,
    driver,
    verbose,
    config_file,
    dryrun,
):
    """Generate summary info for one ore more hosts.
    All hosts HAVE to exist in the hosts.yaml file and filters may be used on existing host or groups.

    The username and password have to be provided.

    All files will be saved in a temp folder in your home drive ~/.nnb/<host>
    """

    if not (host_list or group_list):
        raise click.UsageError("Please provide a host or group\n")

    click.echo("Starting summary process")

    nr_summary(
        user,
        password,
        host_list=host_list,
        group_list=group_list,
        config_file=config_file,
        platform=driver,
        verbose=verbose,
        dryrun=dryrun,
    )


base.add_command(backup_command)
base.add_command(summary_command)


if __name__ == "__main__":
    base()
