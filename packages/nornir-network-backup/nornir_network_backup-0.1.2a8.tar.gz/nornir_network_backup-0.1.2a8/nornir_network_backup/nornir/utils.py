import json
import os
from pathlib import Path

import click
import ruamel.yaml
from nornir import InitNornir
from nornir.core import Nornir
from nornir.core.inventory import Host
from nornir.core.plugins.inventory import (
    InventoryPluginRegister,
    TransformFunctionRegister,
)
from io import StringIO

from nornir_task_duration.plugins.processors import TaskDuration

from nornir_network_backup.nornir.plugins.inventory import (
    NMAPDiscoveryInventory,
    load_credentials,
    transform_consolidate_fact_commands,
)


def _init_nornir(
    config_file: str,
    regenerate_hostsfile: bool,
    gather_facts: bool,
):
    """Initiates the nornir object without applying any filters.
    Some parameters defined in the config file may be overwritten by
    CLI provided parameters.
    """

    # register extra plugins
    InventoryPluginRegister.register("NMAPDiscoveryInventory", NMAPDiscoveryInventory)
    TransformFunctionRegister.register("load_credentials", load_credentials)

    nornir_config = None

    with open(config_file, "r") as f:
        yml = ruamel.yaml.YAML(typ="safe")
        nornir_config = yml.load(f)

    if (
        regenerate_hostsfile is not None
        and nornir_config["inventory"]["plugin"] == "NMAPDiscoveryInventory"
    ):
        nornir_config["inventory"]["options"]["regenerate"] = regenerate_hostsfile

    if gather_facts is not None:
        nornir_config["user_defined"]["facts"]["enabled"] = gather_facts

    nr = InitNornir(**nornir_config)

    nr = nr.with_processors([TaskDuration()])

    return nr


def _apply_transform_consolidate_fact_commands(nr: Nornir) -> Nornir:
    """applies the inventory transformation that creates the "consolidated_fact_commands" argument
    holding all the fact commands that should be executed for the host
    """

    nr = transform_consolidate_fact_commands(nr)
    return nr


def _apply_inventory_transformation(
    nr, username: str = None, password: str = None, platform: str = None
):
    """adds username, password, platform to each nornir host"""

    transform_function = TransformFunctionRegister.get_plugin("load_credentials")
    for h in nr.inventory.hosts.values():
        transform_function(
            h,
            **(
                {
                    "username": username,
                    "password": password,
                    "platform": platform,
                }
                or {}
            ),
        )


def add_host_to_nornir_inventory(
    hostname: str, ip: str, username: str, password: str, platform: str
):
    """adds a host to the nornir inventory programatically"""
    if not platform:
        raise click.UsageError(
            "This host is not known in the database, you will have to provide the platform driver manually\n"
        )

    return Host(
        name=hostname,
        hostname=hostname,
        username=username,
        password=password,
        platform=platform,
    )


def generate_filename(
    filetype: str,
    hostname: str,
    user_config: dict,
    extension: str = None,
    command: str = None,
    remove_txt: bool = False,
):
    """convenience function that will generate the filename

    args:
        filetype: backup|diff|fact
        remove_txt: if the same file with .txt extension exists AND the new file
                    is a .yaml fact file, then remove the txt
    """
    config_backup_folder = user_config["backup_config"]["folder"]
    config_diff_folder = user_config["backup_config"]["config_diff_folder"]
    erase_existing_diff_file = user_config["backup_config"]["save_config_diff"]
    facts_folder = user_config["facts"]["folder"]
    hostname = str(hostname).lower()

    if filetype == "backup":
        return f"{config_backup_folder}/{hostname}-config.txt"

    if filetype == "diff":
        outputdir = config_diff_folder or config_backup_folder
        diff_file = os.path.join(outputdir, f"{hostname}.diff")
        if erase_existing_diff_file:
            remove_file(diff_file)
        return diff_file

    if filetype == "fact":
        cmd_nice = command.replace(" ", "_").replace("|", "_")
        output_dir = facts_folder or config_backup_folder
        if extension != "txt" and remove_txt:
            remove_file(f"{output_dir}/{hostname}-{cmd_nice}.txt")
        return f"{output_dir}/{hostname}-{cmd_nice}.{extension}"

    return None


def remove_file(fn: str):
    try:
        os.unlink(fn)
    except Exception:
        pass


def rename_file(org_fn: str, new_fn: str):
    """renames a file from one name to another"""
    try:
        os.rename(org_fn, new_fn)
    except Exception:
        pass


def touch_file(fn: str):
    """creates an empty file"""
    try:
        open(fn, mode="w").close()
    except Exception:
        pass


def fact_to_yml(content):
    """converts a list or dict into YAML format
    If the content is a string then the content will not be converted to YAML.

    returns:
        content: the converted content
        extension: either YAML or TXT, depending if conversion succeeded
    """
    extension = "txt"
    try:
        if type(content) is dict or type(content) is list:
            stream = StringIO()
            yaml = ruamel.yaml.YAML(typ="safe")
            yaml.dump(content, stream)
            content = stream.getvalue()
            extension = "yaml"
    except Exception:
        pass
    return content, extension


def fact_to_json(content):
    """converts a list or dict into JSON format
    If the content is a string then the content will not be converted to YAML.

    returns:
        content: the converted content
        extension: either JSON or TXT, depending if conversion succeeded
    """
    extension = "txt"
    if type(content) is dict or type(content) is list:
        content = json.dumps(content, indent=4)
        extension = "json"
    return content, extension


def clean_command_string(cmd: str) -> str:
    """cleans a command to generate a string without spaces or special characters"""
    return cmd.replace(" ", "_").replace("|", "_")


def generate_comment(
    data,
    comment_str="!",
    header=["", "### START OF CONFIG ###", ""],
    footer=[""],
) -> str:
    """generates a router configuration comment

    args:
        data: the text that should be changed into comment
        comment_str: the comment string to be used
        header: list of strings that should be prepended
        footer: list of strings that should be appended

    if data = string => prepend with comment_str
    if data = dict => sort alphabetically and make key: value strings with comment_str
    if data = list => prepend every entry with comment_str

    Examples:
        data = "this is  a test"
            => "! this is a test"

        data = ["this", "is", "a", "test"]
            => "! this"
               "! is"
               "! a"
               "! test"

        data = {"this": "is", "a": "test"}
            => "! a: test"
               "! this: is"

    return the entire block as a string
    """
    result = []
    if type(data) is str:
        result.append(data)
    elif type(data) is list:
        # lists within lists are skipped
        for item in data:
            if type(item) is str:
                result.append(item)
    elif type(data) is dict:
        for key in sorted(data.keys()):
            result.append(f"{key}: {data[key]}")

    # add header
    if header:
        result = header + result

    # add footer
    if footer:
        result = result + footer

    result += [""]

    return "\n".join(map(lambda x: f"{comment_str} {x}", result)) + "\n"


def rename_failed_hosts_backup_file(failed_hosts, user_config):
    """for every host that failed, the config backup file will be renamed
    and ".failed" will be appended

    In some cases the job may be failed but getting the running config was
    successful, in that case the original config backup will be stored as well,
    so there will a a .failed + a config file at the same time.

    If the filename does not yet exist, then an emtpy file will be created
    """
    for host in failed_hosts:
        backup_fn = generate_filename("backup", host, user_config)
        backup_fn_handle = Path(backup_fn)
        if backup_fn_handle.exists():
            if (
                backup_fn_handle.stat().st_size == 0
                or backup_fn_handle.stat().st_ctime > 86400
            ):
                rename_file(backup_fn, f"{backup_fn}.failed")
                return
        touch_file(f"{backup_fn}.failed")
