# start with README.md
# this program is to get the reporting chain for a manager
# start the program and use the terminal to enter a manager's email address
# another option is to set the manager value in the .env file
# the program returns the reports to terminal
# the program uses a dictionary to store the reports  
# the program writes the dictionary to output.json at the end

import os

import json

import requests

from dotenv import find_dotenv, load_dotenv

# import datetime module for now() 
import datetime

# find the .env file
dotenv_path = find_dotenv()

# load entries as environment variables 
load_dotenv(dotenv_path)

# to view the variables use 'print os.environ'

print(':' * 100)

# create empty dictionary
report_dict = {
    }

index = 0

# use now() to get current time 
current_time = datetime.datetime.now() 
 
# get variables from .env file
domain = os.getenv("domain")
api_token = os.getenv("api_token")

# set headers
headers = {
    'Accept': 'application/json',
    'Authorization': f"SSWS {api_token}",
}

# ask user to input manager email
manager = input('enter manager email here: ')
# alternatively set the manager value in the .env file and use os.getenv("manager") below
# manager = os.getenv("manager") //// use this when setting the manager value in the .env file. remove input prompt.

def func_set_endpoint_url(manager):
    # requests.utils.quote() is to URI encode user_email
    # this is necessary when working with international or special characters
    manager_uri = requests.utils.quote(manager)

    # generate the url for the request 
    endpoint_url = f'https://{domain}.okta.com/api/v1/users?search=profile.manager eq "{manager_uri}"'

    return endpoint_url

endpoint_url = func_set_endpoint_url(manager)

def func_get_request(endpoint_url):
    # get first reports here
    response = requests.get(endpoint_url, headers=headers)

    # set response json as data
    data = response.json()

    # Extract the profile.email values from each object
    emails = [obj["profile"]["email"] for obj in data]
    return emails        

emails = func_get_request(endpoint_url)

email_len = len(emails)

# add top level manager to dictionary
report_dict[manager] = emails

# print top level manager details
print('current_time: ', current_time) 
print('url: ', endpoint_url)
print('email_len: ', email_len)
print('emails: ', emails)
print('*'*100)

def func_print(endpoint_url, emails, email_len):
    print('manager: ', email)
    print('endpoint_url: ', endpoint_url)
    if email_len == 0:
        print('alert: records not found')
    else:
        print('email_len: ', email_len)
        print('emails: ', emails)
    print('*'*100)

def func_repeater(email):
    endpoint_url = func_set_endpoint_url(email)
    emails = func_get_request(endpoint_url)
    email_len = len(emails)
    func_print(endpoint_url, emails, email_len)
    return emails

# this gets the top level reports and their reports
# copy and nest the following conditional for each additional level 
for email in emails:
    emails = func_repeater(email)
    # add record to dictionary 
    report_dict[email] = emails

print(report_dict)

# write dictionary to output.json
with open("output.json", "w") as outfile: 
    json.dump(report_dict, outfile)
