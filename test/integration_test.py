import json
import sys
import requests

URL = 'http://localhost:5006/'

def main():
    imgs = sys.argv[1:]
    if len(imgs) == 0:
        print('No input images')
        return

    print('Uploading images...')
    ids = []
    for im in imgs:
        headers = {
            'Content-Type': 'image/' + im.split('.')[-1]
        }
        with open(im, 'rb') as f:
            r = requests.post(URL + 'image', headers=headers, data=f)
            ids.append(int(r.text))

    print('Sorting images...')
    headers = {'Content-Type': 'application/json'}
    r = requests.post(URL + 'image/sort', headers=headers, data=json.dumps(ids))
    print(r.content)


if __name__ == '__main__':
    main()
