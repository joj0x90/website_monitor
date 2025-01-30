# website_monitor

This is a simple monitoring system for checking the http-return code of any website. \
Additionally you can specify a notification per email or slack for any website, so that you receive a message, when a specific website is unreachable.

## used python-packages
You have to install the following packages, to run the application:
* requests ```pip install requests```

## Config-file
You just have to adapt the config-file according to your needs. \
The config file is a basic json-file with following structure: 
``` json
{
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
      "notification-type": "slack",
      "method": "<WIP>"
    }
  ]
}
```

The structure is just a list of targets, which have the following parameters:
* **url:** the full website's URL
* **status:** the expected http status code (in case you want to check, if a website returns something other than boring 200)
* **notification_type:** currently only 'email' or 'slack' exist
* **method:** for email its the email-adress under which you want to receive the information, for slack its the App's webhook.

App-specifics are managed using a .env file, which is structured like this:
``` .env
APP_NAME="Website-Monitor"
APP_VERSION="0.1"

# smtp email server
MAIL_ADDRESS="noreply@domain.com"
MAIL_USER="<user>"
MAIL_PASSWORD="<password>"
MAIL_SERVER="mail.server.com"
SMTP_PORT=1234

# Slack-configuration
SLACK_WEBHOOK="https://hooks.slack.com/services/<Webhook>"
```
this specifies some basic App-data and the smtp-mail account used for sending email-notifications:
* **mail_address:** your mail-address (will be shown as sender in the mail)
* **mail_user:** The username of your mailserver
* **mail_pass:** The password for your mail_user
* **mail_server:** Your mail-server's outgoing smtp address
* **mail_port:** the mail-server's smtp port (currently only unencrypted) 

## Further development
I would really like to add a webserver with a simple GUI possibly using flask, to make it easier to manage the config file and see, which targets are currently in which state. \
I would like to add a timer, that the websites will be pinged once a minute and only if a website does not have the expected return type for three rounds (minutes) to then send the notification, in case you have network issues at the moment of the first request.