import requests


def upload(name, file):
    response = requests.put(
        "https://pixeldrain.com/api/files",
        data={
            "name": name,
            "anonymous": True,
            "file": file
        }
    )
    if response.status_code != 200:
        return False
    else:
        info = requests.get(f"https://pixeldrain.com/api/file/{response.json()["id"]}/info").json()
        return info
