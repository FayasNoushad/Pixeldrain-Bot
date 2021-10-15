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
        return True
    
