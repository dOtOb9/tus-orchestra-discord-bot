import requests
import json
from os import getenv


URL = getenv("SPREADSHEET_EXEC_URL")

headers = {
    "Content-Type" : "application/json"
}

async def user_post(json_data):

    response = requests.post(URL, headers=headers, data=json.dumps(json_data))

    if response.status_code == 200:
        return response.text
    else:
        return f"❌エラーが発生しました。: {response.status_code}"
    
#-----------------------------------------------------------------------------------

async def generate_activity_date(date_text):
    json_data = {
        "mode": "generate_activity_date",
        "date_text": date_text,
    }

    requests.post(URL, headers=headers, data=json.dumps(json_data))

#-----------------------------------------------------------------------------------

async def can_send_activity_dm(id, Bool):
    json_data = {
        "mode": "belong_contact_list",
        "id": str(id),
        "bool": str(Bool).upper(),
    }

    requests.post(URL, headers=headers, data=json.dumps(json_data))

