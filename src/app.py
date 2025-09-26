from src.config import *
from src.orchestration import generate_template, check_all_keywords
from src.youtube import youtube_connection

from pathlib import Path
import yaml





def launch_app(args, logger):


    config = configure(logger)

    if args.generate is not None:
        # templating mode
        logger.info("Generating research template")
        generate_template(Path(args.generate))
        return
    elif args.file is not None:
       # search mode
        file_path = Path(args.file)

        logger.info("Searching for copyright infringement")
        logger.info(f"- inputs from file: {file_path}")

        if not file_path.exists():
            logger.error("Input file is not existing - Aborting")
            logger.error("-" * 50)
            return

        # connecting to youtube api
        youtube = youtube_connection(config["api_key"], logger)
        if not youtube:
            logger.error("Cannot connect to youtube")
            return


        # searching
        check_all_keywords(file_path, logger, youtube, language=config["language"])

        return

    else:
        logger.error("Nothing to do - Should not happen")
        logger.error(f"Reminder of args: {args}")
        return
