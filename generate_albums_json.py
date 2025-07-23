import os
import sys
import json
import logging
import json
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

# Get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))
# Add the MusicPi directory to the system path
sys.path.append(parentdir)

# Logging setup
log = logging.getLogger('generate_albums_json')
logging.basicConfig(filename=parentdir + '/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_artist_from_mp3(file_path):
    """
    Extract the artist name from an MP3 file using mutagen.
    """
    try:
        audio = EasyID3(file_path)
        return audio.get('artist', ['Unknown Artist'])[0]
    except (ID3NoHeaderError, KeyError):
        return "Unknown Artist"

def clean(name):
    """
    Strips leading numeric prefixes like '01.', '1 ', '111.' from the string,
    and also removes .mp3 extension (case-insensitive) from the title.
    Examples:
      '01. Key.mp3' ? 'Key'
      '1 Key.MP3' ? 'Key'
      '111. Song name.Mp3' ? 'Song name'
    """
    cleaned = re.sub(r'\.[^.\\/:*?"<>|\s]+$', '', name)
    cleaned = re.sub(r'^\d{2}\.\s', '', cleaned)
    return cleaned

def build_folder_structure(path):
    """
    Recursively builds a folder structure starting from the given path.
    Sorts files and directories numerically if filenames start with numbers,
    and alphabetically otherwise.
    """
    folder_name = os.path.basename(path)
    full_path = os.path.abspath(path)
    subdirs = [d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))]
    files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

    # Custom sorting function
    def custom_sort_key(name):
        """
        Sorts by numeric prefix if present, otherwise alphabetically.
        """
        match = re.match(r'^\D*(\d+)', name)
        if match:
            return (int(match.group(1)), name.lower())
        return (float('inf'), name.lower())

    # Sort files and subdirectories using the custom sort key
    files.sort(key=custom_sort_key)
    subdirs.sort(key=custom_sort_key)

    node = {
        "title": clean(folder_name),
        "items": {}
    }

    # Add "Play All" option with absolute path
    node["items"]["0"] = {
        "title": "Play All",
        "action": {
            "do": "mpv",
            "path": full_path
        }
    }

    # Add files to the node
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

    # Add subdirectories to the node
    for idx, subdir in enumerate(subdirs):
        sub_path = os.path.join(full_path, subdir)
        node["items"][str(len(files) + idx + 1)] = build_folder_structure(sub_path)

    return node

if __name__ == "__main__":
    # Set the root media directory
    with open('mediaDir.json', 'r') as file:
        data = json.load(file)
    root_dir = data["mediaDir"]
    tree = build_folder_structure(root_dir)

    menus_file = os.path.join(parentdir, "menus.json")

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
