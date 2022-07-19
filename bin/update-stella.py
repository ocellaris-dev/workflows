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
    if not debug:
        message = "[Stella Update]\n" + " 새로운 버전이 감지되었습니다.\n Misskey " + ins + " -> " + repo + "\n" + current_time + "\n*본 업데이트는 자동으로 진행됩니다."
    else:
        message = "[Stella Update]\n" + " 새로운 버전이 감지되었습니다.\n Misskey " + ins + " -> " + repo + "\n" + current_time + "\n*본 업데이트는 자동으로 진행됩니다.\n**[본 메시지는 자동 업데이트 시스템을 테스트하기 위한 디버그 메시지입니다. 업데이트가 진행되지 않으니 무시하시길 바랍니다.]**"
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
    print("get_time-> ", utils.get_time())
    print("gen_str-> ", utils.gen_str())
    print("get_snapshot_utc_time-> ", utils.get_snapshot_utc_time())
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
    print("debug mode enabled. starting feature test sequence.")
    debug_functions()
else:
    get_update()
