import logging

from nornir.core.inventory import Host
from nornir.core.task import Result, Task
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file
from nornir_network_backup.nornir.tasks.textfsm_parser import task_textfsm
from nornir_network_backup.nornir.utils import (
    fact_to_yml,
    generate_filename,
    remove_file,
    clean_command_string,
)
from nornir_network_backup.nornir.tasks.netmiko_multiple_commands import (
    netmiko_multiple_commands,
)

logger = logging.getLogger(__name__)

CONNECTION_NAME = "netmiko"


def parse_facts(task: Task, commands: list, results: dict) -> dict:
    """Parse the facts with textfsm"""
    parsed_results = {}

    for cmd in commands:
        cmd_nice = clean_command_string(cmd)
        _content = results.get(cmd)

        task_fact_to_yaml = task.run(
            name=f"fact_to_yaml_{cmd_nice}",
            task=task_textfsm,
            cmd=cmd,
            data=_content,
        )
        if task_fact_to_yaml.changed and task_fact_to_yaml.result:
            _content = task_fact_to_yaml.result
            parsed_results[cmd] = _content

    return Result(host=task.host, result=parsed_results)


def save_facts(task: Task, user_config: dict, commands: list, fact_data: dict) -> None:
    """stores each fact to a file, either .txt or .yml
    existing files for failed commands will be removed
    """
    for cmd in commands:
        content, extension = fact_to_yml(fact_data.get(cmd))

        fact_file = generate_filename(
            filetype="fact",
            hostname=task.host,
            user_config=user_config,
            command=cmd,
            extension=extension,
            remove_txt=True,
        )

        if not content:
            remove_file(fact_file)
            continue

        # may fail with OSError: [Errno 24], how to catch this?
        task.run(
            task=write_file,
            filename=fact_file,
            content=f"{content}",
        )
    return Result(host=task.host)


def task_get_facts(task: Task, user_config: dict, **kwargs) -> Result:
    """Gets all the facts, stored in consolidated_fact_commands
    Runs the textfsm parser if needed and store each fact in a
    separate file

    This task should never fail since the primary job is to get the
    running-config file.

    We will make a report of failed commands
    """

    commands = task.host.get("consolidated_fact_commands", [])
    use_textfsm = user_config["textfsm"]["enabled"]

    results_facts_summary = {
        "all_commands": commands,
        "failed_commands": [],
        "success_commands": [],
        "parsed_commands": [],
        "failed_parser": False,
        "failed": False,
    }

    logger.debug(f"get all facts: {commands}, textfsm parsing enabled:{use_textfsm}")

    facts_results = task.run(
        task=netmiko_multiple_commands,
        commands=commands,
        name="netmiko_multiple_facts",
    )

    results_facts_summary["success_commands"] = (
        [] if not facts_results.success_commands else facts_results.success_commands
    )
    results_facts_summary["failed_commands"] = (
        [] if not facts_results.failed_commands else facts_results.failed_commands
    )
    results_facts_summary["failed"] = True if facts_results.failed_commands else False

    logger.debug(
        f"fact results: {facts_results.success_commands} {facts_results.result}"
    )

    # store the raw output of the success commands
    facts_raw_output = {}
    for cmd in facts_results.success_commands:
        facts_raw_output[cmd] = facts_results.result.get(cmd, "").splitlines()

    logger.debug(f"facts raw output: {facts_raw_output}")

    if use_textfsm:
        parsed_results = parse_facts(
            task,
            facts_results.success_commands,
            facts_results.result,
        )
        for cmd in parsed_results.result:
            facts_results.result[cmd] = parsed_results.result[cmd]
            if isinstance(parsed_results.result[cmd], list) or isinstance(
                parsed_results.result[cmd], dict
            ):
                results_facts_summary["parsed_commands"].append(cmd)

    if len(results_facts_summary["parsed_commands"]) != len(
        results_facts_summary["success_commands"]
    ):
        results_facts_summary["failed_parser"] = True

    save_facts(
        task,
        user_config,
        facts_results.all_commands,
        facts_results.result,
    )

    return Result(
        host=task.host,
        result=facts_results.result,
        facts_raw_output=facts_raw_output,
        results_facts_summary=results_facts_summary,
    )


# def task_get_facts_original(task: Task, user_config: dict, **kwargs) -> Result:
#     # commands = get_fact_commands(task.host)
#     commands = task.host.get("consolidated_fact_commands", [])

#     facts = {
#         "all_commands": [],
#         "failed_commands": [],
#         "success_commands": [],
#         "failed": False,
#     }

#     for cmd in commands:
#         cmd_nice = clean_command_string(cmd)
#         facts["all_commands"].append(cmd)

#         output = task.run(
#             name=f"fact_netmiko_send_command_{cmd_nice}",
#             task=netmiko_send_command,
#             command_string=f"{cmd}\n",
#             # use_textfsm=user_config["textfsm"]["enabled"],
#             # severity_level=logging.DEBUG,
#         )

#         if output.failed:
#             facts["failed_commands"].append(cmd)

#         else:
#             facts["success_commands"].append(cmd)

#             use_textfsm = user_config["textfsm"]["enabled"]

#             _content = output.result
#             # don't use netmiko textfsm parsing to have better error control
#             # but if it succeeds then we'll replace the result
#             if use_textfsm:
#                 task_fact_to_yaml = task.run(
#                     name=f"fact_to_yaml_{cmd_nice}",
#                     task=task_textfsm,
#                     cmd=cmd,
#                     data=_content,
#                 )
#                 if task_fact_to_yaml.changed and task_fact_to_yaml.result:
#                     _content = task_fact_to_yaml.result

#                 # try:
#                 #     __content = parse_output(
#                 #         platform=task.host.platform, command=cmd, data=_content
#                 #     )
#                 #     _content = __content
#                 # except Exception:
#                 #     logger.error(
#                 #         f"unable to parse textfsm for host:{task.host.name} platform:{task.host.platform} command:{cmd}"
#                 #     )
#                 #     pass

#             # >>> vlan_parsed = parse_output(platform="cisco_ios", command="show vlan", data=vlan_output)

#             content, extension = fact_to_yml(_content)

#             fact_file = generate_filename(
#                 filetype="fact",
#                 hostname=task.host,
#                 user_config=user_config,
#                 command=cmd,
#                 extension=extension,
#                 remove_txt=True,
#             )

#             if not output.result:
#                 remove_file(fact_file)
#                 continue

#             # may fail with OSError: [Errno 24], how to catch this?
#             task.run(
#                 task=write_file,
#                 filename=fact_file,
#                 content=f"{content}",
#             )

#     # save the result to the inventory Host object
#     # facts = {"all_commands": [], "failed_commands": [], "success_commands": []}
#     facts["total_commands"] = len(facts["all_commands"])
#     facts["total_failed_commands"] = len(facts["failed_commands"])
#     facts["total_success_commands"] = len(facts["success_commands"])
#     facts["failed"] = True if facts["failed_commands"] else False

#     task.host.data.setdefault("_backup_results", {}).setdefault("facts", facts)

#     return Result(host=task.host, result=facts)
#     # return Result(host=task.host, result=facts, failed=failed)
