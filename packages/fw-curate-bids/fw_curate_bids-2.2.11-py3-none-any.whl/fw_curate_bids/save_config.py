"""Methods to save and use a config file for the curate-bids gear."""

import json
import logging
from datetime import datetime

import flywheel

log = logging.getLogger(__name__)


def attach_config_to(gear_context, project, config_file_name, okay_to_use_saved_config):
    data = dict()
    data["okay_to_use"] = okay_to_use_saved_config
    data["config"] = dict()

    keys = ["base_template", "intendedfor_regexes", "reset", "verbosity"]
    data["config"] = {key: gear_context.config.get(key) for key in keys}

    template = gear_context.get_input("template")
    if template is not None:
        data["inputs"] = {
            "template": {
                "hierarchy_id": template["hierarchy"]["id"],
                "file_name": template["location"]["name"],
            }
        }
    else:
        data["inputs"] = {}

    file_spec = flywheel.FileSpec(config_file_name, json.dumps(data), "text/plain")
    project.upload_file(file_spec)
    log.info(
        "Attached %s to project '%s'.  okay_to_use_saved_config is %s",
        config_file_name,
        project.label,
        okay_to_use_saved_config,
    )


def run_job_with_saved_config(fw, config, project, container, config_file_name, job):
    """Launch a new job with the saved config and input file (if provided).

    Note: The "saved config" is those four config values plus a possible input json file.  The goal
    is to let the user not do anything but click the "Run Gear" button If they don't provide that file,
    the gear engine won't have it ready for this job, so a new job has to be launched to get that input file.

    Args:
        fw: Flywheel Client:
        config:  The current gear config.json
        project: The full project object
        container: The full project, subject, or session that the new analysis will be attached to
        config_file_name: The name of the file that will hold config/input information attached to the project
        job:  The current job so the ID can be put in the name of the new analysis job

    Returns:
        True if a job was not launched (disabled config file) and so it still needs to be run

    """
    data = project.read_file(config_file_name)
    read_config = json.loads(data)

    if read_config["okay_to_use"]:  # turn this feature off by setting this to False
        config.update(read_config["config"])

        # without this, jobs will be spawned forever to do nothing:
        config["use_or_save_config"] = "Ignore Config File"

        inputs = dict()
        for key, val in read_config["inputs"].items():
            inputs_container = fw.get(val["hierarchy_id"])
            inputs[key] = inputs_container.get_file(val["file_name"])

        gear = fw.lookup("gears/curate-bids")

        now = datetime.now()
        analysis_label = (
            f'curate-bids {now.strftime("%m-%d-%Y %H:%M:%S")} launched by job {job.id}'
        )

        analysis_id = gear.run(
            analysis_label=analysis_label,
            config=config,
            inputs=inputs,
            destination=container,
        )
        log.info("Launched %s id=%s", analysis_label, analysis_id)
        return False  # job launched, does not still need to be run

    else:
        log.info(
            "Found disabled saved config file.  Ignoring it and using currently supplied input and config. "
        )
        return True  # job still needs to be launched because it wasn't done here


def decide_use_or_save_config(use_or_save_config):
    """Figure out what to do with the configuration file.

    The use_or_save_config option sets the configuration and input file that will be used on subsequent
    runs of this gear.  For 'Save Config File', a configuration file will be
    attached to the project called 'curate-bids-<run level>-config.json' where <run level>
    is 'project', 'subject' or 'session'.  For 'Ignore Config File', that file will be
    ignored and the currently set configuration will
    be used.  The default, leaving this option blank, is to use the saved configuration file
    if it is present or to use the current configuration if not.

    Args:
        use_or_save_config:  (string) one of "Save Config File", "Ignore Config File", "Disable Config File", or ""

    Returns:
        save_config:  (bool) True if the configuration should be saved to the project
        use_saved_config:  (bool) True if the existing saved configuration should be used
        okay_to_use_saved_config:  (bool) True if the saved configuration file is not disabled
    """

    if use_or_save_config == "Save Config File":
        # Save some values from current config.json as 'curate-bids-<run-level>-config.json' on
        # the project, so it will be used by default (the last else below)
        save_config = True
        use_saved_config = False
        okay_to_use_saved_config = True
        log.info("Saving Config")
    elif use_or_save_config == "Ignore Config File":
        # Ignore config file and use the current config
        save_config = False
        use_saved_config = False
        okay_to_use_saved_config = True
        log.info("Using current config, ignoring saved Config if present")
    elif use_or_save_config == "Disable Config File":
        save_config = True
        use_saved_config = False
        okay_to_use_saved_config = False
        log.info("Disabling saved Config file")
    elif (
        use_or_save_config == ""
    ):  # use_or_save_config is not set.  This is the default
        # Check for 'curate-bids-config.json' at the run level and use it if present
        save_config = False
        use_saved_config = True
        okay_to_use_saved_config = True
        log.info("Using Saved Config if present")
    else:
        raise ValueError("Unknown value for use_or_save_config: %s", use_or_save_config)

    return save_config, use_saved_config, okay_to_use_saved_config
