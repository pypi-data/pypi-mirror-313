from setuptools import setup
import re

requirements = ["flask", "requests", "aiohttp", "asyncio"]
    
readme = ''
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("telehook/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]
    
setup(
    name='TeleHook',
    author='ishikki-Akabane',
    author_email='ishikkiakabane@outlook.com',
    version=version,
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/ishikki-akabane/TeleHook',
    download_url="https://github.com/ishikki-akabane/TeleHook/releases/latest",
    license='Apache License 2.0',
    classifiers=[
        "Framework :: AsyncIO",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Build Tools",

    ],
    description='A lightweight Python library for building Telegram bots with webhook integration.',
    include_package_data=True,
    keywords=['telegram', 'python', 'webhook', 'free', 'api', 'code', 'pyrogram'],
    install_requires=requirements
)
