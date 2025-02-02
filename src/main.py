import requests
import time, threading, os

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
        # Read the version string from the version_file
        with open("version_file", "r") as file:
                version = file.read().strip()

        # Set the environment variable (optional, if needed)
        os.environ["APP_VERSION"] = version

        [wait_seconds, target_list] = config.parse("config.json")
        if config.GLOBAL_VERBOSE:
                print(f"starting Website-Monitor {os.environ.get("APP_VERSION", "0.1")} ")
                print(f"refresh every {wait_seconds} seconds")
    
        check_targets(target_list)