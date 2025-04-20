import requests

data = {
    "user_id":"Hello Postgrest",
    "text":"This is Fastapi"
}

url = "https://test-postgrest-fastapi.onrender.com/new_text"

header = {"Accept":"application/json", "Content-Type":"application/json"}

try:
    req = requests.post(url=url, headers=header, json=data)
    print(req.text)
except Exception as e:
    print(e)
