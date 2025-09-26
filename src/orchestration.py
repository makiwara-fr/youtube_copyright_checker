from googleapiclient.discovery import build
from pathlib import Path
from datetime import datetime
import pandas as pd

from src.youtube import youtube_connection
from src.search import check_keyword





def check_all_keywords(file_path:Path, logger):


    """
    
    returns:
    - dataframe with keywords, link and timestamp
    """

    df = pd.read_excel(file_path, sheet_name="keywords")
    
    df_exclusion = pd.read_excel(file_path, sheet_name="exclusion")
    logger.debug(f"exclusions is {len(df_exclusion)} long")
    exclusions = [tuple(row[1:]) for row in df_exclusion.itertuples()]
    
    df_audit = pd.DataFrame()

    youtube = youtube_connection(logger)


    if not youtube:
        logger.error("Cannot connect to youtube")
        return

    # Parcourir les marques et rechercher des vidéos
    for index, row in df.iterrows():
        kw = row["keywords"]

        try:
            audit = check_keyword(kw, youtube, channel_exclusions=exclusions)

            df_audit = pd.concat([df_audit, pd.DataFrame(audit, columns=['keywords', 'title', 'link', 'views', 'channelId', 'channelTitle', 'subscribers'])])

            suspicions=(len(audit)>0)

            df.at[index, "Suspicions"] = suspicions
            df.at[index, "latest check"] = datetime.now()
            if suspicions:
                logger.info(f"Found {len(audit)} videos suspicious for {kw}")
        except Exception as e:
            logger.error(f"Error in processing {kw}. Details below:")
            logger.error(e)




    # save results
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:

        if len(df_audit) == 0: # no results found
            logger.info("Nothing to report. Stopping")
            return

        df.to_excel(writer, sheet_name="keywords", index=False)
        audit_sheet_name= f"audit_{datetime.now().strftime("%Y-%m-%d-%H-%M")}"
        df_audit.to_excel(writer, sheet_name=audit_sheet_name, index=False)


        worksheet = writer.sheets[audit_sheet_name]
        link_col = df_audit.columns.get_loc('link') + 1  # +1 car Excel est 1-indexé

        # Appliquer le format hyperlien à toute la colonne
        for i, url in enumerate(df_audit['link'], start=2):  # start=2 pour sauter l'en-tête
            worksheet.cell(row=i, column=link_col).value = url
            worksheet.cell(row=i, column=link_col).hyperlink = url
            worksheet.cell(row=i, column=link_col).style = "Hyperlink"



def generate_template(file_path: Path):
    """ generate template excel file for processing 
    
    inputs:
    - file_path: a pathlib path towards the target file

    """


    df = pd.DataFrame({"keywords": ["your keywords here"], "latest check": ["pending"], "Suspicions": [""]})
    df_exclusion = pd.DataFrame({"channelId": [""], "channelTitle": [""]})

    file_path.parent.mkdir(exist_ok=True)

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="keywords", index=False)
        df_exclusion.to_excel(writer, sheet_name="exclusion", index=False)
        
    # df.to_excel(file_path, index=False, sheet_name="keywords")
