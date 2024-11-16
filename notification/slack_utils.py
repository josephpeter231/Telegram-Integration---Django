import requests
from django.conf import settings

def send_slack_message(message):
    """
    Sends a message to the configured Slack channel.
    """
    webhook_url = settings.SLACK_WEBHOOK_URL
    payload = {'text': message}

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Slack: {e}")
