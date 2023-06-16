import requests
import json
import os
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# urls for sample 1
URL_funny = "https://www.reddit.com/r/funny/new.json?limit=100"
URL_AskReddit = "https://www.reddit.com/r/AskReddit/new.json?limit=100"
URL_gaming = "https://www.reddit.com/r/gaming/new.json?limit=100"
URL_aww = "https://www.reddit.com/r/aww/new.json?limit=100"
URL_pics = "https://www.reddit.com/r/pics/new.json?limit=100"
URL_Music = "https://www.reddit.com/r/Music/new.json?limit=100"
URL_science = "https://www.reddit.com/r/science/new.json?limit=100"
URL_worldnews = "https://www.reddit.com/r/worldnews/new.json?limit=100"
URL_videos = "https://www.reddit.com/r/videos/new.json?limit=100"
URL_todayilearned = "https://www.reddit.com/r/todayilearned/new.json?limit=100"

# additional urls for sample 2
URL_memes = "https://www.reddit.com/r/memes/new.json?limit=100"
URL_politics = "https://www.reddit.com/r/politics/new.json?limit=100"
URL_nfl = "https://www.reddit.com/r/nfl/new.json?limit=100"
URL_nba = "https://www.reddit.com/r/nba/new.json?limit=100"
URL_wallstreetbets = "https://www.reddit.com/r/wallstreetbets/new.json?limit=100"
URL_teenagers = "https://www.reddit.com/r/teenagers/new.json?limit=100"
URL_PublicFreakout = "https://www.reddit.com/r/PublicFreakout/new.json?limit=100"
URL_leagueoflegends = "https://www.reddit.com/r/leagueoflegends/new.json?limit=100"
URL_unpopularopinion = "https://www.reddit.com/r/unpopularopinion /new.json?limit=100"

# lists of urls
list_URL_subsribers = [URL_funny, URL_AskReddit, URL_gaming, URL_aww, URL_pics, URL_Music, URL_science, URL_worldnews,
                       URL_videos, URL_todayilearned]
list_URL_postsbyday = [URL_AskReddit, URL_memes, URL_politics, URL_nfl, URL_nba, URL_wallstreetbets, URL_teenagers,
                       URL_PublicFreakout, URL_leagueoflegends, URL_unpopularopinion]


# cache files for sample 1
CACHE_FILE_funny = "reddit_data_funny.json"
CACHE_FILE_AskReddit = "reddit_data_AskReddit.json"
CACHE_FILE_gamming = "reddit_data_gamming.json"
CACHE_FILE_aww = "reddit_data_aww.json"
CACHE_FILE_pics = "reddit_data_pics.json"
CACHE_FILE_Music = "reddit_data_Music.json"
CACHE_FILE_science = "reddit_data_science.json"
CACHE_FILE_worldnews = "reddit_data_worldnews.json"
CACHE_FILE_videos = "reddit_data_videos.json"
CACHE_FILE_todayilearned = "reddit_data_todayilearned.json"

# additional cache files for sample 2
CACHE_FILE_memes = "reddit_data_memes.json"
CACHE_FILE_politics = "reddit_data_politics.json"
CACHE_FILE_nfl = "reddit_data_nfl.json"
CACHE_FILE_nba = "reddit_data_nba.json"
CACHE_FILE_wallstreetbets = "reddit_data_wallstreetbets.json"
CACHE_FILE_teenagers = "reddit_data_teenagers.json"
CACHE_FILE_PublicFreakout = "reddit_data_PublicFreakout.json"
CACHE_FILE_leagueoflegends = "reddit_data_leagueoflegends.json"
CACHE_FILE_unpopularopinion = "reddit_data_unpopularopinion.json"

# lists of caches
list_CACHE_subscribers = [CACHE_FILE_funny, CACHE_FILE_AskReddit, CACHE_FILE_gamming, CACHE_FILE_aww, CACHE_FILE_pics,
                          CACHE_FILE_Music, CACHE_FILE_science, CACHE_FILE_worldnews, CACHE_FILE_videos,
                          CACHE_FILE_todayilearned]
list_CACHE_postsbyday = [CACHE_FILE_AskReddit, CACHE_FILE_memes, CACHE_FILE_politics, CACHE_FILE_nfl, CACHE_FILE_nba,
                         CACHE_FILE_wallstreetbets, CACHE_FILE_teenagers, CACHE_FILE_leagueoflegends,
                         CACHE_FILE_unpopularopinion]

# output files
output_sample_1 = "sample1.json"
output_sample_2 = "sample2.json"

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


def write_posts(output_name, list_files):
    # add lists of posts to a temporary list
    temp_list_posts = []
    for file in list_files:
        print(f"\nReading {file}")
        with open(file, 'r') as fh:
            print(f'Loading from {file}\n')
            root_element = json.load(fh)
            posts = root_element["data"]["children"]
            temp_list_posts.append(posts)
    # add each individual post to the file
    fh2 = open(output_name, 'w')
    print(f"\nWriting posts to file {output_name}\n")
    for elem in temp_list_posts:
        for post in elem:
            json.dump(post, fh2)
            fh2.write("\n")
    fh2.close()
    return 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def main():

    # load json in caches, so that we need only one call

    # sample 1
    for cache, url in zip(list_CACHE_subscribers, list_URL_subsribers):
        check_exists(cache, url)
    # sample 2
    for cache, url in zip(list_CACHE_postsbyday, list_URL_postsbyday):
        check_exists(cache, url)

    # now collect posts only, and store them all in a single file for each sample

    # sample 1
    write_posts(output_sample_1, list_CACHE_subscribers)
    # sample 2
    write_posts(output_sample_2, list_CACHE_postsbyday)
    print("\n")

    return 0


if __name__ == '__main__':
    main()


