from unittest import TestCase

from utils.common_utils import *


class CommonUtilsTests(TestCase):
    _GREEN_COLOR_CODE = "007500"
    _ORANGE_COLOR_CODE = "FFA500"
    _RED_COLOR_CODE = "b30000"

    _UNIQUE_LIST = ["value1", "value2", "value3", "value4"]

    def test_get_color_code_by_number__when_number_is_less_than_3__expect_green_color_code(self):
        # Arrange
        expected_result = self._GREEN_COLOR_CODE

        # Act
        actual_result = get_color_code_by_number(2)

        # Assert
        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_equals_3__expect_green_color_code(self):
        # Arrange
        expected_result = self._GREEN_COLOR_CODE

        # Act
        actual_result = get_color_code_by_number(3)

        # Assert
        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_is_greater_than_3_and_less_than_12__expect_orange_color_code(self):
        # Arrange
        expected_result = self._ORANGE_COLOR_CODE

        # Act
        actual_result = get_color_code_by_number(6)

        # Assert
        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_equals_12__expect_orange_color_code(self):
        # Arrange
        expected_result = self._ORANGE_COLOR_CODE

        # Act
        actual_result = get_color_code_by_number(12)

        # Assert
        self.assertEqual(expected_result, actual_result)

    def test_get_color_code_by_number__when_number_is_greater_than_12__expect_red_color_code(self):
        # Arrange
        expected_result = self._RED_COLOR_CODE

        # Act
        actual_result = get_color_code_by_number(13)

        # Assert
        self.assertEqual(expected_result, actual_result)

    def test_add_unique_items_to_list__when_all_items_are_unique__expect_all_to_be_added(self):
        # Arrange
        expected_elements = ["value1", "value2", "value3", "value4", "value5", "value6"]
        expected_elements_count = 6

        # Act
        new_list = add_unique_items_to_list(self._UNIQUE_LIST, "value5", "value6")
        actual_elements_count = len(new_list)

        # Assert
        self.assertListEqual(expected_elements, new_list)
        self.assertEqual(expected_elements_count, actual_elements_count)

    def test_add_unique_items_to_list__when_not_all_items_are_unique__expect_to_add_unique_items_only(self):
        # Arrange
        expected_elements = ["value1", "value2", "value3", "value4", "value5", "value6"]
        expected_elements_count = 6

        # Act
        new_list = add_unique_items_to_list(self._UNIQUE_LIST, "value1", "value2", "value5", "value6")
        actual_elements_count = len(new_list)

        # Assert
        self.assertListEqual(expected_elements, new_list)
        self.assertEqual(expected_elements_count, actual_elements_count)

    def test_add_unique_items_to_list__when_all_items_are_duplicate__expect_no_change(self):
        # Arrange
        expected_elements = self._UNIQUE_LIST
        expected_elements_count = 4

        # Act
        new_list = add_unique_items_to_list(self._UNIQUE_LIST, "value1", "value2")
        actual_elements_count = len(new_list)

        # Assert
        self.assertListEqual(expected_elements, new_list)
        self.assertEqual(expected_elements_count, actual_elements_count)
