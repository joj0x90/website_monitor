import requests
import time, threading

import config
import target

wait_seconds = 60
verbose = False


def check_targets(target_list):
        for target in target_list:
                [correct, status] = target.check_status()
                if verbose:
                        target.print_target()
                        print(correct)
                if(not(correct)):
                        target.notification.notify(target.host.url, status)

        threading.Timer(wait_seconds, check_targets, args=[target_list]).start()

if __name__ == "__main__":
        target_list = config.parse("config.json")
    
        check_targets(target_list)