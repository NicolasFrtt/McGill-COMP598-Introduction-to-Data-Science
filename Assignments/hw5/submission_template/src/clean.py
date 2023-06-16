import ast
import json
from dateutil import parser
import datetime
import pytz
import sys

# --------------------- HELPER FUNCTIONS --------------------- #


def title_helper(line):
    # check if there is either a title or a title_text field
    if (("title" not in line) and ("title_text" not in line)) or (("title" in line) and ("title_text" in line)):
        return False
    return True


def date_helper(line):
    if "createdAt" in line:
        try:
            line["createdAt"] = parser.parse(line["createdAt"])
            line["createdAt"] = line["createdAt"].astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return False
    return True


def author_helper(line):
    if "author" in line:
        if (line["author"] is None) or (line["author"] == "N/A") or (line["author"] == ""):
            return False
    return True


def total_count_helper(line):
    try:
        # note that the int type casting works only with int, float and strings,
        # so this line also serves as a type check
        line["total_count"] = int(line["total_count"])
    except:
        # if didn't work AND did have a total_count field, remove
        if "total_count" in line:
            return False
    return True


def tags_helper(line):
    # split tags that contain a space
    if "tags" in line:
        temp_list = []
        for tag in line["tags"]:
            tagList = tag.split(" ")
            for tag_nospace in tagList:
                temp_list.append(tag_nospace)
        line["tags"] = temp_list
        return len(line["tags"])
    return -1


def valid_format_helper(line):
    try:
        temp = json.loads(line)
    except:
        return False
    return temp

# ------------------------------------------------------------ #



def main():

    input_file = sys.argv[2]
    output_file = sys.argv[4]

    input_data = open(input_file, 'r')
    # get a list of strings where every entry is a line
    lines_list_str = input_data.readlines()

    # list to isolate valid format
    lines_list_valid = []

    # check for valid format and keep only valid json lines
    for line in lines_list_str:
        temp = valid_format_helper(line)
        if temp is False:
            continue
        lines_list_valid.append(temp)

    # lines_list_valid_toRemove = []

    new_list_final = []
    # iterate through elements to apply modifications:
    for line in lines_list_valid:

        # check if there is either a title or a title_text field
        if title_helper(line) is False:
            # lines_list_valid_toRemove.append(line)
            continue

        # rename title_text as title
        if "title_text" in line:
            temp = line.pop("title_text")
            line["title"] = temp

        # remove wrong date formats using the try catch and convert to UTC time
        if date_helper(line) is False:
            # lines_list_valid_toRemove.append(line)
            continue

        # remove author that are empty, null, or N/A
        if author_helper(line) is False:
            # lines_list_valid_toRemove.append(line)
            continue

        # remove posts with bad type for total_count, or parse it if possible
        if total_count_helper(line) is False:
            # lines_list_valid_toRemove.append(line)
            continue

        # split tags that contain a space
        tags_helper(line)

        new_list_final.append(line)

    '''
    used for a previous implementation that ended up being too complex
    
    lines_list_valid_copyStr = []
    for x in lines_list_valid:
        temp = str(x)
        lines_list_valid_copyStr.append(temp)

    lines_list_valid__toRemove_copyStr = []
    for x in lines_list_valid_toRemove:
        temp = str(x)
        lines_list_valid__toRemove_copyStr.append(temp)

    finalList = list(set(lines_list_valid_copyStr) - set(lines_list_valid__toRemove_copyStr))

    '''

    output_file_write = open(output_file, "w")
    for elem in new_list_final:
        # elem = "{0}".format(elem)
        # elem_json = json.loads(elem)
        json.dump(elem, output_file_write)
        output_file_write.write("\n")
    output_file_write.close()


if __name__ == "__main__":
    main()










