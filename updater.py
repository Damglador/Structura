import requests
from zipfile import ZipFile
import os

def update(url,structura_version, lookup_verison):
    initial_check = requests.get(url,headers={"structuraVersion": structura_version,"lookupVersion":lookup_verison}).json()
    updated=False
    if initial_check["info"] == 'Update Availible':
        response = requests.get(initial_check["url"], allow_redirects=True,stream=True)
        if response.headers.get('content-type') == "application/xml":
            print(response.content)
        else:
            with open("lookup_temp.zip","wb") as file:
                file.write(response.content)
            with ZipFile("lookup_temp.zip", 'r') as zObject:
                zObject.extractall(path="")
            os.remove("lookup_temp.zip")
            updated=True
    else:
        print("up to date")
    return updated
if __name__ =="__main__":
    update("https://update.structuralab.com/structuraUpdate",
           "Structura1-7",
           "none")
    
