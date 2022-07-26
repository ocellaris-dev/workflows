import json
import string
import time
import random
import datetime
import requests


def get_package_info():
    res = requests.get("https://raw.githubusercontent.com/ocellaris-dev/stella/develop/package.json")
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
    stt = time.strftime("%H:%M", tm)
    return f"{stt} (UTC+9)"


def get_snapshot_utc_time():
    utc = datetime.datetime.utcnow()
    return utc.strftime("%Y%m%d%H%M%S")
