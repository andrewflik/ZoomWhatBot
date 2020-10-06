"""
    "access_token": "ya29.a0AfH6SMBRg9YKpGp0S2T_gN-Gs9oZ7Xp7OUBf9U3R7Zm-BfmHQG6002yGolPiKie3botNZjPQh2xZ1JsrEStRUUpG7rI-LPJuDIno4eNpGlNefp7_qFoPdZuifs3pRBZZS5eRJvaaY28V2TyNp11WVTLQD2DLKIFBeyo"
"""

import pandas as pd
from drive_ import *   # Import
import os
import os.path
from googleapiclient import *
from apiclient.http import MediaFileUpload
import json
import requests

#"https://drive.google.com/file/d/1YQVIkdbxHkwP6dcD6MtBLZCH3UNt9CEq/view?usp=sharing"

def uploadFile():
    from apiclient.http import MediaFileUpload
data = dict()
data = {"UID1": ["Dev", 1, 2], "UID2": ["Dev", 1, 2], "UID3": ["Dev", 1, 2], "UID4": ["Dev", 1, 2], "UID5": ["Dev", 1, 2]}

df = pd.DataFrame.from_dict(data, orient='index', columns=["Name", "Joining Time", "Leaving Time"])
print(df)
df.to_excel("op.xlsx")


"""
import requests
headers = {"Authorization": "Bearer ya29.a0AfH6SMCc-cDoKr_X_FIep-NntuEXkRX2UQfirpnadZVnUOs_sIPkJZaTUIt04qWpiOTxZ3gynbwPBGUUEb4ofw85pFn2GL4JiFJYUkYZ4dSChppXbNCo2ufKVIghMdvYmOqiGM0x8MEVMijZvg5pMWOGhR_HJTKWKzc"} #put ur access token after the word 'Bearer '
para = {
    "name": "sample.txt", #file name to be uploaded
    "parents": ["1-HQDPtcH0DxqwOOQWycW6Km8aQHyHZPH"] # make a folder on drive in which you want to upload files; then open that folder; the last thing in present url will be folder id
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': (open("./sample.txt", "rb")) # replace 'application/zip' by 'image/png' for png images; similarly 'image/jpeg' (also replace your file name)
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files,
)
print(r.text)
"""

