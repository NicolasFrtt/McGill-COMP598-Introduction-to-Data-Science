import json
import os
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# input files
input_file = sys.argv[1]
#input_sample_1 = "sample1.json"
#input_sample_2 = "sample2.json"

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

    if check_exists(input_file) == -1:
        return -1

    # get a list of posts
    list_posts = []
    print(f"Reading {input_file}")
    with open(input_file, 'r') as fh:
        print(f'Loading from {input_file}\n')
        for line in fh:
            list_posts.append(json.loads(line))

    # compute average of title length
    count = 0
    for post in list_posts:
        count = count + len(post['data']['title'])
    count = count/len(list_posts)

    print(f"The average post title length is {count}.")

    return count


if __name__ == '__main__':
    main()

