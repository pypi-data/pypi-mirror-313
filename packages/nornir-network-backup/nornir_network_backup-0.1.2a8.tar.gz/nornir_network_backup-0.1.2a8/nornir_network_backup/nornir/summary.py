import logging
import sys
from pathlib import Path
from prettytable import PrettyTable

import click
from nornir.core.filter import F
from ruamel.yaml import YAML
import json

from nornir_network_backup.models.models import BackupNornirUserParams
from nornir_network_backup.nornir.config import init_user_defined_config
from nornir_network_backup.nornir.tasks.backup_config import task_backup_config
from nornir_network_backup.nornir.utils import (
    _apply_inventory_transformation,
    _init_nornir,
    add_host_to_nornir_inventory,
)

logger = logging.getLogger(__name__)

CONNECTION_NAME = "netmiko"


PRETTYTABLE = {
    "show_ip_interface_brief": {
        "field_names": [
            "intf",
            "ipaddr",
            "status",
            "proto",
            "ifdescr",
        ]
    },
    "show_product-info-area": {
        "field_names": [
            "product_name",
            "serial",
            "mac",
        ]
    },
    "show_system_status": {
        "field_names": [
            "serial",
            "software",
            "boot_version",
            "version",
            "restarted",
            "reload_reason",
        ]
    },
    "show_reboot_counters": {
        "field_names": [
            "hardware_reset",
            "power_fail_detection",
            "total_software_reboots",
            "system_defense",
            "generic_software_reboot",
            "admin_requested_reboot",
            "spurious_power_fails",
        ]
    },
    "show_isdn_active": {
        "field_names": [
            "app",
            "call_id",
            "call_ref",
            "port",
            "bchannel",
            "call_type",
            "calling_nbr",
            "called_nbr",
            "duration",
        ]
    },
    "show_voice_voice-port_all": {
        "field_names": [
            "port",
            "lp",
            "sense",
            "if_state",
            "vp_state",
        ]
    },
    "show_voice_voice-port_pri_all": {
        "field_names": [
            "port",
            "physical_type",
            "proto_descriptor",
            "config_state",
            "loop_state",
            "framing",
            "l1_status",
            "l2_status",
            "nbr_voice_communication",
            "outgoing_calls",
            "outgoing_failures",
            "incoming_calls",
            "incoming_failures",
        ]
    },
    "show_system_secure-crashlog": {
        "field_names": [
            "uptime",
            "crash_time",
            "crash_filename",
            "coredump_file",
            "crash_caused_by",
            "restarted",
            "reload_reason",
            "core_generated_by",
        ]
    },
}


def get_facts(folder, hostname, cmd):
    fact_file = f"{folder}/{hostname}-{cmd}.yaml"
    if not Path(fact_file).exists():
        return None
    try:
        # default, if not specfied, is 'rt' (round-trip)
        with open(fact_file) as f:
            yaml = YAML(typ="safe")
            data = yaml.load(f)
        if data:
            # return json.dumps(data, indent=4)
            return data
    except Exception:
        return False


def print_summary(nr):
    """print the summary data of the CPE"""
    commands = [
        "show_ip_interface_brief",
        "show_product-info-area",
        "show_system_status",
        "show_reboot_counters",
        "show_isdn_active",
        "show_voice_voice-port_all",
        "show_voice_voice-port_pri_all",
        "show_system_secure-crashlog",
    ]
    for _host in nr.inventory.hosts:
        host = nr.inventory.hosts[_host]
        hostname = host.name.lower()
        print("\n\n")
        print("*" * 100)
        print(hostname)
        print("*" * 100)

        for cmd in commands:
            data = get_facts(nr.config.user_defined["facts"]["folder"], hostname, cmd)
            if not data:
                continue

            print(f"\n{cmd}:")

            if cmd not in PRETTYTABLE:
                print(json.dumps(data, indent=4))
                continue

            pt = PrettyTable()
            pt.field_names = PRETTYTABLE[cmd]["field_names"]

            if type(data) is list:
                for _row in data:
                    row = []
                    for col in pt.field_names:
                        val = _row.get(col, "")
                        val = ",".join(val) if type(val) is list else val
                        row.append(val)
                    pt.add_row(row)
            elif type(data) is dict:
                row = []
                for col in pt.field_names:
                    val = _row.get(col, "")
                    val = ",".join(val) if type(val) is list else val
                    row.append(val)
                pt.add_row(row)

            print(pt)


def nr_summary(
    username: str,
    password: str,
    host_list: list,
    group_list: list,
    config_file: str = None,
    platform: str = None,
    verbose=None,
    dryrun=False,
):
    """Starts the backup process for many hosts based on nornir filtering:

    if all_hosts is True => use all hosts, regardless if host_list or group_list is defined
    """

    nr = _init_nornir(
        config_file=config_file,
        regenerate_hostsfile=False,
        gather_facts=True,
    )

    # overriding some of the config parameters
    nr.config.user_defined.setdefault("textfsm", {})
    nr.config.user_defined.setdefault("facts", {})
    nr.config.user_defined.setdefault("backup_config", {})
    nr.config.user_defined["backup_config"].setdefault("reports", {})
    nr.config.user_defined["textfsm"]["enabled"] = True
    nr.config.user_defined["facts"]["enabled"] = True
    nr.config.user_defined["facts"]["folder"] = str(Path("~/.nnb/").expanduser())
    nr.config.user_defined["backup_config"]["reports"].setdefault("summary", {})
    nr.config.user_defined["backup_config"]["reports"].setdefault("details", {})
    nr.config.user_defined["backup_config"]["reports"]["summary"]["enabled"] = True
    nr.config.user_defined["backup_config"]["reports"]["details"]["enabled"] = True
    nr.config.user_defined["backup_config"]["save_config_diff"] = False
    nr.config.user_defined["backup_config"]["folder"] = str(
        Path("~/.nnb/").expanduser()
    )

    validated_config = BackupNornirUserParams(**nr.config.user_defined)
    # print(validated_config.dict())

    init_user_defined_config(nr)

    _filter = []

    for host in host_list:
        _filter.append(
            f"F(name__eq='{host.lower()}') | F(hostname__eq='{host.lower()}')"
        )

    for group in group_list:
        _filter.append(f"F(groups__contains='{group.lower()}')")

    if _filter:
        nr_filtered = nr.filter(eval("|".join(_filter)))
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

    if not nr_filtered.inventory.hosts:
        raise click.UsageError("no hosts found to process - exit script\n")

    print(
        f"Get info on {len(nr_filtered.inventory.hosts)} host(s): {[ str(h) for h in nr_filtered.inventory.hosts]}"
    )

    if dryrun:
        print(
            "dryrun mode is enabled - we will not connect to any devices, output will be generated on files that may exist"
        )

    # run_backup_process(nr_filtered, nr)

    if not dryrun:
        result = nr_filtered.run(
            task=task_backup_config,
            user_config=nr.config.user_defined,
        )

        if result.failed:
            print(f"ERROR fetching data from these hosts: {result.failed_hosts}")

        logger.debug("closing nornir connections")
        nr_filtered.close_connections()

    print_summary(nr_filtered)
