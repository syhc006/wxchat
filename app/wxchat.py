import random
import time

import itchat
import requests

KEY = ""
USER_ID = "wxchat"


def get_response_v2(msg):
    apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": KEY,
            "userId": USER_ID
        }
    }
    try:
        r = requests.post(apiUrl, json=data).json()
        results = r.get('results')
        texts = list(filter(lambda x: x.get("resultType") == "text", results))
        response = texts[0].get("values").get("text")
        return response
    except:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = msg['Text']
    reply = get_response_v2(msg['Text'])
    time.sleep(random.randint(3, 5))
    return reply or defaultReply


def main():
    itchat.auto_login(hotReload=False)
    itchat.run()


if __name__ == "__main__":
    main()
