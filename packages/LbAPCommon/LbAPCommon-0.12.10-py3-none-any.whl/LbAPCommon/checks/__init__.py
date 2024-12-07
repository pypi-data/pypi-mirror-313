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

from ..config import default_validations
from . import num_entries, validations
from . import range as range_checks
from .common import CheckLeniency, CheckResult

all_checks = {}

all_checks.update(range_checks.all_checks)
all_checks.update(num_entries.all_checks)
all_checks.update(validations.all_checks)


def run_job_checks(
    jobs_data,
    job_name: str,
    checks_list: list[str],
    check_data,
    test_ntuple_path_list: list[str],
):
    """Run checks and return CheckResult objects.

    Args:
        jobs_data: Job configuration, usually loaded from a config file.
        job_name (str): Job name to run checks or validations against.
        checks_data: Checks configuration, usually loaded from a config file.
        checks_list (list[str]): List of checks to run specified by their names.
        test_ntuple_path_list (list[str]): A list of paths to ntuple files to be used by each check.

    Returns:
        dict[CheckResult]: A dictionary of CheckResults detailing the result of each check.
    """
    check_results = {}

    default_leniency = CheckLeniency.Strict

    used_check_types = [check_data[check]["type"] for check in checks_list]

    # First add any default checks if they haven't been explicitly requested by the user
    for check_type in default_validations:
        if check_type not in used_check_types:
            check_data[check_type] = {"type": check_type, "mode": "Strict"}
            checks_list.append(check_type)

    for check in checks_list:
        data = check_data[check]
        check_type = data["type"]

        if check_type not in all_checks:
            raise ValueError(
                f"Check type {check_type!r} does not exist - check if it is being registered properly."
            )
        registered_check = all_checks[check_type]

        leniency = data.get("mode", default_leniency)

        if not leniency == CheckLeniency.Ignore:
            check_result: CheckResult = registered_check["func"](
                **{
                    **(
                        {"test_ntuple_path_list": test_ntuple_path_list}
                        if "test_ntuple_path_list" in registered_check["pars"]
                        else {}
                    ),
                    **{
                        par: val
                        for par, val in data.items()
                        if par in registered_check["pars"]
                    },
                    **(
                        {"jobs_data": jobs_data}
                        if "jobs_data" in registered_check["pars"]
                        else {}
                    ),
                    **(
                        {"job_name": job_name}
                        if "job_name" in registered_check["pars"]
                        else {}
                    ),
                },
            )
        else:
            check_result = CheckResult(check_type=check_type, can_combine=False)
            check_result.success("Check ignored due to user configuration")
        if not isinstance(check_result, CheckResult):
            check_result = CheckResult(check_type=check_type, can_combine=False)
            check_result.error(
                f"Check type {check_type!r} did not return CheckResult object"
            )

        check_result.check_type = check_type
        check_result.update_passed(leniency)
        check_results[check] = check_result

    return check_results
