

import requests
import logging
import os
import importlib

from telehook.types import Message
from telehook.filters import Filters
from telehook.methods import Methods


BOT_TOKEN = "7612816971:AAFeh2njq6BcCEi-xTN5bLE7qKnAnzvvHMY"
CHAT_ID = 7869684136


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeleClient:
    def __init__(self, token, url=None, plugins_path=None):
        """
        Initialize the TeleClient.

        Args:
            token (str): Telegram Bot API token.
            url (str): Optional webhook URL for the bot.
            plugins (dict): Dictionary specifying plugin configuration (e.g., {"root": "server.plugins"}).
        """
        self.token = token
        self.url = url
        self.api_url = f"https://api.telegram.org/bot{self.token}/"
        self.message_handlers = []
        self.edited_message_handlers = []
        self.method = Methods(self)

        if plugins and "root" in plugins:
            self.load_plugins(plugins["root"])

    def load_plugins(self, root_path):
        """
        Dynamically load plugin modules from the specified root path.

        Args:
            root_path (str): Root path for plugins, e.g., "server.plugins".
        """
        try:
            # Import the root module
            root_module = importlib.import_module(root_path)
            # List all modules in the root
            root_dir = os.path.dirname(root_module.__file__)
            for filename in os.listdir(root_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = f"{root_path}.{filename[:-3]}"
                    importlib.import_module(module_name)
                    logger.info(f"Loaded plugin: {module_name}")
        except Exception as e:
            logger.error(f"Failed to load plugins from {root_path}: {e}")

    def setup_webhook(self):
        response = requests.post(
            f"{self.api_url}setWebhook",
            data={"url": self.url}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def process_update(self, update):
        """
        Process an incoming update.

        Args:
            update (dict): The Telegram webhook update.
        """
        if "message" in update:
            try:
                message = Message(self, update["message"])
            except Exception as e:
                requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')
            for handler, filter_ in self.message_handlers:
                if filter_(message):
                    handler(self, message)

        elif "edited_message" in update:
            try:
                edited_message = Message(self, update["edited_message"])
            except Exception as e:
                requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={e}')
            for handler, filter_ in self.edited_message_handlers:
                if filter_(edited_message):
                    handler(self, edited_message)

    def on_message(self, filter_func):
        """
        Decorator to handle messages with a specific filter.

        Args:
            filter_func (function): A function that determines whether the handler should be called.

        Returns:
            function: The decorated function.
        """
        def decorator(func):
            self.message_handlers.append((func, filter_func))
            return func
        return decorator

    def on_edited(self, filter_func):
        """
        Decorator to handle edited messages with a specific filter.

        Args:
            filter_func (function): A function that determines whether the handler should be called.

        Returns:
            function: The decorated function.
        """
        def decorator(func):
            self.edited_message_handlers.append((func, filter_func))
            return func
        return decorator

