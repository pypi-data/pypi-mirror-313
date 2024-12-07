import argparse
import json
import os
import re
import sys
from pathlib import Path
from traceback import print_exception

from auto_dlp import config_intepreter

_wait_after_finishing_execution = True


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

def command_entry_point():
    try:
        main()
    except Exception as e:
        print_exception(e)
        if _wait_after_finishing_execution:
            input()

def main():
    parser = argparse.ArgumentParser(prog="auto-dlp",
                                     description="A light-weight program for managing (and downloading) music",
                                     allow_abbrev=True, add_help=True, exit_on_error=True)
    parser.add_argument("FOLDER",
                        help="The folder in which to execute this program. It must contain a musicmanager.json file.")
    parser.add_argument("-rd", "--redownload", metavar="SONG",
                        help="Will delete the current version of the specified song, meaning that it will be redownloaded on the next execution of this program")
    parser.add_argument("-tn", "--test-name", metavar="NAME",
                        help="Allows to try out what the renaming system does to a specific string")
    parser.add_argument("-w", "--wait", action="store_true", help="After finishing execution, wait for any input")

    args = parser.parse_args()
    global wait_after_finish
    wait_after_finish = args.wait

    exec_dir = Path(args.FOLDER).expanduser().resolve()
    print(f"Executing Music Manger in directory {exec_dir}")

    redownload = () if args.redownload is None else [args.redownload]
    test_names = () if args.test_name is None else [args.test_name]
    manage_music(exec_dir, redownload_songs=redownload, test_names=test_names)

    if args.wait:
        input("Press ENTER to close program")
