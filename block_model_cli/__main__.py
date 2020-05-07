import sys
import json
import CLI
import os
import load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, MINERAL_GRADES_INFORMATION_FILE_NAME


def check_neccesary_files_existence():
    if not os.path.isfile(LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile(DB_NAME):
        load_block_model.create_db()
    if not os.path.isfile(MINERAL_GRADES_INFORMATION_FILE_NAME):
        with open(MINERAL_GRADES_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    check_neccesary_files_existence()
    CLI.main_menu()


if __name__ == "__main__":
    main()
