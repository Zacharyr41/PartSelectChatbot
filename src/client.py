import requests
import json
from constants import HEROKU_URL

LOCAL_URL = "http://0.0.0.0:8080/chat/"

data = {
    "message": "Does PartSelect generally have good fridges?",
}


resp = requests.post(LOCAL_URL, data=json.dumps(data))
print(resp.text)
