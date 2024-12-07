"""Utils testing"""

import unittest
from aind_data_schema_models import utils  # Assuming the functions are defined in a module named utils


class TestUtils(unittest.TestCase):
    """Tests methods in utils module"""

    def test_to_class_name(self):
        """Test to class name method"""

        # Regular cases
        self.assertEqual(utils.to_class_name("Smart SPIM"), "Smart_Spim")
        self.assertEqual(utils.to_class_name("SmartSPIM"), "Smartspim")
        self.assertEqual(utils.to_class_name("single-plane-ophys"), "Single_Plane_Ophys")

        # Edge cases
        self.assertEqual(utils.to_class_name("123test"), "_123Test")  # Starts with a number
        self.assertEqual(utils.to_class_name("a-b-c"), "A_B_C")  # Hyphenated

        # Empty string
        self.assertEqual(utils.to_class_name(""), "")

    def test_to_class_name_underscored(self):
        """Test to class name underscored method"""

        # Regular cases
        self.assertEqual(utils.to_class_name_underscored("Smart SPIM"), "_Smart_Spim")
        self.assertEqual(utils.to_class_name_underscored("SmartSPIM"), "_Smartspim")
        self.assertEqual(utils.to_class_name_underscored("single-plane-ophys"), "_Single_Plane_Ophys")

        # Edge cases
        self.assertEqual(utils.to_class_name_underscored("123test"), "_123Test")  # Starts with a number
        self.assertEqual(utils.to_class_name_underscored("a-b-c"), "_A_B_C")  # Hyphenated

        # Empty string
        self.assertEqual(utils.to_class_name_underscored(""), "_")  # Should still return an underscore


if __name__ == "__main__":
    unittest.main()
