###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import os
import re
from collections import defaultdict

import numpy as np
import uproot

from .common import CheckResult, register_check
from .utils import map_input_to_jobs

all_checks = {}


@register_check(all_checks, "branches_exist")
def branches_exist(
    test_ntuple_path_list,
    branches,
    tree_pattern,
):
    """Branches exist check.

    Check that all matching TTree objects contain a minimum number of entries.

    Args:
        test_ntuple_path_list: List of paths to files to analyse
        branches: List of branches that will be required to exist in TTree objects
        tree_pattern: A regular expression for the TTree objects to check

    Returns:
        A CheckResult object, which for each tree contains no tree_data key/values (an empty dict)
    """
    result = CheckResult(can_combine=True)

    for filepath in test_ntuple_path_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if not re.fullmatch(tree_pattern, key):
                    continue
                if key in trees_opened:
                    continue
                trees_opened.append(key)

                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}

                # Check that branches exist
                if not set(branches).issubset(obj.keys()):
                    missing_branches = list(set(branches) - set(obj.keys()))
                    result.can_combine = False
                    result.fail(
                        f"Required branches not found in Tree {key}: {missing_branches}"
                    )
                else:
                    result.success(f"All required branches were found in Tree {key}")

    # If no matches are found the check should be marked as failed, and can return early
    if len(result.tree_data) == 0:
        result.can_combine = False
        result.fail(f"No TTree objects found that match {tree_pattern}")

    return result


# Default Validations


@register_check(all_checks, "duplicate_inputs")
def duplicate_inputs(jobs_data: dict, job_name: str) -> CheckResult:
    """Check the yaml for any duplicate inputs between jobs.

    Args:
        jobs_data: Configuration for all of the jobs.
        job_name: Name of the job to validate.
        mode: How strict this validation should be.

    Returns:
        A CheckResult object, which for the given job corresponds to whether or not the job uses the same input as another.
        If a duplicate is found the value of CheckResult.passed depends on the selected mode.
    """
    result = CheckResult(can_combine=False)

    job_data = jobs_data[job_name]
    input_to_job = map_input_to_jobs(jobs_data)

    if "bk_query" in job_data["input"]:
        input_type = "bk_query"
        job_input = job_data["input"]["bk_query"].lower()
    elif "job_name" in job_data["input"]:
        input_type = "job_name"
        job_input = job_data["input"]["job_name"].lower()
    elif "transform_ids" in job_data["input"]:
        input_type = "transform_ids"
        job_input = tuple(job_data["input"]["transform_ids"])
    else:
        result.error(
            f"Job input for {job_name} must either be a bk_query, job_name or transform_ids!"
        )

    job_names = input_to_job[job_input]

    if len(job_names) > 1:
        result.warning(
            f"{job_name!r} shares an input ({job_data['input'][input_type]}) with the "
            f"following jobs {[name for name in job_names if name!=job_name]}"
        )

    return result


@register_check(all_checks, "job_name_matches_polarity")
def job_name_matches_polarity(jobs_data: dict, job_name: str) -> CheckResult:
    """Try to determine the expected polarity for the job and if that matches that of the input.

    Args:
        job_data: Configuration for the job.
        job_name: Name of the job to validate.

    Returns:
        A CheckResult object, which for the given job corresponds to whether or not the job's expected polarity matches its input.
        If not then the value of CheckResult.passed depends on the selected mode.
    """
    job_data = jobs_data[job_name]
    job_name = job_name.lower()
    result = CheckResult(can_combine=False)

    if "bk_query" in job_data["input"]:
        target = job_data["input"]["bk_query"].lower()
    elif "job_name" in job_data["input"]:
        target = job_data["input"]["job_name"].lower()
    elif "transform_ids" in job_data["input"]:
        result.success("Input is transform_ids, skip polarity check.")
        return result
    else:
        result.error(
            f"Job input for {job_name} must either be a bk_query, job_name or transform_ids!"
        )
        return result

    if "bk_query" in job_data["input"]:
        match = re.search(r"-mag(up|down)[-/]", target)
    else:
        match = re.search(r"mag(up|down)", target)
        if not match:
            match = re.search(r"([^a-z0-9]|\b)m(u|d)([^a-z0-9]|\b)", job_name)
    if not match:
        result.warning(
            f"Failed to find magnet polarity in {target}, skipping polarity validation for {job_name}. "
            "If you think a polarity should have been found please contact the Analysis Productions admins!"
        )
    else:
        good_pol = match.groups()[0]
        bad_pol = {"down": "up", "up": "down"}[good_pol]
        if f"mag{bad_pol}" in job_name:
            result.warning(
                f"Found 'mag{bad_pol}' in job name {job_name!r} with"
                f"'mag{good_pol}' input ({target!r}). "
                "Has the wrong magnet polarity been used?"
            )
        match = re.search(r"([^a-z0-9]|\b)m(u|d)([^a-z0-9]|\b)", job_name)
        if match and match.groups()[1] == bad_pol[0]:
            result.warning(
                f"Found 'm{bad_pol[0]}' in job name {job_name!r} with"
                f"'mag{good_pol}' input ({target!r}). "
                "Has the wrong magnet polarity been used?"
            )
    return result


@register_check(all_checks, "both_polarities_used")
def both_polarities_used(jobs_data: dict) -> CheckResult:
    """Check that for each bk_query both polarities have been used an equal number of times.

    Args:
        jobs_data: Configuration for all of the jobs.

    Returns:
        A CheckResult object, which for the given job corresponds to whether or not the job uses the same input as another.
        If a duplicate is found the value of CheckResult.passed depends on the selected mode.
    """
    result = CheckResult(can_combine=False)
    bk_query_to_job = map_input_to_jobs(jobs_data, bk_queries_only=True)

    polarity_len_swap = {"magdown": 5, "magup": 7}
    polarity_swap = {"magdown": "magup", "magup": "magdown"}

    for query in bk_query_to_job:
        index = None
        query_polarity = None
        both_polarities = False
        for polarity in {"magdown", "magup"}:
            if polarity in query:
                index = query.find(polarity)
                query_polarity = polarity
        if query_polarity:
            for compare_query in bk_query_to_job:
                if compare_query != query:
                    if polarity_swap[query_polarity] in compare_query:
                        if (
                            compare_query[:index]
                            + query_polarity
                            + compare_query[
                                (index + polarity_len_swap[query_polarity]) :
                            ]
                            == query
                        ):
                            both_polarities = True
                            if len(bk_query_to_job[query]) != len(
                                bk_query_to_job[compare_query]
                            ):
                                result.warning(
                                    f"The number of jobs requesting {query} does not"
                                    " match the number of jobs requesting its opposite"
                                    f" polarity counterpart {compare_query}."
                                )
            if not both_polarities:
                result.warning(
                    f"{query} has been requested as input for {len(bk_query_to_job[query])} job(s)"
                    " but its opposite polarity counterpart has not been requested for any jobs."
                    " Are you sure you do not want the other polarity?"
                )

    return result


@register_check(all_checks, "event_stats")
def event_stats(
    test_ntuple_path_list,
    tree_pattern="(DecayTree|(.*?)/DecayTree)",
):
    """Event retention statistics.

    Args:
        test_ntuple_path_list: List of paths to files to analyse
        tree_pattern: A regular expression for the TTree objects to check

    Returns:
        A CheckResult object, which for each tree contains no tree_data key/values (an empty dict)
    """
    result = CheckResult(can_combine=False)

    result.tree_data = defaultdict(dict)
    trees_opened = []

    for filepath in test_ntuple_path_list:
        eventNumbers_all = None
        with uproot.open(filepath) as f:
            filepath_basename = os.path.basename(filepath)
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue
                if tree_pattern is not None and not re.fullmatch(tree_pattern, key):
                    continue
                out_key = key
                if len(test_ntuple_path_list) > 1:
                    out_key = f"{filepath_basename}:{key}"
                if out_key in trees_opened:
                    continue
                trees_opened.append(out_key)

                # Check that event number branches exist
                branches = obj.keys()
                eventNumber_branch = None

                if "eventNumber" in branches:
                    eventNumber_branch = "eventNumber"  # DecayTreeTuple
                elif "EVENTNUMBER" in branches:
                    eventNumber_branch = "EVENTNUMBER"  # FunTuple
                else:
                    result.warning(
                        f"Required branches not found in Tree {key}: EVENTNUMBER or eventNumber"
                    )
                    return result

                df = obj.arrays([eventNumber_branch], library="pd")

                nCand = df.groupby(eventNumber_branch).size()
                result.tree_data[out_key] = {
                    "events": int(nCand.count()),
                    "mean(nCand)": float(nCand.mean()),
                    "max(nCand)": float(nCand.max()),
                    "min(nCand)": float(nCand.min()),
                }

                unique_eventNumber = df[
                    eventNumber_branch
                ].unique()  # returns numpy array

                if eventNumbers_all is not None:
                    eventNumbers_all = np.unique(
                        np.concatenate([eventNumbers_all, unique_eventNumber])
                    )
                else:
                    eventNumbers_all = unique_eventNumber

                result.success(
                    f"Tree {key} has {result.tree_data[out_key]['events']} events. "
                    f"Multiple candidates: mean = {result.tree_data[out_key]['mean(nCand)']:.2f}, "
                    f"max = {result.tree_data[out_key]['max(nCand)']}"
                )

        # this is the number of events in the processed event sample for this file where
        # output exists in one or more TTrees stored in the file.
        if eventNumbers_all is not None and len(eventNumbers_all):
            unique_events_in_output = int(eventNumbers_all.shape[0])
            result.tree_data["all_trees"] = {"n_events": unique_events_in_output}
            result.success(
                f"Output across all trees contain info from {unique_events_in_output} unique events."
            )

    if len(trees_opened) == 0:
        result.warning("No TTree objects found in output")

    return result
