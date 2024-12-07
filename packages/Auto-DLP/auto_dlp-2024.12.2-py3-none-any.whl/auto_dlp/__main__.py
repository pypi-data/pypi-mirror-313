from traceback import print_exception

import auto_dlp

if __name__ == "__main__":
    try:
        auto_dlp.main()
    except Exception as e:
        print_exception(e)
        if auto_dlp.wait_after_finishing_execution:
            input()
