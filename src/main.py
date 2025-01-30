import requests
import time, threading

import config
import target

wait_seconds = 5 * 60
verbose = False


def check_targets(target_list):
        for target in target_list:
                [correct, status] = target.check_status()
                if verbose:
                        target.print_target()
                        print(correct)
                if(not(correct)):
                        if not(target.already_notified):
                                target.already_notified = True
                                target.notification.notify(target.host.url, status)
                        else:
                                print("already notified user")

        threading.Timer(wait_seconds, check_targets, args=[target_list]).start()

if __name__ == "__main__":
        print("starting Website-Monitor")
        [wait_seconds, target_list] = config.parse("config.json")
        print(f"refresh every {wait_seconds} seconds")
    
        check_targets(target_list)