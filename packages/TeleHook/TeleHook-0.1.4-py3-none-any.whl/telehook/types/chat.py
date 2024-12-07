# Chats

class Chat:
    def __init__(self, chat_data):
        self.id = chat_data.get('id')
        self.type = chat_data.get('type')
        self.title = chat_data.get('title', None)
        self.username = chat_data.get('username', None)
