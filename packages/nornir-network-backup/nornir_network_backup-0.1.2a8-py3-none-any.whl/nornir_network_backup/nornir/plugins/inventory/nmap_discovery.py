"""Nornir inventory plugin
This uses the output of the nmap network discovery output.

Expected format: comma separated CSV file with at least the following fields
    - hostname  (ex. routerA)
        - user friendly name
    - enterprise  (ex. ciscoSystems)
        - Ciena Corporation
        - ciscoSystems
        - OneAccess
    - os_slug  (ex. ios-xr)
        - ciena-generic
        - ios-generic
        - ios-xe
        - ios-xr
        - oneos-generic
        - oneos5
        - oneos6
        - saos6
    - sysObjectId (ex. .1.3.6.1.3.9.1)
    - sysLocation (ex. Office A)
    - mgmt_ip  (ex. 1.2.3.4)
    - physSerial  (ex. 123123abcdabcd)
    - physSoftware (ex. 15.3(3)M6)
    - physDescription (ex. C887VAM-K9) 
    - physName   (ex. C887VAM-K9 chassis_ Hw Serial#:  .....)
    - physModel  (ex. C887VAM-K9)
    - communities (ex. public)


_key,_updates,hostname,status,telnet,ssh,snmp,bgp,enterprise,os_slug,mgmt_ip,mgmt_safe,sysObjectId,sysContact,sysLocation,sysUpTime,physSerial,physSoftware,physDescription,physName,physModel,ip,communities
00009-SAS51-012,0,00009-SAS51-012,up,open,open,open,closed,Ciena Corporation,saos6,10.8.90.22,1,1.3.6.1.4.1.6141.1.96,Orange Belgium,Belgium,176d01h52m28.19s (1521314819 timeticks),M8686648,saos-06-18-00-0200,5142 Service Aggregation Switch,5142,,10.8.90.22,public
ipgsolution01-16leu-ci.as47377.net,0,ipgsolution01-16leu-ci,up,closed,open,open,open,OneAccess,oneos5,94.104.128.174,1,1.3.6.1.4.1.13191.1.1.320,,,408d17h06m8.45s (3531276845 timeticks),S1948007796154862,ONEOS92-DUAL_FT-V5.2R2E7_HA8,LBB_320,MB92SFPENW+R,LBB_320,94.104.128.174,5pr1t5
jvp01-84roc-01.as47377.net,0,jvp01-84roc-01,up,closed,open,open,open,OneAccess,oneos5,94.105.3.144,1,1.3.6.1.4.1.13191.1.1.4,,,121d19h45m18.90s (1052551890 timeticks),T1938008109107928,ONEOS90-MONO_FT-V5.2R2E7_HA8,LBB_4G+,MB90Ss0UFPE0SNWsd+xG,LBB_4G+,94.105.3.144,5pr1t5
euroshoe02-31aal-01.as47377.net,0,euroshoe02-31aal-01,up,open,open,open,closed,ciscoSystems,ios-xe,94.105.3.106,1,1.3.6.1.4.1.9.1.1856,,,222d18h51m10.38s (1924867038 timeticks),FCZ2046E0T0,15.3(3)M6,C887VAM-K9,C887VAM-K9 chassis_ Hw Serial#: FCZ2046E0T0_ Hw Revision: 1.0,C887VAM-K9,94.105.3.106,5pr1t5
NOS-ASR-01.as47377.net,0,NOS-ASR-01,up,closed,open,open,closed,ciscoSystems,ios-xr,195.242.172.40,1,1.3.6.1.4.1.9.1.2390,,Belgium,447d16h23m26.90s (3867980690 timeticks),FOC2243P75J,7.1.1,A9K-RSP5-SE,ASR 9000 Route Switch Processor 5 for Service Edge 40G,A9K-RSP5-SE,195.242.172.40,53h3lth0nl13
"""


import csv
import logging
import pathlib
from typing import Any, Dict, Type
import re

import ruamel.yaml
from archive_rotator.algorithms import SimpleRotator
from archive_rotator.rotator import rotate
from nornir.core.inventory import (
    ConnectionOptions,
    Defaults,
    Group,
    Groups,
    Host,
    HostOrGroup,
    Hosts,
    Inventory,
    ParentGroups,
)
from nornir.plugins.inventory.simple import SimpleInventory

logger = logging.getLogger(__name__)

# maps the os_slug field to the netmiko platform
MAP_OS_SLUG_TO_PLATFORM = {
    "ciena-generic": "ciena_saos",
    "saos6": "ciena_saos",
    "ios-xe": "cisco_ios",
    "ios-xr": "cisco_xr",
    "ios-generic": "cisco_ios",
    "oneos5": "oneaccess_oneos",
    "oneos6": "oneaccess_oneos",
    "oneos-generic": "oneaccess_oneos",
}

# maps enterprise to vendor
MAP_ENTERPRISE_TO_VENDOR = {
    "Ciena Corporation": "ciena",
    "ciscoSystems": "cisco",
    "Juniper Networks_ Inc.": "juniper",
    "OneAccess": "oneaccess",
}


class NMAPDiscoveryInventory(SimpleInventory):
    def __init__(
        self,
        nmap_discovery_file: str,
        host_file: str = "hosts.yaml",
        group_file: str = "groups.yaml",
        defaults_file: str = "defaults.yaml",
        encoding: str = "utf-8",
        backups: int = 0,
        regenerate: bool = True,
        exception_if_group_not_exists: bool = False,
        map_ip_to_function: list[dict] = [],
    ) -> None:
        """
        NMAPDiscoveryInventory is an inventory plugin that generates the hosts file
        dynamically based on a CSV file. Once the hosts.yaml is generated then the
        SimpleInventory plugin is called to generate the inventory.

        The YAML files follow the same structure as the native objects
        Args:
            nmap_discovery_file: path to the nmap discovery file in CSV format
            host_file: path to file with hosts definition
            group_file: path to file with groups definition. If
                it doesn't exist it will be skipped
            defaults_file: path to file with defaults definition.
                If it doesn't exist it will be skipped
            encoding: Encoding used to save inventory files. Defaults to utf-8
            backups: Make backup files and keep "backups" amount of historical files
            regenerate: if True then always regenerate the hosts file, otherwise skip it
                        if the hosts already exists
            exception_if_group_not_exists: if false and a group does not exist then it will not be
                        added to the host and no error will be generated
        """
        self.nmap_discovery_file = pathlib.Path(
            nmap_discovery_file
        ).expanduser()
        self.host_file = pathlib.Path(host_file).expanduser()
        self.group_file = pathlib.Path(group_file).expanduser()
        self.defaults_file = pathlib.Path(defaults_file).expanduser()
        self.encoding = encoding
        self.backups = backups
        self.regenerate = regenerate
        self.exception_if_group_not_exists = exception_if_group_not_exists
        self.map_ip_to_function = map_ip_to_function

        if not self.host_file.exists() or self.regenerate:
            self.generate_hosts_from_csv()

        super().__init__(
            host_file=self.host_file,
            group_file=self.group_file,
            defaults_file=self.defaults_file,
            encoding=self.encoding,
        )

    def generate_hosts_from_csv(self):
        """
        This will generate the hosts dict based ont the inventory file. This hosts
        file is the loaded by the standard SimpleInventory plugin.

        The groups will be added but it's expected that these groups exist in the
        groups.yaml file.
        If they don't exist then they will not be added to the host unless the option
        exception_if_group_not_exists is set to True in which case the hosts are added
        but execution of the script will fail until all groups are defined.


        dops-lab-02:
            hostname: 94.105.12.148
            platform: oneaccess_oneos
            data:
                cmd_facts:
                - show ip vrf brief
            groups:
                - oneaccess_oneos
                - lbb_320
        """
        yaml = ruamel.yaml.YAML(typ="safe")
        hosts = dict()

        logger.info(
            f"generating hosts.yaml from nmap CSV file '{self.nmap_discovery_file}'"
        )
        with open(self.nmap_discovery_file, newline="\n") as csvfile:
            discovery_reader = csv.DictReader(
                csvfile, delimiter=",", quotechar='"'
            )
            for row in discovery_reader:
                hostname = (row["hostname"] or row["mgmt_ip"]).lower()
                platform = MAP_OS_SLUG_TO_PLATFORM.get(row["os_slug"])
                enterprise = row["enterprise"]
                vendor = MAP_ENTERPRISE_TO_VENDOR.get(enterprise)
                hwtype = row["physModel"] or row["physName"]
                hwcategory = (
                    "PBXPLUG"
                    if hwtype and "pbxplug" in hwtype.lower()
                    else None
                )
                groups = [
                    grp.lower()
                    for grp in [
                        platform,
                        row["os_slug"],
                        hwtype,
                        vendor,
                        hwcategory,
                    ]
                    if grp
                ]
                # generate groups based on ip address if map_ip_to_function is specified
                if row["mgmt_ip"] and self.map_ip_to_function:
                    for rec in self.map_ip_to_function:
                        if re.match(rec["regex"], row["mgmt_ip"]) and rec["function"]:
                            groups.append(rec["function"].lower())
                            if row["os_slug"]:
                                groups.append(f"{platform}-{rec['function'].lower()}")
                data = dict(
                    communities=row.get("communities", "").split("|"),
                    serial=row["physSerial"],
                    sysobjid=row["sysObjectId"],
                    software=row["physSoftware"],
                    mgmt_ip=row["mgmt_ip"],
                    other_ip=row.get("ip", "").split("|"),
                )
                if enterprise:
                    data["enterprise"] = enterprise
                if vendor:
                    data["vendor"] = vendor
                if hwtype:
                    data["hwtype"] = hwtype
                if row["os_slug"]:
                    data["os_slug"] = row["os_slug"]
                if hwcategory:
                    data["hwcategory"] = hwcategory
                record = dict(
                    hostname=row["mgmt_ip"], groups=groups, data=data
                )
                if platform:
                    record["platform"] = platform
                hosts[hostname] = record

        self.validate_host_groups(hosts)

        if self.backups and pathlib.Path(self.host_file).exists():
            rotate(SimpleRotator(self.backups), self.host_file)

        with open(self.host_file, mode="wt", encoding=self.encoding) as file:
            yaml.dump(hosts, file)

    def validate_host_groups(self, hosts: dict):
        """Reads an existing groups file and checks if all the generated host groups exist.
        If they don't exist and exception_if_group_not_exists is True then an exception is thrown.
        If they don't exist and exception_if_group_not_exists is False then the group will be removed
        from the host
        """
        missing_groups = []

        groups = dict()
        if self.group_file.exists():
            with open(self.group_file, "r") as f:
                yml = ruamel.yaml.YAML(typ="safe")
                groups = yml.load(f)

        # logger.debug(groups)

        for host in hosts:
            has_missing_groups = False
            _groups = []
            for grp in hosts[host]["groups"]:
                if grp not in groups:
                    has_missing_groups = True
                    missing_groups.append(grp)
                else:
                    _groups.append(grp)
            if has_missing_groups and not self.exception_if_group_not_exists:
                hosts[host]["groups"] = _groups

        if missing_groups:
            logger.warning(
                f"Groups are used but not defined in '{self.group_file}' : {set(missing_groups)}"
            )
            missing_config = "\n".join(
                [f"{grp}: {{}}" for grp in set(missing_groups)]
            )
            logger.warning(f"Add device groups:\n{missing_config}")
