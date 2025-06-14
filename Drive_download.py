## This is a demo version of the script, it works perfectly fine if you login in 
## to your google account for the OAuth to authenticate you and only works for files
## in folders which are available in your drive, which is still very useful but gets
## quite tedious when you need to alternate between accounts or you need to download from
## an account's drive which is not owned by you, for that an API key will be needed instead
## of OAuth client as that way an authentication process will no longer be needed
## I'm gonna implement that into the code later instead, consider this the "safer" yet
## Tedious version of the final product

## Also it uses a file outside of it to use the Service of the desire API of Google
## Which is a bit wonky and I am yet to properly understand how it works but i'll figure
## it out once I'm done with this project

from Google import Create_Service
import os
import re
import pandas as pd

def ExtensionExtractor(mime = None):
    ## The book1.xlsx file is basically an excel file which contains every possible
    ## MIME Types in the third column and their relevant extension formats in the first
    ## Here, when I get the files as a response from the API it contains the MIME type
    ## which is stored in a dictionary alongside alot of other infos but we can't convert
    ## the MIME type to a downloadable link hence we are reformatting it
    
    df = pd.read_excel('Book1.xlsx')
    result = dict(zip(df.iloc[:,3], df.iloc[:,1]))  # 3rd column as key, 1st as value
    return result[mime]
## For the secret file you're going to need to create a Google Cloud console
## https://www.youtube.com/watch?v=wJ6WC0G8w4o watch this video to know how

ClIENT_SECRET_FILE = "client_secret_GoogleCloudDemo.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = Create_Service(ClIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


## To Retrieve the files sent from the Drive API via a Query

## I still need to properly understand how the query and response works for the Google.py file
## will explain later
Folder_ID = "1MiPEQsJue-FZ4I2wOXSysdvfSm803Swl"
query = f"parents='{Folder_ID}'"
response = service.files().list(q=query).execute()
files = response.get("files")
nextPageToken = response.get("nextPageToken")
print(response)

## Not always required but this basically checks in case there's multiple
## pages in the folder
while nextPageToken:
    response = service.files().list(q=query).execute()
    files.extend(response.get("files"))
    nextPageToken = response.get("nextPageToken")
# print(files)
File_IDs = []
File_types = []

## Singling out the ID's and File types

for i in files:
    types = re.findall(".*\.(.*)", i["name"])
    if types:
        File_IDs.append(i["id"])
        File_types.append(types)
    else:
        mime = i["mimeType"]
        mimetype = ExtensionExtractor(mime)
        if mimetype:
            File_IDs.append(i["id"])
            File_types.append([mimetype])
        else:
            continue
    
## Creating the Download link from the File ID

links = []
for i in File_IDs:
    s1 = f"https://drive.google.com/uc?id={i}&export?=download"
    links.append(s1)
  
## Designating path of the File

file_path = "Drive Downloads.txt"

## Finding which links are clear to add and separating the ones which
## aren't along with the format in which the download links are gonna download

clear = []
clear_types = []
filea = open("Drive Downloads.txt", "a") ## Basically creates it if it doesn't exist, otherwise appends to the end
if os.path.exists(file_path): ## To check if the path I mentioned exists
    if os.path.getsize(file_path) != 0:
        lx = open("Drive Downloads.txt")
        finds = []
        for i in lx:
            find = re.findall(".*(https.+)", i)
            if find:
                finds.append(find[0])
        if finds:
            for j in range(len(links)-1, -1, -1):
                print(links[j])
                if links[j] not in finds and links[j] not in clear:
                    clear.append(links[j])
                    clear_types.append(File_types[j])
    else:
        for j in range(len(links)-1, -1, -1):
            if links[j] not in clear:
                clear.append(links[j])
                clear_types.append(File_types[j])
# print(File_types)                                  
# print(clear_types)

## Final step where I arrange the links in the text editor
## so that they are all available in a single place

if clear:
    for i in range(len(clear)):
        filea.write("-"*(len(clear[i])+19))
        filea.write("\n")
        filea.write(f"{clear_types[i]} File: {clear[i]}\n")
        filea.write("-"*(len(clear[i])+19))
        filea.write("\n")
    
