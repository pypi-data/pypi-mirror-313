###############################################################################
# (c) Copyright 2021-2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Contains utility functions used to display and save the output of the checks.
"""
import copy
import json
import warnings
from collections import defaultdict

import hist
import numpy as np
import uproot
from hist import Hist

from .common import CheckResult


def map_input_to_jobs(jobs_data: dict, bk_queries_only=False):
    """Map each input used in the production to the job name(s) that use it as input.

    Args:
        jobs_data (dict): Configuration for all of the jobs.

    Returns:
        dict: A mapping from each input to a list of each job in the production that uses it.
    """
    input_to_job = defaultdict(set)
    for job_name, job_data in jobs_data.items():
        if "bk_query" in job_data["input"]:
            input_to_job[job_data["input"]["bk_query"].lower()].add(job_name)
        elif "job_name" in job_data["input"]:
            if not bk_queries_only:
                input_to_job[job_data["input"]["job_name"].lower()].add(job_name)
        elif "transform_ids" in job_data["input"]:
            if not bk_queries_only:
                input_to_job[tuple(job_data["input"]["transform_ids"])].add(job_name)
        else:
            raise ValueError(
                f"Job input for {job_name} must either be a bk_query, transform_ids, or a job_name!"
            )

    return input_to_job


def hist_to_root(job_name, check_results, output_path):
    """Save histograms to a root file.

    Creates a .root file at the provided output location, containing any
    histograms stored in the check results.

    Args:
        job_name (str): Name of the job within the production for which these
          checks were run. Unused.
        check_results (dict): Results of all checks performed for that job, as
          returned by checks.run_job_checks().
        output_path (str): Path of the root file to be created
    """
    # Create the file only if the check produce histograms in output
    checks_with_histo = ["range", "range_nd", "range_bkg_subtracted"]
    with uproot.recreate(output_path) as file_root:
        for cr in check_results:
            if (
                check_results[cr].passed
                and check_results[cr].check_type in checks_with_histo
            ):
                for key, data in check_results[cr].tree_data.items():
                    for hist_counter, _histo in enumerate(data.get("histograms", [])):
                        histo_name = f"{key}/{cr}_{hist_counter}"
                        file_root[histo_name] = _histo


def serialise_hist(obj):
    """Converts histograms into JSON.

    Creates a JSON serialisation of a histogram from the hist library. This
    uses a custom serialisation format, defined by this function.

    Args:
        obj (hist.basehist.BaseHist): A histogram from the hist library.

    Returns:
        JSON-style dict containing hist information (version 1).
    """
    if isinstance(obj.variances(flow=True), type(None)):
        raise ValueError(
            "Filling an unweighted storage with weights will result in incorrectly calculated variances"
        )

    serialised_obj = {
        "version": 1,
        "name": str(obj.name),
        "axes": [
            {
                "name": str(axis.name),
                "nbins": int(len(axis)),
                "min": float(axis.edges[0]),
                "max": float(axis.edges[-1]),
            }
            for axis in obj.axes
        ],
        "contents": list(obj.values(flow=True).tolist()),
        "sumw2": list(obj.variances(flow=True).tolist()),
    }
    return serialised_obj


def deserialise_hist(hist_json, check_type):
    """Converts custom JSON representation of histograms into a hist.

    Creates a histogram from the hist library from serialised JSON, as defined
    by serialise_hist(). This is made backwards-compatible using the "version"
    property of the serialised JSON, which allows hists to be reconstructed
    differently depending on the version number.

    Args:
        hist_json (dict): JSON-style dict containing hist serialisation.

    Returns:
        hist library histogram
    """
    if hist_json["version"] == 1:
        axes = [
            hist.axis.Regular(ax["nbins"], ax["min"], ax["max"], name=ax["name"])
            for ax in hist_json["axes"]
        ]
        hist_storage = (
            hist.storage.Double()
            if check_type != "range_bkg_subtracted"
            else hist.storage.Weight()
        )
        if 1 <= len(axes) <= 3:
            h = Hist(*axes, name=hist_json["name"], storage=hist_storage)
        else:
            raise ValueError(f"Expected between 1 and 3 axes, got {len(axes)}")

        # fill hists with values & variances
        if check_type == "range_bkg_subtracted":
            h.view(flow=True).value = np.array(hist_json["contents"])
            h.view(flow=True).variance = np.array(hist_json["sumw2"])
        else:
            h.view(flow=True)[:] = np.array(hist_json["contents"])
            # for Double() storage hists, variances are set automatically by this

        return h
    else:
        raise ValueError(
            f"Invalid hist serialisation version ({hist_json['version']}) selected!"
        )


def checks_to_JSON(
    checks_data,
    all_check_results,
    json_output_path=None,
):
    """Converts information about all checks into JSON.

    Args:
        checks_data (dict): Information defining checks, as returned by
          parsing.parse_yaml()
        all_check_results (dict): dict of results of checks for all different
          jobs. For one job, = {"job_name": checks.run_job_checks(...)}.
        json_output_path (str, None): If not None, will additionally write the
          output JSON to a file at the provided location.

    Returns:
        Plaintext JSON (string) containing check information
    """
    all_check_results_copy = copy.deepcopy(all_check_results)

    result = {}
    for job in all_check_results_copy:
        result[job] = {}
        for check in all_check_results_copy[job]:
            result[job][check] = {}

            result[job][check]["passed"] = all_check_results_copy[job][check].passed
            result[job][check]["messages"] = all_check_results_copy[job][check].messages
            result[job][check]["can_combine"] = all_check_results_copy[job][
                check
            ].can_combine
            result[job][check]["input"] = checks_data[check]
            result[job][check]["output"] = all_check_results_copy[job][check].tree_data

            # Convert histograms to JSON representation
            for tree in result[job][check]["output"]:
                if "histograms" in result[job][check]["output"][tree]:
                    n_hists = len(result[job][check]["output"][tree]["histograms"])
                    for n in range(n_hists):
                        result[job][check]["output"][tree]["histograms"][n] = (
                            serialise_hist(
                                result[job][check]["output"][tree]["histograms"][n]
                            )
                        )

    if json_output_path is not None:
        with open(json_output_path, "w", encoding="utf8") as json_file:
            json.dump(result, json_file, indent="  ")

    return json.dumps(result, indent="  ")


def JSON_to_checks(check_results_json):
    """Converts JSON of check results into check data and results.

    Deserialise information about all checks from a JSON format back into check
    data and results.

    Args:
        check_results_json (dict): JSON-style dict containing serialised check
          information, as created by checks_to_JSON().

    Returns:
        A tuple (checks_data, all_check_results) where checks_data contains
          information on how the checks are defined, and all_check_results
          contains the results of all checks. These return values should match
          exactly what was passed to checks_to_JSON() when creating this JSON.
    """
    checks_data = {}
    all_check_results = {}

    for job in check_results_json:
        all_check_results[job] = {}
        for check, json_data in check_results_json[job].items():
            checks_data[check] = json_data["input"]

            all_check_results[job][check] = CheckResult(
                check_type=json_data["input"]["type"],
                passed=json_data["passed"],
                messages=json_data["messages"],
                can_combine=json_data["can_combine"],
                tree_data=json_data["output"],
            )

            # Convert histograms from JSON representation
            for tree in all_check_results[job][check].tree_data:
                if "histograms" in all_check_results[job][check].tree_data[tree]:
                    for n, h in enumerate(
                        all_check_results[job][check].tree_data[tree]["histograms"]
                    ):
                        all_check_results[job][check].tree_data[tree]["histograms"][
                            n
                        ] = deserialise_hist(
                            h, all_check_results[job][check].check_type
                        )

    return checks_data, all_check_results


def _add_check_results(check_data, *results):
    """Add results from multiple of the same check on separate data.

    Adds together the results of the same check on multiple different datasets.
    All sets of results should be from the same job on different data, and
    should also be defined by identical YAML config. This function does not
    check that these conditions are met, this is done in combine_checks().

    Args:
        check_data (dict): YAML-type dictionary which configures the check.
        *results: Variable length argument list. All arguments should be of
          type CheckResult, and be created by the same check.

    Returns:
        A CheckResult containing the combination of results. This should
        be equivalent to if the check had been run once on all datasets
        combined (with the exception of the messages).
    """
    # Input validation
    if not all([isinstance(res, CheckResult) for res in results]):
        raise ValueError(
            "Arguments passed to *results must all be of type CheckResult "
            f"(result types: {[type(res) for res in results]})"
        )
    if not all([results[0].check_type == res.check_type for res in results]):
        raise ValueError(
            "Arguments passed to *results must have the same check type "
            f"(result check types: {[res.check_type for res in results]})"
        )
    if not all(
        [
            list(results[0].tree_data.keys()) == list(res.tree_data.keys())
            for res in results
        ]
    ):
        raise ValueError(
            "Arguments passed to *results must have the same list of TTrees in tree_data "
            f"(result TTrees: {[list(res.tree_data.keys()) for res in results]})"
        )
    if len(results) == 0:
        raise ValueError("Found 0 checks to be combined")

    # Create basic CheckResult with everything except tree_data combined
    added_result = CheckResult(
        check_type=results[0].check_type,
        passed=True,  # this gets modified later by the check result addition
        messages=[msg for res in results for msg in res.messages],
        can_combine=True,  # the output of a combination can be combined again with other CheckResults objects if necessary
        tree_data={tree: {} for tree in results[0].tree_data},
    )

    # Add data together
    for tree in results[0].tree_data:
        data_added = added_result.tree_data[tree]

        # range check
        if added_result.check_type == "range":
            data_added["histograms"] = []
            data_added["histograms"].append(
                sum([res.tree_data[tree]["histograms"][0] for res in results])
            )
            data_added["num_entries"] = data_added["histograms"][0].sum()
            bin_centers = data_added["histograms"][0].axes[0].centers
            data_added["mean"] = (
                sum(bin_centers * data_added["histograms"][0].values())
                / data_added["histograms"][0].sum()
            )
            if data_added["num_entries"] >= 2:
                data_added["variance"] = sum(
                    (bin_centers - data_added["mean"]) ** 2
                    * data_added["histograms"][0].values()
                ) / (data_added["histograms"][0].sum() - 1)
            else:
                data_added["variance"] = 0
            data_added["stddev"] = data_added["variance"] ** 0.5
            data_added["num_entries_in_mean_window"] = sum(
                [res.tree_data[tree]["num_entries_in_mean_window"] for res in results]
            )
            # update check result
            added_result.passed = added_result.passed and all(
                [
                    data_added["num_entries"] > 0,
                    (
                        abs(data_added["mean"] - check_data["exp_mean"])
                        <= check_data["mean_tolerance"]
                        if check_data.get("exp_mean") is not None
                        and check_data.get("mean_tolerance") is not None
                        else True
                    ),
                    (
                        abs(data_added["stddev"] - check_data["exp_std"])
                        <= check_data["std_tolerance"]
                        if check_data.get("exp_std") is not None
                        and check_data.get("std_tolerance") is not None
                        else True
                    ),
                ]
            )

        # range_bkg_subtracted check
        elif added_result.check_type == "range_bkg_subtracted":
            data_added["histograms"] = []
            for i in range(4):
                data_added["histograms"].append(
                    sum([res.tree_data[tree]["histograms"][i] for res in results])
                )
            # update check result
            added_result.passed = added_result.passed and all(
                [
                    data_added["histograms"][1].view().value.sum() > 0,
                    data_added["histograms"][2].view().value.sum() > 0,
                ]
            )

        # range_nd check
        elif added_result.check_type == "range_nd":
            data_added["histograms"] = []
            data_added["histograms"].append(
                sum([res.tree_data[tree]["histograms"][0] for res in results])
            )
            data_added["num_entries"] = data_added["histograms"][0].sum()
            # update check result
            added_result.passed = added_result.passed and (
                data_added["num_entries"] > 0
            )

        # num_entries check
        elif added_result.check_type == "num_entries":
            data_added["num_entries"] = sum(
                [res.tree_data[tree]["num_entries"] for res in results]
            )
            # update check result
            added_result.passed = added_result.passed and (
                data_added["num_entries"] >= check_data["count"]
            )

        # num_entries_per_invpb check
        elif added_result.check_type == "num_entries_per_invpb":
            data_added["num_entries"] = sum(
                [res.tree_data[tree]["num_entries"] for res in results]
            )
            data_added["lumi_invpb"] = sum(
                [res.tree_data[tree]["lumi_invpb"] for res in results]
            )
            data_added["num_entries_per_invpb"] = (
                data_added["num_entries"] / data_added["lumi_invpb"]
            )
            # update check result
            added_result.passed = added_result.passed and (
                data_added["num_entries_per_invpb"] >= check_data["count_per_invpb"]
            )

        elif added_result.check_type == "branches_exist":
            # Nothing stored in tree_data for branches_exist checks
            # update check result
            added_result.passed = added_result.passed and all(
                res.passed for res in results
            )

        elif added_result.check_type == "duplicate_inputs":
            added_result.passed = all([res.passed for res in results])

        elif added_result.check_type == "job_name_matches_polarity":
            added_result.passed = all([res.passed for res in results])

        elif added_result.check_type == "both_polarities_used":
            added_result.passed = all([res.passed for res in results])

    return added_result


def combine_checks(checks_info_tuple_list):
    """Combine the results of checks on separate datasets.

    Combines check results for separate datasets. In order for results to be
    combined, the input must be identical (names and contents), and the job
    name must match.

    Args:
        checks_info_tuple_list (list): List containing tuples of check info
          (checks_data, all_check_results), as described in the args of
          checks_to_JSON(). Each element of the list should correspond to a
          different dataset so there is no duplication when combining.

    Returns:
        A tuple (checks_data, comb_check_results) where checks_data contains
          information on how the checks are defined, and comb_check_results
          contains the results of all checks after combining.
    """
    # Input validation: checks_info_tuple_list should be a list of tuples (len=2) of dicts
    if not all(len(tup) == 2 for tup in checks_info_tuple_list):
        raise ValueError(
            "Invalid checks_info_tuple_list passed - all elements must be tuples of length 2"
        )

    # Establish the combined checks_data with info from user's production YAML
    checks_data = {}
    for tup in checks_info_tuple_list:
        data, _results = tup
        for c_name, c_data in data.items():
            # Add check if not already present
            if c_name not in checks_data:
                checks_data[c_name] = c_data
            # Otherwise, confirm that the check is configured identically
            else:
                if c_data != checks_data[c_name]:
                    warnings.warn(
                        f"Found check with duplicate name ({c_name}) but different configuration - cannot be combined",
                        stacklevel=2,
                    )

    # Create a dict containing indices of datasets to include when combining a check for each job
    checks_datasets = {}
    for i, tup in enumerate(checks_info_tuple_list):
        data, results = tup
        for job_name, job_check_results in results.items():
            # Add job if not already present
            if job_name not in checks_datasets:
                checks_datasets[job_name] = {}

            # Fill in dataset list
            for check_name in job_check_results:
                # Skip if this is a duplicate check with different configuration
                if checks_data[check_name] != data[check_name]:
                    continue

                # Add check to that job if not already present
                if check_name not in checks_datasets[job_name]:
                    checks_datasets[job_name][check_name] = []
                # Don't combine checks if the can_combine flag is set to False.
                if not job_check_results[check_name].can_combine:
                    warnings.warn(
                        f"The result for {job_name} cannot be included in the {check_name} "
                        "combination as the can_combine flag is False.",
                        stacklevel=2,
                    )
                    continue
                checks_datasets[job_name][check_name].append(i)

    # Combine results
    comb_check_results = {}
    for job_name in checks_datasets:
        comb_check_results[job_name] = {}
        for check_name in checks_datasets[job_name]:
            datasets = checks_datasets[job_name][check_name]
            comb_check_results[job_name][check_name] = _add_check_results(
                checks_data[check_name],
                *[
                    cit[1][job_name][check_name]
                    for i, cit in enumerate(checks_info_tuple_list)
                    if i in datasets
                ],
            )

    return checks_data, comb_check_results
