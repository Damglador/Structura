import requests
from zipfile import ZipFile
import os
from log_config import get_logger

logger = get_logger(__name__)


def update(url,structura_version, lookup_verison):
    initial_check = requests.get(url,headers={"structuraVersion": structura_version,"lookupVersion":lookup_verison}).json()
    logger.info(initial_check)
    updated=False
    logger.info(initial_check)
    if initial_check["info"] == 'Update Availible':
        logger.info('Update Availible')
        logger.info(initial_check["url"])
        response = requests.get(initial_check["url"], allow_redirects=True,stream=True)
        if response.headers.get('content-type') == "application/xml":
            logger.info(response.content)
        else:
            with open("lookup_temp.zip","wb") as file:
                file.write(response.content)
            logger.info("download completed")
            with ZipFile("lookup_temp.zip", 'r') as zObject:
                zObject.extractall(path="")
            os.remove("lookup_temp.zip")
            logger.info("update complete")
            updated=True
    else:
        logger.info("up to date")
    return updated
if __name__ =="__main__":
    update("https://update.structuralab.com/structuraUpdate",
           "Structura1-7",
           "none")
    
