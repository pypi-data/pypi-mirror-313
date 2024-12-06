"""Test the metric value class."""

import unittest

from pydantic import ValidationError
from aind_qcportal_schema.metric_value import (
    DropdownMetric,
    CheckboxMetric,
    RulebasedMetric,
    MultiAssetMetric,
)


class MetricValueTest(unittest.TestCase):
    """Test the metric value class."""

    def test_constructors(self):
        """Build valid versions of each metric."""

        v = DropdownMetric(value="a", options=["a", "b"])
        self.assertIsNotNone(v)

        v = CheckboxMetric(value="a", options=["a", "b"])
        self.assertIsNotNone(v)

        v = RulebasedMetric(value="a", rule="a")
        self.assertIsNotNone(v)

    def test_multi_asset(self):
        """Ensure multi_asset validators work"""

        with self.assertRaises(ValidationError):
            MultiAssetMetric(
                values=[1, 2, 3],
                options=[0, 1, 2, 3],
            )

        mam = MultiAssetMetric(
            values=[1, 2, 3], options=[0, 1, 2, 3], type="dropdown"
        )

        self.assertIsNotNone(mam)


if __name__ == "__main__":
    unittest.main()
