import datetime
import logging
from pathlib import Path

from nornir.core.inventory import Host
from nornir.core.task import MultiResult, Result, Task
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file
from nornir_network_backup.nornir.summaryfacts import SummaryFacts

from nornir_network_backup.nornir.tasks.get_facts import task_get_facts
from nornir_network_backup.nornir.utils import (
    generate_comment,
    generate_filename,
    remove_file,
)

logger = logging.getLogger(__name__)

CONNECTION_NAME = "netmiko"


def _running_config_sanitation(conf: str):
    """Validates or cleans data in the running config."""
    new_running_config = []
    for line in conf.splitlines():
        if line.endswith("#"):
            continue
        new_running_config.append(line)

    return "\n".join(new_running_config)


def task_backup_config(
    task: Task,
    user_config: dict,
    **kwargs,
    # config_backup_folder,
) -> Result:

    # print(f"host parameters: {task.host.dict()}")

    task_starttime = datetime.datetime.now()

    config_file = None
    config_diff_file = None

    # import sys
    # sys.exit()

    result = {
        "get_running_config": False,
        "save_running_config": False,
        "failed": False,
    }

    result_facts = {}

    # print(summary_facts)

    cmd_running_config = task.host.extended_data().get("cmd_running_config")
    # print(f"show running config command = {cmd_running_config}")

    # r = None
    summary_facts = dict()

    r = None
    try:
        r = task.run(task=netmiko_send_command, command_string=cmd_running_config)
    except Exception as e:
        logger.debug("show running-config failed ... let's retry with timing")
        logger.error(e)

    if not r:
        try:
            r = task.run(task=netmiko_send_command, command_string=cmd_running_config, use_timing=True)
        except Exception as e:
            logger.debug("show running-config still failed ...")
            logger.error(e)


    if r:

        if r.failed:
            result["failed"] = True

        if not r.failed:
            result["get_running_config"] = True
            facts_raw_output_config = ""

            # get all the facts
            if user_config["facts"]["enabled"]:
                fact_tasks_output = task.run(
                    task=task_get_facts,
                    user_config=user_config,
                )

                # get "summary" facts, these will be included in the general backup config
                if not fact_tasks_output.failed:

                    result_facts = fact_tasks_output.results_facts_summary

                    # add facts that should be included in the running-config (as comment)
                    if user_config["facts"].get("facts_in_config"):
                        for _fact_output_cmd in fact_tasks_output.facts_raw_output:
                            if (
                                _fact_output_cmd
                                not in user_config["facts"]["facts_in_config"]
                            ):
                                continue

                            facts_raw_output_config += (
                                generate_comment(
                                    [
                                        line
                                        for line in fact_tasks_output.facts_raw_output[
                                            _fact_output_cmd
                                        ]
                                        if line and not line.endswith("#")
                                    ],
                                    comment_str=f"! {_fact_output_cmd.upper()}:",
                                    header=[],
                                    footer=[],
                                )
                                + "\n" * 2
                            )

                    try:
                        summary_facts = get_summary_facts(
                            fact_tasks_output,
                            host=task.host,
                            wanted_summary_facts_dict=user_config["facts"]["summary"],
                        )

                    except Exception as e:
                        logger.error(
                            f"exception occurred getting the summary facts: {e}"
                        )
                        summary_facts = []
                # print(fact_tasks_output.result)
            # else:
            #     summary_facts = dict()

            backup_config_file = generate_filename(
                filetype="backup",
                hostname=task.host,
                user_config=user_config,
            )

            r = task.run(
                task=write_file,
                filename=backup_config_file,
                content=generate_comment(summary_facts)
                + facts_raw_output_config
                + generate_comment("### RUNNING-CONFIG ###", header=[""])
                + "\n"
                + _running_config_sanitation(r.result)
                + "\n" * 2
                + generate_comment(["", "### END OF CONFIG ###"], header=[""]),
            )

            if not r.failed:
                result["save_running_config"] = True
                config_file = backup_config_file

                # remove the .failed file if it should exist
                if Path(f"{config_file}.failed"):
                    remove_file(f"{config_file}.failed")

                if user_config["backup_config"]["save_config_diff"]:
                    diff_file = generate_filename(
                        filetype="diff",
                        hostname=task.host,
                        user_config=user_config,
                    )
                    if r.diff and diff_file:
                        config_diff_file = diff_file
                        task.run(
                            task=write_file,
                            filename=diff_file,
                            content=r.diff,
                        )

            if r.failed:
                result["failed"] = True

    task_endtime = datetime.datetime.now()
    task_duration = task_endtime - task_starttime

    # save the result to the inventory Host object
    task.host.data.setdefault("_backup_results", {}).setdefault("config", {})
    task.host.data["_backup_results"]["config"] = result
    task.host.data["_backup_results"]["starttime"] = task_starttime
    task.host.data["_backup_results"]["endtime"] = task_endtime
    task.host.data["_backup_results"]["duration"] = task_duration.total_seconds()
    task.host.data["_backup_results"]["config"]["backup_file"] = (
        Path(config_file).name if config_file else ""
    )
    task.host.data["_backup_results"]["config"]["diff_file"] = (
        config_diff_file if config_diff_file else ""
    )
    task.host.data["_backup_results"]["facts"] = result_facts

    # TODO: this could still fail!!
    # ex.
    # --------------------------------------------------
    # --- START BACKUP PROCESS FOR 1 HOSTS ---
    # --------------------------------------------------
    # wgk01-16luk-01: SUCCESS in 0.018524 seconds
    # wgk01-16luk-01: FAILED
    # --------------------------------------------------
    # --- 0 FINISHED, 1 FAILED IN 0.019956 SECONDS ---
    print(
        f"{task.host}: {'FAILED' if result['failed'] else 'SUCCESS'} in {task_duration.total_seconds()} seconds"
    )
    logger.info(
        f"{task.host}: {'FAILED' if result['failed'] else 'SUCCESS'} in {task_duration.total_seconds()} seconds"
    )

    # let's close the connection manually
    logger.debug(f"close nornir connections for host {task.host}")
    task.host.close_connections()

    return Result(host=task.host, result=result)


def get_summary_facts(
    results: MultiResult,
    host: Host,
    wanted_summary_facts_dict: dict,
) -> dict:
    """Get summary facts from all the previous 'show' results of all the tasks
    with name "fact_netmiko_send_command"

    We'll check the fact output results first, afterwards we'll check the host
    data fields (fact info has priority)

    If the host data field does not exist (because you may be running an ad-hoc host which does
    not exist in the hosts file) but the data exists from the facts, then we will
    overwrite the data fields.

    "summary" facts are pre-defined keywords in the nornir configuration file and
    these will be added on top of the backup configuration file as comments. Only
    the facts that are found in the output fatcs commands will be displayed

    Example config backup file

        !
        ! ### START OF CONFIG ###
        !
        ! BOOT_VERSION: BOOT16-SEC-V3.4R3E40C
        ! DEVICE: LBB_140
        ! HOSTNAME: dops-lab-02
        ! MAC: 70:FC:8C:07:22:CC
        ! RELOAD_REASON: Power Fail detection
        ! SERIAL: T1703006230033175
        ! SOFTWARE: ONEOS16-MONO_FT-V5.2R2E7_HA8
        !
        Building configuration...

        Current configuration:

        !
        bind ssh Dialer 1
        bind ssh Loopback 1
        !


    args:
        wanted_summary_facts: list of dict, the fact name is stored in the key value
            Example:
            - key: hostname
            - key: serial
            - key: software
            - key: boot_version
            - key: recovery_version
            - key: reload_reason
            - key: device
            - key: mac
            - key: mgmt_ip
            - key: vendor
            - key: hwtype
            - key: other_ip
            - key: os_slug


    """
    have_summary_facts = {}
    wanted_summary_facts = SummaryFacts(wanted_summary_facts_dict)
    logger.debug(f"wanted summary facts:{wanted_summary_facts}")

    for r in results:
        if not r.name.startswith("fact_to_yaml_") or r.failed:
            continue

        logger.debug(f"extract facts from result: {r.name} - {r.result}")

        for res in _extract_fact_from_result(r.result, wanted_summary_facts):
            # print(res)
            # print(type(res))
            if res:
                have_summary_facts[res[0]] = res[1]

        # print(r.result)
        # print(r.name)
        # print(type(r.result))
        # print(r.result)
        # print(f"failed: {r.failed}")

    # find missing wanted facts in the hosts.yaml file
    missing_wanted_facts = [
        key.lower()
        for key in wanted_summary_facts.fact_keys()
        if key.upper() not in have_summary_facts.keys()
    ]
    # print(f"MISSING WANTED KEYS:{missing_wanted_facts}")

    # try to find missing keys from the nornir host inventory
    for key in missing_wanted_facts:
        # print(f"KEY:{key}")
        if key in host.data:
            value = host.data[key]
            if not value:
                continue
            if type(value) is list:
                value = "|".join(value)
            have_summary_facts[key.upper()] = value

    # for key in host.data.keys():
    #     print(f"KEY:{key}")
    #     if key.upper() in missing_wanted_facts:
    #         have_summary_facts[key.upper()] = host.data[key]

    # set the host.data fields if needed
    for key, val in have_summary_facts.items():
        if (
            (key.lower() in host.data and not host.data.get(key.lower()))
            or (key.lower() not in host.data)
        ) and val:
            logger.debug(f"create or update host.data key '{key}' with value '{val}'")
            host.data[key.lower()] = val

    return have_summary_facts


def _extract_fact_from_result(result, wanted_summary_facts: SummaryFacts):
    """checks all the results to see if we should extract something for the summary facts

    The result should be a list of dict or a dict

    args:
        result: list of Nornir results
        wanted_summary_facts: SummaryFacts object
    """
    if type(result) is list:
        for entry in result:
            for rc in _extract_fact_from_result(entry, wanted_summary_facts):
                yield rc

    if type(result) is dict:
        for fact in wanted_summary_facts.facts:
            if fact.key in result:
                value = result[fact.key]
                if not value:
                    continue
                if type(value) is list:
                    value = "|".join(value)
                yield [fact.key.upper(), value]
