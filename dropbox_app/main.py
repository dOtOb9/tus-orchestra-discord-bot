import dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

from os import getenv
from dotenv import load_dotenv

import datetime

load_dotenv()

auth_flow = DropboxOAuth2FlowNoRedirect(getenv('DBX_APP_KEY'), getenv('DBX_APP_SECRET'))

authorize_url = auth_flow.start()

print('1. Go to: ' + authorize_url)

auth_code = input('2. Paste the authorization code here: ')

access_token = ""

try:
    result = auth_flow.finish(auth_code)
    access_token = result.access_token
    print('Access token:', access_token)
except Exception as e:
    print('Error:', e)


dbx = dropbox.Dropbox(access_token)

name = dbx.users_get_current_account()

print(name)

for entry in dbx.files_list_folder('').entries:
    start_dt = datetime.datetime.now()
    link = dbx.sharing_create_shared_link(entry.path_lower)
    print(link.url)
    end_dt = datetime.datetime.now()

    print("Time taken: ", end_dt - start_dt)
    input()