import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(logger_name, debug=True):
    
    logger = logging.getLogger(logger_name)
    
    log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    log_dir_path = Path('logs/')
    log_dir_path.mkdir(exist_ok=True)
    log_filepath = log_dir_path.joinpath(log_filename)


    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logger.setLevel(level)

    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(level)

    # Handler pour la console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')  
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)


    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    return logger