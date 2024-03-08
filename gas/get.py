import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

URL = getenv("SPREADSHEET_EXEC_URL")


async def user_info(id):
    params = {
        "mode": "user_data",
        "id": str(id),
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        return f"❌エラーが発生しました。: {response.status_code}"
    
#-----------------------------------------------------------------------------------
    
async def can_send_activity_dm(type):
    params = {
        "mode": "can_send_activity_dm",
        "type": type,
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return f"❌エラーが発生しました。: {response.status_code}"

#-----------------------------------------------------------------------------------

async def can_send_attend_code():
    params = {
        "mode": "can_send_attend_code",
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        return response.json()