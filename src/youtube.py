from googleapiclient.discovery import build
from pathlib import Path
import yaml

from src.config import *


def youtube_connection(api_key, logger):
    """connect to youtube api"""
    

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    return youtube
