import requests
import json
import os
import sys
import argparse

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# urls
# URL_McGill = "https://www.reddit.com/r/mcgill/new.json?limit=100"
# URL_Concordia = "https://www.reddit.com/r/concordia/new.json?limit=100"
# subreddit = sys.argv[4]


# cache files
CACHE_FILE_McGill = "reddit_data_McGill.json"
CACHE_FILE_Concordia = "reddit_data_Concordia.json"


# output file
# output_file = sys.argv[2]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def check_exists(cache_name, url):
    # if the cache does not exit, then get the data from url
    if not os.path.exists(cache_name):
        print(f"Writing to {cache_name}.\n")
        r = requests.get(url, headers={'User-agent': 'Chrome'})
        root_element = r.json()
        with open(cache_name, 'w') as fh:
            json.dump(root_element, fh)
        return 0
    else:
        print(f"Cache {cache_name} already exists.\n")
        return 1


def write_posts(output_name, file):
    # select list of posts
    print(f"\nReading {file}")
    with open(file, 'r') as fh:
        print(f'Loading from {file}\n')
        root_element = json.load(fh)
        posts = root_element["data"]["children"]
    # add each individual post to the file
    fh2 = open(output_name, 'w')
    print(f"\nWriting posts to file {output_name}\n")
    for post in posts:
        json.dump(post, fh2)
        fh2.write("\n")
    fh2.close()
    return 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    parser = argparse.ArgumentParser("collect")
    parser.add_argument("-s", help="subreddit", type=str, required=True)
    parser.add_argument("-o", help="output_file", type=str, required=True)
    args = parser.parse_args()

    subreddit = args.s
    output_file = args.o
    url = "https://www.reddit.com" + subreddit + "/new.json?limit=100"

    # check if the directory exists, and create it if it does not

    output_dir = "./" + output_file
    if not os.path.exists(os.path.dirname(output_dir)):
        print(f"Creating directory {os.path.dirname(output_dir)}")
        try:
            os.makedirs(os.path.dirname(output_dir))
        except:  # Guard against race condition
            print(f"Error while trying to create directory.")
            return -1

    # load json in caches, so that we need only one call
    # then collect posts only, and store them all in a single file

    if "mcgill" in url.lower():
        check_exists(CACHE_FILE_McGill, url)
        write_posts(output_file, CACHE_FILE_McGill)
    elif "concordia" in url.lower():
        check_exists(CACHE_FILE_Concordia, url)
        write_posts(output_file, CACHE_FILE_Concordia)
    else:  # case for other inputs
        r = requests.get(url, headers={'User-agent': 'Chrome'})
        root_element = r.json()
        posts = root_element["data"]["children"]
        fh2 = open(output_name, 'w')
        print(f"\nWriting posts to file {output_name}\n")
        for post in posts:
            json.dump(post, fh2)
            fh2.write("\n")
        fh2.close()

    print("\n")

    return 0


if __name__ == '__main__':
    main()

