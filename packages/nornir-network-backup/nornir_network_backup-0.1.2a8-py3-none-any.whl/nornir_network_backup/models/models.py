import os
import pathlib
import logging

from pydantic import BaseModel, validator, Extra
from typing import Union

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_FOLDER = "out_files"
DEFAULT_BACKUP_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "configs")
DEFAULT_DIFF_FOLDER = DEFAULT_BACKUP_FOLDER
DEFAULT_FACTS_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "facts")
DEFAULT_LOG_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "logs")
DEFAULT_REPORT_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "reports")
DEFAULT_REPORT_SUMMARY_FILENAME = os.path.join(
    DEFAULT_REPORT_FOLDER, "config-backups-summary.csv"
)
DEFAULT_REPORT_DETAILS_FILENAME = os.path.join(
    DEFAULT_REPORT_FOLDER, "config-backups-details.csv"
)


class myBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid


class TextFSM(myBaseModel):
    #   textfsm:
    #     enabled: True
    #     templates_folder: /home/mwallraf/ntc-templates/ntc_templates/templates/

    enabled: bool = False
    templates_folder: pathlib.Path = None

    @validator("templates_folder", always=True)
    def validate_templates_folder(cls, v, values):
        """validates that the folder exists and is a valid NTC Textfsm folder (check for index file)"""

        # when disabled the unset the folder path for convenience
        if "enabled" in values and values["enabled"] is False:
            v = None
            return v

        if v:
            # if the path is configured then it should exist
            if not v.exists():
                raise ValueError(f"Textfsm templates path does not exist: {v}")

            # if the path exists the we expect the "index" file to be present
            if v.exists() and not pathlib.Path(f"{str(v)}/index").exists():
                raise ValueError(
                    f"Textfsm templates folder is defined but does not seem to be a valid NTC Textfsm folder, there is a missing 'index' file: {v}"
                )

            # set/override the environment variable NTC_TEMPLATES_DIR
            os.environ["NTC_TEMPLATES_DIR"] = str(v)
            logger.debug(f"set the NTC_TEMPLATES_DIR environment variable to: {v}")

        if not v:
            # the envvar NTC_TEMPLATES_DIR should exist
            if not os.environ.get("NTC_TEMPLATES_DIR"):
                raise ValueError(
                    "Textfsm is enabled but the environment variable NTC_TEMPLATES_DIR is not set. Please set this environment variable or configure the templates_folder variable in the nornir config file."
                )

            # the path defined in envvar NTC_TEMPLATES_DIR should exist
            if not pathlib.Path(os.environ["NTC_TEMPLATES_DIR"]).exists():
                raise ValueError(
                    f"Textfsm is enabled and the environment variable NTC_TEMPLATES_DIR is set but the path does not exist: {os.environ['NTC_TEMPLATES_DIR']}"
                )

        return v


class Summary(myBaseModel):
    enabled: bool = True
    filename: Union[pathlib.Path, None] = pathlib.Path(DEFAULT_REPORT_SUMMARY_FILENAME)
    append: bool = True


class Details(myBaseModel):
    enabled: bool = True
    filename: Union[pathlib.Path, None] = pathlib.Path(DEFAULT_REPORT_DETAILS_FILENAME)
    append: bool = True


class Reports(myBaseModel):
    min_success_rate: int = 95
    summary: Summary = Summary()
    details: Details = Details()


class BackupConfig(myBaseModel):
    folder: pathlib.Path = pathlib.Path(DEFAULT_OUTPUT_FOLDER)
    config_diff_folder: pathlib.Path = pathlib.Path(DEFAULT_DIFF_FOLDER)
    erase_existing_diff_files: bool = True
    save_config_diff: bool = True
    reports: Reports = Reports()


class SummaryFact(myBaseModel):
    key: str


class Facts(myBaseModel):
    enabled: bool = False
    folder: Union[pathlib.Path, None] = pathlib.Path(DEFAULT_FACTS_FOLDER)
    summary: list[SummaryFact] = []
    facts_in_config: list[str] = []


class BackupNornirUserParams(myBaseModel):
    """model to validate the Nornir user_defined parameters used by the backup script

    {
        "textfsm": {"enabled": False, "templates_folder": None},
        "backup_config": {
            "folder": pathlib.Path("out_files"),
            "config_diff_folder": pathlib.Path("out_files/configs"),
            "erase_existing_diff_files": True,
            "save_config_diff": True,
            "reports": {
                "summary": {
                    "enabled": True,
                    "filename": pathlib.Path(
                        "out_files/reports/config-backups-summary.csv"
                    ),
                    "append": True,
                },
                "details": {
                    "enabled": True,
                    "filename": pathlib.Path(
                        "out_files/reports/config-backups-details.csv"
                    ),
                    "append": True,
                },
            },
        },
        "facts": {
            "enabled": False,
            "folder": pathlib.Path("out_files/facts"),
            "summary": [],
        },
    }

    """

    textfsm: TextFSM = TextFSM()
    backup_config: BackupConfig = BackupConfig()
    facts: Facts = Facts()
