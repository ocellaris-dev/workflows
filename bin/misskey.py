import json
import requests

def send_toot(text, credential, local):
    if not local:
        message = {'i': credential, 'text': text}
    else:
        message = {'i': credential, 'text': text, 'localOnly': True}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']


def send_reply(text, credential, replyid, local):
    if not local:
        message = {'i': credential, 'text': text, 'replyId': replyid}
    else:
        message = {'i': credential, 'text': text, 'replyId': replyid, 'localOnly': True}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']
