#!/usr/bin/env python3
"""Save BIDS mapping from containers and file names to BIDS paths and fieldmap IntendedFors as sorted csv files.

Notes:
- You need to be logged in to a Flywheel instance using the CLI (fw login ...)
- This script requres the latest version of flywheel-bids
  See https://pypi.org/project/flywheel-bids/#history
  Install it with, e.g. pip install flywheel-bids==1.0.0

INTENDED_FOR is a space separated pair of regular expressions, the first one matches the fieldmap acquisition name and the second of each pair matches the BIDS filename.

Example with --intended-for parameter:
   save_bids_curation.py  Group Project -i '.*fmap(_|-)SE(_|-).* _run-1 .*gre-.* _run-2'
"""

import argparse
import logging
import os
import pickle
import re
from pathlib import Path

import flywheel
from fw_curate_bids.BIDSCuration import BIDSCuration
from fw_curate_bids.get_bids import get_bids_info

PICKLE_FILE_NAME = "./bids_data.pickle"

log = logging.getLogger(__name__)


def make_file_name_safe(input_basename, replace_str=""):
    """Remove non-safe characters from a filename and return a filename with
        these characters replaced with replace_str.

    :param input_basename: the input basename of the file to be replaced
    :type input_basename: str
    :param replace_str: the string with which to replace the unsafe characters
    :type   replace_str: str
    :return: output_basename, a safe
    :rtype: str
    """

    safe_patt = re.compile(r"[^A-Za-z0-9_\-.]+")
    # if the replacement is not a string or not safe, set replace_str to x
    if not isinstance(replace_str, str) or safe_patt.match(replace_str):
        # print("{} is not a safe string, removing instead".format(replace_str))
        replace_str = ""

    # Replace non-alphanumeric (or underscore) characters with replace_str
    safe_output_basename = re.sub(safe_patt, replace_str, input_basename)

    if safe_output_basename.startswith("."):
        safe_output_basename = safe_output_basename[1:]

    # print('"' + input_basename + '" -> "' + safe_output_basename + '"')

    return safe_output_basename


def main(bc, args, project, pre_path, fw, save_sidecar_as_metadata):
    if args.pickle and Path(PICKLE_FILE_NAME).exists():
        log.info(PICKLE_FILE_NAME)

        with open(PICKLE_FILE_NAME, "rb") as f:
            data = pickle.load(f)

        bc = data["bc"]
        num_subjects = data["num_subjects"]
        num_sessions = data["num_sessions"]
        num_duplicates = data["num_duplicates"]

    else:
        if args.subject:
            num_subjects, num_sessions, num_duplicates = get_bids_info(
                project, bc, args.subject
            )
        else:
            num_subjects, num_sessions, num_duplicates = get_bids_info(project, bc)

        if args.pickle:  # save all data to a file so it can be just loaded next time (saves time while debugging)
            data = dict()
            data["bc"] = bc
            data["num_subjects"] = num_subjects
            data["num_sessions"] = num_sessions
            data["num_duplicates"] = num_duplicates

            with open(PICKLE_FILE_NAME, "wb") as f:
                pickle.dump(data, f)

    bc.save_niftis(pre_path)

    bc.save_intendedfors(
        pre_path, args.intended_for_regexes, fw, save_sidecar_as_metadata
    )

    bc.save_acquisition_details(num_subjects, num_sessions, pre_path)

    # This must be called after save_acquisition_details() because it
    # sets bc.most_subjects_have
    bc.save_acquisitions(pre_path)

    if num_duplicates > 0:
        print("ERROR: the following BIDS paths appear more than once:")
        for subject, paths in bc.all_seen_paths.items():
            for path, times_seen in paths.items():
                if times_seen > 0:
                    print(f"  {path}")
        print(f"{num_duplicates} duplicate BIDS paths were detected")
    else:
        print("No duplicates were found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("group_id", help="fw://group_id/project_label")
    parser.add_argument("project_label", help="fw://group_id/project_label")
    parser.add_argument(
        "--project_id",
        action="store",
        type=str,
        help="hexadecimal id that returns the project with fw.get",
    )
    parser.add_argument(
        "-s",
        "--subject",
        action="store",
        type=str,
        help="subject ID",
    )
    parser.add_argument(
        "-a",
        "--api-key",
        action="store",
        type=str,
        help="api-key (default is to use currently logged in instance",
    )
    parser.add_argument(
        "-i",
        "--intended-for-regexes",
        action="store",
        type=str,
        help="pairs of regex's specifying field map acquisition name to BIDS Filename passed in as a single string.",
    )
    parser.add_argument(
        "-p",
        "--pickle",
        action="store_true",
        help="Save/use pickled data instead of getting it multiple times (for debugging)",
    )

    args = parser.parse_args()

    if args.api_key:
        fw = flywheel.Client(api_key=args.api_key)
    else:  # This works if you are logged into a Flywheel instance on a Terminal:
        fw = flywheel.Client("")

    group_id = args.group_id
    safe_group_label = make_file_name_safe(group_id, replace_str="_")

    project_label = args.project_label
    safe_project_label = make_file_name_safe(project_label, replace_str="_")

    pre_path = f"{safe_group_label}_{safe_project_label}"

    if args.project_id:
        project = fw.get(args.project_id)
    else:
        project = fw.projects.find_one(f"group={group_id},label={project_label}")

    if "BIDS" in project.info:
        save_sidecar_as_metadata = True
    else:
        save_sidecar_as_metadata = False

    # Prints the instance you are logged into to make sure it is the right one.
    print(fw.get_config().site.api_url)

    bc = BIDSCuration()

    os.sys.exit(main(bc, args, project, pre_path, fw, save_sidecar_as_metadata))
