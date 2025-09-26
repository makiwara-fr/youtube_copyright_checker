from src.app import launch_app
from src.utils.logger import setup_logger
from src.config import *

import argparse



def main():

    app_name = APP_NAME
   

    parser = argparse.ArgumentParser(
                    prog=app_name,
                    description='Search youtube for keywords that match your copyrighted materials',
                    epilog='')
    

    parser.add_argument('-g', '--generate', nargs='?', const=DEFAULT_FILE,
                        help=f"""provide name of file to be generated\n
                        {app_name} -g [file_name]\n
                        will generate a file [file_name] you can then input to script. No provided name will be defaulted to {DEFAULT_FILE}
                        """)     
    parser.add_argument('-f', '--file', nargs='?', const=DEFAULT_FILE, default=DEFAULT_FILE,
                        help="file with all keywords filled in"
    )      # option that takes a value
    parser.add_argument('-d', '--debug', action="store_true", default=False)

    args = parser.parse_args()
   
    if not FORCE_DEBUG:
        debug=args.debug
    else:
        debug=True

    

    logger = setup_logger(app_name, debug=debug)

    name_length = len(app_name)
    logger.info("-"*name_length)
    logger.info(app_name)
    logger.info("-"*name_length)

    logger.debug("DEBUG is ON")
    logger.debug("")
    logger.debug(args)

    launch_app(args, logger)


if __name__ == "__main__":
    main()
    