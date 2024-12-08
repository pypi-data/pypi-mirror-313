import os.path as path
import re
import sys
from collections import Counter
from json import dumps

from requests import get

import auto_dlp.file_locations as fs
import auto_dlp.utils as utils

# def _ask_for_api_key():
#     key = input("Please enter a valid Google Cloud Youtube API key (This is for getting the playlist item (in the future there might be a different implementation for this feature)): ").strip()
#     if key == "":
#         return _ask_for_api_key()
#
#     fs.touch_file(fs.yt_api_key_file())
#     with fs.yt_api_key_file().open("w") as file:
#         print(key.strip(), file=file)
#
#     return key

# Wow, such secure
_key_url = "https://pastebin.com/8vmQFLbm"


def _download_api_key():
    response = get(_key_url)
    if response.status_code != 200:
        raise RuntimeError("Could not reach server to request api key, please try again later")

    pat = re.compile("this is where the key is:(?P<api_key>.*)not any further", flags=re.IGNORECASE)
    match = pat.search(response.text)
    key = match.groupdict()["api_key"]

    file = fs.yt_api_key_file()
    fs.touch_file(file)
    with open(file, "w") as fhandle:
        fhandle.write(key)

    return key


@utils.lazy
def API_KEY():
    file = fs.yt_api_key_file()
    if not path.exists(file) or path.getsize(file) <= 0:
        print("Api key file was not found", file=sys.stderr, flush=True)
        return utils.scramble(_download_api_key()).strip()

    with open(file) as fhandle:
        return utils.scramble(fhandle.read()).strip()


def request(url, params):
    params["key"] = API_KEY()
    response = get(url, params)

    if response.status_code == 200 and "error" not in response.json():
        return response

    try:
        err_msg = response.json()["error"]["message"]
    except KeyError:
        err_msg = "Error message could not be read"

    if response.status_code == 403:
        print("API key was not recognised by Youtube")
        sys.exit()

    raise RuntimeError(f"Network error: {response.status_code} {err_msg}")


def deduplicate_playlist_items(config, playlist_items):
    name_counter = Counter()

    for item in playlist_items:
        name_counter[item["name"]] += 1

    index_names = set()

    for name, count in name_counter.items():
        if count > 1:
            index_names.add(name)

    if len(index_names) == 0:
        return playlist_items

    name_counter = Counter()

    for item in playlist_items:
        name = item["name"]
        if item["name"] in index_names:
            name_counter[name] += 1
            item["name"] = f"{name} ={name_counter[name]}="

    return playlist_items


def get_playlist_items(config, playlist_id):
    def send_request(params):
        params["playlist_id"] = playlist_id
        params["part"] = "contentDetails, snippet"
        params["maxResults"] = 50
        response = request("https://www.googleapis.com/youtube/v3/playlistItems", params)
        items = {}

        try:
            items_json = response.json()["items"]

            for item in items_json:
                pos = item["snippet"]["position"]
                items[pos] = {
                    "name": item["snippet"]["title"],
                    "id": item["contentDetails"]["videoId"]
                }
        except KeyError:
            print(dumps(response.json(), indent=4), file=sys.stderr)
            raise RuntimeError("Failed getting playlist items")

        if "nextPageToken" in response.json():
            return response.json()["pageInfo"]["totalResults"], response.json()["nextPageToken"], items
        return response.json()["pageInfo"]["totalResults"], None, items

    received_items = 0
    result_count, page_token, items_map = send_request({})

    items_list = [None] * result_count

    def place_items():
        for index, item in items_map.items():
            if items_list[index] is None:
                items_list[index] = item
                continue

            raise RuntimeError("The Youtube Api returned the same result twice")

    place_items()
    received_items += 50

    while received_items < result_count:
        _, page_token, items_map = send_request({"pageToken": page_token})
        try:
            place_items()
        except RuntimeError as e:
            if playlist_id in config.fragile_playlists:
                return deduplicate_playlist_items(config, list(filter(lambda x: x is not None, items_list)))
            raise e
        received_items += 50

    return deduplicate_playlist_items(config, items_list)


def get_song_channel(song_id):
    response = request("https://www.googleapis.com/youtube/v3/videos", {
        "key": API_KEY(),
        "part": "snippet",
        "id": song_id
    })

    try:
        channel = response.json()["items"][0]["snippet"]["channelId"]
    except KeyError:
        print(dumps(response.json(), indent=4), file=sys.stderr)
        raise RuntimeError("Failed getting song thumbnails")

    return channel


def get_song_thumbnails(song_id):
    response = request("https://www.googleapis.com/youtube/v3/videos", {
        "key": API_KEY(),
        "part": "snippet",
        "id": song_id
    })

    try:
        thumbnails = response.json()["items"][0]["snippet"]["thumbnails"]
    except KeyError:
        print(dumps(response.json(), indent=4), file=sys.stderr)
        raise RuntimeError("Failed getting song thumbnails")

    return thumbnails


def get_playlist_thumbnails(playlist_id):
    response = request("https://www.googleapis.com/youtube/v3/playlists", {
        "key": API_KEY(),
        "part": "snippet",
        "id": playlist_id
    })

    try:
        thumbnails = response.json()["items"][0]["snippet"]["thumbnails"]
    except KeyError:
        print(dumps(response.json(), indent=4), file=sys.stderr)
        raise RuntimeError("Failed getting song thumbnails")

    return thumbnails


def get_channel_thumbnails(channel_id):
    response = request("https://www.googleapis.com/youtube/v3/channels", {
        "key": API_KEY(),
        "part": "snippet",
        "id": channel_id
    })

    try:
        thumbnails = response.json()["items"][0]["snippet"]["thumbnails"]
    except KeyError:
        print(dumps(response.json(), indent=4), file=sys.stderr)
        raise RuntimeError("Failed getting song thumbnails")

    return thumbnails
