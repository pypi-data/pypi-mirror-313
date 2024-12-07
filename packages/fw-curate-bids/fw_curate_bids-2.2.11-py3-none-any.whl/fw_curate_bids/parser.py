"""Parser module to parse gear config.json: inputs and config options."""

from typing import Any
import logging

from flywheel_gear_toolkit import GearToolkitContext

CONFIG_FILE_NAME_PRE = "curate-bids-"  # + project  subject  or  session
CONFIG_FILE_NAME_POST = "-config.json"

log = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext,
) -> tuple[Any, bool, Any | None, str | Any, int, str, Any, Any, Any]:
    # gear_context.config.get("verbosity") can be "INFO","DEBUG"
    verbosity = 0
    if gear_context.config.get("verbosity") == "DEBUG":
        verbosity = 1

    if verbosity == 0:
        print('setting log level to "info"')
        logging.basicConfig(
            format="[ %(module)s %(asctime)2s %(levelname)2s] %(message)s"
        )
        log.setLevel(logging.INFO)

    elif verbosity == 1:
        print('setting log level to "debug"')
        logging.basicConfig(
            format="[ %(module)s %(asctime)2s %(levelname)2s: %(lineno)s] %(message)s"
        )
        log.setLevel(logging.DEBUG)

    template = gear_context.get_input("template")
    if template:
        template_file = template["location"]["path"]
        log.info(
            "Input project curation template is '%s'", template["location"]["name"]
        )
    else:
        template_file = None

    destination_id = gear_context.destination["id"]

    fw = gear_context.client

    destination = fw.get(destination_id)

    project = fw.get_project(destination.parents["project"])

    # The use of session_only and session_id here is confusing to maintain backwards compatibility.
    # Ideally, subject_id would be set if curating a specific subject and session_id would be set if curating a
    # specific session.  But the function main_with_args() expected to find the project using a session ID.  If
    # session_only is True, only the session should be curated but if it is false, the entire_project should be
    # curated.  Previously entire_project was a config parameter, but now the gear must be run at the proper
    # level (project, subject, session) to curate that level.  Now these variables are set to achieve the desired
    # behavior of running the gear at the user-specified level.  subject_id was added as a kwarg to main_with_args()
    # to be able to run at the subject level and if it is set, main_with_args() will find the project using the
    # subject_id.  For now, assume the gear is running at a particular session:
    session_only = True
    subject_id = ""
    session_id = destination.parents["session"]

    # --- Set up for run ---
    if destination.parent.type == "project":  # subject_id will not be used
        session = (
            project.sessions.find_first()
        )  # just get one so the project id can be found
        session_id = session.id
        session_only = False  # session_id will not be used to curate only the session
        log.info("Curating entire project")
        config_file_name = CONFIG_FILE_NAME_PRE + "project" + CONFIG_FILE_NAME_POST
        container = project

    elif destination.parent.type == "subject":  # run on only this subject
        subject_id = destination.parents[
            "subject"
        ]  # project id will be found via subject_id
        session_only = False  # session_id will not be used to curate only the session
        log.info("Curating single subject, id %s", subject_id)
        config_file_name = CONFIG_FILE_NAME_PRE + "subject" + CONFIG_FILE_NAME_POST
        container = fw.get_subject(subject_id)

    elif destination.parent.type == "session":  # run on only this session
        log.info("Curating single session, id %s", session_id)
        config_file_name = CONFIG_FILE_NAME_PRE + "session" + CONFIG_FILE_NAME_POST
        container = fw.get_session(session_id)

    else:
        raise ValueError("Unexpected destination.parent.type!")

    return (
        session_id,
        session_only,
        template_file,
        subject_id,
        verbosity,
        config_file_name,
        container,
        destination,
        project,
    )
