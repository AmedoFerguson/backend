import requests

IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"
IMGUR_CLIENT_ID = "cae9fdb8403f3a4"  # Вставьте свой Client ID

def upload_image_to_imgur(image_file):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    response = requests.post(IMGUR_UPLOAD_URL, headers=headers, files={"image": image_file})

    if response.status_code == 200:
        data = response.json()
        return data["data"]["link"]  # Возвращаем URL загруженного изображения
    else:
        raise Exception(f"Imgur upload failed: {response.status_code}, {response.text}")
