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
    
async def can_send_activity_dm(type, time_slots):
    params = {
        "mode": "can_send_activity_dm",
        "type": type,
        "slots": {
            "first": time_slots.first,
            "second": time_slots.second,
            "third": time_slots.third,
            "forth": time_slots.forth,
        }
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