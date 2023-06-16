import os
import sys
import argparse
import pandas as pd
import numpy as np
import json
import networkx as nx

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
    parser.add_argument("-i", help="json", type=str, required=True)
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

        # open file
        with open(input_file, "r") as f:
            interactions_dict = json.load(f)

    # create nx object
    graph = nx.Graph()
    # for each pony, create a new node
    for pony1 in interactions_dict:
        graph.add_node(pony1)
        # compute sum of weight for each node
        weight_sum = 0
        # create edges and add weight of each edge for the current node
        for pony2 in interactions_dict[pony1]:
            # update sum of weight
            weight_sum = weight_sum + interactions_dict[pony1][pony2]
            # add weighted edge
            graph.add_edge(pony1, pony2, weight=interactions_dict[pony1][pony2])
        # store sum of weight for each pony
        graph.nodes[pony1]["sum_weight"] = weight_sum

    # get the 3 most weighted nodes of the graph, by sorting using the new attribute created above
    most_weight = sorted(graph, key=lambda x: graph.nodes[x]["sum_weight"], reverse=True)
    most_weight = most_weight[:3]
    # get the 3 nodes with most edges, by sorting using the getitem function that returns the list of neighbours
    most_number_edge = sorted(graph, key=lambda x: len(graph.__getitem__(x)), reverse=True)
    most_number_edge = most_number_edge[:3]
    # get the 3 most central ponies by betweenness, by sorting using the betweenness_centrality function
    betweenness_list = nx.betweenness_centrality(graph, weight="weight")
    most_central = sorted(betweenness_list, reverse=True, key=lambda x: betweenness_list[x])
    most_central = most_central[:3]

    # create the output dictionary
    output_json = dict()
    output_json["most_connected_by_num"] = most_number_edge
    output_json["most_connected_by_weight"] = most_weight
    output_json["most_central_by_betweenness"] = most_central

    # write the output dictionary into the output file
    final_json = json.dumps(output_json, indent=4)
    with open(output_file, "w") as fi:
        fi.write(final_json)

    return 0


if __name__ == '__main__':
    main()

