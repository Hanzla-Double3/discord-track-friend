import requests
from datetime import datetime
import os
import time
import json
from Secrets import Secret

sec = Secret()

def send_pushbullet_notification(title, body):
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Access-Token': sec["PUSH_BULLET_TOKEN"],
        'Content-Type': 'application/json'
    }
    data = {'type': 'note', 'title': title, 'body': body}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print('Notification sent successfully.')
    else:
        print(
            f'Failed to send notification. Status code: {response.status_code}'
        )
        print(response.json())


url = "https://discord.com/api/v9/users/@me/relationships"
headers = {
    "Authorization": sec["DISCORD_TOKEN"],
    "Content-Type": "application/json"
}
first = 1
while (1):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            send_pushbullet_notification(f"Error responce code {response.status_code}", response.text)
            exit(-1)
        
        response = response.json()
        
        found = 0
        for user in response:
            if user["id"] == sec["USERID"]:
                found = 1
                with open("log.txt", "a") as f:
                    f.write(f"{datetime.now()}: {str(user)}")  
                if first == 1:
                    send_pushbullet_notification("Initiated and found", "200")
                    first = 0
        if found == 0:
            with open("log.txt", "a") as f:
                f.write(f"{datetime.now()}: User not found")

            send_pushbullet_notification("Not found", "404")

        time.sleep(60 * 30)
    except Exception as e:
        send_pushbullet_notification("Error", str(e))
        print(str(e))
        exit(-1)
