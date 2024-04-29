import requests
import json
from PIL import Image
from io import BytesIO
from csv import insert


api_img = 'https://api.unsplash.com/photos/random?client_id=5mMofpL6vwFnjXrcJDWvSGGutw3A4kGMZNfVeavueaQ'
api_gif = 'https://api.giphy.com/v1/gifs/random?api_key=QD6CRkEdp33paK1SNd937mXkiHfFUhgJ&tag=electronics&rating=g'


# функция для запроса фото и гиф
def take_image(type):
    if type == 'image':
        response_img = requests.get(api_img).json()
        if not response_img:
            print("Ошибка выполнения запроса:")
            print(response_img)
            print("Http статус:", response_img.status_code, "(", response_img.reason, ")")
        else:
            with open('data/latest/latest_unsplash.json', 'w') as site:
                json.dump(response_img, site, indent='    ', separators=(',', ': '))
            insert(response_img['id'], response_img['slug'], response_img['description'], response_img['updated_at'])
            response_img = response_img['urls']['small']
            img = Image.open(BytesIO(requests.get(response_img).content))
            img.save('data/latest/latest.png', 'PNG')
            return response_img
    elif type == 'gif':
        response_gif = requests.get(api_gif).json()
        if not response_gif:
            print("Ошибка выполнения запроса:")
            print(response_gif)
            print("Http статус:", response_gif.status_code, "(", response_gif.reason, ")")
        else:
            with open('data/latest/latest_giphy.json', 'w') as site:
                json.dump(response_gif, site, indent='    ', separators=(',', ': '))
            response_gif = requests.get(response_gif['data']['images']['original']['url']).content
            gif = Image.open(BytesIO(response_gif))
            gif.save('data/latest/latest.gif', 'GIF')
            return response_gif