# README: 
* pip install requests
* pip install python-dotenv
* make sure that you are using .env to store your secret variables 
* the program uses domain and api_token from the .env file
* domain = 'domain' ### the first part of your okta domain url ex. domain.okta.com ###
* api_token = '00...'

# get_reports
* this program will prompt you to submit an email
* the email is used to search for anyone that has the email in the profile.manager field in okta
* see this page for details https://developer.okta.com/docs/reference/user-query/
* the request will create an output.json file with the following:
    * manager
        * reports
            * reports
