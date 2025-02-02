# website_monitor

This is a simple monitoring system for checking the http-return code of any website. \
Additionally you can specify a notification per email or slack for any website, so that you receive a message, when a specific website is unreachable.

## used python-packages
You have to install the following packages, to run the application:
* requests ```pip install requests```
+ dotenv ```pip install python-dotenv```
* pyinstaller ```pip install pyinstaller``` (for building an executable)

## Config-file
You just have to adapt the config-file according to your needs. \
The config file is a basic json-file with following structure: 
``` json
{
  "refresh": 30,
  "targets": [
    {
      "url": "https://example.com/",
      "status": 200,
      "notification-type": "email",
      "method": "user@company.com"
    },
    {
      "url": "https://test.example.com/",
      "status": 200,
      "notification-type": "slack"
    }
  ]
}
```
First node is refresh, this sets the time between each poll, dont set it too small, since the servers might block you since it would behave like a DOS-attack.\
If it is not set, the default is 5 minutes (300 secs). \
The structure is just a list of targets, which have the following parameters:
* **url:** the full website's URL
* **status:** the expected http status code (in case you want to check, if a website returns something other than boring 200)
* **notification_type:** currently only 'email' or 'slack' exist
* **method:** for email its the email-adress under which you want to receive the information, for slack its the App's webhook.

App-specifics are managed using a .env file, which is structured like this:
``` .env
APP_NAME="Website-Monitor"

# Flag for printing debug statements: false | true
APP_DEBUG="true"

# smtp email server
MAIL_ADDRESS="noreply@domain.com"
MAIL_USER="<user>"
MAIL_PASSWORD="<password>"
MAIL_SERVER="mail.server.com"
SMTP_PORT=1234

# Slack-configuration
SLACK_WEBHOOK="https://hooks.slack.com/services/<Webhook>"

# for publishing the docker-mage
DOCKER_USERNAME="<docker-username>"
DOCKER_TOKEN="<docker PAT>"
```
this specifies some basic App-data and the smtp-mail account used for sending email-notifications:
* **mail_address:** your mail-address (will be shown as sender in the mail)
* **mail_user:** The username of your mailserver
* **mail_pass:** The password for your mail_user
* **mail_server:** Your mail-server's outgoing smtp address
* **mail_port:** the mail-server's smtp port (currently only unencrypted) 

### Slack-configuration
To configure your slack webhook, go to this [site](https://api.slack.com/messaging/webhooks), create a new App and give it the webhook feature, copy the webhook url and create a new channel in your slack workspace. \
You can then select this channel, so that every message over this webhook arrives in this channel.

## Building
You can manage the build step using a Justfile.
* ```just run``` will run the programm locally
* ```just build-exec-locally``` will build an executable in dist/main
* ```just build-targz``` will package the executable together with the example config and .env-files as one *.tar.gz file
* ```just build-images``` will build the docker images for the current version (set in .env-file) and latest but wont push it to your docker account (specify docker-credentials in .env-file)
* ```just publish-current-image``` will push the image with the current version number to your docker repository
* ```just publish-latest-image``` will push the image with the tag "latest" to your defined docker repository

## Further development
I would really like to add a webserver with a simple GUI possibly using flask, to make it easier to manage the config file and see, which targets are currently in which state. \
I would like to add a timer, that the websites will be pinged once a minute and only if a website does not have the expected return type for three rounds (minutes) to then send the notification, in case you have network issues at the moment of the first request.