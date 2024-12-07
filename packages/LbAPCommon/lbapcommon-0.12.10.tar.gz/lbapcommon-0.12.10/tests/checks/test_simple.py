###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re
from pathlib import Path
from textwrap import dedent

import pytest

import LbAPCommon
from LbAPCommon import checks

pytest.importorskip("XRootD")  # tests here will not run on CI
pytestmark = pytest.mark.flaky


def test_num_entries_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check_num_entries"]
    assert result.passed
    assert result.has_all_messages("Found 5135823 in DecayTree (1000 required)")
    assert result.tree_data["DecayTree"]["num_entries"] == 5135823


def test_num_entries_passing_multiple_files():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetUp.root",
        ],
    )["check_num_entries"]
    assert result.passed
    assert result.has_all_messages("Found 8556118 in DecayTree (1000 required)")
    assert result.tree_data["DecayTree"]["num_entries"] == 8556118


def test_num_entries_failing():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000000000
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check_num_entries"]
    assert not result.passed
    assert result.has_all_messages(
        "Found too little entries 5135823 in DecayTree (1000000000 required)"
    )
    assert result.tree_data["DecayTree"]["num_entries"] == 5135823


def test_lenient_num_entries_failing():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000000000
            tree_pattern: DecayTree
            mode: Lenient

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check_num_entries"]
    assert result.passed
    assert result.has_all_messages(
        "Found too little entries 5135823 in DecayTree (1000000000 required)",
    )
    assert result.tree_data["DecayTree"]["num_entries"] == 5135823


def test_none_num_entries_failing():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000000000
            tree_pattern: DecayTree
            mode: Ignore

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check_num_entries"]
    assert result.passed
    assert result.has_all_messages("Check ignored due to user configuration")


def test_num_entries_failing_tree_name():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000000000
            tree_pattern: RandomName

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check_num_entries"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check_num_entries"]
    assert not result.passed
    assert result.has_all_messages("No TTree objects found that match RandomName")
    for _key, data in result.tree_data.items():
        assert data["histograms"] == []


def test_num_entries_per_invpb_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: num_entries_per_invpb
            count_per_invpb: 10000
            tree_pattern: DecayTree
            lumi_pattern: LumiTuple

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Found 11513.1 entries per unit luminosity (pb-1) in DecayTree (10000.0 required)"
    )
    assert result.tree_data["DecayTree"]["num_entries_per_invpb"] == 11513.1


def test_num_entries_per_invpb_failing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: num_entries_per_invpb
            count_per_invpb: 10000000
            tree_pattern: DecayTree
            lumi_pattern: LumiTuple

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "Found too little 11513.1 entries per unit luminosity (pb-1) in DecayTree (10000000.0 required)"
    )
    assert result.tree_data["DecayTree"]["num_entries_per_invpb"] == 11513.1


def test_num_entries_per_invpb_failing_MC():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: num_entries_per_invpb
            count_per_invpb: 10000
            tree_pattern: DecayTree
            lumi_pattern: LumiTuple

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "Failed to get luminosity information (total luminosity = 0)"
    )


def test_num_entries_per_invpb_failing_MC_nameTTree():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: num_entries_per_invpb
            count_per_invpb: 10000
            tree_pattern: RandomName
            lumi_pattern: LumiTuple

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "No TTree objects found that match RandomName",
    )


def test_range_check_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 5134459.0 events)"
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 5134459


def test_range_check_passing_multiple_files():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root",
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetUp.root",
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 8553802.0 events)"
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 8553802


def test_range_check_DTF_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: Dst_D0Fit_M[:, 0]
            limits:
                min: 2000.0
                max: 2080.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of Dst_D0Fit_M[:, 0] successfully filled from TTree DecayTree (contains 37515.0 events)",
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 37515


def test_range_check_DTF_diff_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: Dst_D0Fit_M[:,0]-Dst_D0Fit_D0_M[:,0]
            limits:
                min: 139.0
                max: 160.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of Dst_D0Fit_M[:,0]-Dst_D0Fit_D0_M[:,0] successfully filled from TTree DecayTree (contains 28310.0 events)"
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 28310


def test_range_check_DTF_diff_failing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: Dst_D0Fit_M-Dst_D0Fit_D0_M
            limits:
                min: 139.0
                max: 160.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "Expression 'Dst_D0Fit_M-Dst_D0Fit_D0_M' evaluated to a variable-length array"
        " with shape '37685 * var * float32' in 'DecayTree'."
        " Selecting by default Dst_D0Fit_M-Dst_D0Fit_D0_M[:,0]. If this is not intended,"
        " please update the expression value accordingly.",
        "Expression 'Dst_D0Fit_M-Dst_D0Fit_D0_M' evaluated to non 1-D array with type "
        "'37685 * var * float32' in 'DecayTree'",
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    for h in result.tree_data["DecayTree"]["histograms"]:
        assert h.sum() == 0


def test_range_check_failing_range():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: -100000.0
                max: -99999.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No events found in range for Tree DecayTree")
    assert list(result.tree_data.keys()) == ["DecayTree"]
    for h in result.tree_data["DecayTree"]["histograms"]:
        assert h.sum() == 0


# def test_lenient_range_check_failing_range():
#     rendered_yaml = dedent(
#         """\
#     checks:
#         check:
#             type: range
#             expression: H1_PZ
#             limits:
#                 min: -100000.0
#                 max: -99999.0
#             n_bins: 50
#             tree_pattern: DecayTree
#             mode: Lenient

#     job_1:
#         application: DaVinci/v45r8
#         input:
#             bk_query: /bookkeeping/path/ALLSTREAMS.DST
#         output: FILETYPE.ROOT
#         options:
#             - options.py
#             - $VAR/a.py
#         wg: Charm
#         inform: a.b@c.d
#         checks:
#             - check
#     """
#     )
#     jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
#     result = checks.run_job_checks(
#         jobs_data,
#         "job_1",
#         ["check"],
#         checks_data,
#         [
#             "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
#         ],
#     )["check"]
#     assert result.passed
#     assert result.has_all_messages(
#         "No events found in range for Tree DecayTree",
#     )
#     assert list(result.tree_data.keys()) == ["DecayTree"]
#     for h in result.tree_data["DecayTree"]["histograms"]:
#         assert h.sum() == 0


def test_none_range_check_failing_range():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: -100000.0
                max: -99999.0
            n_bins: 50
            tree_pattern: DecayTree
            mode: Ignore

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages("Check ignored due to user configuration")


def test_range_check_failing_missing_branch():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: Dst_M
            limits:
                min: 1800.0
                max: 2300.0
            n_bins: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    message = result.messages[0][1]
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert list(result.tree_data.keys()) == ["DecayTree"]
    for h in result.tree_data["DecayTree"]["histograms"]:
        assert h.sum() == 0


def test_range_check_failing_tree_name():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            tree_pattern: RandomName

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No TTree objects found that match RandomName")
    assert list(result.tree_data.keys()) == []


def test_range_check_failing_bad_mean():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            tree_pattern: DecayTree
            exp_mean: 500000.0
            mean_tolerance: 1.0

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "The observed mean (49110.65313794501) differs from the expected value by 450889.346862055 (<=1.0 required)"
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 5134459


def test_range_check_failing_bad_stddev():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range
            expression: H1_PZ
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            tree_pattern: DecayTree
            exp_std: 500000.0
            std_tolerance: 1.0

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "The observed standard deviation (53099.76473607609) differs from the expected value by 446900.2352639239 (<=1.0 required)"
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 5134459


def test_range_check_nd_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: H1_PZ
                y: H2_PZ
                z: H2_PX
            limits:
                x:
                    min: 0.0
                    max: 500000.0
                y:
                    min: 0.0
                    max: 500000.0
                z:
                    min: 0.0
                    max: 500000.0
            n_bins:
                x: 50
                y: 50
                z: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of H1_PZ, H2_PZ successfully filled from TTree DecayTree (contains 2525189.0 events)",
        "Histogram of H1_PZ, H2_PX successfully filled from TTree DecayTree (contains 2525189.0 events)",
        "Histogram of H2_PZ, H2_PX successfully filled from TTree DecayTree (contains 2525189.0 events)",
        "Histogram of H1_PZ, H2_PZ, H2_PX successfully filled from TTree DecayTree (contains 2525189.0 events)",
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []


def test_range_check_nd_DTF_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: Dst_D0Fit_M[:, 0]
                y: Dst_D0Fit_D0_M[:, 0]
            limits:
                x:
                    min: 2000.0
                    max: 2080.0
                y:
                    min: 1850.0
                    max: 1920.0
            n_bins:
                x: 50
                y: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Histogram of Dst_D0Fit_M[:, 0], Dst_D0Fit_D0_M[:, 0] successfully filled from TTree DecayTree (contains 37515.0 events)",
    )
    assert list(result.tree_data.keys()) == ["DecayTree"]
    assert not result.tree_data["DecayTree"]["histograms"] == []
    assert result.tree_data["DecayTree"]["num_entries"] == 37515


def test_range_check_nd_failing_missing_limit():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: H1_PZ
                y: H2_PZ
                z: H2_PX
            limits:
                x:
                    min: 0.0
                    max: 500000.0
                y:
                    min: 0.0
                    max: 500000.0
            n_bins:
                x: 50
                y: 50
                z: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "For each variable, a corresponding range should be defined."
    )
    assert list(result.tree_data.keys()) == []


def test_range_check_nd_failing_missing_branch():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: H1_PZ
                y: Dst_M-D0_M
            limits:
                x:
                    min: 0.0
                    max: 500000.0
                y:
                    min: 0.0
                    max: 500000.0
            n_bins:
                x: 50
                y: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    message = result.messages[0][1]
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert list(result.tree_data.keys()) == ["DecayTree"]
    for h in result.tree_data["DecayTree"]["histograms"]:
        assert h.sum() == 0


def test_range_check_nd_failing_range():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: H1_PZ
                y: H2_PZ
            limits:
                x:
                    min: -1000000.0
                    max: -999999.0
                y:
                    min: -1000000.0
                    max: -999999.0
            n_bins:
                x: 50
                y: 50
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No events found in range for Tree DecayTree")
    assert list(result.tree_data.keys()) == ["DecayTree"]
    for h in result.tree_data["DecayTree"]["histograms"]:
        assert h.sum() == 0


def test_range_check_nd_failing_tree_name():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_nd
            expressions:
                x: H1_PZ
                y: H2_PZ
                z: H2_PX
            limits:
                x:
                    min: 0.0
                    max: 500000.0
                y:
                    min: 0.0
                    max: 500000.0
                z:
                    min: 0.0
                    max: 500000.0
            n_bins:
                x: 50
                y: 50
                z: 50
            tree_pattern: RandomName

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No TTree objects found that match RandomName")
    assert list(result.tree_data.keys()) == []


def test_range_check_bkg_subtracted_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_bkg_subtracted
            expression: D0_PT
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            expr_for_subtraction: D0_MM
            mean_sig: 1865.0
            background_shift: 30.0
            background_window: 10.0
            signal_window: 20.0
            blind_ranges:
                min: 10000.0
                max: 30000.0
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Background subtraction performed successfully for Tree DecayTree"
    )
    assert list(result.tree_data.keys())[0] == "DecayTree"
    assert not result.tree_data["DecayTree"]["histograms"] == []


def test_range_check_bkg_subtracted_DTF_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_bkg_subtracted
            expression: Dst_PX
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            expr_for_subtraction: Dst_D0Fit_M[:, 0]
            mean_sig: 2010.3
            background_shift: 15.0
            background_window: 10.0
            signal_window: 10.0
            blind_ranges:
                min: 10000.0
                max: 30000.0
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    file_list = [Path(__file__).parent.absolute() / "example_tuple_with_lumi.root"]
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        file_list,
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Background subtraction performed successfully for Tree DecayTree"
    )
    assert list(result.tree_data.keys())[0] == "DecayTree"
    assert not result.tree_data["DecayTree"]["histograms"] == []


def test_range_check_bkg_subtracted_failing_range():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_bkg_subtracted
            expression: D0_PT
            limits:
                min: -1000000.0
                max: -999999.0
            n_bins: 50
            expr_for_subtraction: D0_MM
            mean_sig: 1865.0
            background_shift: 30.0
            background_window: 10.0
            signal_window: 20.0
            blind_ranges:
                min: 10000.0
                max: 30000.0
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "Not enough events for background subtraction found in range for Tree DecayTree"
    )
    assert list(result.tree_data.keys())[0] == "DecayTree"


def test_range_check_bkg_subtracted_failing_missing_branch():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_bkg_subtracted
            expression: D0_PT
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            expr_for_subtraction: Dst_M
            mean_sig: 1865.0
            background_shift: 30.0
            background_window: 10.0
            signal_window: 20.0
            blind_ranges:
                min: 10000.0
                max: 30000.0
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root"
        ],
    )["check"]
    message = result.messages[0][1]
    print(message)
    pattern = r"Missing branch in "
    matched = False
    if re.match(pattern, message):
        matched = True
    assert not result.passed
    assert matched
    assert list(result.tree_data.keys())[0] == "DecayTree"


def test_range_check_bkg_subtracted_failing_tree_name():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: range_bkg_subtracted
            expression: D0_PT
            limits:
                min: 0.0
                max: 500000.0
            n_bins: 50
            expr_for_subtraction: D0_MM
            mean_sig: 1865.0
            background_shift: 30.0
            background_window: 10.0
            signal_window: 20.0
            blind_ranges:
                min: 10000.0
                max: 30000.0
            tree_pattern: RandomName

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/MasterclassDatasets/D0lifetime/2014/MasterclassData.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No TTree objects found that match RandomName")
    assert list(result.tree_data.keys()) == []


def test_branches_exist_passing():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: branches_exist
            branches:
                - H1_PZ
                - H2_PZ
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages("All required branches were found in Tree DecayTree")


def test_branches_exist_failing_missing_branches():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: branches_exist
            branches:
                - H1_PZ
                - H2_PZ
                - RandomName
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages(
        "Required branches not found in Tree DecayTree: ['RandomName']"
    )


def test_lenient_branches_exist_failing_missing_branches():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: branches_exist
            branches:
                - H1_PZ
                - H2_PZ
                - RandomName
            tree_pattern: DecayTree
            mode: Lenient

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        "Required branches not found in Tree DecayTree: ['RandomName']"
    )


def test_none_branches_exist_failing_missing_branches():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: branches_exist
            branches:
                - H1_PZ
                - H2_PZ
                - RandomName
            tree_pattern: DecayTree
            mode: Ignore

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert result.passed
    assert result.has_all_messages("Check ignored due to user configuration")


def test_branches_exist_failing_tree_name():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: branches_exist
            branches:
                - H1_PZ
                - H2_PZ
            tree_pattern: RandomName

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_1",
        ["check"],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )["check"]
    assert not result.passed
    assert result.has_all_messages("No TTree objects found that match RandomName")


# default checks


def test_wrong_polarity():
    rendered_yaml = dedent(
        """\
    job_MagDown:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MagUp:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2017/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_MagUp",
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]

    assert not result.passed
    assert result.has_all_messages(
        "Found 'magup' in job name 'job_magup' with'magdown' input "
        "('/mc/2017/beam6500gev-2018-magdown/sim09g/trig0x617d18a4/reco18/24142001/allstreams.dst'). "
        "Has the wrong magnet polarity been used?"
    )


def test_wrong_polarity_acronym():
    rendered_yaml = dedent(
        """\
    job_MD:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MU:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2017/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_MU",
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]

    assert not result.passed
    assert result.has_all_messages(
        "Found 'mu' in job name 'job_mu' with'magdown' input "
        "('/mc/2017/beam6500gev-2018-magdown/sim09g/trig0x617d18a4/reco18/24142001/allstreams.dst'). "
        "Has the wrong magnet polarity been used?"
    )


def test_tuple_in_job_name():
    rendered_yaml = dedent(
        """\
    job_MagDown_tuple:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MagUp_tuple:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_MagDown_tuple",
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]
    assert result.passed

    result = checks.run_job_checks(
        jobs_data,
        "job_MagUp_tuple",
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]
    assert result.passed


def test_polarity_acronym():
    rendered_yaml = dedent(
        """\
    job_MagDown_2018:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MagUp_2018:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MD_2017:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2017/Beam6500GeV-2017-MagDown/Sim09g/Trig0x62661709/Reco17/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_MU_2017:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2017/Beam6500GeV-2017-MagUp/Sim09g/Trig0x62661709/Reco17/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    for job_name in [
        "job_MagDown_2018",
        "job_MagUp_2018",
        "job_MD_2017",
        "job_MU_2017",
    ]:
        result = checks.run_job_checks(
            jobs_data,
            job_name,
            [],
            checks_data,
            [],
        )["job_name_matches_polarity"]
        assert result.passed


# def test_missing_polarity():
#     rendered_yaml = dedent(
#         """\
#     checks:
#         both_polarities_used:
#             type: both_polarities_used
#             mode: Strict

#     job_MagDown:
#         application: DaVinci/v45r3
#         input:
#             bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
#         output: FILETYPE.ROOT
#         options:
#             - $VAR/a.py
#         wg: Charm
#         inform: a.b@c.d
#         checks:
#             - both_polarities_used
#     """
#     )
#     jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
#     result = checks.run_job_checks(
#         jobs_data,
#         "job_MagDown",
#         [],
#         checks_data,
#         [],
#     )["both_polarities_used"]
#     assert not result.passed
#     assert result.has_all_messages(
#         "/mc/2018/beam6500gev-2018-magdown/sim09g/trig0x617d18a4/reco18/24142001/allstreams.dst"
#         " has been requested as input for 1 job(s)"
#         " but its opposite polarity counterpart has not been requested for any jobs."
#         " Are you sure you do not want the other polarity?"
#     )


# def test_duplicate_bk_query():
#     rendered_yaml = dedent(
#         """\
#     checks:
#         duplicate_inputs:
#             type: duplicate_inputs
#             mode: Strict

#     job_1:
#         application: DaVinci/v45r3
#         input:
#             bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
#         output: FILETYPE.ROOT
#         options:
#             - $VAR/a.py
#         wg: Charm
#         inform: a.b@c.d
#         checks:
#             - duplicate_inputs

#     job_2:
#         application: DaVinci/v45r3
#         input:
#             bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
#         output: FILETYPE.ROOT
#         options:
#             - $VAR/b.py
#         wg: Charm
#         inform: a.b@c.d
#         checks:
#             - duplicate_inputs

#     """
#     )
#     for i, job_name in enumerate(["job_1", "job_2"]):
#         other_job_name = ["job_2", "job_1"][i]
#         jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
#         result = checks.run_job_checks(
#             jobs_data,
#             job_name,
#             [],
#             checks_data,
#             [],
#         )["duplicate_inputs"]
#         assert not result.passed
#         assert result.has_all_messages(
#             f"{job_name!r} shares an input "
#             "(/MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST) "
#             f"with the following jobs [{other_job_name!r}]"
#         )


def test_lenient_duplicate_bk_query():
    rendered_yaml = dedent(
        """\
    checks:
        duplicate_bk_query:
            type: duplicate_inputs
            mode: Lenient

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - duplicate_bk_query

    job_2:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - duplicate_bk_query
    """
    )
    for i, job_name in enumerate(["job_1", "job_2"]):
        other_job_name = ["job_2", "job_1"][i]
        jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
        result = checks.run_job_checks(
            jobs_data,
            job_name,
            ["duplicate_bk_query"],
            checks_data,
            [],
        )["duplicate_bk_query"]
        assert result.passed
        assert result.has_all_messages(
            f"{job_name!r} shares an input "
            "(/MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST) "
            f"with the following jobs [{other_job_name!r}]"
        )


def test_none_duplicate_bk_query():
    rendered_yaml = dedent(
        """\
    checks:
        duplicate_bk_query:
            type: duplicate_inputs
            mode: Ignore

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - duplicate_bk_query

    job_2:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - duplicate_bk_query
    """
    )
    for job_name in ["job_1", "job_2"]:
        jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
        result = checks.run_job_checks(
            jobs_data,
            job_name,
            ["duplicate_bk_query"],
            checks_data,
            [],
        )["duplicate_bk_query"]
        assert result.passed
        assert result.has_all_messages("Check ignored due to user configuration")


def test_good_job_chain_polarity():
    rendered_yaml = dedent(
        """\
    job_1_MagDown:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_1_MagUp:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_2_MagDown:
        application: DaVinci/v45r3
        input:
            job_name: job_1_MagDown
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    result = checks.run_job_checks(
        jobs_data,
        "job_2_MagDown",
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]
    assert result.passed


def test_bad_job_chain_polarity():
    rendered_yaml = dedent(
        """\
    job_1_MagDown:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_1_MagUp:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d

    job_2_MagDown:
        application: DaVinci/v45r3
        input:
            job_name: job_1_MagUp
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    job_name = "job_2_MagDown"
    target = "job_1_MagUp"
    result = checks.run_job_checks(
        jobs_data,
        job_name,
        [],
        checks_data,
        [],
    )["job_name_matches_polarity"]
    assert not result.passed
    assert result.has_all_messages(
        f"Found 'magdown' in job name {job_name.lower()!r} with"
        f"'magup' input ({target.lower()!r}). "
        "Has the wrong magnet polarity been used?"
    )


def test_lenient_bad_job_chain_polarity():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: job_name_matches_polarity
            mode: Lenient

    job_1_MagDown:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check

    job_1_MagUp:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check

    job_2_MagDown:
        application: DaVinci/v45r3
        input:
            job_name: job_1_MagUp
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    job_name = "job_2_MagDown"
    target = "job_1_MagUp"
    result = checks.run_job_checks(
        jobs_data,
        job_name,
        ["check"],
        checks_data,
        [],
    )["check"]
    assert result.passed
    assert result.has_all_messages(
        f"Found 'magdown' in job name {job_name.lower()!r} with"
        f"'magup' input ({target.lower()!r}). "
        "Has the wrong magnet polarity been used?"
    )


def test_none_bad_job_chain_polarity():
    rendered_yaml = dedent(
        """\
    checks:
        check:
            type: job_name_matches_polarity
            mode: Ignore

    job_1_MagDown:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagDown/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check

    job_1_MagUp:
        application: DaVinci/v45r3
        input:
            bk_query: /MC/2018/Beam6500GeV-2018-MagUp/Sim09g/Trig0x617d18a4/Reco18/24142001/ALLSTREAMS.DST
        output: FILETYPE.DST
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check

    job_2_MagDown:
        application: DaVinci/v45r3
        input:
            job_name: job_1_MagUp
        output: FILETYPE.ROOT
        options:
            - $VAR/b.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
    job_name = "job_2_MagDown"
    result = checks.run_job_checks(
        jobs_data,
        job_name,
        ["check"],
        checks_data,
        [],
    )["check"]
    assert result.passed
    assert result.has_all_messages("Check ignored due to user configuration")


# def test_event_stats_passing():
#     rendered_yaml = dedent(
#         """\
#     job_1:
#         application: DaVinci/v45r8
#         input:
#             bk_query: /bookkeeping/path/ALLSTREAMS.DST
#         output: FILETYPE.ROOT
#         options:
#             - options.py
#             - $VAR/a.py
#         wg: Charm
#         inform: a.b@c.d
#     """
#     )
#     jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)
#     result = checks.run_job_checks(
#         jobs_data,
#         "job_1",
#         [],
#         checks_data,
#         [
#             "root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/LHCb/Collision16/XICP.ROOT/00176894/0000/00176894_00000001_1.xicp.root"
#         ],
#     )["event_stats"]
#     assert result.passed
#     assert result.has_all_messages(
#       "Tree Xicp_ToPpKmPip/DecayTree has 2752584 events."
#       " Multiple candidates: mean = 1.0629786411604514, max = 30"
#     )
