import requests
import json
from PIL import Image
from io import BytesIO


api_img = 'https://api.unsplash.com/photos/random?client_id=5mMofpL6vwFnjXrcJDWvSGGutw3A4kGMZNfVeavueaQ'

# функция для запроса фото и гиф
def take_image(type):
    if type == 'image':
        unsplash_im_url = requests.get(api_img).json()
        if not unsplash_im_url:
            print("Ошибка выполнения запроса:")
            print('https://api.unsplash.com/photos/random?client_id=5mMofpL6vwFnjXrcJDWvSGGutw3A4kGMZNfVeavueaQ')
            print("Http статус:", unsplash_im_url.status_code, "(", unsplash_im_url.reason, ")")
        else:
            with open('data/latest/latest_unsplash.json', 'w') as site:
                json.dump(unsplash_im_url, site, indent='    ', separators=(',', ': '))
            unsplash_im_url = unsplash_im_url['urls']['full']
            img = Image.open(BytesIO(requests.get(unsplash_im_url).content))
            img.save('data/latest/latest.png', 'PNG')
    elif type == 'gif':
        response_gif = requests.get('https://api.giphy.com/v1/gifs/random?api_key=QD6CRkEdp33paK1SNd937mXkiHfFUhgJ&tag=electronics&rating=g').json()
        with open('data/latest/latest_giphy.json', 'w') as site:
            json.dump(response_gif, site, indent='    ', separators=(',', ': '))
        response_gif = requests.get(response_gif['data']['images']['original']['url']).content

        print(response_gif)
        gif = Image.open(BytesIO(response_gif))
        print(gif)
        gif.save('data/latest/latest.gif', 'GIF')
