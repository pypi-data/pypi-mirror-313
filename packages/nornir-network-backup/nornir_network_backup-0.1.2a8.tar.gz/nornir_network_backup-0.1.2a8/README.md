# nornir-network-backup

> This is a beta version. Extra options and documentation will follow soon !

This python library installs the `nnb` command which will generate configuration backups of network equipment via SSH (routers, switches, ..). This tool will replace `RANCID` which - surprisingly - still is commonly being used.

This tool uses the `Nornir` framework and connects to network devices using the `Netmiko` library.

Features:

- Uses the Nornir framework and expects the same files as nornir (config.yaml, hosts.yaml, groups.yaml)
- Generates backup config files for each device (ex. show running-config)
- Includes "meta" data on top of each backup config (ex. hostname, serial number, hardware type, ..)
- Takes `facts` from the devices and store them in separate files
- Parse facts using `textfsm` and store the results as yaml
- Define all fact commands in the nornir config files, different facts per group can be defined
- Store the .diff file for each backup config file
- Generate summary reports to keep track of historical backup info
- Include reports that can give summaries based on the gathered fact data

## REQUIREMENTS

The following python libraries are required:

- nornir
- nornir-utils
- nornir-netmiko

  If you want to used different Nornir runner or inventory plugins then you may need those as well.  
  The `nornir_salt RetryRunner` plugin for example allows automatic re-tries if a connection fails.

## INSTALLATION

The library can be installed as a standard python library using pip, poetry, ..

```shell
pip3 install nornir_network_backup
```

## USAGE

Checkout <TODO> this repo to have a complete example with all the parameters to get you started immediately. This also has Dockerfile so you can start taking backups immediately.

Once this library is installed it will allow you to start backups using the `nnb backup` command.  
You can then refer to a nornir group or individual nornir hosts. If the host you want to backup does not exist in the nornir inventory then you will have to specify the driver manually and it will still allow you to run the backup for the unknown host.

The following examples assume 

Examples:

```shell
# take a backup for 2 hosts, both hosts will be lookuped up in the nornir inventory
nnb backup -h host1 -h 1.2.3.4 -u someuser -p somepass

# take a backup for a group of hosts, the group should be defined
nnb backup -g cisco -u someuser -p somepass

# show all hosts that will backed up
nnb backup --all --dry-run
```


### Credentials

You can provide credentials in different ways:

- defined the nornir config files
- as CLI argument
- by setting environment variables NORNIR_USERNAME and NORNIR_PASSWORD
- by running the nnb command and prepending the environment variables

## Function

- take the running config of 1 or more hosts and save it to a file
  - the file will be overwritten every day
  - optional take a diff of the previous file and save it as well
- run "show" commands and save each output to a separate file in a facts folder
  - files will be overwritten every time
  - all files in a single facts folder
  - save a file with meta data: info about the last backup time, commands executed, failed + successful commands
  - the commands may change depending on vendor or hw type or software
  - commands which can be parsed with textfsm will be saved as YAML, if they cannot be parsed then it will be .config text files
- it should be possible to run the backup file for a single host
- or run agains a complete file
- generate an overall report with:
  - last run time
  - hosts succeeded
  - hosts failed
  - hosts skipped

## Output folder structure

```text
|- backup folder
|  |-- facts folder
|  |-- reports folder  
```

## Commands

```shell
nnb backup
nnb backup-single-host
```

## Usage

```shell
poetry run nnb backup-single-host
```

## Environment Variables

Used by nornir_utils.plugins.inventory.load_credentials transform function, in case username + password are not defined by CLI

NORNIR_USERNAME

NORNIR_PASSWORD

## TEXTFSM

Facts command output can be parsed by NTC Textfsm. It depends on the configuration settings if Textfsm parsing is done.  
The path to the NTC textfsm templates should be valid and include the `index` file. If Textfsm is enabled and no `templates_folder` path is provided then it's expected that the environment variable `NTC_TEMPLATES_DIR` is set.

```python
user_defined:
  textfsm:
    enabled: True
    templates_folder: /home/mwallraf/ntc-templates/ntc_templates/templates/
```

Options:

  **enabled**: Use textfsm or not

  **templates_folder**: path to the NTC textfsm templates, this should be a folder containing an index file. If the folder is not set then the environment variable NTC_TEMPLATES_DIR should exist and have a valid path.



## CAVEATS
Sometimes fact commands may fail and netmiko may generate unexpected timeouts. In that case you can make sure that certain commands are never executed for device groups by prepending the command with a ^ (carret).

Example:

pbxplug:
  data:
    cmd_facts:
      - show voice voice-port all
      - show isdn active
      - show voice voice-port pri all
      - show voice voice-port pri all reset
      - ^show cellular equipment
      - ^show cellular network


