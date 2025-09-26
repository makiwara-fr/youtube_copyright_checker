from googleapiclient.discovery import build
from pathlib import Path
import yaml



def youtube_connection(logger):
    """ connect to youtube api
    
    

    """
    CONFIG_PATH = Path(__file__).parent.parent.joinpath("config/config.yaml")
    
    # check API Key
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        api_key = config["api_key"]

    except:
        # create the file
        logger.info("Could not find create the config file. Will create it")
        api_key = input("Insert your api key here: ")
        config = {"api_key": api_key}
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
            yaml.dump(config, config_file, default_flow_style=False, indent=4)


    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    return youtube
