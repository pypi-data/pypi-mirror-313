import requests

def get_random_doujin():
    # Obtener la URL redirigida desde /random
    random_url = "https://nhentai.net/random"
    response = requests.get(random_url)
    if response.status_code == 200:
        # Extraer el ID del doujin de la URL redirigida
        doujin_url = response.url
        doujin_id = doujin_url.split('/')[-2]
        return doujin_id
    else:
        return None

def get_doujin_info(doujin_id):
    url = f"https://nhentai.net/api/gallery/{doujin_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_cover_image_url(doujin_info):
    media_id = doujin_info['media_id']
    cover = doujin_info['images']['cover']
    cover_extension = 'jpg' if cover['t'] == 'j' else 'png'
    cover_url = f"https://t3.nhentai.net/galleries/{media_id}/cover.{cover_extension}"
    return cover_url




