import requests

import config
import target      

if __name__ == "__main__":
    target_list = config.parse("config.json")
    
    for target in target_list:
        target.print_target()
        [correct, status] = target.check_status()
        print(correct)
        if(not(correct)):
                target.notification.notify(target.host.url, status)