import json
import os
import sys
import random
import argparse

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# inputs
#input_file = sys.argv[3]
#num_posts_to_output_str = sys.argv[4]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def check_exists(file_name):
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.\n")
        return -1
    else:
        return 0


def write_name_and_title_tsv(output, list_post):
    with open(output, 'w', encoding='utf-8') as fh2:
        fh2.write("Name\ttitle\tcoding\n")
        for post in list_post:
            name = post['data']['name']
            title = post['data']['title']
            fh2.write(name)
            fh2.write("\t")
            fh2.write(title)
            fh2.write("\t\n")
    return 0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    parser = argparse.ArgumentParser("extract")
    parser.add_argument("-o", help="output_file", type=str, required=True)
    parser.add_argument("input", help="input_file", type=str)
    parser.add_argument("numPost", help="num_posts_to_output", type=int)
    args = parser.parse_args()

    output_file = args.o
    input_file = args.input
    num_posts_to_output = args.numPost

    # check if num_of_posts is an integer
    #try:
    #    num_posts_to_output = int(num_posts_to_output_str)
    #except:
    #    print(f"num_posts_to_output should be an integer.")
    #    return -1

    # check if output directory exists, and if not create it
    output_dir = "./" + output_file
    if not os.path.exists(os.path.dirname(output_dir)):
        print(f"Creating directory {os.path.dirname(output_dir)}")
        try:
            os.makedirs(os.path.dirname(output_dir))
        except:  # Guard against race condition
            print(f"Error while trying to create directory.")
            return -1

    # check if input file exists
    if check_exists(input_file) == -1:
        return -1

    # get a list of posts
    list_posts = []
    print(f"Reading {input_file}")
    with open(input_file, 'r') as fh:
        print(f'Loading from {input_file}\n')
        for line in fh:
            list_posts.append(json.loads(line))

    # get random posts from list of posts
    if num_posts_to_output >= len(list_posts):
        write_name_and_title_tsv(output_file, list_posts)
    else:
        random_posts = random.sample(list_posts, num_posts_to_output)
        write_name_and_title_tsv(output_file, random_posts)

    return 0


if __name__ == '__main__':
    main()

