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
import json
from textwrap import dedent

import hist
import numpy as np
import pytest
from hist import Hist

from LbAPCommon.checks import utils as checks_utils


def test_1D_hist_serialise_then_deserialise():
    axis0 = hist.axis.Regular(10, -5.0, 5.0, name="x-axis name")
    h = Hist(axis0, name="demo hist 1D")

    x = np.array(
        [-4.6, -2.5, -1.5, -0.9, -0.8, -0.8, -0.3, 0.0, 0.5, 1.4, 2.0, 3.7, 6.0]
    )
    h.fill(x)

    hist_json = checks_utils.serialise_hist(h)

    h2 = checks_utils.deserialise_hist(hist_json, "range")

    assert h == h2


def test_1D_hist_deserialise_then_serialise_v1():
    hist_json = {
        "version": 1,
        "name": "demo hist 1D",
        "axes": [{"name": "x-axis name", "nbins": 10, "min": -5.0, "max": 5.0}],
        "contents": [0.0, 1.0, 0.0, 1.0, 1.0, 4.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0],
        "sumw2": [0.0, 1.0, 0.0, 1.0, 1.0, 4.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0],
    }

    h = checks_utils.deserialise_hist(hist_json, "range")

    hist_json_2 = checks_utils.serialise_hist(h)

    assert hist_json == hist_json_2


def test_2D_hist_serialise_then_deserialise():
    axis0 = hist.axis.Regular(10, -5.0, 5.0, name="x-axis name")
    axis1 = hist.axis.Regular(8, -1.0, 2.0, name="y-axis name")
    h = Hist(axis0, axis1, name="demo hist 2D")

    x = np.array(
        [-4.6, -2.5, -1.5, -0.9, -0.8, -0.8, -0.3, 0.0, 0.5, 1.4, 2.0, 3.7, 6.0]
    )
    y = np.array(
        [-1.2, -0.8, -0.2, -0.4, -0.3, -0.2, 0.0, -0.1, 0.2, 0.4, 0.3, 0.6, 0.9]
    )
    h.fill(x, y)

    hist_json = checks_utils.serialise_hist(h)

    h2 = checks_utils.deserialise_hist(hist_json, "range_nd")

    assert h == h2


def test_2D_hist_deserialise_then_serialise_v1():
    hist_json = {
        "version": 1,
        "name": "demo hist 2D",
        "axes": [
            {"name": "x-axis name", "nbins": 10, "min": -5.0, "max": 5.0},
            {"name": "y-axis name", "nbins": 8, "min": -1.0, "max": 2.0},
        ],
        "contents": [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        ],
        "sumw2": [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        ],
    }

    h = checks_utils.deserialise_hist(hist_json, "range_nd")

    hist_json_2 = checks_utils.serialise_hist(h)

    assert hist_json == hist_json_2


def test_check_results_json_deserialise_then_serialise():
    check_results_json = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 5135823 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 5135823
        }
      }
    },
    "check_range": {
      "passed": true,
      "messages": [
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 4776546.0 events)"
      ],
      "can_combine": true,
      "input": {
        "type": "range",
        "expression": "H1_PZ",
        "limits": {
          "min": 0.0,
          "max": 500000.0
        },
        "blind_ranges": [
          {
            "min": 80000.0,
            "max": 100000.0
          },
          {
            "min": 180000.0,
            "max": 200000.0
          }
        ],
        "tree_pattern": "DecayTree",
        "n_bins": 50
      },
      "output": {
        "DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "DecayTree H1_PZ",
              "axes": [
                {
                  "name": "H1_PZ",
                  "nbins": 50,
                  "min": 0.0,
                  "max": 500000.0
                }
              ],
              "contents": [
                0.0,
                1068515.0,
                911171.0,
                630749.0,
                449908.0,
                336446.0,
                265471.0,
                219142.0,
                186119.0,
                0.0,
                0.0,
                122888.0,
                107285.0,
                92548.0,
                78798.0,
                65261.0,
                53400.0,
                44413.0,
                36398.0,
                0.0,
                0.0,
                19816.0,
                16119.0,
                12874.0,
                10512.0,
                8506.0,
                6869.0,
                5591.0,
                4593.0,
                3772.0,
                3049.0,
                2522.0,
                2166.0,
                1754.0,
                1520.0,
                1286.0,
                1033.0,
                932.0,
                822.0,
                720.0,
                610.0,
                474.0,
                443.0,
                391.0,
                347.0,
                310.0,
                262.0,
                210.0,
                186.0,
                171.0,
                174.0,
                0.0
              ],
              "sumw2": [
                0.0,
                1068515.0,
                911171.0,
                630749.0,
                449908.0,
                336446.0,
                265471.0,
                219142.0,
                186119.0,
                0.0,
                0.0,
                122888.0,
                107285.0,
                92548.0,
                78798.0,
                65261.0,
                53400.0,
                44413.0,
                36398.0,
                0.0,
                0.0,
                19816.0,
                16119.0,
                12874.0,
                10512.0,
                8506.0,
                6869.0,
                5591.0,
                4593.0,
                3772.0,
                3049.0,
                2522.0,
                2166.0,
                1754.0,
                1520.0,
                1286.0,
                1033.0,
                932.0,
                822.0,
                720.0,
                610.0,
                474.0,
                443.0,
                391.0,
                347.0,
                310.0,
                262.0,
                210.0,
                186.0,
                171.0,
                174.0,
                0.0
              ]
            }
          ],
          "num_entries": 4776546,
          "mean": 44931.44209225662,
          "variance": 2682154203.3712554,
          "stddev": 51789.51827707278,
          "num_entries_in_mean_window": 0
        }
      }
    }
  }
}"""
    )

    checks_data, all_check_results = checks_utils.JSON_to_checks(
        json.loads(check_results_json)
    )

    check_results_json_2 = checks_utils.checks_to_JSON(checks_data, all_check_results)

    assert check_results_json == check_results_json_2


def test_range_check_bkg_subtracted_json_deserialise_then_serialise():
    check_results_json = dedent(
        """\
{
  "job_1": {
    "histogram_deltaM_bkg_subtracted": {
      "passed": true,
      "messages": [
        "Background subtraction performed successfully for Tree KmPimPipPip_Tuple/DecayTree"
      ],
      "can_combine": true,
      "input": {
        "type": "range_bkg_subtracted",
        "expression": "Dst_M-D0_M",
        "limits": {
          "min": 139.0,
          "max": 155.0
        },
        "expr_for_subtraction": "D0_M",
        "mean_sig": 1865.0,
        "background_shift": 25.0,
        "background_window": 10.0,
        "signal_window": 30.0,
        "tree_pattern": "KmPimPipPip_Tuple/DecayTree",
        "n_bins": 50
      },
      "output": {
        "KmPimPipPip_Tuple/DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "KmPimPipPip_Tuple/DecayTree Dst_M-D0_M",
              "axes": [
                {
                  "name": "D0_M",
                  "nbins": 50,
                  "min": 1830.0,
                  "max": 1900.0
                }
              ],
              "contents": [
                2721.0,
                127.0,
                103.0,
                98.0,
                128.0,
                112.0,
                122.0,
                96.0,
                106.0,
                120.0,
                115.0,
                132.0,
                128.0,
                145.0,
                143.0,
                137.0,
                196.0,
                198.0,
                238.0,
                231.0,
                324.0,
                383.0,
                388.0,
                485.0,
                542.0,
                539.0,
                551.0,
                600.0,
                534.0,
                483.0,
                448.0,
                400.0,
                338.0,
                327.0,
                270.0,
                223.0,
                221.0,
                175.0,
                153.0,
                144.0,
                117.0,
                119.0,
                98.0,
                120.0,
                115.0,
                96.0,
                99.0,
                104.0,
                118.0,
                105.0,
                110.0,
                2600.0
              ],
              "sumw2": [
                2721.0,
                127.0,
                103.0,
                98.0,
                128.0,
                112.0,
                122.0,
                96.0,
                106.0,
                120.0,
                115.0,
                132.0,
                128.0,
                145.0,
                143.0,
                137.0,
                196.0,
                198.0,
                238.0,
                231.0,
                324.0,
                383.0,
                388.0,
                485.0,
                542.0,
                539.0,
                551.0,
                600.0,
                534.0,
                483.0,
                448.0,
                400.0,
                338.0,
                327.0,
                270.0,
                223.0,
                221.0,
                175.0,
                153.0,
                144.0,
                117.0,
                119.0,
                98.0,
                120.0,
                115.0,
                96.0,
                99.0,
                104.0,
                118.0,
                105.0,
                110.0,
                2600.0
              ]
            },
            {
              "version": 1,
              "name": "KmPimPipPip_Tuple/DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                0.0,
                4.0,
                5.0,
                14.0,
                9.0,
                21.0,
                17.0,
                15.0,
                26.0,
                20.0,
                25.0,
                37.0,
                61.0,
                52.0,
                95.0,
                133.0,
                195.0,
                368.0,
                570.0,
                813.0,
                799.0,
                639.0,
                442.0,
                292.0,
                188.0,
                129.0,
                111.0,
                89.0,
                69.0,
                61.0,
                50.0,
                64.0,
                46.0,
                41.0,
                46.0,
                52.0,
                37.0,
                39.0,
                36.0,
                34.0,
                37.0,
                31.0,
                57.0,
                39.0,
                43.0,
                56.0,
                40.0,
                48.0,
                42.0,
                41.0,
                0.0
              ],
              "sumw2": [
                0.0,
                0.0,
                4.0,
                5.0,
                14.0,
                9.0,
                21.0,
                17.0,
                15.0,
                26.0,
                20.0,
                25.0,
                37.0,
                61.0,
                52.0,
                95.0,
                133.0,
                195.0,
                368.0,
                570.0,
                813.0,
                799.0,
                639.0,
                442.0,
                292.0,
                188.0,
                129.0,
                111.0,
                89.0,
                69.0,
                61.0,
                50.0,
                64.0,
                46.0,
                41.0,
                46.0,
                52.0,
                37.0,
                39.0,
                36.0,
                34.0,
                37.0,
                31.0,
                57.0,
                39.0,
                43.0,
                56.0,
                40.0,
                48.0,
                42.0,
                41.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "KmPimPipPip_Tuple/DecayTree Dst_M-D0_M background",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                1.0,
                0.0,
                0.0,
                8.0,
                2.0,
                9.0,
                3.0,
                10.0,
                9.0,
                16.0,
                12.0,
                10.0,
                10.0,
                13.0,
                19.0,
                16.0,
                16.0,
                19.0,
                34.0,
                40.0,
                42.0,
                32.0,
                31.0,
                22.0,
                20.0,
                24.0,
                14.0,
                16.0,
                11.0,
                21.0,
                18.0,
                20.0,
                23.0,
                17.0,
                23.0,
                23.0,
                14.0,
                16.0,
                18.0,
                13.0,
                13.0,
                32.0,
                13.0,
                16.0,
                22.0,
                14.0,
                15.0,
                17.0,
                14.0,
                16.0,
                0.0
              ],
              "sumw2": [
                0.0,
                1.0,
                0.0,
                0.0,
                8.0,
                2.0,
                9.0,
                3.0,
                10.0,
                9.0,
                16.0,
                12.0,
                10.0,
                10.0,
                13.0,
                19.0,
                16.0,
                16.0,
                19.0,
                34.0,
                40.0,
                42.0,
                32.0,
                31.0,
                22.0,
                20.0,
                24.0,
                14.0,
                16.0,
                11.0,
                21.0,
                18.0,
                20.0,
                23.0,
                17.0,
                23.0,
                23.0,
                14.0,
                16.0,
                18.0,
                13.0,
                13.0,
                32.0,
                13.0,
                16.0,
                22.0,
                14.0,
                15.0,
                17.0,
                14.0,
                16.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "KmPimPipPip_Tuple/DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                -0.6666666666666666,
                4.0,
                5.0,
                8.666666666666668,
                7.666666666666667,
                15.0,
                15.0,
                8.333333333333334,
                20.0,
                9.333333333333334,
                17.0,
                30.333333333333336,
                54.333333333333336,
                43.333333333333336,
                82.33333333333333,
                122.33333333333333,
                184.33333333333334,
                355.3333333333333,
                547.3333333333334,
                786.3333333333334,
                771.0,
                617.6666666666666,
                421.3333333333333,
                277.3333333333333,
                174.66666666666666,
                113.0,
                101.66666666666667,
                78.33333333333333,
                61.666666666666664,
                47.0,
                38.0,
                50.66666666666667,
                30.666666666666668,
                29.666666666666668,
                30.666666666666668,
                36.66666666666667,
                27.666666666666668,
                28.333333333333336,
                24.0,
                25.333333333333336,
                28.333333333333336,
                9.666666666666668,
                48.333333333333336,
                28.333333333333336,
                28.333333333333336,
                46.66666666666667,
                30.0,
                36.66666666666667,
                32.66666666666667,
                30.333333333333336,
                0.0
              ],
              "sumw2": [
                0.0,
                0.4444444444444444,
                4.0,
                5.0,
                17.555555555555557,
                9.88888888888889,
                25.0,
                18.333333333333332,
                19.444444444444443,
                30.0,
                27.11111111111111,
                30.333333333333332,
                41.44444444444444,
                65.44444444444444,
                57.77777777777778,
                103.44444444444444,
                140.11111111111111,
                202.11111111111111,
                376.44444444444446,
                585.1111111111111,
                830.7777777777778,
                817.6666666666666,
                653.2222222222222,
                455.77777777777777,
                301.77777777777777,
                196.88888888888889,
                139.66666666666666,
                117.22222222222223,
                96.11111111111111,
                73.88888888888889,
                70.33333333333333,
                58.0,
                72.88888888888889,
                56.22222222222222,
                48.55555555555556,
                56.22222222222222,
                62.22222222222222,
                43.22222222222222,
                46.111111111111114,
                44.0,
                39.77777777777778,
                42.77777777777778,
                45.22222222222222,
                62.77777777777778,
                46.111111111111114,
                52.77777777777778,
                62.22222222222222,
                46.666666666666664,
                55.55555555555556,
                48.22222222222222,
                48.111111111111114,
                0.0
              ]
            }
          ]
        }
      }
    }
  }
}"""
    )

    checks_data, all_check_results = checks_utils.JSON_to_checks(
        json.loads(check_results_json)
    )

    check_results_json_2 = checks_utils.checks_to_JSON(checks_data, all_check_results)

    assert check_results_json == check_results_json_2


def test_combine_check_results_simple():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 5135823 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 5135823
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 4864177 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 4864177
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries"].check_type == "num_entries"
    )
    assert all_check_results_comb["job_1"]["check_num_entries"].passed
    assert all_check_results_comb["job_1"]["check_num_entries"].can_combine
    assert all_check_results_comb["job_1"]["check_num_entries"].messages == [
        "Found 5135823 in DecayTree (1000 required)",
        "Found 4864177 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 10000000
    )


def test_combine_check_results_simple_low_stat():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": false,
      "messages": [
        "Found 2 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 2
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 4864177 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 4864177
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries"].check_type == "num_entries"
    )
    assert all_check_results_comb["job_1"]["check_num_entries"].passed
    assert all_check_results_comb["job_1"]["check_num_entries"].can_combine
    assert all_check_results_comb["job_1"]["check_num_entries"].messages == [
        "Found 2 in DecayTree (1000 required)",
        "Found 4864177 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 4864179
    )


def test_combine_check_results_simple_low_stat_failing():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": false,
      "messages": [
        "Found 2 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 2
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": false,
      "messages": [
        "Found 3 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 3
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries"].check_type == "num_entries"
    )
    assert not all_check_results_comb["job_1"]["check_num_entries"].passed
    assert all_check_results_comb["job_1"]["check_num_entries"].can_combine
    assert all_check_results_comb["job_1"]["check_num_entries"].messages == [
        "Found 2 in DecayTree (1000 required)",
        "Found 3 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 5
    )


def test_combine_check_results_error():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": false,
      "messages": [
        "No TTree objects found that match RandomTree"
      ],
      "can_combine": false,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "RandomTree"
      },
      "output": {}
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": false,
      "messages": [
        "No TTree objects found that match RandomTree"
      ],
      "can_combine": false,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "RandomTree"
      },
      "output": {}
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    with pytest.warns(UserWarning) as w:
        with pytest.raises(ValueError, match="Found 0 checks to be combined"):
            checks_utils.combine_checks(
                [
                    (checks_data_a, all_check_results_a),
                    (checks_data_b, all_check_results_b),
                ]
            )

    assert len(w) == 2
    assert (
        w[0].message.args[0]
        == "The result for job_1 cannot be included in the check_num_entries combination as the can_combine flag is False."
    )
    assert (
        w[1].message.args[0]
        == "The result for job_1 cannot be included in the check_num_entries combination as the can_combine flag is False."
    )


def test_add_check_results_range():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_range": {
      "passed": true,
      "messages": [
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 4776546.0 events)"
      ],
      "can_combine": true,
      "input": {
        "type": "range",
        "expression": "H1_PZ",
        "limits": {
          "min": 0.0,
          "max": 500000.0
        },
        "blind_ranges": [
          {
            "min": 80000.0,
            "max": 100000.0
          },
          {
            "min": 180000.0,
            "max": 200000.0
          }
        ],
        "tree_pattern": "DecayTree",
        "n_bins": 50
      },
      "output": {
        "DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "DecayTree H1_PZ",
              "axes": [
                {
                  "name": "H1_PZ",
                  "nbins": 50,
                  "min": 0.0,
                  "max": 500000.0
                }
              ],
              "contents": [
                0.0,
                1068515.0,
                911171.0,
                630749.0,
                449908.0,
                336446.0,
                265471.0,
                219142.0,
                186119.0,
                0.0,
                0.0,
                122888.0,
                107285.0,
                92548.0,
                78798.0,
                65261.0,
                53400.0,
                44413.0,
                36398.0,
                0.0,
                0.0,
                19816.0,
                16119.0,
                12874.0,
                10512.0,
                8506.0,
                6869.0,
                5591.0,
                4593.0,
                3772.0,
                3049.0,
                2522.0,
                2166.0,
                1754.0,
                1520.0,
                1286.0,
                1033.0,
                932.0,
                822.0,
                720.0,
                610.0,
                474.0,
                443.0,
                391.0,
                347.0,
                310.0,
                262.0,
                210.0,
                186.0,
                171.0,
                174.0,
                0.0
              ],
              "sumw2": [
                0.0,
                1068515.0,
                911171.0,
                630749.0,
                449908.0,
                336446.0,
                265471.0,
                219142.0,
                186119.0,
                0.0,
                0.0,
                122888.0,
                107285.0,
                92548.0,
                78798.0,
                65261.0,
                53400.0,
                44413.0,
                36398.0,
                0.0,
                0.0,
                19816.0,
                16119.0,
                12874.0,
                10512.0,
                8506.0,
                6869.0,
                5591.0,
                4593.0,
                3772.0,
                3049.0,
                2522.0,
                2166.0,
                1754.0,
                1520.0,
                1286.0,
                1033.0,
                932.0,
                822.0,
                720.0,
                610.0,
                474.0,
                443.0,
                391.0,
                347.0,
                310.0,
                262.0,
                210.0,
                186.0,
                171.0,
                174.0,
                0.0
              ]
            }
          ],
          "num_entries": 4776546,
          "mean": 44931.44209225662,
          "variance": 2682154203.3712554,
          "stddev": 51789.51827707278,
          "num_entries_in_mean_window": 0
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_range": {
      "passed": true,
      "messages": [
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 3180634.0 events)"
      ],
      "can_combine": true,
      "input": {
        "type": "range",
        "expression": "H1_PZ",
        "limits": {
          "min": 0.0,
          "max": 500000.0
        },
        "blind_ranges": [
          {
            "min": 80000.0,
            "max": 100000.0
          },
          {
            "min": 180000.0,
            "max": 200000.0
          }
        ],
        "tree_pattern": "DecayTree",
        "n_bins": 50
      },
      "output": {
        "DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "DecayTree H1_PZ",
              "axes": [
                {
                  "name": "H1_PZ",
                  "nbins": 50,
                  "min": 0.0,
                  "max": 500000.0
                }
              ],
              "contents": [
                0.0,
                721133.0,
                605047.0,
                416555.0,
                295772.0,
                221484.0,
                175071.0,
                145067.0,
                123700.0,
                0.0,
                0.0,
                82422.0,
                71972.0,
                61970.0,
                51986.0,
                43985.0,
                36234.0,
                29660.0,
                24616.0,
                0.0,
                0.0,
                13292.0,
                10926.0,
                8732.0,
                7407.0,
                5790.0,
                4764.0,
                3831.0,
                3145.0,
                2653.0,
                2119.0,
                1791.0,
                1463.0,
                1269.0,
                1004.0,
                927.0,
                763.0,
                617.0,
                555.0,
                421.0,
                408.0,
                348.0,
                287.0,
                297.0,
                236.0,
                203.0,
                175.0,
                140.0,
                139.0,
                148.0,
                110.0,
                0.0
              ],
              "sumw2": [
                0.0,
                721133.0,
                605047.0,
                416555.0,
                295772.0,
                221484.0,
                175071.0,
                145067.0,
                123700.0,
                0.0,
                0.0,
                82422.0,
                71972.0,
                61970.0,
                51986.0,
                43985.0,
                36234.0,
                29660.0,
                24616.0,
                0.0,
                0.0,
                13292.0,
                10926.0,
                8732.0,
                7407.0,
                5790.0,
                4764.0,
                3831.0,
                3145.0,
                2653.0,
                2119.0,
                1791.0,
                1463.0,
                1269.0,
                1004.0,
                927.0,
                763.0,
                617.0,
                555.0,
                421.0,
                408.0,
                348.0,
                287.0,
                297.0,
                236.0,
                203.0,
                175.0,
                140.0,
                139.0,
                148.0,
                110.0,
                0.0
              ]
            }
          ],
          "num_entries": 3180634,
          "mean": 45064.719801146566,
          "variance": 2726509275.8041983,
          "stddev": 52215.98678378297,
          "num_entries_in_mean_window": 0
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_range": {
            "type": "range",
            "expression": "H1_PZ",
            "limits": {
                "min": 0.0,
                "max": 500000.0,
            },
            "blind_ranges": [
                {"min": 80000.0, "max": 100000.0},
                {"min": 180000.0, "max": 200000.0},
            ],
            "tree_pattern": "DecayTree",
            "n_bins": 50,
        }
    }

    assert all_check_results_comb["job_1"]["check_range"].check_type == "range"
    assert all_check_results_comb["job_1"]["check_range"].passed
    assert all_check_results_comb["job_1"]["check_range"].messages == [
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 4776546.0 events)",
        "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 3180634.0 events)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_range"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 7957180.0
    )
    assert (
        all_check_results_comb["job_1"]["check_range"].tree_data["DecayTree"]["mean"]
        == 44984.71569073466
    )
    assert (
        all_check_results_comb["job_1"]["check_range"].tree_data["DecayTree"][
            "variance"
        ]
        == 2699887678.927709
    )
    assert (
        all_check_results_comb["job_1"]["check_range"].tree_data["DecayTree"]["stddev"]
        == 51960.443405803504
    )
    assert (
        all_check_results_comb["job_1"]["check_range"].tree_data["DecayTree"][
            "num_entries_in_mean_window"
        ]
        == 0
    )


def test_combine_check_results_range_bkg_subtracted():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "histogram_deltaM_bkg_subtracted": {
      "passed": true,
      "messages": [
        "Background subtraction performed successfully for Tree DecayTree"
      ],
      "can_combine": true,
      "input": {
        "type": "range_bkg_subtracted",
        "expression": "Dst_M-D0_M",
        "limits": {
          "min": 139.0,
          "max": 155.0
        },
        "expr_for_subtraction": "D0_M",
        "mean_sig": 1865.0,
        "background_shift": 25.0,
        "background_window": 10.0,
        "signal_window": 30.0,
        "tree_pattern": "DecayTree",
        "n_bins": 50
      },
      "output": {
        "DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M",
              "axes": [
                {
                  "name": "D0_M",
                  "nbins": 50,
                  "min": 1830.0,
                  "max": 1900.0
                }
              ],
              "contents": [
                1327.0,
                60.0,
                55.0,
                45.0,
                62.0,
                58.0,
                60.0,
                58.0,
                59.0,
                59.0,
                52.0,
                69.0,
                63.0,
                69.0,
                73.0,
                63.0,
                100.0,
                100.0,
                118.0,
                119.0,
                167.0,
                195.0,
                190.0,
                238.0,
                273.0,
                271.0,
                291.0,
                313.0,
                259.0,
                235.0,
                212.0,
                190.0,
                170.0,
                168.0,
                142.0,
                117.0,
                123.0,
                98.0,
                77.0,
                70.0,
                63.0,
                62.0,
                47.0,
                61.0,
                58.0,
                52.0,
                59.0,
                58.0,
                60.0,
                53.0,
                54.0,
                1268.0
              ],
              "sumw2": [
                1327.0,
                60.0,
                55.0,
                45.0,
                62.0,
                58.0,
                60.0,
                58.0,
                59.0,
                59.0,
                52.0,
                69.0,
                63.0,
                69.0,
                73.0,
                63.0,
                100.0,
                100.0,
                118.0,
                119.0,
                167.0,
                195.0,
                190.0,
                238.0,
                273.0,
                271.0,
                291.0,
                313.0,
                259.0,
                235.0,
                212.0,
                190.0,
                170.0,
                168.0,
                142.0,
                117.0,
                123.0,
                98.0,
                77.0,
                70.0,
                63.0,
                62.0,
                47.0,
                61.0,
                58.0,
                52.0,
                59.0,
                58.0,
                60.0,
                53.0,
                54.0,
                1268.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                0.0,
                1.0,
                1.0,
                5.0,
                6.0,
                9.0,
                9.0,
                6.0,
                11.0,
                6.0,
                12.0,
                18.0,
                26.0,
                27.0,
                45.0,
                65.0,
                100.0,
                191.0,
                308.0,
                407.0,
                405.0,
                297.0,
                218.0,
                139.0,
                96.0,
                71.0,
                52.0,
                46.0,
                39.0,
                35.0,
                26.0,
                29.0,
                23.0,
                21.0,
                24.0,
                30.0,
                20.0,
                17.0,
                17.0,
                21.0,
                18.0,
                20.0,
                25.0,
                18.0,
                13.0,
                28.0,
                20.0,
                30.0,
                18.0,
                21.0,
                0.0
              ],
              "sumw2": [
                0.0,
                0.0,
                1.0,
                1.0,
                5.0,
                6.0,
                9.0,
                9.0,
                6.0,
                11.0,
                6.0,
                12.0,
                18.0,
                26.0,
                27.0,
                45.0,
                65.0,
                100.0,
                191.0,
                308.0,
                407.0,
                405.0,
                297.0,
                218.0,
                139.0,
                96.0,
                71.0,
                52.0,
                46.0,
                39.0,
                35.0,
                26.0,
                29.0,
                23.0,
                21.0,
                24.0,
                30.0,
                20.0,
                17.0,
                17.0,
                21.0,
                18.0,
                20.0,
                25.0,
                18.0,
                13.0,
                28.0,
                20.0,
                30.0,
                18.0,
                21.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M background",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                1.0,
                0.0,
                0.0,
                3.0,
                0.0,
                4.0,
                3.0,
                3.0,
                7.0,
                7.0,
                8.0,
                4.0,
                3.0,
                4.0,
                12.0,
                6.0,
                11.0,
                6.0,
                18.0,
                15.0,
                15.0,
                16.0,
                16.0,
                12.0,
                10.0,
                15.0,
                9.0,
                7.0,
                4.0,
                10.0,
                10.0,
                9.0,
                15.0,
                10.0,
                15.0,
                13.0,
                5.0,
                8.0,
                9.0,
                7.0,
                7.0,
                15.0,
                4.0,
                9.0,
                12.0,
                6.0,
                9.0,
                7.0,
                6.0,
                10.0,
                0.0
              ],
              "sumw2": [
                0.0,
                1.0,
                0.0,
                0.0,
                3.0,
                0.0,
                4.0,
                3.0,
                3.0,
                7.0,
                7.0,
                8.0,
                4.0,
                3.0,
                4.0,
                12.0,
                6.0,
                11.0,
                6.0,
                18.0,
                15.0,
                15.0,
                16.0,
                16.0,
                12.0,
                10.0,
                15.0,
                9.0,
                7.0,
                4.0,
                10.0,
                10.0,
                9.0,
                15.0,
                10.0,
                15.0,
                13.0,
                5.0,
                8.0,
                9.0,
                7.0,
                7.0,
                15.0,
                4.0,
                9.0,
                12.0,
                6.0,
                9.0,
                7.0,
                6.0,
                10.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                -0.6666666666666666,
                1.0,
                1.0,
                3.0,
                6.0,
                6.333333333333334,
                7.0,
                4.0,
                6.333333333333334,
                1.333333333333334,
                6.666666666666667,
                15.333333333333334,
                24.0,
                24.333333333333332,
                37.0,
                61.0,
                92.66666666666667,
                187.0,
                296.0,
                397.0,
                395.0,
                286.3333333333333,
                207.33333333333334,
                131.0,
                89.33333333333333,
                61.0,
                46.0,
                41.333333333333336,
                36.333333333333336,
                28.333333333333336,
                19.333333333333336,
                23.0,
                13.0,
                14.333333333333334,
                14.0,
                21.333333333333336,
                16.666666666666668,
                11.666666666666668,
                11.0,
                16.333333333333336,
                13.333333333333334,
                10.0,
                22.333333333333332,
                12.0,
                5.0,
                24.0,
                14.0,
                25.333333333333336,
                14.0,
                14.333333333333334,
                0.0
              ],
              "sumw2": [
                0.0,
                0.4444444444444444,
                1.0,
                1.0,
                6.333333333333333,
                6.0,
                10.777777777777779,
                10.333333333333334,
                7.333333333333333,
                14.11111111111111,
                9.11111111111111,
                15.555555555555555,
                19.77777777777778,
                27.333333333333332,
                28.77777777777778,
                50.333333333333336,
                67.66666666666667,
                104.88888888888889,
                193.66666666666666,
                316.0,
                413.6666666666667,
                411.6666666666667,
                304.1111111111111,
                225.11111111111111,
                144.33333333333334,
                100.44444444444444,
                77.66666666666667,
                56.0,
                49.111111111111114,
                40.77777777777778,
                39.44444444444444,
                30.444444444444443,
                33.0,
                29.666666666666664,
                25.444444444444443,
                30.666666666666664,
                35.77777777777778,
                22.22222222222222,
                20.555555555555557,
                21.0,
                24.11111111111111,
                21.11111111111111,
                26.666666666666664,
                26.77777777777778,
                22.0,
                18.333333333333332,
                30.666666666666668,
                24.0,
                33.111111111111114,
                20.666666666666668,
                25.444444444444443,
                0.0
              ]
            }
          ]
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "histogram_deltaM_bkg_subtracted": {
      "passed": true,
      "messages": [
        "Background subtraction performed successfully for Tree DecayTree"
      ],
      "can_combine": true,
      "input": {
        "type": "range_bkg_subtracted",
        "expression": "Dst_M-D0_M",
        "limits": {
          "min": 139.0,
          "max": 155.0
        },
        "expr_for_subtraction": "D0_M",
        "mean_sig": 1865.0,
        "background_shift": 25.0,
        "background_window": 10.0,
        "signal_window": 30.0,
        "tree_pattern": "DecayTree",
        "n_bins": 50
      },
      "output": {
        "DecayTree": {
          "histograms": [
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M",
              "axes": [
                {
                  "name": "D0_M",
                  "nbins": 50,
                  "min": 1830.0,
                  "max": 1900.0
                }
              ],
              "contents": [
                1394.0,
                67.0,
                48.0,
                53.0,
                66.0,
                54.0,
                62.0,
                38.0,
                47.0,
                61.0,
                63.0,
                63.0,
                65.0,
                76.0,
                70.0,
                74.0,
                96.0,
                98.0,
                120.0,
                112.0,
                157.0,
                188.0,
                198.0,
                247.0,
                269.0,
                268.0,
                260.0,
                287.0,
                275.0,
                248.0,
                236.0,
                210.0,
                168.0,
                159.0,
                128.0,
                106.0,
                98.0,
                77.0,
                76.0,
                74.0,
                54.0,
                57.0,
                51.0,
                59.0,
                57.0,
                44.0,
                40.0,
                46.0,
                58.0,
                52.0,
                56.0,
                1332.0
              ],
              "sumw2": [
                1394.0,
                67.0,
                48.0,
                53.0,
                66.0,
                54.0,
                62.0,
                38.0,
                47.0,
                61.0,
                63.0,
                63.0,
                65.0,
                76.0,
                70.0,
                74.0,
                96.0,
                98.0,
                120.0,
                112.0,
                157.0,
                188.0,
                198.0,
                247.0,
                269.0,
                268.0,
                260.0,
                287.0,
                275.0,
                248.0,
                236.0,
                210.0,
                168.0,
                159.0,
                128.0,
                106.0,
                98.0,
                77.0,
                76.0,
                74.0,
                54.0,
                57.0,
                51.0,
                59.0,
                57.0,
                44.0,
                40.0,
                46.0,
                58.0,
                52.0,
                56.0,
                1332.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                0.0,
                3.0,
                4.0,
                9.0,
                3.0,
                12.0,
                8.0,
                9.0,
                15.0,
                14.0,
                13.0,
                19.0,
                35.0,
                25.0,
                50.0,
                68.0,
                95.0,
                177.0,
                262.0,
                406.0,
                394.0,
                342.0,
                224.0,
                153.0,
                92.0,
                58.0,
                59.0,
                43.0,
                30.0,
                26.0,
                24.0,
                35.0,
                23.0,
                20.0,
                22.0,
                22.0,
                17.0,
                22.0,
                19.0,
                13.0,
                19.0,
                11.0,
                32.0,
                21.0,
                30.0,
                28.0,
                20.0,
                18.0,
                24.0,
                20.0,
                0.0
              ],
              "sumw2": [
                0.0,
                0.0,
                3.0,
                4.0,
                9.0,
                3.0,
                12.0,
                8.0,
                9.0,
                15.0,
                14.0,
                13.0,
                19.0,
                35.0,
                25.0,
                50.0,
                68.0,
                95.0,
                177.0,
                262.0,
                406.0,
                394.0,
                342.0,
                224.0,
                153.0,
                92.0,
                58.0,
                59.0,
                43.0,
                30.0,
                26.0,
                24.0,
                35.0,
                23.0,
                20.0,
                22.0,
                22.0,
                17.0,
                22.0,
                19.0,
                13.0,
                19.0,
                11.0,
                32.0,
                21.0,
                30.0,
                28.0,
                20.0,
                18.0,
                24.0,
                20.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M background",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                0.0,
                0.0,
                0.0,
                5.0,
                2.0,
                5.0,
                0.0,
                7.0,
                2.0,
                9.0,
                4.0,
                6.0,
                7.0,
                9.0,
                7.0,
                10.0,
                5.0,
                13.0,
                16.0,
                25.0,
                27.0,
                16.0,
                15.0,
                10.0,
                10.0,
                9.0,
                5.0,
                9.0,
                7.0,
                11.0,
                8.0,
                11.0,
                8.0,
                7.0,
                8.0,
                10.0,
                9.0,
                8.0,
                9.0,
                6.0,
                6.0,
                17.0,
                9.0,
                7.0,
                10.0,
                8.0,
                6.0,
                10.0,
                8.0,
                6.0,
                0.0
              ],
              "sumw2": [
                0.0,
                0.0,
                0.0,
                0.0,
                5.0,
                2.0,
                5.0,
                0.0,
                7.0,
                2.0,
                9.0,
                4.0,
                6.0,
                7.0,
                9.0,
                7.0,
                10.0,
                5.0,
                13.0,
                16.0,
                25.0,
                27.0,
                16.0,
                15.0,
                10.0,
                10.0,
                9.0,
                5.0,
                9.0,
                7.0,
                11.0,
                8.0,
                11.0,
                8.0,
                7.0,
                8.0,
                10.0,
                9.0,
                8.0,
                9.0,
                6.0,
                6.0,
                17.0,
                9.0,
                7.0,
                10.0,
                8.0,
                6.0,
                10.0,
                8.0,
                6.0,
                0.0
              ]
            },
            {
              "version": 1,
              "name": "DecayTree Dst_M-D0_M signal",
              "axes": [
                {
                  "name": "Dst_M-D0_M",
                  "nbins": 50,
                  "min": 139.0,
                  "max": 155.0
                }
              ],
              "contents": [
                0.0,
                0.0,
                3.0,
                4.0,
                5.666666666666667,
                1.6666666666666667,
                8.666666666666668,
                8.0,
                4.333333333333334,
                13.666666666666666,
                8.0,
                10.333333333333334,
                15.0,
                30.333333333333336,
                19.0,
                45.333333333333336,
                61.333333333333336,
                91.66666666666667,
                168.33333333333334,
                251.33333333333334,
                389.3333333333333,
                376.0,
                331.3333333333333,
                214.0,
                146.33333333333334,
                85.33333333333333,
                52.0,
                55.666666666666664,
                37.0,
                25.333333333333336,
                18.666666666666668,
                18.666666666666668,
                27.666666666666668,
                17.666666666666668,
                15.333333333333334,
                16.666666666666668,
                15.333333333333334,
                11.0,
                16.666666666666668,
                13.0,
                9.0,
                15.0,
                -0.33333333333333215,
                26.0,
                16.333333333333336,
                23.333333333333336,
                22.666666666666668,
                16.0,
                11.333333333333334,
                18.666666666666668,
                16.0,
                0.0
              ],
              "sumw2": [
                0.0,
                0.0,
                3.0,
                4.0,
                11.222222222222221,
                3.888888888888889,
                14.222222222222221,
                8.0,
                12.11111111111111,
                15.88888888888889,
                18.0,
                14.777777777777779,
                21.666666666666668,
                38.111111111111114,
                29.0,
                53.111111111111114,
                72.44444444444444,
                97.22222222222223,
                182.77777777777777,
                269.1111111111111,
                417.1111111111111,
                406.0,
                349.1111111111111,
                230.66666666666666,
                157.44444444444446,
                96.44444444444444,
                62.0,
                61.22222222222222,
                47.0,
                33.111111111111114,
                30.88888888888889,
                27.555555555555557,
                39.888888888888886,
                26.555555555555557,
                23.11111111111111,
                25.555555555555557,
                26.444444444444443,
                21.0,
                25.555555555555557,
                23.0,
                15.666666666666666,
                21.666666666666668,
                18.555555555555557,
                36.0,
                24.11111111111111,
                34.44444444444444,
                31.555555555555557,
                22.666666666666668,
                22.444444444444443,
                27.555555555555557,
                22.666666666666668,
                0.0
              ]
            }
          ]
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    hist_json_0 = checks_utils.serialise_hist(
        all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].tree_data[
            "DecayTree"
        ]["histograms"][0]
    )
    hist_json_1 = checks_utils.serialise_hist(
        all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].tree_data[
            "DecayTree"
        ]["histograms"][1]
    )
    hist_json_2 = checks_utils.serialise_hist(
        all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].tree_data[
            "DecayTree"
        ]["histograms"][2]
    )
    hist_json_3 = checks_utils.serialise_hist(
        all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].tree_data[
            "DecayTree"
        ]["histograms"][3]
    )

    h_0 = {
        "version": 1,
        "name": "DecayTree Dst_M-D0_M",
        "axes": [{"name": "D0_M", "nbins": 50, "min": 1830.0, "max": 1900.0}],
        "contents": [
            2721.0,
            127.0,
            103.0,
            98.0,
            128.0,
            112.0,
            122.0,
            96.0,
            106.0,
            120.0,
            115.0,
            132.0,
            128.0,
            145.0,
            143.0,
            137.0,
            196.0,
            198.0,
            238.0,
            231.0,
            324.0,
            383.0,
            388.0,
            485.0,
            542.0,
            539.0,
            551.0,
            600.0,
            534.0,
            483.0,
            448.0,
            400.0,
            338.0,
            327.0,
            270.0,
            223.0,
            221.0,
            175.0,
            153.0,
            144.0,
            117.0,
            119.0,
            98.0,
            120.0,
            115.0,
            96.0,
            99.0,
            104.0,
            118.0,
            105.0,
            110.0,
            2600.0,
        ],
        "sumw2": [
            2721.0,
            127.0,
            103.0,
            98.0,
            128.0,
            112.0,
            122.0,
            96.0,
            106.0,
            120.0,
            115.0,
            132.0,
            128.0,
            145.0,
            143.0,
            137.0,
            196.0,
            198.0,
            238.0,
            231.0,
            324.0,
            383.0,
            388.0,
            485.0,
            542.0,
            539.0,
            551.0,
            600.0,
            534.0,
            483.0,
            448.0,
            400.0,
            338.0,
            327.0,
            270.0,
            223.0,
            221.0,
            175.0,
            153.0,
            144.0,
            117.0,
            119.0,
            98.0,
            120.0,
            115.0,
            96.0,
            99.0,
            104.0,
            118.0,
            105.0,
            110.0,
            2600.0,
        ],
    }

    assert checks_data_comb == {
        "histogram_deltaM_bkg_subtracted": {
            "type": "range_bkg_subtracted",
            "expression": "Dst_M-D0_M",
            "limits": {"min": 139.0, "max": 155.0},
            "expr_for_subtraction": "D0_M",
            "mean_sig": 1865.0,
            "background_shift": 25.0,
            "background_window": 10.0,
            "signal_window": 30.0,
            "tree_pattern": "DecayTree",
            "n_bins": 50,
        }
    }

    h_1 = {
        "version": 1,
        "name": "DecayTree Dst_M-D0_M signal",
        "axes": [{"name": "Dst_M-D0_M", "nbins": 50, "min": 139.0, "max": 155.0}],
        "contents": [
            0.0,
            0.0,
            4.0,
            5.0,
            14.0,
            9.0,
            21.0,
            17.0,
            15.0,
            26.0,
            20.0,
            25.0,
            37.0,
            61.0,
            52.0,
            95.0,
            133.0,
            195.0,
            368.0,
            570.0,
            813.0,
            799.0,
            639.0,
            442.0,
            292.0,
            188.0,
            129.0,
            111.0,
            89.0,
            69.0,
            61.0,
            50.0,
            64.0,
            46.0,
            41.0,
            46.0,
            52.0,
            37.0,
            39.0,
            36.0,
            34.0,
            37.0,
            31.0,
            57.0,
            39.0,
            43.0,
            56.0,
            40.0,
            48.0,
            42.0,
            41.0,
            0.0,
        ],
        "sumw2": [
            0.0,
            0.0,
            4.0,
            5.0,
            14.0,
            9.0,
            21.0,
            17.0,
            15.0,
            26.0,
            20.0,
            25.0,
            37.0,
            61.0,
            52.0,
            95.0,
            133.0,
            195.0,
            368.0,
            570.0,
            813.0,
            799.0,
            639.0,
            442.0,
            292.0,
            188.0,
            129.0,
            111.0,
            89.0,
            69.0,
            61.0,
            50.0,
            64.0,
            46.0,
            41.0,
            46.0,
            52.0,
            37.0,
            39.0,
            36.0,
            34.0,
            37.0,
            31.0,
            57.0,
            39.0,
            43.0,
            56.0,
            40.0,
            48.0,
            42.0,
            41.0,
            0.0,
        ],
    }

    h_2 = {
        "version": 1,
        "name": "DecayTree Dst_M-D0_M background",
        "axes": [{"name": "Dst_M-D0_M", "nbins": 50, "min": 139.0, "max": 155.0}],
        "contents": [
            0.0,
            1.0,
            0.0,
            0.0,
            8.0,
            2.0,
            9.0,
            3.0,
            10.0,
            9.0,
            16.0,
            12.0,
            10.0,
            10.0,
            13.0,
            19.0,
            16.0,
            16.0,
            19.0,
            34.0,
            40.0,
            42.0,
            32.0,
            31.0,
            22.0,
            20.0,
            24.0,
            14.0,
            16.0,
            11.0,
            21.0,
            18.0,
            20.0,
            23.0,
            17.0,
            23.0,
            23.0,
            14.0,
            16.0,
            18.0,
            13.0,
            13.0,
            32.0,
            13.0,
            16.0,
            22.0,
            14.0,
            15.0,
            17.0,
            14.0,
            16.0,
            0.0,
        ],
        "sumw2": [
            0.0,
            1.0,
            0.0,
            0.0,
            8.0,
            2.0,
            9.0,
            3.0,
            10.0,
            9.0,
            16.0,
            12.0,
            10.0,
            10.0,
            13.0,
            19.0,
            16.0,
            16.0,
            19.0,
            34.0,
            40.0,
            42.0,
            32.0,
            31.0,
            22.0,
            20.0,
            24.0,
            14.0,
            16.0,
            11.0,
            21.0,
            18.0,
            20.0,
            23.0,
            17.0,
            23.0,
            23.0,
            14.0,
            16.0,
            18.0,
            13.0,
            13.0,
            32.0,
            13.0,
            16.0,
            22.0,
            14.0,
            15.0,
            17.0,
            14.0,
            16.0,
            0.0,
        ],
    }

    h_3 = {
        "version": 1,
        "name": "DecayTree Dst_M-D0_M signal",
        "axes": [{"name": "Dst_M-D0_M", "nbins": 50, "min": 139.0, "max": 155.0}],
        "contents": [
            0.0,
            -0.6666666666666666,
            4.0,
            5.0,
            8.666666666666668,
            7.666666666666667,
            15.0,
            15.0,
            8.333333333333334,
            20.0,
            9.333333333333334,
            17.0,
            30.333333333333336,
            54.333333333333336,
            43.333333333333336,
            82.33333333333333,
            122.33333333333333,
            184.33333333333334,
            355.3333333333333,
            547.3333333333334,
            786.3333333333334,
            771.0,
            617.6666666666666,
            421.3333333333333,
            277.3333333333333,
            174.66666666666666,
            113.0,
            101.66666666666667,
            78.33333333333333,
            61.666666666666664,
            47.0,
            38.0,
            50.66666666666667,
            30.666666666666668,
            29.666666666666668,
            30.666666666666668,
            36.66666666666667,
            27.666666666666668,
            28.333333333333336,
            24.0,
            25.333333333333336,
            28.333333333333336,
            9.666666666666668,
            48.333333333333336,
            28.333333333333336,
            28.333333333333336,
            46.66666666666667,
            30.0,
            36.66666666666667,
            32.66666666666667,
            30.333333333333336,
            0.0,
        ],
        "sumw2": [
            0.0,
            0.4444444444444444,
            4.0,
            5.0,
            17.555555555555557,
            9.88888888888889,
            25.0,
            18.333333333333332,
            19.444444444444443,
            30.0,
            27.11111111111111,
            30.333333333333332,
            41.44444444444444,
            65.44444444444444,
            57.77777777777778,
            103.44444444444444,
            140.11111111111111,
            202.11111111111111,
            376.44444444444446,
            585.1111111111111,
            830.7777777777778,
            817.6666666666666,
            653.2222222222222,
            455.77777777777777,
            301.77777777777777,
            196.88888888888889,
            139.66666666666666,
            117.22222222222223,
            96.11111111111111,
            73.88888888888889,
            70.33333333333333,
            58.0,
            72.88888888888889,
            56.22222222222222,
            48.55555555555556,
            56.22222222222222,
            62.22222222222222,
            43.22222222222222,
            46.111111111111114,
            44.0,
            39.77777777777778,
            42.77777777777778,
            45.22222222222222,
            62.77777777777778,
            46.111111111111114,
            52.77777777777778,
            62.22222222222222,
            46.666666666666664,
            55.55555555555556,
            48.22222222222222,
            48.111111111111114,
            0.0,
        ],
    }

    assert (
        all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].check_type
        == "range_bkg_subtracted"
    )
    assert all_check_results_comb["job_1"]["histogram_deltaM_bkg_subtracted"].passed
    assert all_check_results_comb["job_1"][
        "histogram_deltaM_bkg_subtracted"
    ].messages == [
        "Background subtraction performed successfully for Tree DecayTree",
        "Background subtraction performed successfully for Tree DecayTree",
    ]

    assert hist_json_0 == h_0
    assert hist_json_1 == h_1
    assert hist_json_2 == h_2
    # hist_json_3 is treated in a different way to take into account expected differences in `contents` and `sumw2`
    # due to the rounding of elements after background subtraction
    assert hist_json_3["version"] == h_3["version"]
    assert hist_json_3["name"] == h_3["name"]
    assert hist_json_3["axes"] == h_3["axes"]
    assert np.allclose(hist_json_3["sumw2"], h_3["sumw2"], rtol=1e-03)
    assert np.allclose(hist_json_3["contents"], h_3["contents"], rtol=1e-03)


def test_combine_check_results_simple_failing():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 5135823 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 5135823
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 4864177 in RandomTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "RandomTree"
      },
      "output": {
        "RandomTree": {
          "num_entries": 4864177
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    with pytest.warns(UserWarning) as w:
        checks_utils.combine_checks(
            [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
        )
    assert len(w) == 1
    assert (
        w[0].message.args[0]
        == "Found check with duplicate name (check_num_entries) but different configuration - cannot be combined"
    )


def test_combine_check_results_simple_different_job_name():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 5135823 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 5135823
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_2": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 4864177 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 4864177
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries"].check_type == "num_entries"
    )
    assert all_check_results_comb["job_1"]["check_num_entries"].passed
    assert all_check_results_comb["job_1"]["check_num_entries"].messages == [
        "Found 5135823 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 5135823
    )

    assert (
        all_check_results_comb["job_2"]["check_num_entries"].check_type == "num_entries"
    )
    assert all_check_results_comb["job_2"]["check_num_entries"].passed
    assert all_check_results_comb["job_2"]["check_num_entries"].messages == [
        "Found 4864177 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_2"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 4864177
    )


def test_combine_check_results_simple_different_check_name():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries": {
      "passed": true,
      "messages": [
        "Found 5135823 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 5135823
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries_v2": {
      "passed": true,
      "messages": [
        "Found 4864177 in DecayTree (1000 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries",
        "count": 1000,
        "tree_pattern": "DecayTree"
      },
      "output": {
        "DecayTree": {
          "num_entries": 4864177
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        },
        "check_num_entries_v2": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree",
        },
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries"].check_type == "num_entries"
    )
    assert all_check_results_comb["job_1"]["check_num_entries"].passed
    assert all_check_results_comb["job_1"]["check_num_entries"].messages == [
        "Found 5135823 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 5135823
    )

    assert (
        all_check_results_comb["job_1"]["check_num_entries_v2"].check_type
        == "num_entries"
    )
    assert all_check_results_comb["job_1"]["check_num_entries_v2"].passed
    assert all_check_results_comb["job_1"]["check_num_entries_v2"].messages == [
        "Found 4864177 in DecayTree (1000 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries_v2"].tree_data["DecayTree"][
            "num_entries"
        ]
        == 4864177
    )


def test_combine_check_results_num_entries_per_invpb():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries_per_invpb": {
      "passed": true,
      "messages": [
        "Found 206.8 entries per unit luminosity (pb-1) in DecayTree (100 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries_per_invpb",
        "count_per_invpb": 100,
        "tree_pattern": "DecayTree",
        "lumi_pattern": "LumiTuple"
      },
      "output": {
        "DecayTree": {
          "num_entries": 2585,
          "lumi_invpb": 12.5,
          "num_entries_per_invpb": 206.8
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries_per_invpb": {
      "passed": true,
      "messages": [
        "Found 201.875 entries per unit luminosity (pb-1) in DecayTree (100 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries_per_invpb",
        "count_per_invpb": 100,
        "tree_pattern": "DecayTree",
        "lumi_pattern": "LumiTuple"
      },
      "output": {
        "DecayTree": {
          "num_entries": 2584,
          "lumi_invpb": 12.8,
          "num_entries_per_invpb": 201.875
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries_per_invpb": {
            "type": "num_entries_per_invpb",
            "count_per_invpb": 100,
            "tree_pattern": "DecayTree",
            "lumi_pattern": "LumiTuple",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].check_type
        == "num_entries_per_invpb"
    )
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].passed
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].can_combine
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].messages == [
        "Found 206.8 entries per unit luminosity (pb-1) in DecayTree (100 required)",
        "Found 201.875 entries per unit luminosity (pb-1) in DecayTree (100 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
            "DecayTree"
        ]["num_entries"]
        == 5169
    )
    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
            "DecayTree"
        ]["lumi_invpb"]
        == 25.3
    )
    assert (
        round(
            all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
                "DecayTree"
            ]["num_entries_per_invpb"],
            3,
        )
        == 204.308
    )


def test_combine_check_results_num_entries_per_invpb_low_stat():
    check_results_json_a = dedent(
        """\
{
  "job_1": {
    "check_num_entries_per_invpb": {
      "passed": false,
      "messages": [
        "Found 20.4 entries per unit luminosity (pb-1) in DecayTree (100 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries_per_invpb",
        "count_per_invpb": 100,
        "tree_pattern": "DecayTree",
        "lumi_pattern": "LumiTuple"
      },
      "output": {
        "DecayTree": {
          "num_entries": 255,
          "lumi_invpb": 12.5,
          "num_entries_per_invpb": 20.4
        }
      }
    }
  }
}"""
    )

    check_results_json_b = dedent(
        """\
{
  "job_1": {
    "check_num_entries_per_invpb": {
      "passed": true,
      "messages": [
        "Found 201.875 entries per unit luminosity (pb-1) in DecayTree (100 required)"
      ],
      "can_combine": true,
      "input": {
        "type": "num_entries_per_invpb",
        "count_per_invpb": 100,
        "tree_pattern": "DecayTree",
        "lumi_pattern": "LumiTuple"
      },
      "output": {
        "DecayTree": {
          "num_entries": 2584,
          "lumi_invpb": 12.8,
          "num_entries_per_invpb": 201.875
        }
      }
    }
  }
}"""
    )

    checks_data_a, all_check_results_a = checks_utils.JSON_to_checks(
        json.loads(check_results_json_a)
    )
    checks_data_b, all_check_results_b = checks_utils.JSON_to_checks(
        json.loads(check_results_json_b)
    )

    checks_data_comb, all_check_results_comb = checks_utils.combine_checks(
        [(checks_data_a, all_check_results_a), (checks_data_b, all_check_results_b)]
    )

    assert checks_data_comb == {
        "check_num_entries_per_invpb": {
            "type": "num_entries_per_invpb",
            "count_per_invpb": 100,
            "tree_pattern": "DecayTree",
            "lumi_pattern": "LumiTuple",
        }
    }

    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].check_type
        == "num_entries_per_invpb"
    )
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].passed
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].can_combine
    assert all_check_results_comb["job_1"]["check_num_entries_per_invpb"].messages == [
        "Found 20.4 entries per unit luminosity (pb-1) in DecayTree (100 required)",
        "Found 201.875 entries per unit luminosity (pb-1) in DecayTree (100 required)",
    ]
    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
            "DecayTree"
        ]["num_entries"]
        == 2839
    )
    assert (
        all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
            "DecayTree"
        ]["lumi_invpb"]
        == 25.3
    )
    assert (
        round(
            all_check_results_comb["job_1"]["check_num_entries_per_invpb"].tree_data[
                "DecayTree"
            ]["num_entries_per_invpb"],
            3,
        )
        == 112.213
    )
