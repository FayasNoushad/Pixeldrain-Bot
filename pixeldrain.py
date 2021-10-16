import requests


def upload_file(file):
    response = requests.post(
        "https://pixeldrain.com/api/file",
        data={"anonymous": True},
        files={"file": open(file, "rb")}
    )
    if response.json()["success"] is True:
        info = requests.get(f"https://pixeldrain.com/api/file/{response.json()['id']}/info")
        return info
    else:
        return response
