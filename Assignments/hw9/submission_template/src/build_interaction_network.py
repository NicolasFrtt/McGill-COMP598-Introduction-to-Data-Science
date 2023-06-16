import os
import sys
import argparse
import pandas as pd
import numpy as np
import json

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# urls

# output file


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def check_exists(file_name):
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.\n")
        return -1
    else:
        return 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def main():
    # get input from command
    parser = argparse.ArgumentParser("collect")
    parser.add_argument("-i", help="csv", type=str, required=True)
    parser.add_argument("-o", help="output_file", type=str, required=True)
    args = parser.parse_args()

    input_file = args.i
    output_file = args.o

    # check if input exists
    if check_exists(input_file) == -1:
        return -1

    # check if the output directory exists, and create it if it does not
    output_dir = output_file
    # if path is not absolute then add "./"
    if not os.path.isabs(output_file):
        output_dir = "./" + output_file
    if not os.path.exists(os.path.dirname(output_dir)):
        print(f"Creating directory {os.path.dirname(output_dir)}")
        try:
            os.makedirs(os.path.dirname(output_dir))
        except:  # Guard against race condition
            print(f"Error while trying to create directory.")
            return -1

    # read input csv
    df = pd.read_csv(input_file)

    # set pony names to lower case
    df['pony'] = df['pony'].str.lower()

    # We will create a new copy df that will help us get the 101 most frequent characters.
    # We don't want to remove the list of not wanted names from the original df,
    # since we will need them to identify which pony talks to those not wanted names
    df_copy = df
    # remove not wanted words from pony names in the copy
    for word in ["others", "ponies", "and", "all"]:
        df_copy = df_copy[~df_copy['pony'].str.contains(word)]
    # count the number of each name
    most_freq = df_copy['pony'].value_counts()
    # only keep the 101 most frequent (already sorted), and only keep the index (i.e. the names, not the count)
    most_freq = most_freq[:101].index.tolist()

    # use shift to assign each pony with its interlocutor
    df["assigned_pony"] = df['pony'].shift(-1)

    # do the same with the episode names, to help identify when we change episode
    df["next_episode"] = df['title'].shift(-1)

    # remove interactions not in top101 (and thus also those with the not wanted words, since they're not in top101!)
    df.loc[~df["assigned_pony"].isin(most_freq) | ~df["pony"].isin(most_freq), "assigned_pony"] = "0"

    # remove self-interactions and interactions between episodes
    df = df[(df['pony'] != df["assigned_pony"]) & (df['title'] == df["next_episode"]) & (df["assigned_pony"] != "0")]

    # create new columns where we get both interlocutors, sorted. This will help us identifying the interactions later.
    df["list_of_interlocutors"] = df.apply(lambda x: list([x["pony"], x["assigned_pony"]]), axis=1)
    for interlocutor in df["list_of_interlocutors"]:
        interlocutor = interlocutor.sort()

    # keep only the columns we are interested in, i.e. the two interlocutors
    df = pd.DataFrame(df["list_of_interlocutors"].tolist(), columns=["pony1", "pony2"])

    # count the interactions between the two ponies
    df = df.groupby(["pony1", "pony2"]).size().rename("interactions_counter").reset_index()
    # sort in descending order
    df = df.sort_values(by='interactions_counter', ascending=False)

    # create the output dictionary
    output_json = {}
    # for each pony in "pony1", add the list of interactions with other ponies from "pony2"
    for pony in df["pony1"]:
        df_temp = df[df["pony1"] == pony]
        output_json[pony] = dict(zip(df_temp["pony2"], df_temp["interactions_counter"]))

    # for each pony in "pony2", add the list of interactions with other ponies from "pony1"
    for ponyy in df["pony2"]:
        df_temp = df[df["pony2"] == ponyy]
        temp = dict(zip(df_temp["pony1"], df_temp["interactions_counter"]))
        # if pony already had some interactions, then add those new
        if ponyy in output_json:
            output_json[ponyy] = {**output_json[ponyy], **temp}
        # otherwise, add this pony with corresponding interactions
        else:
            output_json[ponyy] = temp

    # write the output dictionary into the output file
    final_json = json.dumps(output_json, indent=4)
    with open(output_file, "w") as f:
        f.write(final_json)

    return 0


if __name__ == '__main__':
    main()

