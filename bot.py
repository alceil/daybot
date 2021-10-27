import slack
import os
from datetime import date
from pathlib import Path
from flask import Flask
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print(text)
    if user_id != None and BOT_ID != user_id:
        if 'what day is it?' in text.lower()  :
            today =date.today().strftime("%A")
            print(today)
            client.chat_postMessage(channel=channel_id,text=f"Its {today}")


if __name__ == "__main__":
    app.run(debug=True)