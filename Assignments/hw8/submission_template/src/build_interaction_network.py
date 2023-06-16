import os
import sys
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

    csv_file = args.i
    output_file = args.o

    # check if input exists
    if check_exists(csv_file) == -1:
        return -1

    # check if the output directory exists, and create it if it does not
    output_dir = "./" + output_file
    if not os.path.exists(os.path.dirname(output_dir)):
        print(f"Creating directory {os.path.dirname(output_dir)}")
        try:
            os.makedirs(os.path.dirname(output_dir))
        except:  # Guard against race condition
            print(f"Error while trying to create directory.")
            return -1

    # Read csv and set pony names to lower case
    df = pd.read_csv(input_file)
    df['pony'] = df['pony'].str.lower()

    # Only keep most occuring characters (101)
    df_oc = df
    for i in ["others","pony","and","all"]:
        df_oc = df_oc[~df_oc['pony'].str.contains(i)]
    most_occuring = df_oc["pony"].value_counts()[:101].index.tolist()

    # Get next pony and next episode name
    df["interlocutor"] = df['pony'].shift(-1)
    df["nexttitle"] = df['title'].shift(-1)

    # Remove the not wanted interactions
    df.loc[~df["interlocutor"].isin(most_occuring) | ~df["pony"].isin(most_occuring), "interlocutor"] = "NO"

    # Remove pony talking to himself and remove last from each episode
    df = df[(df['pony'] != df["interlocutor"]) & (df['title'] == df["nexttitle"]) & (df["interlocutor"] != "NO")]

    # put the interactors in a alist
    df["list_of_interaction"] = df.apply(lambda x: list([x["pony"],x["interlocutor"]]),axis=1)

    # Sort the list and expand it backand get count of each interaction
    for i in df["list_of_interaction"]:i = i.sort()
    df = pd.DataFrame(df["list_of_interaction"].tolist(), columns=["pony1","pony2"])
    df = df.groupby(["pony1","pony2"]).size().rename("n_interactions").reset_index()
    df = df.sort_values(by='n_interactions', ascending=False)

    data = {}
    for i in df["pony1"]:
        df1 = df[df["pony1"] == i]
        temp_dict = dict(zip(df1["pony2"],df1["n_interactions"]))
        data[i] = temp_dict

    for i in df["pony2"]:
        df1 = df[df["pony2"] == i]
        temp_dict = dict(zip(df1["pony1"],df1["n_interactions"]))
        if i in data: data[i] = {**data[i], **temp_dict}
        else:data[i] = temp_dict

    json_object = json.dumps(data, indent = 4)
    with open(output_file, "w") as outfile:
        outfile.write(json_object)

    return 0


if __name__ == '__main__':
    main()

