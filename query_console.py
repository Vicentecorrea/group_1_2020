import load_block_model
import os
import block_model_proccesor
import re

from constants import CONTINUE_SHOWING_OPTIONS, QUERY_CONSOLE_OPTIONS, ENTER_COLUMNS_OPTIONS, MAIN_MANU_VALID_OPTIONS, QUERY_MENU_VALID_OPTIONS

def main_menu():
    while True:
        print("What do you want to do\n"
              "(1) Load block file\n"
              "(2) Open query console\n"
              "(0) Exit")

        user_input = input("Option number: ")

        while user_input not in MAIN_MANU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == MAIN_MANU_VALID_OPTIONS[0]:
            exit(0)
        elif user_input == MAIN_MANU_VALID_OPTIONS[1]:
            enter_block_model_information()
        elif user_input == MAIN_MANU_VALID_OPTIONS[2]:
            if len(block_model_proccesor.get_available_models()) > 0:
                query_console()
            else:
                print("There are no available models")


def query_console():
    while True:
        print("What do you want to see")
        user_input = show_options_from_list_and_get_user_input(QUERY_CONSOLE_OPTIONS, is_menu=True)
        while user_input not in QUERY_MENU_VALID_OPTIONS:
            user_input = input("Choose a valid option: ")

        if user_input == QUERY_MENU_VALID_OPTIONS[0]:
            return
        block_model_name = get_model_name_to_work_with()

        if user_input == QUERY_MENU_VALID_OPTIONS[1]:
            show_blocks_in_model(block_model_name)
        elif user_input == QUERY_MENU_VALID_OPTIONS[2]:
            show_number_of_blocks_in_model(block_model_name)
        elif user_input == QUERY_MENU_VALID_OPTIONS[3]:
            show_mass_of_block(block_model_name)
        elif user_input == QUERY_MENU_VALID_OPTIONS[5]:
            show_attribute_of_block(block_model_name)
            return


def show_options_from_list_and_get_user_input(data_to_show, is_menu=False):
    valid_options = list(map(str, range(len(data_to_show))))
    if is_menu:
        for count, model_name in enumerate(data_to_show[:-1], start=1):
            print("({}) {}".format(count, model_name))
        print("(0) {}".format(data_to_show[-1]))
    else:
        for count, model_name in enumerate(data_to_show, start=0):
            print("({}) {}".format(count, model_name))
    user_input = ""
    while user_input not in valid_options:
        user_input = input("Choose your option number: ")
    return user_input


def check_block_model_file_existence(file_name):
    return os.path.isfile(file_name)


def enter_block_model_information():
    block_model_file_path = input("Enter file path: ")

    if not check_block_model_file_existence(block_model_file_path):
        print("FILE NOT FOUND")
        return
    table_columns = []
    model_has_id = input("The dataset has identification column?(y/n):")
    while model_has_id not in CONTINUE_SHOWING_OPTIONS:
        model_has_id = input("The dataset has identification column?(y/n): ")
    model_has_id = True if model_has_id == "y" else False
    if not model_has_id:
        table_columns.append("id")

    user_input = input("How many columns does the model have: ")
    while not user_input.isdigit():
        user_input = input("Enter a valid option. How many columns does the model have:")
    print("Enter columns one by one(Only alphabetic characters)")
    for _ in range(int(user_input)):
        column_name = input("Enter column name: ")
        while not column_name.isalpha():
            column_name = input("Enter a valid column name(Only alphabetic characters): ")
        table_columns.append(column_name)
    # TODO: Make the user capable of re insert column names
    load_block_model.load_block_file(block_model_file_path, table_columns, model_has_id)







def get_model_name_to_work_with():
    print("In which model? ")
    available_block_models = block_model_proccesor.get_available_models()
    block_model_index = show_options_from_list_and_get_user_input(available_block_models)

    return available_block_models[int(block_model_index)]


def show_blocks_in_model(model_name_to_work_with):
    continue_user_input = "y"
    index_to_show = 0
    while continue_user_input == "y":
        print(block_model_proccesor.get_tabulated_blocks(model_name_to_work_with, index_to_show, index_to_show + 50))
        index_to_show += 51
        continue_user_input = input("Continue showing data(y/n): ").lower()
        while continue_user_input not in CONTINUE_SHOWING_OPTIONS:
            continue_user_input = input("Continue showing data(y/n): ").lower()


def show_number_of_blocks_in_model(block_model_name):
    number_of_blocks = block_model_proccesor.get_number_of_blocks_in_model(block_model_name)
    print("{} has {} blocks".format(block_model_name, number_of_blocks))


def check_valid_coordinates(coordinates):
    coordinates = coordinates.replace("-", "").strip().split(" ")
    if len(list(filter(lambda x: x.isdigit(), coordinates))) == len(coordinates) == 3:
        return True
    return False


def get_coordinates_from_user():
    coordinates = input("Enter coordinates separated by space(x y z): ")
    while not check_valid_coordinates(coordinates):
        coordinates = input("Enter valid coordinates(x y z): ")
    x, y, z = coordinates.strip().split(" ")
    return x, y, z


def show_mass_of_block(block_model_name):
    x, y, z = get_coordinates_from_user()
    block_model_columns = block_model_proccesor.get_block_model_columns(block_model_name)
    print("Select the column that represents the mass")
    mass_column_index = int(show_options_from_list_and_get_user_input(block_model_columns))
    mass_column_name = block_model_columns[mass_column_index]
    block_mass = block_model_proccesor.get_mass_in_kilograms(block_model_name, x, y, z, mass_column_name)
    if block_mass != False:
        print("Block in {} with coordinates {} {} {} has a mass of {} kilograms".format(block_model_name, x, y, z,
                                                                                        block_mass))
    else:
        print("Block in {} with coordinates {} {} {} does not exists".format(block_model_name, x, y, z))


def show_attribute_of_block(block_model_name):
    x, y, z = get_coordinates_from_user()
    block_model_columns = block_model_proccesor.get_block_model_columns(block_model_name)
    print("Which column do you want to see?")
    column_to_show_index = int(show_options_from_list_and_get_user_input(block_model_columns))
    column_to_show_name = block_model_columns[column_to_show_index]
    attribute = block_model_proccesor.get_attribute_from_block(block_model_name, x, y, z, column_to_show_name)
    if attribute != False:
        print("Block in {} with coordinates {} {} {}, attribute {} is {}".format(block_model_name, x, y, z,
                                                                                 column_to_show_name, attribute))
    else:
        print("Block in {} with coordinates {} {} {} does not exists".format(block_model_name, x, y, z))


