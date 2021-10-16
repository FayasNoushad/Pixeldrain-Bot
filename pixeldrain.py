import requests


def upload_file(file, name="media"):
    response = requests.put(
        "https://pixeldrain.com/api/files/"+name,
        data={
            "name": name,
            "anonymous": True,
            "file": file
        }
    )
    if response.status_code != 200:
        return False
    else:
        info = requests.get(f"https://pixeldrain.com/api/file/{response.json()['id']}/info").json()
        return info
