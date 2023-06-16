import json
import os
import sys
import argparse
import math

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


def compute_lang(pony_count_f, num_words):
    # read file and get dictionary of pony word counts
    with open(pony_count_f, 'r') as f:
        pony_count = json.load(f)

    # get number of ponies
    number_ponies = len(pony_count)

    # define sub functions for tf-idf implementation
    def tf_idf(w, pony):
        return tf(w, pony) * idf(w)

    def tf(w, pony):
        try:
            temp = pony_count[pony][w]
            return temp
        except:
            print(f"Word {w} not found in input dictionary for pony {pony}.")
            return 0

    def idf(w):
        num_pony_use_w = 0
        for pon in pony_count.keys():
            if w in pony_count[pon]:
                num_pony_use_w = num_pony_use_w + 1
        return math.log(number_ponies/num_pony_use_w)

    # write to output dictionary for each pony
    output_json = dict()
    for pony in pony_count.keys():
        # iterate through every word, compute its tf-idf score and store it
        score_storage_dict = {}
        for w in pony_count[pony]:
            score = tf_idf(w, pony)
            score_storage_dict[w] = score
        # sort the scores and store them in a list
        score_sorted = sorted(score_storage_dict.values(), reverse=True)
        # keep only the num_words highest and add to the output dictionary
        output_json[pony] = score_sorted[0:num_words]

    return output_json

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    # get input from command
    parser = argparse.ArgumentParser("collect")
    parser.add_argument("-c", help="count", type=str, required=True)
    parser.add_argument("-n", help="num_words", type=int, required=True)
    args = parser.parse_args()

    count_file = args.c
    num_words = args.n

    # check if input exists
    if check_exists(count_file) == -1:
        return -1

    # get output dictionary
    output_json = compute_lang(count_file, num_words)

    # print result to stdout
    output_str = json.dumps(output_json, indent=4)
    print(output_str)

    return 0


if __name__ == '__main__':
    main()