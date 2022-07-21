import json
import requests


def send_toot(text, credential, local=False):
    message = {'i': credential, 'text': text, 'localOnly': local}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']


def send_reply(text, credential, replyid, local=False):
    message = {'i': credential, 'text': text, 'replyId': replyid, 'localOnly': local}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']
