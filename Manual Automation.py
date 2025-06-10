import re
from tabulate import tabulate
import pandas as pd
import os


def Download_Generator(share_link = "A"):
    links = []
    file_type_storage = []
    while share_link:
        share_link = input()
        match share_link:
            case "Exit":
                "Session Ended"
                break
            case "End":
                "Session Ended"
                break
            case "exit":
                "Session Ended"
                break
            case "0":
                "Session Ended"
                break
            case "end":
                "Session Ended"
                break
        
        if not share_link.endswith("sharing"):
            print("Not a shared File")
            continue


        FILE_ID = re.search(r"/d/([^/]+)", share_link).group(1)
        File_Type = re.search(r".com/(.+?)/.+", share_link).group(1)

        if File_Type == "document":
            line = f"https://docs.google.com/document/d/{FILE_ID}/export?format=docx"
            file_type = "Google Word"
        elif File_Type == "spreadsheets":
            file_type = "Google Excel"
            line = f"https://docs.google.com/document/d/{FILE_ID}/export?format=xlsx"
        elif File_Type == "presentation":
            file_type = "Google Slides"
            line = f"https://docs.google.com/document/d/{FILE_ID}/export?format=pptx"
        print("Download Link:",line)
        links.append(line)
        file_type_storage.append(file_type)
        print("-"*(len("Download Link:") + len(line)))
        
    return links, file_type_storage
        

def markdown(links):
    headers = ["File Numbers", "Download Links"]
    df = pd.DataFrame(links)
    df.index = range(1, len(df) + 1)
    return tabulate(df, headers=headers, tablefmt="grid")
   
links,types = Download_Generator()
clear = []
clear_types = []
file_path = "Drive Downloads.txt"


if os.path.exists(file_path):
    if os.path.getsize(file_path) != 0:
        lx = open("Drive Downloads.txt")
        finds = []
        for i in lx:
            find = re.findall(".*(https.+)", i)
            if find:
                finds.append(find[0])
        if finds:
            for j in range(len(links)-1, -1, -1):
                if links[j] not in finds and links[j] not in clear:
                    clear.append(links[j])
                    clear_types.append(types[j])
    else:
        for j in range(len(links)-1, -1, -1):
            if links[j] not in clear:
                clear.append(links[j])
                clear_types.append(types[j])
                    
if clear:
    filea = open("Drive Downloads.txt", "a")
    for i in range(len(clear)):
        filea.write("-"*len(clear[i]))
        filea.write("\n")
        filea.write(f"{clear_types[i]} File: {clear[i]}\n")
        filea.write("-"*len(clear[i]))
        filea.write("\n")
    
