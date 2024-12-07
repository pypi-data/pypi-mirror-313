import json
import os
import re
import sys
from pathlib import Path

from auto_dlp import config_intepreter


def manage_music(path: Path, redownload_songs=(), test_names=()):
    original_cur_dir = Path(os.curdir).resolve()
    os.chdir(path)

    try:
        config_file = path / "musicmanager.json"
        if not config_file.exists():
            print(f"No musicmanager.json file found in directory {path.resolve()}", file=sys.stderr)
            return

        with open(config_file) as file:
            string = re.sub("//.*", "", file.read())
            json_data = json.loads(string)

        config_intepreter.execute(json_data, redownload_songs=redownload_songs, test_names=test_names)
    except KeyboardInterrupt:
        print("Program interrupted by user", file=sys.stderr)

    os.chdir(original_cur_dir)
