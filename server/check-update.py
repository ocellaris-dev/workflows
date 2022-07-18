import utils
import github

if not utils.get_package_info() == get_misskey_info():
    print("New version detected.")
    github.trigger_actions()
else:
    print("Misskey is up-to-date!")
    exit()
