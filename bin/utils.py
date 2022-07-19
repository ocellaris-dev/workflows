import json
import string
import time
import random
import requests


def get_package_info():
    res = requests.get("https://raw.githubusercontent.com/misskey-dev/misskey/develop/package.json")
    info = json.loads(res.text)
    return info["version"]


def get_misskey_info():
    res = requests.post("https://stella.ocellaris.dev/api/meta")
    info = json.loads(res.text)
    return info["version"]


def gen_str(size=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


def get_time():
    tm = time.localtime(time.time())
    return time.strftime("%H:%M", tm) + " (KST)"
