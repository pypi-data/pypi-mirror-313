from nornir.core.task import Task, Result
from netmiko.exceptions import ReadTimeout
import logging
import re

logger = logging.getLogger(__name__)

# ANSI_CTRL_C = "\x03"
ANSI_CTRL_C = "\3"

PLATFORMS_CHECK_FOR_ERROR_MESSAGES = ["oneaccess_oneos"]

ERROR_MESSAGES = [
    r".*syntax error:.*",
    r"-+\^.*",
    r".*error:.*",
    r"Aborted:.*",
]

CONNECTION_NAME = "netmiko"


def _output_has_error(host, output):
    """checks if the output contains error messages"""
    if host.platform not in PLATFORMS_CHECK_FOR_ERROR_MESSAGES:
        return False

    for errpattern in ERROR_MESSAGES:
        if re.match(errpattern, output.lower(), re.DOTALL):
            return True

    return False


def netmiko_multiple_commands(
    task: Task, commands=[], fail_when_unsuccessful=False
) -> Result:
    """custom command to have more control over the exception handling

    results.result will contain a dict, each command will be the key and
    the value is the command output

    :args fail_when_unsuccessful: If true and at least one command has failed then completely
        fail the task, otherwise the task will only fail if all commands have failed
    """

    exceptions = []
    failed = False

    failed_commands = []
    success_commands = []

    logger.debug(f"fact commands:{commands}")

    results_dict = {}
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    for cmd in commands:
        try:
            logger.debug(f"-- trying command: {cmd}")

            output = net_connect.send_command(cmd)

            if output and _output_has_error(task.host, output):
                results_dict[cmd] = ""
                raise Exception(f"command {cmd} throws an error")

            results_dict[cmd] = output
            success_commands.append(cmd)

        # In some occasions (mostly on OneAccess), if there is an error,
        # the command will not be cleared and the command will hang
        # until read timeout. To overcome this we have to send
        # CTRL-C to clear the prompt
        except ReadTimeout as e:
            logger.error(f"ERROR-READ TIMEOUT {cmd}: {e}")
            net_connect.write_channel(ANSI_CTRL_C)
            exceptions.append(e)
            failed_commands.append(e)
        except Exception as e:
            logger.error(f"UNHANDLED EXCEPTION {cmd}: {e}")
            net_connect.write_channel(ANSI_CTRL_C)
            exceptions.append(e)
            failed_commands.append(cmd)

    if failed_commands:
        if not success_commands or fail_when_unsuccessful:
            failed = True

    return Result(
        host=task.host,
        result=results_dict,
        exception=exceptions,
        all_commands=commands,
        success_commands=success_commands,
        failed_commands=failed_commands,
        failed=failed,
    )
