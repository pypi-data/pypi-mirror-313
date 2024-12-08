import json
from os.path import getsize
from pathlib import Path

import auto_dlp.YoutubeDataAPIv3 as api
import auto_dlp.file_locations as fs


def _get_content(file):
    with open(file) as fhandle:
        content = json.load(fhandle)
    return content

# Do not cache; object are mutable
def get(config, playlist_id):
    file: Path = fs.playlist_item_cache() / f"{playlist_id}.json"
    if file.exists() and getsize(file) > 0:
        return _get_content(file)

    items = api.get_playlist_items(config, playlist_id)
    fs.touch_file(file)
    with open(file, "w") as fhandle:
        json.dump(items, fhandle)

    return items
