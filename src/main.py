import requests
import time, threading

import config
import target

wait_seconds = 5 * 60

def check_targets(target_list):
        for target in target_list:
                [correct, status] = target.check_status()
                if config.GLOBAL_VERBOSE:
                        target.print_target()
                        print(correct)
                if(not(correct)):
                        if not(target.already_notified):
                                target.already_notified = True
                                target.notification.notify(target.host.url, status)
                        else:
                                if config.GLOBAL_VERBOSE:
                                        print(f"already notified user about {target.host.url}")
                elif(correct and target.already_notified):
                        # reset already_notified when target is online again
                        target.already_notified = False

        threading.Timer(wait_seconds, check_targets, args=[target_list]).start()

if __name__ == "__main__":
        [wait_seconds, target_list] = config.parse("config.json")
        if config.GLOBAL_VERBOSE:
                print("starting Website-Monitor")
                print(f"refresh every {wait_seconds} seconds")
    
        check_targets(target_list)