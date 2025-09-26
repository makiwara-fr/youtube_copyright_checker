from src.config import *
from src.orchestration import generate_template, check_all_keywords


from pathlib import Path

def launch_app(args, logger):
    

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
            logger.error("-"*50)
            return
        

        check_all_keywords(file_path, logger)


        return
    
    else:
        logger.error("Nothing to do - Should not happen")
        logger.error(f"Reminder of args: {args}")
        return