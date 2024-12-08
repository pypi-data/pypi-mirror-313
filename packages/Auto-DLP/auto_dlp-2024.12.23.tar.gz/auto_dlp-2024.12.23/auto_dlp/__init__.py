import argparse
import json
import os
import re
import sys
from pathlib import Path
from traceback import print_exception

from auto_dlp import config_intepreter, example_file

_wait_after_finishing_execution = True
CONFIG_FILENAME = "auto-dlp.json"


def manage_music(path: Path, redownload_songs=(), test_names=(), playlist_test_names=None, verbose=False):
    original_cur_dir = Path(os.curdir).resolve()
    os.chdir(path)

    try:
        config_file = path / CONFIG_FILENAME
        if not config_file.exists():
            print(f"No {CONFIG_FILENAME} file found in directory {path.resolve()}", file=sys.stderr)
            print(f"Use auto-dlp DIRECTORY --create-example to create an example {CONFIG_FILENAME} file")
            return

        with open(config_file) as file:
            string = re.sub("//.*", "", file.read())
            json_data = json.loads(string)

        config_intepreter.execute(json_data, redownload_songs=redownload_songs, test_names=test_names,
                                  playlist_test_names=playlist_test_names, verbose=verbose)
    except KeyboardInterrupt:
        print("Program interrupted by user", file=sys.stderr)

    os.chdir(original_cur_dir)


def command_entry_point():
    try:
        main()
    except Exception as e:
        print_exception(e)
        if _wait_after_finishing_execution:
            wait_to_close()

class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, max_help_position=70, width=100)

def main():
    parser = argparse.ArgumentParser(prog="auto-dlp",
                                     description="A light-weight program for managing (and downloading) music",
                                     allow_abbrev=True, add_help=True, exit_on_error=True, formatter_class=CustomHelpFormatter)
    parser.add_argument("FOLDER",
                        help=f"The folder in which to execute this program. It must contain an {CONFIG_FILENAME} file.")
    parser.add_argument("-rd", "--redownload", metavar="SONG",
                        help="Will delete the current version of the specified song, meaning that it will be redownloaded on the next execution of this program")
    parser.add_argument("-tn", "--test-name", metavar="NAME",
                        help="Allows to try out what the renaming system does to a specific string")
    parser.add_argument("-ptn", "--playlist-test-names", metavar="PLAYLIST",
                        help="Runs all the names of songs in PLAYLIST against -tn")
    parser.add_argument("-w", "--wait", action="store_true", help="After finishing execution, wait for any input")
    parser.add_argument("-v", "--verbose", action="store_true", help="Makes the script print more information")
    parser.add_argument("--create-example", action="store_true", help=f"Creates a sample {CONFIG_FILENAME} file that will perform elementary functions")

    args = parser.parse_args()
    global _wait_after_finishing_execution
    _wait_after_finishing_execution = args.wait

    exec_dir = Path(args.FOLDER).expanduser().resolve()
    print(f"Executing Auto-DLP in directory {exec_dir}")

    if args.create_example:
        example_file.generate_file(exec_dir, CONFIG_FILENAME)
        if args.wait:
            wait_to_close()
        return

    redownload = () if args.redownload is None else [args.redownload]
    test_names = () if args.test_name is None else [args.test_name]
    playlist = args.playlist_test_names

    manage_music(exec_dir, redownload_songs=redownload, test_names=test_names, playlist_test_names=playlist,
                 verbose=args.verbose)

    if args.wait:
        wait_to_close()

def wait_to_close():
    input("Press ENTER to close program")