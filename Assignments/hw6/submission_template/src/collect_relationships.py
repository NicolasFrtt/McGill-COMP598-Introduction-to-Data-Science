import requests
import json
import os, sys
from bs4 import BeautifulSoup

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

url1 = "https://www.whosdatedwho.com/dating/the-weeknd"
url2 = "https://www.whosdatedwho.com/dating/selena-gomez"

input_file = sys.argv[2]
output_file = sys.argv[4]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def check_exists(file_name):
    # if the file does not exit, then get the data from url
    if not os.path.exists(file_name):
        print(f"File {file_name} not found.\n")
        return -1
    else:
        return 0


def create_url(star):
    temp = "https://www.whosdatedwho.com/dating/" + star
    return temp


def cache_new(cache_name, star):
    if not os.path.exists(cache_name):
        print(f"Writing to {cache_name}.\n")
        # get url
        url = create_url(star)
        html_text = requests.get(url=url).text
        # using errors = "ignore" because my computer doesn't accept some characters, even in utf-8
        # it works on other computers though... so just to make sure
        with open(cache_name, 'w', errors="ignore") as fh:
            fh.write(html_text)
        return 0
    else:
        print(f"Cache {cache_name} already exists.\n")
        return 1


def get_relationships(star, cache_dir):
    cache_name = cache_dir + '/' + star + ".txt"
    # check if already written in cache directory
    cache_new(cache_name, star)

    # once created (or if already existed), access the cache
    f = open(cache_name, 'r')
    soup = BeautifulSoup(f, 'html.parser')
    f.close()

    # get all 'p' tags that are in the 'h4' chunk with class 'ff-auto-relationships'

    all_p_tags = soup.find('h4', class_='ff-auto-relationships').find_next_siblings('p')

    # iterate through the p tags, in order to keep only those that are under the "Relationships" title
    list_of_relationships = []
    for elem in all_p_tags:
        if elem.previous.string == "Relationships":
            # get all 'a' tags
            all_a_tags = elem.find_all('a')
            for a_tag in all_a_tags:
                # avoid duplicates
                if a_tag in list_of_relationships:
                    continue
                # get a relationship (using split, since original format is /dating/star-name)
                relationship = a_tag["href"].split("/")[2]
                list_of_relationships.append(relationship)

    return list_of_relationships

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():
    # check if input exists
    if check_exists(input_file) == -1:
        return -1

    # get the input data
    print(f"Reading {input_file}\n")
    fh = open(input_file, 'r')
    input_json = json.load(fh)
    fh.close()

    # get cache directory
    cache_dir = input_json["cache_dir"]
    cache_dir = os.path.abspath(cache_dir)
    # get list of urls based on list of names
    list_star_names = input_json["target_people"]

    # get relationships for each star and add in the output file
    output_json = dict()
    for star in list_star_names:
        output_json[star] = get_relationships(star, cache_dir)

    with open(output_file, "w") as fh:
        json.dump(output_json, fh)

    return 0


if __name__ == '__main__':
    main()



