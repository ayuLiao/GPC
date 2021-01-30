import requests

SESSION = None

def get_session():
    global SESSION
    if SESSION is None:
        SESSION = requests.session()
    return SESSION

def get_user_agent():
    return {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
    }