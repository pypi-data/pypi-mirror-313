# Message

from telehook.types.user import User
from telehook.types.chat import Chat

class Message:
    def __init__(self, client, message_data):
        self.client = client
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        self.chat = Chat(message_data.get('chat', {}))
        self.from_user = User(message_data.get('from', {}))

    def reply_text(self, text):
        """
        Sends a reply message to the same chat.

        Args:
            text (str): The text of the reply message.
        """
        self.client.method.send_message(chat_id=self.chat.id, text=text)


class EditedMessage:
    def __init__(self, client, message_data):
        self.client = client
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        self.chat = Chat(message_data.get('chat', {}))
        self.from_user = User(message_data.get('from', {}))

    def reply_text(self, text):
        """
        Sends a reply message to the same chat.

        Args:
            text (str): The text of the reply message.
        """
        self.client.method.send_message(chat_id=self.chat.id, text=text)
