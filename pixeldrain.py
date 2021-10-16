import requests


def upload_file(file):
    response = requests.post(
        "https://pixeldrain.com/api/file",
        data={"anonymous": True},
        files={"file": open(file, "rb")}
    )
    if response.status_code != 200:
        return False, response.status_code
    else:
        info = requests.get(f"https://pixeldrain.com/api/file/{response.json()['id']}/info").json()
        return info, response.status_code
