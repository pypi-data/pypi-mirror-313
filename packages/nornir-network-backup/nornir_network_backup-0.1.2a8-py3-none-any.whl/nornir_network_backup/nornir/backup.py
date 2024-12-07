import datetime
import logging
import sys

import click
from nornir.core.filter import F
from nornir_inspect import nornir_inspect
from nornir_network_backup.nornir.utils import (
    _init_nornir,
    add_host_to_nornir_inventory,
    _apply_inventory_transformation,
    _apply_transform_consolidate_fact_commands,
)

from nornir_network_backup.nornir.config import init_user_defined_config
from nornir_network_backup.models.models import BackupNornirUserParams
from nornir_network_backup.nornir.report import print_results_csv
from nornir_network_backup.nornir.tasks.backup_config import task_backup_config
from nornir_network_backup.nornir.utils import rename_failed_hosts_backup_file

logger = logging.getLogger(__name__)

CONNECTION_NAME = "netmiko"


def run_backup_process(nr, nr_unfiltered):

    backup_start_time = datetime.datetime.now()

    logger.info(f"--- START BACKUP PROCESS FOR {len(nr.inventory.hosts)} HOSTS ---")
    print(
        "-" * 50
        + f"\n--- START BACKUP PROCESS FOR {len(nr.inventory.hosts)} HOSTS ---\n"
        + "-" * 50
    )

    result = nr.run(
        task=task_backup_config,
        user_config=nr.config.user_defined,
    )

    rename_failed_hosts_backup_file(
        result.failed_hosts, user_config=nr.config.user_defined
    )

    for failed_host in result.failed_hosts:
        # print(f"{failed_host}: FAILED")
        logger.error(f"FAILED HOST: {failed_host}")

    # print(nornir_inspect(result))

    backup_end_time = datetime.datetime.now()

    backup_duration = backup_end_time - backup_start_time

    nbr_processed_hosts = len(result.items())
    nbr_failed_hosts = len(result.failed_hosts)
    nbr_success_hosts = nbr_processed_hosts - nbr_failed_hosts

    # TOOD: why is the validated_config object not used ??
    min_success_rate = nr.config.user_defined["backup_config"]["reports"].get(
        "min_success_rate", 95
    )
    # consider the result a success if we exceed the expected configured success rate
    overall_success = (
        True
        if (
            not result.failed
            or (((nbr_success_hosts / nbr_processed_hosts) * 100) >= min_success_rate)
        )
        else False
    )

    logger.info(
        f"--- {nbr_success_hosts} FINISHED IN {backup_duration.total_seconds()} SECONDS, {nbr_failed_hosts} FAILED ---"
    )
    print(
        "-" * 50
        + f"\n--- {nbr_success_hosts} FINISHED, {nbr_failed_hosts} FAILED IN {backup_duration.total_seconds()} SECONDS ---\n"
        + "-" * 50
    )

    # TODO: parameterize

    print_results_csv(
        nr.config.user_defined["backup_config"]["reports"]["summary"]["filename"],
        nr.config.user_defined["backup_config"]["reports"]["details"]["filename"],
        result,
        append_summary=nr.config.user_defined["backup_config"]["reports"]["summary"][
            "append"
        ],
        append_details=nr.config.user_defined["backup_config"]["reports"]["details"][
            "append"
        ],
        overall_success=overall_success,
        **dict(
            starttime=backup_start_time,
            stoptime=backup_end_time,
            total_host_cnt=len(nr.inventory.hosts),
            filtered_host_cnt=len(nr_unfiltered.inventory.hosts),
        ),
    )


def nr_backup(
    username: str,
    password: str,
    all_hosts: bool,
    host_list: list,
    group_list: list,
    regenerate_hostsfile: bool,
    gather_facts: bool,
    config_file: str = None,
    platform: str = None,
    verbose=None,
    dryrun=False,
):
    """Starts the backup process for many hosts based on nornir filtering:

    if all_hosts is True => use all hosts, regardless if host_list or group_list is defined
    """

    if dryrun:
        print("dryrun mode is enabled - hosts.yaml file will not be re-generated")
        regenerate_hostsfile = False

    nr = _init_nornir(
        config_file=config_file,
        regenerate_hostsfile=regenerate_hostsfile,
        gather_facts=gather_facts,
    )

    init_user_defined_config(nr)

    validated_config = BackupNornirUserParams(**nr.config.user_defined)

    _filter = []

    for host in host_list:
        _filter.append(
            f"F(name__eq='{host.lower()}') | F(hostname__eq='{host.lower()}')"
        )

    for group in group_list:
        _filter.append(f"F(groups__contains='{group.lower()}')")

    if _filter:
        nr_filtered = nr.filter(eval("|".join(_filter)))
    elif all_hosts:
        nr_filtered = nr.filter(~F(platform__eq=""))
    else:
        raise Exception("Please provide a nornir filter")

    # if there are any hosts that don't exist then we will add them
    # dynmically to the inventory but in that case the platform should
    # be added manually
    if host_list and not nr_filtered.inventory.hosts:
        for hostname in host_list:
            logger.info(
                f"-- host {hostname} was not found in the inventory, we will create an entry"
            )
            nr.inventory.hosts[hostname] = add_host_to_nornir_inventory(
                hostname, hostname, username, password, platform
            )
            nr.inventory.hosts[hostname].defaults = nr.inventory.defaults
            grp = nr.inventory.groups.get(platform)
            if grp:
                nr.inventory.hosts[hostname].groups.add(grp)

        nr_filtered = nr.filter(eval("|".join(_filter)))

    # add username + password + platform to each host
    _apply_inventory_transformation(
        nr_filtered, username=username, password=password, platform=platform
    )

    # add consolidated_fact_commands to each host
    nr_filtered = _apply_transform_consolidate_fact_commands(nr_filtered)

    if not nr_filtered.inventory.hosts:
        raise click.UsageError("no hosts found to process - exit script\n")

    print(
        f"starting backup for {len(nr_filtered.inventory.hosts)} hosts: {[ str(h) for h in nr_filtered.inventory.hosts]}"
    )

    if dryrun:
        print("dryrun mode is enabled - backup will not be started")
        sys.exit()

    run_backup_process(nr_filtered, nr)

    logger.debug("closing remaining nornir connections")
    nr_filtered.close_connections()
