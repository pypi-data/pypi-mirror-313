# Filters

class Filters:
    def __init__(self, func):
        self.func = func

    def __call__(self, client, message):
        """
        Make Filters callable like Pyrogram's filters.

        Args:
            client: The Telegram client instance.
            message: The message object.

        Returns:
            bool: Whether the filter condition is satisfied.
        """
        return self.func(client, message)

    def __and__(self, other):
        """
        Combine two filters with AND logic.
        """
        return Filters(lambda client, message: self(client, message) and other(client, message))

    def __or__(self, other):
        """
        Combine two filters with OR logic.
        """
        return Filters(lambda client, message: self(client, message) or other(client, message))

    def __invert__(self):
        """
        Negate a filter with NOT logic.
        """
        return Filters(lambda client, message: not self(client, message))

    @staticmethod
    def command(command):
        """
        Filter for matching specific bot commands.

        Args:
            command (str): The command to filter for (without the leading slash).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            hasattr(message, 'text') and message.text.startswith(f"/{command}"))

    # Use the following filters without calling them
    @staticmethod
    def private():
        """
        Filter for private chats (direct messages).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            getattr(message.chat, "type", None) == "private")

    @staticmethod
    def group():
        """
        Filter for group chats (supergroup or group).

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: 
            getattr(message.chat, "type", None) in {"group", "supergroup"})

    @staticmethod
    def all():
        """
        Filter for all chat types.

        Returns:
            Filters: A filter object.
        """
        return Filters(lambda client, message: True)
