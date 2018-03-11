from sqlalchemy import Column, Integer, String

from entity import Base


class ChatContent(Base):
    def __init__(self, chat_t, from_u, recv_c, send_c):
        self.chat_t = chat_t
        self.from_u = from_u
        self.recv_c = recv_c
        self.send_c = send_c

    __tablename__ = 'chat_content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_t = Column(String(64), unique=False, nullable=False)
    from_u = Column(String(64), unique=False, nullable=False)
    recv_c = Column(String(1024), unique=False, nullable=False)
    send_c = Column(String(1024), unique=False, nullable=False)
