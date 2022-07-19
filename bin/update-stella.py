import os
import subprocess
import sys
import time

import misskey
import utils
import stella

credential = os.getenv("MISSKEY_CREDENTIAL")
debug = False

def send_update_message(repo, ins):
    current_time = utils.get_time()
    message = "[Stella Update]\n" + " 새로운 버전이 감지되었습니다.\n Misskey " + ins + " -> " + repo + "\n" + current_time + "\n*본 업데이트는 자동으로 진행됩니다."
    return misskey.send_toot(message, credential, debug)


def send_done_message(replyid):
    misskey.send_reply("✅ 업데이트가 완료되었습니다.", credential, replyid, debug)


def send_fail_message(replyid):
    misskey.send_reply("❌ 업데이트에 실패했습니다.", credential, replyid, debug)


def get_update():
    repo_ver = utils.get_package_info()
    ins_ver = utils.get_misskey_info()
    print("package.json Version ->")
    print(repo_ver)
    print("Installed Misskey version ->")
    print(ins_ver)
    if repo_ver != ins_ver:
        print("-> New version detected. Take some coffee!")
        print("-> Send update notifications")
        repid = send_update_message(repo_ver, ins_ver)
        snapshot_name = stella.build_snapshot()
        print("-> SNAPSHOT_NAME: ", snapshot_name)
        print("-> Starting Update")
        stella.update_server()
        #subprocess.call(["sudo", "timedatectl", "set-timezone", "UTC"])
        #date = time.strftime('%Y%m%d%H%M%S')
        #random_str = utils.gen_str()
        #snapshot_name = 'stella' + '-' + date + '-' + random_str
        #print("-> SNAPSHOT_NAME:", snapshot_name)
        #subprocess.call(["gcloud", "compute", "snapshots", "create", snapshot_name, '--source-disk', 'stella', '--source-disk-zone=asia-northeast2-b', "--storage-location=asia-northeast2", "-q"])
        #print("-> Start Update")
        #subprocess.call(["gcloud", "compute", "ssh", "--zone", "asia-northeast2-b", "stella", "--command", "sudo bash /home/caipira113/update.sh", "--ssh-key-expire-after=30m", "-q"])
        print("-> Sleep for 15.5 seconds")
        time.sleep(15.5)
        print("-> Check if update is done")
        new_ins_ver = utils.get_misskey_info()
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

def debug_functions():
    print("[Utils Test]")
    print("get_time-> ", uitls.get_time())
    print("gen_str-> ", utils.gen_str())
    print("get_snapshot_utc_time-> ", get_snapshot_utc_time())
    print("[Toot-Notification Test]")
    repo_ver = utils.get_package_info()
    ins_ver = utils.get_misskey_info()
    repid = send_update_message(repo_ver, ins_ver)
    send_done_message(repid)
    send_fail_message(repid)
    print("[Snapshot Build Test]")
    snapshot_name = stella.build_snapshot()
    print("-> SNAPSHOT_NAME: ", snapshot_name)

if len(sys.argv) > 1 and sys.argv[1] == "-d":
    debug = True
    print("debug mode enabled. starting feature sequence.")
    debug_functions()
else:
    get_update()
