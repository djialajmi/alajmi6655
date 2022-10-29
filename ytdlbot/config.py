#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - config.py
# 8/28/21 15:01
#

__author__ = "SuperAbdo superabdo.2015@gmail.com"

import os

# general settings
WORKERS: "int" = 100
PYRO_WORKERS: "int" = 100
APP_ID: "int" = 10162446
APP_HASH = "4ddd3f5e672d793e2f103af34cd31850"
TOKEN = "5768346857:AAHu7TrESOV8wjPwHgT5mnf5wgio76VkVhE"

REDIS = os.getenv("REDIS")

# quota settings
QUOTA = 10 * 1024 * 1024 * 1024  # 10G
# if os.uname().sysname == "Darwin":
#     QUOTA = 10 * 1024 * 1024  # 10M

TG_MAX_SIZE = 1024 * 1024 * 1024 * 0.99
# TG_MAX_SIZE = 10 * 1024 * 1024

EX = 24 * 3600
MULTIPLY = 5  # VIP1 is 5*5-25G, VIP2 is 50G
USD2CNY =  6  # $5 --> ¥30

ENABLE_VIP = False
MAX_DURATION = 60
AFD_LINK = "https://afdian.net/@BennyThink"
COFFEE_LINK = "https://www.buymeacoffee.com/bennythink"
COFFEE_TOKEN = os.getenv("COFFEE_TOKEN")
AFD_TOKEN = os.getenv("AFD_TOKEN")
AFD_USER_ID = os.getenv("AFD_USER_ID")
OWNER = "SuperAbdo"

# limitation settings
AUTHORIZED_USER: "str" = ""
# membership requires: the format could be username/chat_id of channel or group
REQUIRED_MEMBERSHIP: "str" = ""

# celery related
ENABLE_CELERY = False
ENABLE_QUEUE = False
BROKER = f"redis://{REDIS}:6379/4"

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "root")

AUDIO_FORMAT = os.getenv("AUDIO_FORMAT")
ARCHIVE_ID = os.getenv("ARCHIVE_ID")

IPv6 = False
ENABLE_FFMPEG = True
