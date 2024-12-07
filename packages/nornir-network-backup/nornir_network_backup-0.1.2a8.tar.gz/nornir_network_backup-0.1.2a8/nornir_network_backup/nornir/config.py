import os
from pathlib import Path

DEFAULT_USER_DEFINED_PARAMS = {
    "textfsm": {"enabled": False, "templates_folder": ""},
    "backup_config": {
        "folder": "out_files",
        "erase_existing_diff_files": True,
        "save_config_diff": True,
        "config_diff_folder": "",
    },
    "facts": {
        "enabled": True,
        "folder": "out_files/facts",
        "summary": {"serial"},
    },
}


def set_textfsm_envvar(
    templates_folder: str = None, override_envvar: bool = False
) -> None:
    """sets the NTC_TEMPLATES_DIR environment var, needed by NTC textfsm

    Priority for setting NTC_TEMPLATES_DIR:

    1. no action if envvar is already defined + folder exists + override_envvar = False
    2. set if templates_folder is set + exists
    3. throw error if templates_folder is set but does not exist + envvar exists and does
       not exist

    """
    tf = os.environ.get("NTC_TEMPLATES_DIR", None)
    if tf and override_envvar is False:
        return
    if templates_folder and not Path(templates_folder).exists():
        raise Exception("textfsm template folder is set but does not exist")
    os.environ["NTC_TEMPLATES_DIR"] = templates_folder


def init_user_defined_config(nr, create_folders: bool = True) -> None:
    """initializes + validates the user_defined config parameters which are found
    in the nornir config.yaml file

    args:
        nr: the nornir object
        create_folders: if True then create the backup config folders if they don't exist yet
    """

    # add missing keys in the user_defined config of the nornir object
    for p_key in DEFAULT_USER_DEFINED_PARAMS:
        if p_key not in nr.config.user_defined:
            nr.config.user_defined[p_key] = dict()
        for c_key in DEFAULT_USER_DEFINED_PARAMS[p_key]:
            if c_key not in nr.config.user_defined[p_key]:
                nr.config.user_defined[p_key][
                    c_key
                ] = DEFAULT_USER_DEFINED_PARAMS[p_key][c_key]

    templates_folder = nr.config.user_defined["textfsm"]["templates_folder"]
    if os.path.isdir(templates_folder):
        set_textfsm_envvar(templates_folder)
        nr.config.user_defined["textfsm"]["enabled"] = True
    else:
        nr.config.user_defined["textfsm"]["enabled"] = False
        print(
            f"textfsm is disabled - the templates folder '{templates_folder}' does not exist"
        )

    # init config backup path
    backup_path = nr.config.user_defined["backup_config"]["folder"]
    if not backup_path or not os.path.isdir(backup_path):
        if backup_path and create_folders:
            os.mkdir(backup_path)
            print(f"backup folder '{backup_path}' has been created")
        else:
            raise Exception(
                f"backup config folder '{backup_path}' does not exist"
            )

    # init config_diff path
    config_diff_path = nr.config.user_defined["backup_config"][
        "config_diff_folder"
    ]
    config_diff_enabled = nr.config.user_defined["backup_config"][
        "save_config_diff"
    ]
    if (
        config_diff_enabled
        and config_diff_path
        and not os.path.isdir(config_diff_path)
    ):
        os.mkdir(config_diff_path)
        print(
            f"backup config diff folder '{config_diff_path}' has been created"
        )

    # init facts folder
    facts_path = nr.config.user_defined["facts"]["folder"]
    facts_enabled = nr.config.user_defined["facts"]["enabled"]
    if facts_enabled and facts_path and not os.path.isdir(facts_path):
        os.mkdir(facts_path)
        print(f"facts folder '{facts_path}' has been created")
