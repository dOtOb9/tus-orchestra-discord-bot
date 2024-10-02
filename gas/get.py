import requests
from os import getenv

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
    
async def can_send_activity_dm(section):
    params = {
        "mode": "can_send_activity_dm",
        "section": section,
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