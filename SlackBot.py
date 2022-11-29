import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


#Clients Dictionary
clients = {
    "amosweislib" : ["AMFRSH", "SOWIT"]
}

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Flask app
app = Flask(__name__)

# Initialize Slack event adapter
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

# Create a slack client
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']

# Create an event listener for "message" events and message a mention
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id and any(cust in text for cust in clients['amosweislib']):
        client.chat_postMessage(channel=channel_id, text="<@amosweislib>")

if __name__ == "__main__":
    app.run(debug=True)