from googleapiclient.discovery import build
import html




def is_excluded(video_item, exclusions):
    channel_id = video_item["snippet"]["channelId"]
    channel_title = video_item["snippet"]["channelTitle"]

    for id, title in exclusions:
        if channel_id == id or channel_title == title:
            return True
    
    return False




def check_keyword(keyword:str, youtube, channel_exclusions=[]):
    """ check on youtube for specific keywords 
    
    inputs:
    - keyword: str: key word to be searched
    - youtube: connection to youtube v3 api
    - channel exclusion: a list of tuple of channels to be excluded from report (channelID, channelName)

    returns:
    - a list of tuples:
        - keyword: str
        - title: str:
        - link: str
        - views: int
        - channelId: str
        - channel title: str
        - number of subscribers of channel
    
    """
    request = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=30,  
        type="video",
        relevanceLanguage="fr"
    )

    response = request.execute()

    audit = []

    for item in response.get("items", []):
        
        title = html.unescape(item["snippet"]["title"])
        video_id = item["id"]["videoId"]
        channel_id = item["snippet"]["channelId"]
        channel_title = item['snippet']["channelTitle"]

        if not is_excluded(item, channel_exclusions):

            # Récupérer le nombre de vues de la vidéo
            video_stats = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()
            views = int(video_stats["items"][0]["statistics"].get("viewCount", 0)) if video_stats["items"] else 0

            # Récupérer le nombre d'abonnés de la chaîne
            channel_stats = youtube.channels().list(
                part="statistics",
                id=channel_id
            ).execute()
            subscribers = int(channel_stats["items"][0]["statistics"].get("subscriberCount", 0)) if channel_stats["items"] else 0



            audit.append((keyword, title, f"https://www.youtube.com/watch?v={video_id}", views, channel_id, channel_title, subscribers))


    
    return audit

