import os
import sys

import requests

from finter.ai.gpt.config import URL_NAME


def send_slack_message(webhook_url, message):
    formatted_message = f"```{message}```"
    headers = {"Content-Type": "application/json"}
    data = {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": formatted_message}}
        ]
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    return response.text


def get_logs():
    diff_script_path = os.path.join(os.path.dirname(__file__), "tag_diff_logs.sh")
    with os.popen(f"bash {diff_script_path}") as p:
        output = p.read()
    return output

def get_tag(output):
    tag = None
    for line in output.split("\n"):
        if "Most recent tag" in line:
            tag = line.split(": ")[-1]
            break
    return tag

def read_log_file():
    log_output = get_logs()
    recent_tag = get_tag(log_output)
    return log_output, recent_tag

def generate_release_note(log_output, user_prompt=""):
    url = f"http://{URL_NAME}:8282/release_note"
    
    data = {"logs": log_output, "user_prompt": user_prompt}
    response = requests.post(url, json=data)
    return response.json()["result"]


if __name__ == "__main__":
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    log_output, recent_tag = read_log_file()
    
    if "rc" in recent_tag.split(".")[-1]:
        pass
    else:
        rel = generate_release_note(log_output, user_prompt)
        print(rel)

        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        send_slack_message(slack_webhook_url, rel)
