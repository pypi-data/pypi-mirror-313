import os
import sys
from pathlib import Path

import yt_dlp as yt
from yt_dlp import DownloadError

import auto_dlp.file_locations as fs
from auto_dlp import unavailable_items


def _video_url(x):
    return f"https://www.youtube.com/watch?v={x}"


def _song_file_path(song_id):
    return fs.download_cache() / f"{song_id}.mp3"


def _download_song(song_id, config, use_cookies=False):
    if unavailable_items.is_unavailable(song_id):
        return None

    music_dir = Path(os.curdir).resolve()

    path: Path = _song_file_path(song_id)
    fs.touch_folder(path.parent)
    fs.touch_folder(fs.ytdlp_download_cache())

    os.chdir(path.parent)

    ydl_options = {
        'format': 'm4a/bestaudio/best',
        "cache-dir": fs.ytdlp_download_cache(),
        "outtmpl": "%(id)s",
        "print": f"Song %(id)s has been downloaded",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    if use_cookies:
        ydl_options["cookiesfrombrowser"] = ("firefox",)

    try:
        with yt.YoutubeDL(ydl_options) as ydl:
            error_code = ydl.download([_video_url(song_id)])
            print(f"Error Code {error_code}")
    except DownloadError as e:
        print("An error occurred during download", file=sys.stderr)

        if unavailable_items.is_error_message_indicative_of_unavailability(e.msg):
            unavailable_items.know_is_unavailable(song_id)
            return None

        if not use_cookies and config.use_cookies:
            print("Retrying with cookies", file=sys.stderr)
            return _download_song(song_id, config, True)
        else:
            return None

    os.chdir(music_dir)

    if not _song_file_path(song_id).exists():
        raise RuntimeError(f"There was an internal error during the download, somehow the file {_song_file_path(song_id)} was not created")

    return path


def _interruptable_download_song(song_id, config):
    try:
        return _download_song(song_id, config)
    except KeyboardInterrupt as e:
        path: Path = _song_file_path(song_id)
        path.unlink(missing_ok=True)
        raise e


def get_song_file(song_id, config):
    if _song_file_path(song_id).exists():
        return _song_file_path(song_id)

    music_dir = Path(os.curdir).resolve()
    path = _interruptable_download_song(song_id, config)
    os.chdir(music_dir)
    return path


def delete_cached_version(song_id):
    path: Path = _song_file_path(song_id)
    path.unlink(missing_ok=True)
