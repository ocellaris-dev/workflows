import json
import requests

def send_toot(text, credential):
    message = {'i': credential, 'text': text}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    print(info)
    return info['createdNote']['id']


def send_reply(text, credential, replyid):
    message = {'i': credential, 'text': text, 'replyId': replyid}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']
