from tabulate import tabulate
import sqlite3
import json

from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME

def get_model_data_table(model_name, from_id, to_id, db_name=DB_NAME):
    data_table = []
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT * FROM {} WHERE ID >= {} AND ID <= {}".format(model_name, from_id, to_id))
    for row in cursor:
        data_table.append(list(row))
    return data_table


def get_headers_tabulated_table(model_name):
    model_information_json = get_models_information_json()
    separator_lines = []
    for column in model_information_json[model_name]:
        separator_lines.append("_" * len(column))
    return [model_information_json[model_name], separator_lines]


def get_block_model_columns(block_model_name):
    block_models_available = get_models_information_json()
    return block_models_available[block_model_name]


def check_if_model_exists_in_json(model_name):
    model_information_json = get_models_information_json()
    try:
        info = model_information_json[model_name]
        return True
    except:
        return False

def get_models_information_json():
    with open(LOADED_MODELS_INFORMATION_FILE_NAME) as json_file:
        model_information_json = json.load(json_file)
    return model_information_json

def get_tabulated_blocks(model_name, from_id, to_id):
    if check_if_model_exists_in_json(model_name):
        table = get_headers_tabulated_table(model_name)
        table.extend(get_model_data_table(model_name, from_id, to_id))
        return tabulate(table)
    return False

def get_mass_in_kilograms(model_name, x, y, z, mass_column_name, db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT {} FROM {} WHERE x = {} AND y = {} AND z = {}".format(mass_column_name, model_name, x, y, z))
    mass_in_tons = cursor.fetchone()
    if mass_in_tons is not None:
        return mass_in_tons[0] * 1000
    return False

def get_available_models():
    models = get_models_information_json()
    models_names = models.keys()
    return list(models_names)

def get_number_of_blocks_in_model(block_model_name, db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT COUNT(*) FROM {}".format(block_model_name))
    return cursor.fetchall()[0][0]

def get_attribute_from_block(block_model_name, x, y, z, attribute, db_name = DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.execute("SELECT {} from {} WHERE x = {} AND y = {} AND z = {}".format(attribute, block_model_name, x, y, z))
    requested_attributed = cursor.fetchone()
    if requested_attributed is not None:
        return requested_attributed
    return False