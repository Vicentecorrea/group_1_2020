import unittest, json
from api import __main__ as api_main
import block_model_proccesor
from constants import TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME


class TestApi(unittest.TestCase):

    def setUp(self):
        api_main.app.config['TESTING'] = True
        api_main.app.config['DEBUG'] = False
        self.app = api_main.app.test_client()

    def test_get_block_models_names_return_ok_status_code(self):
        self.assertEqual(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, False).status_code, 200)

    def test_get_block_model_blocks_return_ok_status_code(self):
        first_block_model_name = \
            block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(
            api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                            TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_models_names_return_correct(self):
        self.assertEqual(block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME),
                         json.loads(api_main.get_block_models_names(TEST_LOADED_MODELS_INFORMATION_FILE_NAME, False).data))

    def test_get_block_model_blocks_return_correct(self):
        first_block_model_name = \
            block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
        self.assertEqual(
            block_model_proccesor.get_block_list(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                 TEST_DB_NAME), json.loads(
                api_main.get_block_model_blocks(first_block_model_name, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).data))

    def test_get_feature_flags_return_correct(self):
        default_feature_flags_json = {"restful_response": False, "block_info": False}
        default_feature_flags_types_json = {}
        for flag in default_feature_flags_json:
            default_feature_flags_types_json[flag] = type(default_feature_flags_json[flag])
        api_feature_flags_json = api_main.get_feature_flags()
        api_feature_flags_types_json = {}
        for flag in api_feature_flags_json:
            api_feature_flags_types_json[flag] = type(api_feature_flags_json[flag])
        self.assertEqual(default_feature_flags_types_json, api_feature_flags_types_json)

    def test_reblock_block_model_endpoint_bad_parameter_names_return_status_code_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuousattributes": [
                "blockvalue"
            ],
            "proportionalattributes": {"au": "oz_per_ton"},
            "categoricalattributes": ["destination"],
            "columnswith_mass": ["ton"]
        }
        model_name = "mclaughlin_limit"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_reblock_block_model_endpoint_correct_data_return_status_code_200(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "blockvalue"
            ],
            "proportional_attributes": {"au": "oz_per_ton"},
            "categorical_attributes": ["destination"],
            "columns_with_mass": ["ton"]
        }
        model_name = "mclaughlin_limit"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME, TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 200)

    def test_reblock_block_model_endpoint_inexistent_model_returns_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "blockvalue"
            ],
            "proportional_attributes": {"au": "oz_per_ton"},
            "categorical_attributes": ["destination"],
            "columns_with_mass": ["ton"]
        }
        model_name = "kd"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_reblock_block_model_endpoint_incorrect_columns_returns_400(self):
        data = {
            "rx": 1,
            "ry": 1,
            "rz": 1,
            "continuous_attributes": [
                "bkvalue"
            ],
            "proportional_attributes": {"cu": "oz_per_ton"},
            "categorical_attributes": ["destinn"],
            "columns_with_mass": ["ton"]
        }
        model_name = "mclaughlin_limit"
        response = api_main.reblock_block_model(model_name, data, TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME)
        self.assertEqual(response.status_code, 400)

    def test_get_block_model_blocks_existent_model_returns_200(self):
        self.assertEqual(api_main.get_block_model_blocks("mclaughlin_limit",
                                                         TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                         TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 200)

    def test_get_block_model_blocks_unexistent_model_returns_400(self):
        self.assertEqual(api_main.get_block_model_blocks("unexistent_model",
                                                         TEST_LOADED_MODELS_INFORMATION_FILE_NAME,
                                                         TEST_DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME).status_code, 400)
# first_block_model_name = block_model_proccesor.get_model_names_to_dictionary(TEST_LOADED_MODELS_INFORMATION_FILE_NAME)[0]['name']
# print(first_block_model_name)
