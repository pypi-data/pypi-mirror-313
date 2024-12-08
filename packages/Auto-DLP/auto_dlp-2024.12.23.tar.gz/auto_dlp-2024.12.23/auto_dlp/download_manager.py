import shutil

import auto_dlp.downloader as downloader
import auto_dlp.file_cleaning as clean
import auto_dlp.file_locations as fs
import auto_dlp.metadata as metadata
from auto_dlp import playlist_items
from auto_dlp.name_cleaning import clean_name


def _copy_if_necessary(src, dest):
    if dest.exists(): return False

    fs.touch_file(dest)
    shutil.copyfile(src, dest)
    return True


def download_song(config, artist, name, song_id):
    raw_file = downloader.get_song_file(song_id, config)
    file = fs.song_file(artist, name)

    fs.touch_folder(file.parent)
    clean.know_file(file.parent)
    necessary = _copy_if_necessary(raw_file, file)
    clean.know_file(file)

    if necessary:
        metadata.write_for_song(config, artist, name, song_id, file)


def download_playlist(config, artist, playlist_name, playlist_id):
    raw_items = playlist_items.get(config, playlist_id)
    items = [
        {"name": clean_name(config, i["name"]), "id": i["id"]} for i in raw_items
    ]

    fs.touch_folder(fs.playlist_dir(artist, playlist_name))
    clean.know_file(fs.playlist_dir(artist, playlist_name))

    for index, name, song_id, path in fs.playlist_files(artist, playlist_name, items):
        file = downloader.get_song_file(song_id, config)
        if file is None:
            print(f"Skipping unavailable song {name} from {playlist_name}")
            continue

        necessary = _copy_if_necessary(file, path)
        clean.know_file(path)

        if necessary:
            print(f"Downloaded {name} by {artist} from {playlist_name}")
            metadata.write_for_playlist_item(config, artist, playlist_name, name, playlist_id, song_id, index,
                                             len(items), path)

    metadata.process_playlist(config, artist, playlist_name, playlist_id, fs.playlist_dir(artist, playlist_name))
