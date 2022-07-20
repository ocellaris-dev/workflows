import subprocess

import utils


def build_snapshot():
    utc_str = utils.get_snapshot_utc_time()
    random_str = utils.gen_str()
    snapshot_name = "stella-asia-northeast2-b" + "-" + utc_str + "-" + random_str
    subprocess.call(["gcloud", "compute", "snapshots", "create", snapshot_name, '--source-disk', 'stella', '--source-disk-zone=asia-northeast2-b', "--storage-location=asia-northeast2", "-q"])
    return snapshot_name


def update_server():
    return subprocess.call(["gcloud", "compute", "ssh", "--zone", "asia-northeast2-b", "stella", "--command", "sudo bash /home/caipira113/update.sh", "--ssh-key-expire-after=30m", "-q"])
