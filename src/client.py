import requests
import json
from constants import HEROKU_URL

LOCAL_URL = "http://0.0.0.0:8080/chat/"

data = {
    "message": "Does the PS12364199 part work with any PartSelect refrigerators?",
}


resp = requests.post(HEROKU_URL, data=json.dumps(data))
print(resp.text)
