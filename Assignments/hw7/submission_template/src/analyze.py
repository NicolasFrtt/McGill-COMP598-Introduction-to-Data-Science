import json
import os
import sys
import pandas as pd
import argparse

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# input files
# input_file = sys.argv[2]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def check_exists(file_name):
    # if the file does not exit, then get the data from url
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.\n")
        return -1
    else:
        return 0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    parser = argparse.ArgumentParser("analyze")
    parser.add_argument("-o", default="NO_OUTPUT_NO", help="output_file", type=str)
    parser.add_argument("-i", help="input_file", type=str, required=True)
    args = parser.parse_args()

    output_file = args.o
    input_file = args.i

    stdout = True

    # check if input file exists
    if check_exists(input_file) == -1:
        return -1

    # if output file, create the dir if it does not exist
    if "NO_OUTPUT_NO" not in output_file:
        stdout = False  # we have a file provided
        # check if output directory exists, and if not create it
        output_dir = "./" + output_file
        if not os.path.exists(os.path.dirname(output_dir)):
            print(f"Creating directory {os.path.dirname(output_dir)}.")
            try:
                os.makedirs(os.path.dirname(output_dir))
            except:  # Guard against race condition
                print(f"Error while trying to create directory.")
                return -1

    # read input file as data frame
    df = pd.read_csv(input_file, sep="\t")

    # sum the count of the different categories (i.e. the row length of the sub dfs)
    count_c = len((df[df["coding"] == "c"]).index)
    count_r = len((df[df["coding"] == "r"]).index)
    count_f = len((df[df["coding"] == "f"]).index)
    count_o = len((df[df["coding"] == "o"]).index)

    # create json output file
    json_output = dict()

    json_output["course-related"] = count_c
    json_output["food-related"] = count_f
    json_output["residence-related"] = count_r
    json_output["other"] = count_o

    if stdout:
        print(json_output)
    else:
        print(f"Writing to {output_file}.\n")
        with open(output_file, 'w', encoding='utf-8') as fh:
            json.dump(json_output, fh)

    return 0


if __name__ == '__main__':
    main()
