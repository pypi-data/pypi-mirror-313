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

import inspect
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering
from typing import Dict, List


class CheckLeniency(str, Enum):
    """Check leniency levels."""

    Strict = "Strict"  # Dont ignore anything
    Lenient = "Lenient"  # Ignore failures and warnings
    Ignore = "Ignore"  # Ignore everything


@total_ordering
class CheckFailureLevel(int, Enum):
    """Check message failure levels."""

    ERROR = 3
    FAIL = 2
    WARNING = 1
    SUCCESS = 0

    def __lt__(self, other):
        """Comparison op."""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


@dataclass
class CheckResult:
    """Class for representing the return result of ntuple checks."""

    check_type: str = field(default="TO BE SET")
    passed: bool = field(default=False)
    can_combine: bool = field(default=False)
    messages: List[str] = field(default_factory=list)
    tree_data: Dict[str, Dict] = field(default_factory=dict)

    def has_failures(self, minimum=CheckFailureLevel.WARNING):
        """Determine if the messages stored in this CheckResult object are above the set 'minimum' failure level.

        Args:
            minimum (CheckFailureLevel, optional): The minimum failure level. Defaults to CheckFailureLevel.WARNING.

        Returns:
            bool: Whether the CheckResult object is in failure or not.
        """
        return any([m[0] >= minimum for m in self.messages])

    def has_all_messages(self, *message_strings):
        """Check messages exist with supplied strings."""
        message_str_only = [m[1] for m in self.messages]
        for m in message_strings:
            if m not in message_str_only:
                return False
        return True

    def success(self, message):
        """Add a "SUCCESS" message to this CheckResult object.

        Args:
            message (str): A message describing the success.
        """
        self.messages.append((CheckFailureLevel.SUCCESS, message))

    def warning(self, message):
        """Add a "WARNING" message to this CheckResult object.

        Args:
            message (str): A message describing the warning.
        """
        self.messages.append((CheckFailureLevel.WARNING, message))

    def fail(self, message):
        """Add a "FAILURE" message to this CheckResult object.

        Args:
            message (str): A message describing the failure.
        """
        self.messages.append((CheckFailureLevel.FAIL, message))

    def error(self, message):
        """Add an "ERROR" message to this CheckResult object.

        Args:
            message (str): A message describing the error.
        """
        self.messages.append((CheckFailureLevel.ERROR, message))

    def update_passed(self, leniency: CheckLeniency):
        """Determine whether the CheckResult represents a passing check with the given leniency level.

        Args:
            leniency (CheckLeniency): A CheckLeniency level.
        """
        if leniency == CheckLeniency.Ignore:
            # The user doesn't care
            self.passed = True
        elif leniency == CheckLeniency.Lenient:
            # warnings, failures are ignored
            self.passed = not self.has_failures(minimum=CheckFailureLevel.ERROR)
        else:
            # any warnings or errors should set this off
            self.passed = not self.has_failures(minimum=CheckFailureLevel.WARNING)


def register_check(checks_list, check_type):
    """A decorator used to register a function as a check or validation.

    Args:
        checks_list (list): The list instance to add the check into.
        check_type (str): The name of the check. Must be unique...
    """

    def _register_check(check_func):
        checks_list[check_type] = {
            "type": check_type,
            "pars": list(inspect.signature(check_func).parameters.keys()),
            "func": check_func,
        }
        return check_func

    return _register_check
