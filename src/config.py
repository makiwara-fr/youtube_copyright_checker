from pathlib import Path
import yaml

APP_NAME = "youtube_copyright_checker"
DEFAULT_FILE = "keyword_list.xlsx"
DEFAULT_LANGUAGE = "Fr"

FORCE_DEBUG = True  # for development only


CONFIG_PATH = Path(__file__).parent.parent.joinpath("config/config.yaml")


def create_conf_yaml():
    api_key = input("Insert your api key here: ")
    config = {
        "api_key": api_key,
        "language": DEFAULT_LANGUAGE
    }
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
        yaml.dump(config, config_file, default_flow_style=False, indent=4)
    
    return config

def configure(logger):
    """
    
    returns:
     - a dictionary of info 
    """
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        return config

    except:
        # create the file
        logger.info("Could not find create the config file. Will create it")
        return create_conf_yaml()

