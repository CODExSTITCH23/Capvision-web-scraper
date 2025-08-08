import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"  

def notify_slack(message):
    if not SLACK_WEBHOOK_URL or 'hooks.slack.com' not in SLACK_WEBHOOK_URL:
        print("Slack webhook URL is not set. Skipping notification.")
        return
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"Slack notification failed: {response.text}")
    except Exception as e:
        print(f"Slack notification error: {e}") 