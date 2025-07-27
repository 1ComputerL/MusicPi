# This program navigates to a media directory and generates a JSON structure of the directory readable by music_system.py to play the media files provided
# It is run by music_system.py
# Created by AI with instructions and code from ComputerL

### IMPORTS ###
# import standard libraries
import os
import sys
import json
import logging
import json
import re

# import mutagen for mp3 metadata
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

### PATH SETUP ###
# get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))

# add the MusicPi directory to the system path
sys.path.append(parentdir)

### LOGGING SETUP ###
# configure logging
log = logging.getLogger('generate_albums_json')
logging.basicConfig(filename=parentdir + '/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

### FUNCTION DEFINITIONS ###

# get artist name from mp3 metadata
def get_artist_from_mp3(file_path):
    try:
        audio = EasyID3(file_path)
        return audio.get('artist', ['Unknown Artist'])[0]
    except (ID3NoHeaderError, KeyError):
        return "Unknown Artist"

# clean the name of the file
def clean(name):
    cleaned = re.sub(r'\.[^.\\/:*?"<>|\s]+$', '', name)
    cleaned = re.sub(r'^\d{2}\.\s', '', cleaned)
    return cleaned

# build folder structure recursively
def build_folder_structure(path):
    folder_name = os.path.basename(path)
    full_path = os.path.abspath(path)
    subdirs = [d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))]
    files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

    # sort key to sort numerically if possible
    def custom_sort_key(name):
        match = re.match(r'^\D*(\d+)', name)
        if match:
            return (int(match.group(1)), name.lower())
        return (float('inf'), name.lower())

    # sort files and directories
    files.sort(key=custom_sort_key)
    subdirs.sort(key=custom_sort_key)

    # build node dictionary
    node = {
        "title": clean(folder_name),
        "items": {}
    }

    # add play all option
    node["items"]["0"] = {
        "title": "Play All",
        "action": {
            "do": "mpv",
            "path": full_path
        }
    }

    # add files to the node
    for idx, file in enumerate(files):
        file_path = os.path.join(full_path, file)
        artist_name = "Unknown Artist"

        if file.lower().endswith('.mp3'):
            artist_name = get_artist_from_mp3(file_path)

        node["items"][str(idx + 1)] = {
            "title": clean(file),
            "artist": artist_name,
            "action": {
                "do": "mpv",
                "path": file_path
            }
        }

    # add subdirectories recursively
    for idx, subdir in enumerate(subdirs):
        sub_path = os.path.join(full_path, subdir)
        node["items"][str(len(files) + idx + 1)] = build_folder_structure(sub_path)

    return node

### MAIN CODE SECTION ###
# load media directory from settings
if __name__ == "__main__":
    with open('settings.json', 'r') as file:
        data = json.load(file)
    root_dir = data["mediaDir"]
    tree = build_folder_structure(root_dir)

    # set path to menus.json
    menus_file = os.path.join(parentdir, "menus.json")

    # try to load existing menus.json
    try:
        with open(menus_file, "r", encoding='utf-8') as f:
            menus_data = json.load(f)
    except FileNotFoundError:
        log.warning(f"menus.json not found at {menus_file}. Creating a new one.")
        menus_data = {
            "0": {
                "title": "Main Menu",
                "items": {
                    "0": {
                        "title": tree["title"],
                        "items": tree["items"]
                    }
                }
            }
        }
        with open(menus_file, "w", encoding='utf-8') as f:
            json.dump(menus_data, f, indent=4)
        log.info(f"Created new menus.json with structure from {root_dir}.")
    else:
        # try to update existing menus.json
        try:
            menus_data["0"]["items"]["0"]["items"] = tree["items"]
            menus_data["0"]["items"]["0"]["title"] = tree["title"]

            with open(menus_file, "w", encoding='utf-8') as f:
                json.dump(menus_data, f, indent=4)

            log.info(f"Successfully updated menus.json with the new structure from {root_dir}.")
        except KeyError as e:
            log.error(f"KeyError while updating menus.json: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")