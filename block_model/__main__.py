import sys
import block_model_proccesor
import CLI
import json 
import os
import load_block_model

from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME

def check_neccesary_files_existence():
    if not os.path.isfile(LOADED_MODELS_INFORMATION_FILE_NAME):
        with open(LOADED_MODELS_INFORMATION_FILE_NAME, "w+") as f:
            json.dump({}, f, sort_keys=True)
    if not os.path.isfile(DB_NAME):
        load_block_model.create_db()

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    check_neccesary_files_existence()
    CLI.main_menu()
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()