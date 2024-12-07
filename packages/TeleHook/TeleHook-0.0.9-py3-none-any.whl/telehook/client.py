

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
            plugins_path (str): Path to the plugins folder.
        """
        self.token = token
        self.url = url
        self.api_url = f"https://api.telegram.org/bot{self.token}/"
        self.message_handlers = []
        self.edited_message_handlers = []
        self.method = Methods(self)

        if plugins_path:
            self.load_plugins(plugins_path)

    def load_plugins(self, plugins_path):
        """
        Dynamically load plugins from the specified path.

        Args:
            plugins_path (str): Path to the plugins folder.
        """
        logger.info(f"Loading plugins from {plugins_path}")
        try:
            # Add the plugins path to the system path
            if plugins_path not in os.sys.path:
                os.sys.path.append(plugins_path)

            # List all Python files in the plugins folder
            for file in os.listdir(plugins_path):
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]  # Remove .py extension
                    importlib.import_module(f"{plugins_path}.{module_name}")
        except Exception as e:
            logger.error(f"Error loading plugins: {e}")

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

