import json
import subprocess
import os
import time
import string
import random

import requests

credential = os.getenv("MISSKEY_CREDENTIAL")


def gen_str(size=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


def get_package_info():
    res = requests.get("https://raw.githubusercontent.com/misskey-dev/misskey/develop/package.json")
    info = json.loads(res.text)
    return info["version"]


def get_misskey_info():
    res = requests.post("https://stella.ocellaris.dev/api/meta")
    info = json.loads(res.text)
    return info["version"]


def slice_version(ver):
    sliced = ver.split(".")
    if len(sliced) >= 4:
        new_ver = ver.split("-");
        new_tuple = new_ver[0].split(".")
        return tuple(map(int, new_tuple))
    else:
        return tuple(map(int, sliced))


def update_compair(repo_t, ins_t):
    repo = slice_version(repo_t)
    ins = slice_version(ins_t)
    if repo[0] > ins[0]:
        return True
    elif repo[1] > ins[1]:
        return True
    elif repo[2] > ins[2]:
        return True
    else:
        return False


def get_time():
    tm = time.localtime(time.time())
    return time.strftime("%H:%M", tm) + " (KST)"


def send_toot(text, credential):
    message = {'i': credential, 'text': text}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']


def send_reply(text, credential, replyid):
    message = {'i': credential, 'text': text, 'replyId': replyid}
    res = requests.post("https://stella.ocellaris.dev/api/notes/create", json=message)
    info = json.loads(res.text)
    return info['createdNote']['id']

def send_update_message(repo, ins):
    current_time = get_time()
    message = "[Stella Update]\n새로운 버전이 감지되었습니다.\n Misskey " + ins + " -> " + repo + "\n" + current_time + " ~" + "\n*본 업데이트는 자동으로 진행됩니다."
    return send_toot(message, credential)


def send_done_message(replyid):
    send_reply("✅ 업데이트가 완료되었습니다.", credential, replyid)


def send_fail_message(replyid):
    send_reply("❌ 업데이트에 실패했습니다.", credential, replyid)


def get_update():
    repo_ver = get_package_info()
    ins_ver = get_misskey_info()
    print("package.json Version ->")
    print(repo_ver)
    print("Installed Misskey version ->")
    print(ins_ver)
    if update_compair(repo_ver, ins_ver):
        print("YES")
        print("New version detected. Take some coffee!")
        print("-> Send update notifications")
        repid = send_update_message(repo_ver, ins_ver)
        subprocess.call(["sudo", "timedatectl", "set-timezone", "UTC"])
        date = time.strftime('%Y%m%d%H%M%S')
        random_str = gen_str()
        snapshot_name = 'stella' + '-' + date + '-' + random_str
        print("-> SNAPSHOT_NAME:", snapshot_name)
        subprocess.call(["gcloud", "compute", "snapshots", "create", snapshot_name, '--source-disk', 'stella', '--source-disk-zone=asia-northeast2-b',"--storage-location=asia-northeast2", "-q"])
        print("-> Start Update")
        subprocess.call(["gcloud", "compute", "ssh", '--zone=asia-northeast2-b', 'stella', '--command','"sudo bash /home/caipira113/update.sh"', "--ssh-key-expire-after=30m", "-q"])
        print("-> Sleep for 15.5 seconds")
        time.sleep(15.5)
        print("-> Check if update is done")
        new_ins_ver = get_misskey_info()
        if repo_ver == new_ins_ver:
            print("Update Success.")
            send_done_message(repid)
            exit()
        else:
            print("Update failed.")
            send_fail_message(repid)
            exit(255)
    else:
        print("Misskey is up-to-date!")
        exit()


get_update()
