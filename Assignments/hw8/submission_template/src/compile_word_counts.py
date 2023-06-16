import json
import os
import sys
import argparse
import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# urls
# URL_McGill = "https://www.reddit.com/r/mcgill/new.json?limit=100"
# URL_Concordia = "https://www.reddit.com/r/concordia/new.json?limit=100"
# subreddit = sys.argv[4]


# output file
# output_file = sys.argv[2]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def check_exists(file_name):
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.\n")
        return -1
    else:
        return 0


def compute_word_counts(csv_file, stopwords_path):

    # get data, and set dialog and names to lower case
    df_dialog = pd.read_csv(csv_file)
    df_dialog['pony'] = df_dialog['pony'].str.lower()
    df_dialog['dialog'] = df_dialog['dialog'].str.lower()

    # only keep exact poney names
    poney_names = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    df_dialog = df_dialog[df_dialog['pony'].isin(poney_names)]

    # replace punctuation with " "
    df_dialog['dialog'] = df_dialog['dialog'].str.replace('[()\[\],-.?!:;#&]', ' ', regex=True)

    # get stopwords
    with open(stopwords_path, 'r') as f:
        stopwords = f.read().splitlines()
    stopwords = stopwords[6:]

    output_json = dict()

    # iterate through ponies:
    for pony in poney_names:
        # isolate pony dialog
        df_pony = df_dialog[df_dialog['pony'] == pony]
        # get list of all words by splitting on " "
        all_words = ' '.join(df_pony['dialog']).split(' ')
        # remove non alphabetic words and ""
        all_words_alpha = []
        for word in all_words:
            if word.isalpha():
                all_words_alpha.append(word)
        # for each word, create a new field inside words_dict,
        # except if word is in stopwords, or is already in words_dict (in which case add 1 to the counter)
        words_dict = {}
        for word in all_words_alpha:
            if word in stopwords:
                continue
            if word in words_dict:
                words_dict[word] = words_dict[word] + 1
            else:
                words_dict[word] = 1
        # keep only counts greater or equal to 5
        words_dict = dict((key, value) for key, value in words_dict.items() if value >= 5)
        # write the dictionary to the corresponding pony in the output dictionary
        output_json[pony] = words_dict
    return output_json

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def main():
    # get input from command
    parser = argparse.ArgumentParser("collect")
    parser.add_argument("-d", help="csv", type=str, required=True)
    parser.add_argument("-o", help="output_file", type=str, required=True)
    args = parser.parse_args()

    csv_file = args.d
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

    # get the stopwords path
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    stopwords_path = parent_dir + "/data/stopwords.txt"

    output_json = compute_word_counts(csv_file, stopwords_path)

    with open(output_file, 'w') as fh:
        json.dump(output_json, fh, indent=2)

    return 0


if __name__ == '__main__':
    main()
