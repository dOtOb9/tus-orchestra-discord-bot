from os import getenv, environ

import dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

from dotenv import load_dotenv
load_dotenv()


DBX_APP_KEY = getenv("DBX_APP_KEY")
DBX_APP_SECRET = getenv("DBX_APP_SECRET")

def startDropboxOAuth():
    auth_flow = DropboxOAuth2FlowNoRedirect(consumer_key=DBX_APP_KEY, consumer_secret=DBX_APP_SECRET, token_access_type="offline")

    auth_url = auth_flow.start()

    return auth_url, auth_flow


def verify_access_token(auth_code, auth_flow, discord_id):
    try:
        result = auth_flow.finish(auth_code)
        environ[discord_id + "_DBX_REFRESH_TOKEN"] = result.refresh_token

        token = getenv(discord_id + "_DBX_REFRESH_TOKEN")

        return "登録が完了しました。"

    except:
        return "エラーが発生しました。"
