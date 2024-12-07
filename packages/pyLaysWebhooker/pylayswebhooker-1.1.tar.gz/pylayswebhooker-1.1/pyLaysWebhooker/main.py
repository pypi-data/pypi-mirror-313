import requests
import json
def pyInstantSend(webhookURL, message):
    stupid = {'content': message}
    requests.post(webhookURL,stupid)
def pySend():
    webhookURL = input('What is the webhook URL? ')
    message = input('Type in your message. ')
    messageToJSON = {'content': message}
    requests.post(webhookURL,messageToJSON)