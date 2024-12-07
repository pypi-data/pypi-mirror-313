import re
import sys
from pathlib import Path, PurePosixPath
from time import sleep

import requests

import auto_dlp.adb_fs_cleaning as adb_clean
import auto_dlp.download_manager as download
import auto_dlp.downloader as downloader
import auto_dlp.file_cleaning as clean
import auto_dlp.file_locations as fs
import auto_dlp.variables as variables
from auto_dlp import adb, playlist_items, age_hints
from auto_dlp.file_locations import touch_folder
from auto_dlp.metadata import process_artist
from auto_dlp.name_cleaning import clean_name


class Config:
    properties = ["config dir", "adb push", "adb push dir", "restart adb", "extra adb folders", "clean push dir",
                  "name rules", "artists", "rule macros", "use cookies", "rename", "name samples", "retry interval",
                  "fragile playlists"]

    def __init__(self):
        self.config_dir = None
        self.adb_push = False
        self.adb_push_dir = PurePosixPath("/sdcard/Music/")
        self.restart_adb = False
        self.extra_adb_folders = []
        self.clean_push_dir = True
        self.name_rules = []
        self.compiled_name_rules = []
        self.rule_macros = {}
        self.name_samples = 4
        self.artists = []
        self.use_cookies = False
        self.rename = {}
        self.retry_interval = 10
        self.fragile_playlists = []

    def assign_property(self, key, value):
        match key:
            case "config dir":
                self.config_dir = Path(value)
                variables.CONFIG_DIR = self.config_dir
            case "adb push":
                self.adb_push = bool(value)
            case "adb push dir":
                self.adb_push_dir = PurePosixPath(value)
            case "clean push dir":
                self.clean_push_dir = bool(value)
            case "restart adb":
                self.restart_adb = bool(value)
            case "name rules":
                self.name_rules = list(value)
            case "rule macros":
                self.rule_macros = dict(value)
            case "name_samples":
                self.name_samples = int(value)
            case "artists":
                self.artists = [
                    Artist.from_json(self, name, json) for name, json in value.items()
                ]
            case "use cookies":
                self.use_cookies = bool(value)
            case "rename":
                self.rename = dict(value)
            case "retry interval":
                self.retry_interval = float(value)
            case "fragile playlists":
                self.fragile_playlists = list(value)
            case "extra adb folders":
                self.extra_adb_folders = list(value)

    @classmethod
    def from_json(cls, json):
        config = Config()

        for key, value in json.items():
            if key not in cls.properties:
                raise ValueError(f"Unknown property key: {key}")

            config.assign_property(key, value)

        return config

    def __str__(self):
        return (f"""config file: {self.config_dir}
adb push: {self.adb_push}
name rules: {" ".join(self.name_rules)}
artists:
""" + "\n".join(map(str, self.artists)))


class Artist:
    properties = ["songs", "playlists"]

    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.songs = {}
        self.playlists = {}

    def all_songs(self):
        yield from self.songs.values()

        for name, playlist_id in self.playlists.items():
            for entry in playlist_items.get(self.config, playlist_id):
                yield entry["id"]

    def assign_property(self, key, value):
        match key:
            case "songs":
                # self.songs = dict(value)
                self.songs = _process_years_in_names(dict(value), age_hints.add_hint_song)
            case "playlists":
                # self.playlists = dict(value)
                self.playlists = _process_years_in_names(dict(value), age_hints.add_hint_playlist)

    @classmethod
    def from_json(cls, config, name, json):
        artist = Artist(config, name)

        for key, value in json.items():
            if key not in cls.properties:
                raise ValueError(f"Unknown property key: {key}")

            artist.assign_property(key, value)

        return artist

    def __str__(self):
        return "\n".join((
            f"""    {self.name}:""",
            *(f"        {name}: {song_id}" for name, song_id in self.songs.items()),
            *(f"        {name}: {playlist_id}" for name, playlist_id in self.playlists.items())
        ))


def _process_years_in_names(map, hint_function):
    new_map = {}

    for name, obj_id in map.items():
        new_name = age_hints.parse_name(name, obj_id, hint_function)
        new_map[new_name] = obj_id

    return new_map


def _execute_artist(config, artist):
    print(f"Looking at {artist.name}")
    touch_folder(fs.artist_dir(artist.name))
    clean.know_file(fs.artist_dir(artist.name))

    for song_name, song_id in artist.songs.items():
        print(f"Downloading {song_name} ({song_id})")
        download.download_song(config, artist.name, song_name, song_id)

    process_artist(config, artist, artist.all_songs(), fs.artist_dir(artist.name), fs.artist_songs_dir(artist.name))

    for playlist_name, playlist_id in artist.playlists.items():
        print(
            f"Downloading {playlist_name} ({playlist_id})\n\tinto {fs.playlist_dir(artist.name, playlist_name).resolve()}")
        download.download_playlist(config, artist.name, playlist_name, playlist_id)


def _resiliently_execute_artist(config, artist):
    try:
        _execute_artist(config, artist)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection to Internet services failed: {e}", file=sys.stderr, flush=True)
        print(f"Retrying in {config.retry_interval} seconds")
        sleep(config.retry_interval)
        _resiliently_execute_artist(config, artist)


def get_song_locations(config, song):
    song_re = re.compile(song, flags=re.IGNORECASE)

    for artist in config.artists:
        for name, song_id in artist.songs.items():
            if song == song_id or song_re.fullmatch(name) is not None:
                yield fs.song_file(artist.name, name), song_id

        for playlist_name, playlist_id in artist.playlists.items():
            for entry in playlist_items.get(config, playlist_id):
                name = clean_name(config, entry["name"])
                song_id = entry["id"]

                if song_id == song or song_re.fullmatch(name) is not None:
                    yield fs.playlist_dir(artist.name, playlist_name) / f"{name}.mp3", song_id


def redownload(config, song):
    print(f"Redownloading {song}")
    occurrence_count = 0
    for path, song_id in get_song_locations(config, song):
        occurrence_count += 1
        print(f"Deleting song with id {song_id} and {path}")
        path.unlink(missing_ok=True)
        downloader.delete_cached_version(song_id)
    print(f"Deleted {occurrence_count} occurrences of {song} as name or id")


def execute(json_file, redownload_songs=(), test_names=(), playlist_test_names=None, verbose=False):
    config = Config.from_json(json_file)

    if playlist_test_names is not None:
        for artist in config.artists:
            if playlist_test_names in artist.playlists:
                playlist_test_names = artist.playlists[playlist_test_names]
        test_names = list(test_names)
        test_names += map(lambda x: x["name"], playlist_items.get(config, playlist_test_names))

    if len(test_names) > 0:
        for name in test_names:
            print(f"{name} becomes {clean_name(config, name, verbose=verbose)}")
        return

    if len(redownload_songs) > 0:
        for song in redownload_songs:
            redownload(config, song.strip())
        return

    print(config)

    for artist in config.artists:
        _resiliently_execute_artist(config, artist)

    clean.clean_all(config)

    if not config.adb_push: return

    if adb.is_device_connected():
        if config.adb_push:
            adb.push_files(config)

        if config.clean_push_dir:
            adb_clean.clean_all(config)
    else:
        print("No Android device connected to this computer using usb", file=sys.stderr)
