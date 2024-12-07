"""Main module."""

import logging

from fw_curate_bids.save_config import (
    decide_use_or_save_config,
    run_job_with_saved_config,
    attach_config_to,
)
from fw_curate_bids.save_bids_curation import make_file_name_safe
from fw_curate_bids.BIDSCuration import BIDSCuration
from fw_curate_bids.get_bids import get_bids_info

from flywheel_bids.curate_bids import main_with_args

log = logging.getLogger(__name__)


def run(
    gear_context,
    session_id=None,
    session_only=False,
    template_file=None,
    subject_id=None,
    verbosity=None,
    config_file_name=None,
    container=None,
    destination=None,
    project=None,
):
    """Calls the BIDS Client to curate the project and then creates the 5-csv file "report".

    Returns:
        int: 0 on success, 1 on failure
    """
    log.info("Starting BIDS Curation")

    # Get all config parameters that didn't need to be used in the parser
    dry_run = gear_context.config.get("dry_run", False)
    reset = gear_context.config.get("reset")
    template_type = gear_context.config.get("base_template")
    intended_for_regexes = gear_context.config.get("intendedfor_regexes")
    use_or_save_config = gear_context.config.get("use_or_save_config")
    arg_save_sidecar_as_metadata = gear_context.config.get("save_sidecar_as_metadata")

    save_config, use_saved_config, okay_to_use_saved_config = decide_use_or_save_config(
        use_or_save_config
    )

    still_needs_to_run = True

    if use_saved_config:
        if project.get_file(config_file_name):
            still_needs_to_run = run_job_with_saved_config(
                gear_context.client,
                gear_context.config,
                project,
                container,
                config_file_name,
                destination.reload().job,
            )
        else:
            log.info("Did not find saved project configuration file")
    elif save_config:
        attach_config_to(
            gear_context,
            project,
            config_file_name,
            okay_to_use_saved_config,
        )

    if still_needs_to_run and okay_to_use_saved_config:
        # Then didn't run before and use_or_save_config != "Disable Config File":

        if arg_save_sidecar_as_metadata == "yes":
            save_sidecar_as_metadata = True
        elif arg_save_sidecar_as_metadata == "no":
            save_sidecar_as_metadata = False
        else:  # check to see if the project has "BIDS" metadata
            if "BIDS" in project.info:
                if (
                    "Acknowledgements" in project.info["BIDS"]
                ):  # then it was curated the old way
                    save_sidecar_as_metadata = True  # ignore sidecar json files
                else:
                    save_sidecar_as_metadata = False
            else:
                save_sidecar_as_metadata = False

        if save_sidecar_as_metadata:
            log.info("Sidecar data is stored in NIfTI file metadata, not sidecar files")
        else:
            log.info("Sidecar data is in sidecar files, not NIfTI metadata")

        # Call the BIDS client: flywheel_bids.curate_bids.main_with_args()
        main_with_args(
            gear_context.client,
            session_id,
            reset,
            session_only,
            template_type,
            template_file,
            subject_id=subject_id,
            verbosity=verbosity,
            dry_run=dry_run,
            save_sidecar_as_metadata=save_sidecar_as_metadata,
        )

        group_id = destination.parents["group"]
        safe_group_label = make_file_name_safe(group_id, replace_str="_")

        safe_project_label = make_file_name_safe(project.label, replace_str="_")

        pre_path = f"output/{safe_group_label}_{safe_project_label}"

        bc = BIDSCuration()

        if session_only is False:
            session_id = (
                ""  # if this was set get_bids_info() will only return that session
            )

        num_subjects, num_sessions, num_duplicates = get_bids_info(
            project,
            bc,
            subject_id=subject_id,
            session_id=session_id,
            save_sidecar_as_metadata=save_sidecar_as_metadata,
        )

        bc.save_niftis(pre_path)

        bc.save_intendedfors(
            pre_path,
            intended_for_regexes,
            gear_context.client,
            save_sidecar_as_metadata,
        )

        bc.save_acquisition_details(num_subjects, num_sessions, pre_path)

        # This must be called after save_acquisition_details() because it sets bc.most_subjects_have
        bc.save_acquisitions(pre_path)

        if num_duplicates > 0:
            log.error("The following BIDS paths appear more than once:")
            for subject, paths in bc.all_seen_paths.items():
                for path, times_seen in paths.items():
                    if times_seen > 0:
                        log.info(f"  {path}")
            log.error("%s duplicate BIDS paths were detected", num_duplicates)
            return 1
        else:
            log.info("No duplicates were found.")
            return 0

    else:
        log.info("Did not curate")
        return 1
