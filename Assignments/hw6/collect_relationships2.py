# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import sys
import os


def checkstarexists(cachedir, star):
    if os.path.exists(cachedir + "/" + star + ".json"):
        return True
    elif os.path.exists(cachedir) == False:
        os.mkdir(cachedir)
    return False


def getlistofdates(star, url):
    if url == -1:
        url = requests.get(url="https://www.whosdatedwho.com/dating/" + star).text
    soup = BeautifulSoup(url, 'html.parser')
    relations = soup.find("h4", class_="ff-auto-relationships").find_next_siblings("p")
    dated_stars = []
    for relation in relations:
        if relation.previous.string == "About":
            break
        for s in relation.find_all("a"):
            temp_star = s["href"].split("/")[2]
            dated_stars.append(temp_star)

    return dated_stars


def main():
    input_file = sys.argv[2]
    output_file = sys.argv[4]

    data = json.load(open(input_file, 'r'))
    new = dict()

    for star in data["target_people"]:
        if checkstarexists(data["cache_dir"], star):
            new[star] = getlistofdates(star, open(data["cache_dir"] + "/" + star + ".json", "r"))

        else:
            new[star] = getlistofdates(star, -1)
            star_file = open(data["cache_dir"] + "/" + star + ".json", "w")
            print(f"Writing to file {star}")
            star_file.write(requests.get(url="https://www.whosdatedwho.com/dating/" + star).text)
            star_file.close()

    output_file = open(output_file, "w")
    json.dump(new, output_file)
    output_file.close()


if __name__ == "__main__":
    main()