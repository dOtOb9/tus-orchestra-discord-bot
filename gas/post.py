import requests
import json
from os import getenv

URL = getenv("SPREADSHEET_EXEC_URL")


async def user_post(json_data):
    headers = {
        "Content-Type" : "application/json"
    }

    response = requests.post(URL, headers=headers, data=json.dumps(json_data))

    if response.status_code == 200:
        return response.text
    else:
        return f"❌エラーが発生しました。: {response.status_code}"
    
#-----------------------------------------------------------------------------------

async def generate_activity_date(date_text):
    params = {
        "mode": "generate_activity_date",
        "date_text": date_text,
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        print(f"generate_activity_date: \n{response.text}")
    else:
        print(f"generate_activity_date: \n❌エラーが発生しました。: {response.status_code}")

#-----------------------------------------------------------------------------------
