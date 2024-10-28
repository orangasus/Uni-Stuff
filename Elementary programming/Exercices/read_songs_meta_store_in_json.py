import json
import os
import sys

import tinytag


def pull_song_metadat(music_file):
    tag = tinytag.TinyTag.get(f"{PATH_TO_MUSIC}/{music_file}")
    return {"Artist": tag.artist, "Title": tag.title, "Year": tag.year, "Duration": tag.duration}


def read_user_input():
    try:
        a, b = sys.argv[1], sys.argv[2]
        return a, b
    except Exception as e:
        print(f"Something went wrong: {e}")
        return "./resources/Music", "./resources/results.json"


PATH_TO_MUSIC, FILE_NAME = read_user_input()
list_of_song_data = []
for music_file in os.listdir(PATH_TO_MUSIC):
    list_of_song_data.append(pull_song_metadat(music_file))
with open(FILE_NAME, 'w') as handler:
    json.dump(list_of_song_data, handler)
with open(FILE_NAME, 'r') as handler:
    results = json.load(handler)
    for el in results:
        print(el)
