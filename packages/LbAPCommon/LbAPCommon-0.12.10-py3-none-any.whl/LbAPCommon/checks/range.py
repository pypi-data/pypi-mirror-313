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
import re
from itertools import combinations

import awkward as ak
import hist
import numpy
import uproot
from hist import Hist

from .common import CheckFailureLevel, CheckResult, register_check

all_checks = {}


@register_check(all_checks, "range")
def range_check(
    test_ntuple_path_list,
    expression,
    limits,
    n_bins,
    tree_pattern,
    blind_ranges=None,
    exp_mean=None,
    exp_std=None,
    mean_tolerance=None,
    std_tolerance=None,
):
    """Range check.

    Check if there is at least one entry in the TTree object with a specific variable falling in a pre-defined range.
    If the expected mean and standard deviation values are given in input, they are compared with the observed ones
    and their agreement within the provided *_tolerance is checked. It is also possible to blind some regions.

    Args:
        test_ntuple_path_list (list[file-like]): List of paths to files to analyse
        expression (str): Name of the variable (or expression depending on varibales in the TTree) to be checked
        limits (dict): Pre-defined range for x axis
        n_bins (int): Number of bins for the histogram
        tree_pattern (regex): A regular expression for the TTree object to check
        blind_ranges (dict, optional): Regions to be blinded in the histogram (optional)
        exp_mean (float, optional): Expected mean value (optional)
        exp_std (float, optional): Expected standard deviation (optional)
        mean_tolerance (float, optional): Maximum shift tolerated between expected and observed mean values (optional)
        std_tolerance (float, optional): Maximum shift tolerated between expected and observed values of standard deviation
            (optional)

    Returns:
        A CheckResult object, which for each tree contains result.tree_data key/values:
            histograms (list[Hist]): Filled 1D histogram of the quantity defined by the expression parameter
            num_entries (float): The total number of entries in the histogram (with blind ranges applied)
            mean (float): The mean of the histogram (approximated using binned data)
            variance (float): The variance of the histogram (approximated using binned data)
            stddev (float): The standard deviation of the histogram (approximated using binned data)
            num_entries_in_mean_window (float): The number of events falling in the exp_mean +- exp_std region (with
                blind ranges applied)
    """
    result = CheckResult(can_combine=True)

    bin_centers = None

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
                    axis0 = hist.axis.Regular(
                        n_bins, limits["min"], limits["max"], name=expression
                    )
                    bin_centers = axis0.centers
                    h = Hist(axis0, name=f"{key} {expression}")
                    result.tree_data[key]["histograms"] = [h]
                    result.tree_data[key]["num_entries"] = 0
                    result.tree_data[key]["mean"] = 0
                    result.tree_data[key]["variance"] = 0
                    result.tree_data[key]["stddev"] = 0
                    result.tree_data[key]["num_entries_in_mean_window"] = 0

                values_obj = {}
                # Check if the branch is in the Tree or if the expression is correctly written
                try:
                    values_obj = obj.arrays(expression, library="ak")
                except uproot.exceptions.KeyInFileError as e:
                    result.error(f"Missing branch in {key!r} with {e!r}")
                    result.can_combine = False
                    continue

                # check that we extracted one array only.
                if len(values_obj.fields) != 1:
                    result.error(
                        f"Ambiguous expression {expression!r} returned more than one branch in {key!r}"
                    )
                    continue

                sole_arr_field = values_obj.fields[0]
                array_type = str(ak.type(values_obj[sole_arr_field]))
                # check that the expression evaluated to a 1-dimensional, plottable, array
                # otherwise, by default select sole_arr_field[:,0], but raise a warning and add a message in the result object
                if "var * " in array_type:
                    # We have a jagged array.
                    new_expression = expression + "[:,0]"
                    result.warning(
                        f"Expression {expression!r} evaluated to a variable-length array with shape {array_type!r} in {key!r}. "
                        f"Selecting by default {expression}[:,0]. "
                        "If this is not intended, please update the expression value accordingly."
                    )
                    try:
                        values_obj = obj.arrays(new_expression, library="ak")
                    except uproot.exceptions.KeyInFileError as e:
                        result.error(f"Missing branch in {key!r} with {e!r}")
                        continue
                    sole_arr_field = values_obj.fields[0]

                test_array = values_obj[sole_arr_field]

                if test_array.ndim != 1:
                    # We don't have a plottable 1-D array.
                    result.error(
                        f"Expression {expression!r} evaluated to non 1-D array with type {array_type!r} in {key!r}"
                    )
                    continue

                # Go to numpy & apply limits
                test_array = test_array.to_numpy()

                test_array = test_array[
                    (test_array < limits["max"]) & (test_array > limits["min"])
                ]

                # Apply blinding
                if blind_ranges is not None:
                    if isinstance(blind_ranges, dict):
                        # Take into account that there could be multiple regions to blind
                        blind_ranges = [blind_ranges]
                    for blind_range in blind_ranges:
                        lower, upper = blind_range["min"], blind_range["max"]
                        test_array = test_array[
                            ~((lower < test_array) & (test_array < upper))
                        ]

                # Fill histogram
                result.tree_data[key]["histograms"][0].fill(test_array)

                # Add to event counters
                result.tree_data[key]["num_entries"] += test_array.size

                if exp_mean is not None and exp_std is not None:
                    events_in_exp_mean_region = test_array[
                        (exp_mean - exp_std < test_array)
                        & (test_array < exp_mean + exp_std)
                    ]
                    result.tree_data[key][
                        "num_entries_in_mean_window"
                    ] += events_in_exp_mean_region.size

    # If no matches are found the check should be marked as failed and skip further checking
    if len(result.tree_data) == 0:
        result.error(f"No TTree objects found that match {tree_pattern}")

    # Check the completely filled histograms
    if not result.has_failures(minimum=CheckFailureLevel.WARNING):
        for key in result.tree_data:
            # Get this tree's histogram
            h = result.tree_data[key]["histograms"][0]

            # Require at least one event
            # However, even if the histogram is empty, we want to be able to combine
            # the result later (so "can_combine" flag is left "True")
            if h.sum() == 0:
                result.error(f"No events found in range for Tree {key}")
                continue

            # Calculate mean, variance, & standard deviation
            mean = sum(bin_centers * h.values()) / h.sum()
            result.tree_data[key]["mean"] = mean

            if h.sum() >= 2:
                variance = sum((bin_centers - mean) ** 2 * h.values()) / (h.sum() - 1)
            else:
                variance = 0

            result.tree_data[key]["variance"] = variance

            stddev = variance**0.5
            result.tree_data[key]["stddev"] = stddev

            # Apply expected mean requirement
            if exp_mean is not None and mean_tolerance is not None:
                delta_mean = abs(mean - exp_mean)
                if delta_mean > mean_tolerance:
                    result.fail(
                        f"The observed mean ({mean}) differs from the expected"
                        f" value by {delta_mean} (<={mean_tolerance} required)"
                    )
                    continue

            # Apply expected standard deviation requirement
            if exp_std is not None and std_tolerance is not None:
                delta_std = abs(stddev - exp_std)
                if delta_std > std_tolerance:
                    result.fail(
                        f"The observed standard deviation ({stddev}) differs from the expected value by "
                        f"{delta_std} (<={std_tolerance} required)"
                    )
                    continue

            # Histogram check successful
            result.success(
                f"Histogram of {expression} successfully filled from TTree {key} (contains {h.sum()} events)"
            )

    return result


@register_check(all_checks, "range_nd")
def range_nd_check(
    test_ntuple_path_list,
    expressions,
    limits,
    n_bins,
    tree_pattern,
    blind_ranges=None,
):
    """N-dimensional range check.

    Produce 2-dimensional histograms of variables taken from a TTree object.

    Args:
        test_ntuple_path_list (list[file-like]): List of paths to files to analyse
        expressions (dict): Name of the variables (or expressions) to be checked.
        limits (dict): Pre-defined ranges
        n_bins (dict): Number of bins for the histogram
        tree_pattern (regex): A regular expression for the TTree object to check
        blind_ranges (dict, optional): Regions to be blinded in the histogram

    Returns:
        A CheckResult object, which for each tree contains result.tree_data key/values:
            histograms (list[Hist]): A list of filled histograms of the quantities defined by the expression parameters
            num_entries (float): The total number of entries in the histogram (with blind ranges applied)
    """
    result = CheckResult(can_combine=True)

    # for these first two checks don't change behaviour based on
    # the requested mode since these must pass for the check to make sense
    # Check if the number of variables matches expectations
    length_expr = len(expressions)
    length_limits = len(limits)
    if length_expr != 2 and length_expr != 3:
        result.error("Expected two or three variables.")
        result.can_combine = False
        return result

    if length_expr != length_limits:
        result.error("For each variable, a corresponding range should be defined.")
        result.can_combine = False
        return result

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
                    result.tree_data[key]["histograms"] = []
                    for key_i, key_j in combinations(list(expressions.keys()), 2):
                        axis0 = hist.axis.Regular(
                            n_bins[key_i],
                            limits[key_i]["min"],
                            limits[key_i]["max"],
                            name=expressions[key_i],
                        )
                        axis1 = hist.axis.Regular(
                            n_bins[key_j],
                            limits[key_j]["min"],
                            limits[key_j]["max"],
                            name=expressions[key_j],
                        )
                        h = Hist(
                            axis0,
                            axis1,
                            name=f"{key} {expressions[key_i]}/{expressions[key_j]}",
                        )
                        result.tree_data[key]["histograms"] += [h]
                    if length_expr == 3:
                        for key_i, key_j, key_k in combinations(
                            list(expressions.keys()), 3
                        ):
                            axis0 = hist.axis.Regular(
                                n_bins[key_i],
                                limits[key_i]["min"],
                                limits[key_i]["max"],
                                name=expressions[key_i],
                            )
                            axis1 = hist.axis.Regular(
                                n_bins[key_j],
                                limits[key_j]["min"],
                                limits[key_j]["max"],
                                name=expressions[key_j],
                            )
                            axis2 = hist.axis.Regular(
                                n_bins[key_k],
                                limits[key_k]["min"],
                                limits[key_k]["max"],
                                name=expressions[key_k],
                            )
                            h = Hist(
                                axis0,
                                axis1,
                                axis2,
                                name=f"{key} {expressions[key_i]}/{expressions[key_j]}/{expressions[key_k]}",
                            )
                        result.tree_data[key]["histograms"] += [h]

                    result.tree_data[key]["num_entries"] = 0

                values_obj = {}
                values_obj_new = {}
                list_expressions = list(expressions.values())
                list_keys = list(expressions.keys())
                # Check if the branch is present in the TTree or if the expressions are correctly written
                try:
                    values_obj = obj.arrays(list_expressions, library="ak")
                except uproot.exceptions.KeyInFileError as e:
                    result.error(f"Missing branch in {key!r} with {e!r}")
                    result.can_combine = False
                    continue

                for index, expr in enumerate(list_expressions):
                    # Check if the branch is present in the TTree or if the expressions are correctly written
                    values_obj_tmp = obj.arrays(expr, library="ak")
                    # Check that we extracted one array only.
                    if len(values_obj_tmp.fields) != 1:
                        result.error(
                            f"Ambiguous expression {expr!r} returned more than one branch in {key!r}"
                        )
                        continue

                    sole_arr_field = values_obj_tmp.fields[0]
                    array_type = str(ak.type(values_obj[sole_arr_field]))
                    # check that the expression evaluated to a 1-dimensional, plottable, array
                    # otherwise, by default select sole_arr_field[:,0], but raise a warning and
                    # add a message in the result object
                    if "var * " in array_type:
                        # We have a jagged array.
                        new_expression = expr + "[:,0]"
                        result.warning(
                            f"Expression {expr!r} evaluated to a variable-length array with shape {array_type!r} in {key!r}. "
                            f"Selecting by default {expr}[:,0]. "
                            "If this is not intended, please update the expression value accordingly."
                        )
                        try:
                            values_obj_tmp = obj.arrays(new_expression, library="ak")
                        except uproot.exceptions.KeyInFileError as e:
                            result.error(f"Missing branch in {key!r} with {e!r}")
                            continue
                        list_expressions[index] = new_expression
                        expressions[list_keys[index]] = new_expression
                        sole_arr_field = values_obj_tmp.fields[0]

                    test_array = values_obj_tmp[sole_arr_field]
                    if test_array.ndim != 1:
                        # We don't have a plottable 1-D array.
                        result.error(
                            f"Expression {expr!r} evaluated to non 1-D array with type {array_type!r} in {key!r}"
                        )
                        continue
                if result.has_failures(minimum=CheckFailureLevel.ERROR):
                    continue

                # Go to numpy
                values_obj = obj.arrays(list_expressions, library="ak").to_numpy()

                # Apply blinding and limits
                mask_total = []
                indexes = []
                mask = numpy.zeros(len(values_obj[list_expressions[0]]), dtype=bool)
                for ax, range_limits in limits.items():
                    lower, upper = range_limits["min"], range_limits["max"]
                    indexes = numpy.where(
                        (
                            (values_obj[expressions[ax]] > upper)
                            | (values_obj[expressions[ax]] < lower)
                        )
                    )
                    mask_tmp = numpy.zeros(
                        len(values_obj[list_expressions[0]]), dtype=bool
                    )
                    mask_tmp[indexes] = True
                    mask = numpy.logical_or(mask, mask_tmp)
                mask_total.append(mask)
                if blind_ranges is not None:
                    if isinstance(blind_ranges, dict):
                        # Take into account that there could be multiple regions to blind
                        blind_ranges = [blind_ranges]
                    for blind_range in blind_ranges:
                        mask = numpy.ones(
                            len(values_obj[list_expressions[0]]), dtype=bool
                        )
                        for ax, range_limits in blind_range.items():
                            lower, upper = range_limits["min"], range_limits["max"]
                            indexes = numpy.where(
                                (
                                    (values_obj[expressions[ax]] < upper)
                                    & (values_obj[expressions[ax]] > lower)
                                )
                            )
                            mask_tmp = numpy.zeros(
                                len(values_obj[list_expressions[0]]), dtype=bool
                            )
                            mask_tmp[indexes] = True
                            mask = numpy.logical_and(mask, mask_tmp)
                        mask_total.append(mask)
                mask_final = numpy.zeros(
                    len(values_obj[list_expressions[0]]), dtype=bool
                )
                for mask in mask_total:
                    mask_final = numpy.logical_or(mask_final, mask)
                for expr in list_expressions:
                    values_obj_new[expr] = values_obj[expr][~mask_final]
                # Fill the histograms
                hist_index = 0
                for key_i, key_j in combinations(list_keys, 2):
                    h = result.tree_data[key]["histograms"][hist_index]
                    h.fill(
                        values_obj_new[expressions[key_i]],
                        values_obj_new[expressions[key_j]],
                    )
                    hist_index += 1
                # If more than two variables are given in input, return also 3D histograms
                if length_expr == 3:
                    for key_i, key_j, key_k in combinations(list_keys, 3):
                        h = result.tree_data[key]["histograms"][hist_index]
                        h.fill(
                            values_obj_new[expressions[key_i]],
                            values_obj_new[expressions[key_j]],
                            values_obj_new[expressions[key_k]],
                        )
                        hist_index += 1

                # Add to event counter
                result.tree_data[key]["num_entries"] += values_obj_new[
                    list_expressions[0]
                ].size

    # If no matches are found the check should be marked as failed and skip further checking
    if len(result.tree_data) == 0:
        result.can_combine = False
        result.error(f"No TTree objects found that match {tree_pattern}")

    # Check the completely filled histograms
    if not result.has_failures():
        for key in result.tree_data:
            for h in result.tree_data[key]["histograms"]:
                # Require at least one event
                if h.sum() == 0:
                    result.fail(f"No events found in range for Tree {key}")
                    continue
                # Histogram check successful
                if len(h.axes) == 2:
                    result.success(
                        f"Histogram of {h.axes[0].name}, {h.axes[1].name} successfully filled"
                        f" from TTree {key} (contains {h.sum()} events)"
                    )
                else:
                    result.success(
                        f"Histogram of {h.axes[0].name}, {h.axes[1].name}, {h.axes[2].name} successfully filled"
                        f" from TTree {key} (contains {h.sum()} events)"
                    )
    return result


@register_check(all_checks, "range_bkg_subtracted")
def range_bkg_subtracted_check(
    test_ntuple_path_list,
    expression,
    limits,
    expr_for_subtraction,
    mean_sig,
    background_shift,
    background_window,
    signal_window,
    n_bins,
    blind_ranges,
    tree_pattern,
):
    """Range check with background subtraction.

    Check if there is at least one entry in the TTree object with a specific variable falling in a pre-defined range.
    The background-subtracted histogram is then produced as output. Background is subtracted assuming a linear
    distribution. In particular, signal ([m-s, m+s]) and background ([m-b-delta, m-b] U [m+b, m+b+delta]) windows have
    to be defined on a control variable. Then, one histogram is created for events falling in the signal region and
    another histogram is created for events falling in the background region. The subtraction, using the proper scaling
    factor, is finally performed. It is also possible to blind some regions.

    Args:
        test_ntuple_path_list (list[file-like]): List of paths to files to analyse
        expression (str): Name of the variable (or expression depending on varibales in the TTree) to be checked
        limits (dict): Pre-defined range
        expr_for_subtraction (str): Name of the control variable (or expression depending on varibales in the TTree) to
            be used to perform background subtraction
        mean_sig (float): Expected mean value of expr_for_subtraction variable. The signal window will be centered
            around this value.
        background_shift (float):  Shift, w.r.t the "mean_sig" value, used to define the two background regions.
        background_window (float):  Length of the background windows (of expr_for_subtraction variable).
        signal_window (float): Length of the signal window (of expr_for_subtraction variable) used for background
            subtraction. The window is centered around the value of "mean_sig".
        n_bins (int): Number of bins for the histogram
        blind_ranges (dict): Regions to be blinded in the histogram
        tree_pattern (regex): A regular expression for the TTree object to check

    Returns:
        A CheckResult object, which for each tree contains tree_data key/values:
            histograms: A list of filled 1D histograms,
                Index 0: The control variable used to perform the subtraction
                Index 1: Events in the signal window
                Index 2: Events in the background window
                Index 3: The background-subtracted result
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

                # Calculate the min and max values of each of the two background regions.
                # By construction, the two intervals have the same length
                background_range_low = {
                    "min": mean_sig - background_shift - background_window,
                    "max": mean_sig - background_shift,
                }
                background_range_high = {
                    "min": mean_sig + background_shift,
                    "max": mean_sig + background_shift + background_window,
                }
                # Calculate the min and max values of each of the signal region
                signal_range = {
                    "min": mean_sig - signal_window / 2.0,
                    "max": mean_sig + signal_window / 2.0,
                }
                # First time: initialise the CheckResult
                if key not in result.tree_data:
                    result.tree_data[key] = {}

                    # Create the histogram for the control variable used to perform background subtraction
                    axis0 = hist.axis.Regular(
                        n_bins,
                        background_range_low["min"],
                        background_range_high["max"],
                        name=expr_for_subtraction,
                    )
                    result.tree_data[key]["histograms"] = [
                        Hist(
                            axis0,
                            name=f"{key} {expression}",
                            storage=hist.storage.Weight(),
                        )
                    ]
                    # Add ranges to histogram metadata. Signal and background regions can be then highlighted in the final plot.
                    result.tree_data[key]["histograms"][0].metadata = [
                        background_range_low["min"],
                        background_range_low["max"],
                        background_range_high["min"],
                        background_range_high["max"],
                        signal_range["min"],
                        signal_range["max"],
                    ]

                    # Add signal & background region histograms (using same axis)
                    axis1 = hist.axis.Regular(
                        n_bins, limits["min"], limits["max"], name=expression
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} signal",
                            storage=hist.storage.Weight(),
                        )
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} background",
                            storage=hist.storage.Weight(),
                        )
                    )
                    result.tree_data[key]["histograms"].append(
                        Hist(
                            axis1,
                            name=f"{key} {expression} signal after bkg subtraction",
                            storage=hist.storage.Weight(),
                        )
                    )

                # Control variable
                # Check if the branch is in the Tree or if the expression is correctly written
                values_obj = {}
                try:
                    values_obj = obj.arrays(expr_for_subtraction, library="ak")
                except uproot.exceptions.KeyInFileError as e:
                    result.error(f"Missing branch in {key!r} with {e!r}")
                    result.can_combine = False
                    continue

                # check that we extracted one array only.
                if len(values_obj.fields) != 1:
                    result.error(
                        f"Ambiguous expression {expr_for_subtraction!r} returned more than one branch in {key!r}"
                    )
                    continue

                sole_arr_field = values_obj.fields[0]
                array_type = str(ak.type(values_obj[sole_arr_field]))
                # check that the expression evaluated to a 1-dimensional, plottable, array
                # otherwise, by default select sole_arr_field[:,0], but raise a warning and add a message in the result object
                if "var * " in array_type:
                    # We have a jagged array.
                    result.warning(
                        f"Expression {expr_for_subtraction!r} evaluated to a variable-length array with "
                        f"shape {array_type!r} in {key!r}. "
                        f"Selecting by default {expr_for_subtraction}[:,0]. "
                        "If this is not intended, please update the expression value accordingly."
                    )
                    expr_for_subtraction = expr_for_subtraction + "[:,0]"
                    try:
                        values_obj = obj.arrays(expr_for_subtraction, library="ak")
                    except uproot.exceptions.KeyInFileError as e:
                        result.error(f"Missing branch in {key!r} with {e!r}")
                        continue
                    sole_arr_field = values_obj.fields[0]

                var_for_bkgsub_array = values_obj[sole_arr_field]

                if var_for_bkgsub_array.ndim != 1:
                    # We don't have a plottable 1-D array.
                    result.error(
                        f"Expression {expression!r} evaluated to non 1-D array with type {array_type!r} in {key!r}"
                    )
                    continue

                # Go to numpy and fill control variable histogram
                var_for_bkgsub_array = var_for_bkgsub_array.to_numpy()
                result.tree_data[key]["histograms"][0].fill(var_for_bkgsub_array)

                # Select events in signal region
                cut_string = (
                    "("
                    + expr_for_subtraction
                    + ">"
                    + str(signal_range["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(signal_range["max"])
                    + ")"
                )

                # Varibale to be checked
                # Check if the branch is in the Tree or if the expression is correctly written
                try:
                    values_obj = obj.arrays(expression, cut_string, library="ak")
                except uproot.exceptions.KeyInFileError as e:
                    result.messages += [f"Missing branch in {key!r} with {e!r}"]
                    result.passed = False
                    continue

                # check that we extracted one array only.
                if len(values_obj.fields) != 1:
                    result.messages += [
                        f"Ambiguous expression {expression!r} returned more than one branch in {key!r}"
                    ]
                    result.passed = False
                    continue

                sole_arr_field = values_obj.fields[0]
                array_type = str(ak.type(values_obj[sole_arr_field]))
                # check that the expression evaluated to a 1-dimensional, plottable, array
                # otherwise, by default select sole_arr_field[:,0], but raise a warning and add a message in the result object
                if "var * " in array_type:
                    # We have a jagged array.
                    new_expression = expression + "[:,0]"
                    result.warning(
                        f"Expression {expression!r} evaluated to a variable-length array with shape {array_type!r} in {key!r}. "
                        f"Selecting by default {expression}[:,0]. "
                        "If this is not intended, please update the expression value accordingly."
                    )
                    try:
                        values_obj = obj.arrays(
                            new_expression, cut_string, library="ak"
                        )
                    except uproot.exceptions.KeyInFileError as e:
                        result.error(f"Missing branch in {key!r} with {e!r}")
                        continue
                    sole_arr_field = values_obj.fields[0]

                values_sig = values_obj[sole_arr_field]

                if values_sig.ndim != 1:
                    # We don't have a plottable 1-D array.
                    result.error(
                        f"Expression {expression!r} evaluated to non 1-D array with type {array_type!r} in {key!r}"
                    )
                    continue

                # Go to numpy
                test_array_sig = values_sig.to_numpy()
                test_array_sig = test_array_sig[
                    numpy.where(
                        (test_array_sig < limits["max"])
                        & (test_array_sig > limits["min"])
                    )
                ]

                # Select events in background region
                cut_string = (
                    "( ("
                    + expr_for_subtraction
                    + ">"
                    + str(background_range_low["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(background_range_low["max"])
                    + ") ) | ( ("
                    + expr_for_subtraction
                    + ">"
                    + str(background_range_high["min"])
                    + ") & ("
                    + expr_for_subtraction
                    + "<"
                    + str(background_range_high["max"])
                    + ") )"
                )

                values_bkg = obj.arrays(expression, cut_string, library="ak")
                sole_arr_field = values_bkg.fields[0]
                test_array_bkg = values_bkg[sole_arr_field].to_numpy()
                test_array_bkg = test_array_bkg[
                    numpy.where(
                        (test_array_bkg < limits["max"])
                        & (test_array_bkg > limits["min"])
                    )
                ]

                # Apply blinding
                if blind_ranges is not None:
                    if isinstance(blind_ranges, dict):
                        blind_ranges = [blind_ranges]
                        # Take into account that there could be multiple regions to blind
                    for blind_range in blind_ranges:
                        lower, upper = blind_range["min"], blind_range["max"]
                        test_array_sig = test_array_sig[
                            ~((lower < test_array_sig) & (test_array_sig < upper))
                        ]
                        test_array_bkg = test_array_bkg[
                            ~((lower < test_array_bkg) & (test_array_bkg < upper))
                        ]

                # Fill signal & background histograms
                result.tree_data[key]["histograms"][1].fill(test_array_sig)
                result.tree_data[key]["histograms"][2].fill(test_array_bkg)

    # If no matches are found the check should be marked as failed and skip further checks
    if len(result.tree_data) == 0:
        result.can_combine = False
        result.fail(f"No TTree objects found that match {tree_pattern}")
        return result

    if not result.has_failures(CheckFailureLevel.ERROR):
        for key in result.tree_data:
            # Require events in both signal and background histograms
            if (result.tree_data[key]["histograms"][1].view().value.sum() == 0) or (
                result.tree_data[key]["histograms"][2].view().value.sum() == 0
            ):
                result.fail(
                    f"Not enough events for background subtraction found in range for Tree {key}"
                )
                continue

            # Assume linear background distribution and evaluate fraction of background in the signal region
            alpha = 2.0 * background_window / signal_window

            # Histogram subtraction
            hsub = (
                result.tree_data[key]["histograms"][1]
                + (-1 * alpha) * result.tree_data[key]["histograms"][2]
            )
            result.tree_data[key]["histograms"][3] = hsub

            result.success(
                f"Background subtraction performed successfully for Tree {key}"
            )

    return result
