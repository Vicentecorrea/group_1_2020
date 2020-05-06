import unittest
import load_block_model as lbm
from constants import TEST_DB_NAME, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME
from block_model import BlockModel
from block import Block
test_model_name = "mclaughlin_test"
test_db_name = "block_model_test.db"

test_existent_block_model_file_path = "mclaughlin_test.blocks"
test_nonexistent_block_model_file_path = "kd_test.blocks"

mclaughlin_columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'au']
mclaughlin_minerals = {"au": "oz_per_ton"}
mclaughlin_block_model_test = BlockModel("mclaughlin_limit", [Block({'id': 0,
                                                                     'x': 31,
                                                                     'y': 208,
                                                                     'z': 44,
                                                                     'blockvalue': -646,
                                                                     'ton': 489.58,
                                                                     'destination': 0,
                                                                     'au': 0.038})], mclaughlin_columns,
                                         mclaughlin_minerals)


class TestLoadBlockModel(unittest.TestCase):

    def test_get_model_name_from_path_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some\\text\\before\\name.name"), "name")

    def test_get_model_name_from_path_that_contains_normal_slash_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some/text/before/name.name"), "name")

    def test_get_model_name_from_path_that_contains_special_characters_returns_correct_name(self):
        self.assertEqual(lbm.get_model_name_from_path("some/text/before-the/name.name"), "name")

    def test_retrieve_columns_types_valid_types(self):
        column_types = ["INT", "INT", "INT", "INT", "FLOAT", "INT", "FLOAT"]
        self.assertEqual(lbm.retrieve_columns_types(test_existent_block_model_file_path), column_types)

    def test_load_block_file_return_true(self):
        columns = ["id", "x", "y", "z", "tonn", "blockvalue", "destination", "CU", "processProfit"]
        minerals = {"CU": "oz_per_ton"}
        self.assertEqual(lbm.load_block_file(test_nonexistent_block_model_file_path,
                                             columns,
                                             minerals,
                                             TEST_DB_NAME,
                                             TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                             TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), True)

    def test_load_existent_block_file_return_false(self):
        columns = ['id', 'x', 'y', 'z', 'blockvalue', 'ton', 'destination', 'Au']
        minerals = {"au": "oz_per_ton"}
        lbm.load_block_file(test_existent_block_model_file_path,
                            columns,
                            minerals,
                            TEST_DB_NAME,
                            TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                            TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(
            lbm.load_block_file(test_existent_block_model_file_path,
                                columns,
                                minerals,
                                TEST_DB_NAME,
                                TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), False)


    def test_load_block_model_object_returns_true(self):
        self.assertEqual(lbm.load_block_model_object(mclaughlin_block_model_test, test_db_name,
                                                     TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                     TEST_MINERAL_GRADES_INFORMATION_FILE_NAME), True)

if __name__ == "__main__":
    unittest.main()
