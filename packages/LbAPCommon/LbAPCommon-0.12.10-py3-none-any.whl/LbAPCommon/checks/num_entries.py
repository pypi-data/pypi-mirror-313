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
import math
import re

import numpy
import uproot

from .common import CheckFailureLevel, CheckResult, register_check

all_checks = {}


@register_check(all_checks, "num_entries")
def num_entries(
    test_ntuple_path_list,
    count,
    tree_pattern,
):
    """Number of entries check.

    Check that all matching TTree objects contain a minimum number of entries.

    Args:
        test_ntuple_path_list (list[file-like]): List of paths to files to analyse
        count (int): The minimum number of entries required
        tree_pattern (regex): A regular expression for the TTree objects to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            num_entries: The total number of events in the TTree
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
                    result.tree_data[key]["num_entries"] = 0

                result.tree_data[key]["num_entries"] += obj.num_entries

    for key, data in result.tree_data.items():
        nentries = data["num_entries"]
        if not nentries >= count:
            result.fail(
                f"Found too little entries {nentries} in {key} ({count} required)"
            )
        else:
            result.success(f"Found {nentries} in {key} ({count} required)")

    # If no matches were found the check should be marked as failed
    if len(result.tree_data) == 0:
        result.warning(f"No TTree objects found that match {tree_pattern}")

    return result


@register_check(all_checks, "num_entries_per_invpb")
def num_entries_per_invpb(
    test_ntuple_path_list,
    count_per_invpb,
    tree_pattern,
    lumi_pattern,
):
    """Number of entries per inverse picobarn check.

    Check that the matching TTree objects contain a minimum number of entries per unit luminosity (pb-1).

    Args:
        test_ntuple_path_list (list[file-like]): List of paths to files to analyse
        count_per_invpb (float): The minimum number of entries per unit luminosity required
        tree_pattern (regex): A regular expression for the TTree objects to check
        lumi_pattern (regex): A regular expression for the TTree object containing the luminosity information

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            num_entries (float): The total number of events in the TTree
            lumi_invpb (float): The total luminosity, in inverse picobarns
            num_entries_per_invpb (float): The total number of events divided by the total luminosity
    """
    result = CheckResult(can_combine=True)
    lumi = 0

    for filepath in test_ntuple_path_list:
        trees_opened = []
        with uproot.open(filepath) as f:
            for key, obj in f.items(cycle=False):
                if not isinstance(obj, uproot.TTree):
                    continue

                # If object is the decay TTree
                if re.fullmatch(tree_pattern, key):
                    if key in trees_opened:
                        continue
                    trees_opened.append(key)

                    # First time: initialise the CheckResult
                    if key not in result.tree_data:
                        result.tree_data[key] = {}
                        result.tree_data[key]["num_entries"] = 0
                        result.tree_data[key]["lumi_invpb"] = 0
                        result.tree_data[key]["num_entries_per_invpb"] = None

                    # Add number of entries to counter
                    result.tree_data[key]["num_entries"] += obj.num_entries

                # If object is lumi TTree
                if re.fullmatch(lumi_pattern, key):
                    try:
                        lumi_arr = obj["IntegratedLuminosity"].array(library="np")
                        err_lumi_arr = obj["IntegratedLuminosityErr"].array(
                            library="np"
                        )
                    except uproot.exceptions.KeyInFileError as e:
                        result.error(
                            f"Missing luminosity branch in {key!r} with error {e!r}"
                        )
                        result.can_combine = False
                        break

                    err_lumi_quad_sum = math.sqrt(numpy.sum(err_lumi_arr**2))
                    if err_lumi_quad_sum / numpy.sum(lumi_arr) >= 1:
                        result.can_combine = False
                        result.fail(
                            "Luminosity information is not reliable: 100% or greater relative uncertainty"
                        )
                        break
                    # Add to luminosity counter
                    lumi += numpy.sum(lumi_arr)

    # If no matches are found the check should be marked as failed and skip further checks
    if len(result.tree_data) == 0:
        result.can_combine = False
        result.error(f"No TTree objects found that match {tree_pattern}")

    if not result.has_failures(CheckFailureLevel.ERROR):
        for key in result.tree_data:
            if lumi == 0:
                result.can_combine = False
                result.error(
                    "Failed to get luminosity information (total luminosity = 0)"
                )
                continue

            entries_per_lumi = round(result.tree_data[key]["num_entries"] / lumi, 2)
            result.tree_data[key]["lumi_invpb"] = lumi
            result.tree_data[key]["num_entries_per_invpb"] = entries_per_lumi
            if entries_per_lumi < count_per_invpb:
                result.fail(
                    f"Found too little {entries_per_lumi} entries per unit luminosity (pb-1)"
                    f" in {key} ({count_per_invpb} required)"
                )
            else:
                result.success(
                    f"Found {entries_per_lumi} entries per unit luminosity (pb-1)"
                    f" in {key} ({count_per_invpb} required)"
                )

    return result
