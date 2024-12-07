import logging
import csv
from pathlib import Path

logger = logging.getLogger(__name__)


def print_results_csv(
    summary_file,
    details_file,
    result,
    append_summary=False,
    append_details=False,
    overall_success=False,
    **kwargs,
):
    """print summary and detailed output files"""
    backup_starttime = kwargs["starttime"]
    backup_stoptime = kwargs["stoptime"]
    total_host_cnt = kwargs["total_host_cnt"]
    filtered_host_cnt = kwargs["filtered_host_cnt"]

    backup_duration = backup_stoptime - backup_starttime
    nbr_processed_hosts = len(result.items())
    nbr_failed_hosts = len(result.failed_hosts)
    nbr_success_hosts = nbr_processed_hosts - nbr_failed_hosts
    success_rate = (nbr_success_hosts / nbr_processed_hosts) * 100
    backup_start_date = backup_starttime.strftime("%Y-%m-%d")
    backup_start_time = backup_starttime.strftime("%H:%M:%S")

    backup_stats = {
        "backup_start_date": backup_start_date,
        "backup_start_time": backup_start_time,
        "overall_result": (
            "success" if overall_success else "failed"
        ),  # not result.failed else "failed",
        "nbr_unfiltered_hosts": total_host_cnt,
        "nbr_filtered_hosts": filtered_host_cnt,
        "nbr_processed_hosts": nbr_processed_hosts,
        "nbr_failed_hosts": nbr_failed_hosts,
        "nbr_success_hosts": nbr_success_hosts,
        "success_rate": success_rate,
        "failed_rate": 100 - success_rate,
        "backup_duration": backup_duration.total_seconds(),
    }

    try:
        print_backup_summary_csv(
            summary_file,
            backup_stats,
            append=append_summary,
        )
    except Exception as e:
        logger.warning(
            f"Error occurred while generating the summary report file: {summary_file}"
        )
        logger.exception(e)
        pass

    try:
        print_backup_result_details_csv(
            details_file,
            result,
            backup_stats,
            append=append_details,
        )
    except Exception as e:
        logger.warning(
            f"Error occurred while generating the detailed report file: {details_file}"
        )
        logger.exception(e)
        pass


def print_backup_summary_csv(
    filename,
    stats,
    append=False,
):
    """prints a summary of the entire backup process in CSV format"""

    logger.debug(f"Generate the backup summary report: {filename}")

    with open(filename, "a" if append else "w") as csvfile:
        fieldnames = [
            "backup_start_date",
            "backup_start_time",
            "backup_duration",
            "overall_result",
            "nbr_filtered_hosts",
            "nbr_processed_hosts",
            "nbr_unfiltered_hosts",
            "nbr_success_hosts",
            "nbr_failed_hosts",
            "success_rate",
            "failed_rate",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        fp = Path(filename)
        if not append or (fp.exists() and fp.stat().st_size == 0):
            writer.writeheader()
        writer.writerow(stats)

    # write the backup summary
    # with open("config-backups-summary.txt", "a") as f:
    #     f.write(json.dumps(backup_summary, indent=4))


def print_backup_result_details_csv(filename, result, stats, append=False):
    """prints the backup result details in CSV format"""

    logger.debug(f"Generate the backup details report: {filename}")

    records = []
    # write the host details
    for host, host_data in result.items():
        backup_results = host_data.host.data.get("_backup_results", {})
        facts_failed = backup_results.get("facts", {}).get("failed", True)
        config_failed = backup_results.get("config", {}).get("failed", True)
        try:
            record = {
                "result": "failed" if (facts_failed or config_failed) else "success",
                "backup_start_date": stats["backup_start_date"],
                "backup_start_time": stats["backup_start_time"],
                "backup_duration": stats["backup_duration"],
                "task_start_time": str(backup_results.get("starttime", "")),
                "task_stop_time": str(backup_results.get("endtime", "")),
                "task_duration": backup_results.get("duration", -1),
                "host": host,
                "hwtype": host_data.host.data.get("hwtype", ""),
                "vendor": host_data.host.data.get("vendor", ""),
                "software": host_data.host.data.get("software", ""),
                "platform": host_data.host.platform,
                "os_slug": host_data.host.data.get("os_slug", ""),
                "config_file": backup_results.get("config", {}).get("backup_file", ""),
                "changed": (
                    True
                    if backup_results.get("config", {}).get("diff_file", "")
                    else False
                ),
                "facts_commands": ",".join(
                    backup_results.get("facts", {}).get("all_commands", [])
                ),
                "facts_failed_commands": ",".join(
                    backup_results.get("facts", {}).get("failed_commands", [])
                ),
                "facts_failed_parser_commands": ",".join(
                    set(backup_results.get("facts", {}).get("all_commands", []))
                    - set(backup_results.get("facts", {}).get("parsed_commands", []))
                ),
                "facts_count_failed_parser": len(
                    set(backup_results.get("facts", {}).get("all_commands", []))
                    - set(backup_results.get("facts", {}).get("parsed_commands", []))
                ),
                "facts_count": len(
                    backup_results.get("facts", {}).get("all_commands", [])
                ),
                "facts_result": (
                    "failed"
                    if backup_results.get("facts", {}).get("failed", True)
                    else "success"
                ),
                "facts_count_failed": len(
                    backup_results.get("facts", {}).get("failed_commands", [])
                ),
                "facts_parser_result": (
                    "failed"
                    if backup_results.get("facts", {}).get("failed_parser", True)
                    else "success"
                ),
            }
            records.append(record)
        except Exception as e:
            logger.warning(
                f"Something happened creating the detailed output report, skipping record for host: {host}"
            )
            logger.exception(e)
            continue

    with open(filename, "a" if append else "w") as csvfile:
        fieldnames = [
            "host",
            "result",
            "backup_start_date",
            "backup_start_time",
            "backup_duration",
            "task_start_time",
            "task_stop_time",
            "task_duration",
            "facts_result",
            "facts_parser_result",
            "facts_count",
            "facts_count_failed",
            "facts_count_failed_parser",
            "vendor",
            "os_slug",
            "platform",
            "hwtype",
            "software",
            "config_file",
            "changed",
            "facts_failed_commands",
            "facts_failed_parser_commands",
            "facts_commands",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        fp = Path(filename)
        if not append or (fp.exists() and fp.stat().st_size == 0):
            writer.writeheader()
        writer.writerows(records)
