import random
import sys
import time

import itchat
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity import Base
from entity import chatcontent


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
    record2db(msg['User']['NickName'], msg['Text'], reply)
    time.sleep(random.randint(3, 5))
    return reply or defaultReply


def record2db(from_u, recv_c, send_c):
    session = DBSession()
    try:
        record = chatcontent.ChatContent(time.strftime('%Y-%m-%d %H:%M:%S'), from_u, recv_c, send_c)
        session.add(record)
        session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    KEY = "4ef16f8363b749579eef202c81b3b8b4"
    USER_ID = "wxchat"
    ENGINE = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/chocolatedisco?charset=utf8", echo=False)
    Base.metadata.create_all(ENGINE)
    DBSession = sessionmaker(bind=ENGINE)
    itchat.auto_login(hotReload=False)
    itchat.run()
