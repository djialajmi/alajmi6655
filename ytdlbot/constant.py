#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "SuperAbdo superabdo.2015@gmail.com"

import os
import time

from config import (AFD_LINK, COFFEE_LINK, ENABLE_CELERY, ENABLE_VIP, EX,
                    MULTIPLY, REQUIRED_MEMBERSHIP, USD2CNY)
from db import InfluxDB
from downloader import sizeof_fmt
from limit import QUOTA, VIP
from utils import get_func_queue

# 2. At this time of writing, this bot consumes hundreds of GigaBytes of network traffic per day. 
# In order to avoid being abused, 
# every one can use this bot within **{sizeof_fmt(QUOTA)} of quota for every {int(EX / 3600)} hours.**

class BotText:
    start = "مرحبا بك في بوت تحميل الفيديوهات\n يمكنك ادخال امر /help لمعرفة المزيد\nرابط القناة الخاصة بنا https://t.me/dji_alajmi"

    help = f"""
1. هذا البوت يستخدم لتحميل الفيديوهات من اليوتيوب وجميع المواقع الخارجية

2. فقط ارسل رابط الفيديو المراد تحميله
    """

    about = "يمكنك تحميل اي فيديو علي الانترنت من اليوتيوب والمواقع الخارجية\n" \

#     terms = f"""
# يمكنك إستعمال فقط كوتة وقدرها, {sizeof_fmt(QUOTA)} لكل {int(EX / 3600)} ساعة.
# """
# 2. The above traffic, is counted for one-way. 
# For example, if you download a video of 1GB, your current quota will be 9GB instead of 8GB.

# 3. Streaming support is limited due to high costs of conversion.

# 4. I won't gather any personal information, which means I don't know how many and what videos did you download.

# 5. Please try not to abuse this service.

# 6. It's a open source project, you can always deploy your own bot.

# 7. For VIPs, please refer to /vip command
#     """ if ENABLE_VIP else "Please contact the actual owner of this bot"

    vip = f"""
**Terms:**
1. No refund, I'll keep it running as long as I can.
2. I'll record your unique ID after a successful payment, usually it's payment ID or email address.
3. VIPs identity won't expire.

**Pay Tier:**
1. Everyone: {sizeof_fmt(QUOTA)} per {int(EX / 3600)} hours
2. VIP1: ${MULTIPLY} or ¥{MULTIPLY * USD2CNY}, {sizeof_fmt(QUOTA * 5)} per {int(EX / 3600)} hours
3. VIP2: ${MULTIPLY * 2} or ¥{MULTIPLY * USD2CNY * 2}, {sizeof_fmt(QUOTA * 5 * 2)} per {int(EX / 3600)} hours
4. VIP4....VIPn.
5. Unlimited streaming conversion support.
Note: If you pay $9, you'll become VIP1 instead of VIP2.

**Payment method:**
1. (afdian) Mainland China: {AFD_LINK}
2. (buy me a coffee) Other countries or regions: {COFFEE_LINK}
__I live in a place where I don't have access to Telegram Payments. So...__

**After payment:**
1. afdian: with your order number `/vip 123456`
2. buy me a coffee: with your email `/vip someone@else.com`
    """ if ENABLE_VIP else "VIP is not enabled."
    vip_pay = "Processing your payments...If it's not responding after one minute, please contact @BennyThink."

    private = "هذا البوت للخاص فقط"
    membership_require = f"يجب الانضمام هنا لأستخدام البوت\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
إختر جودة الفيديو. **يعمل فقط لفيديوهات اليوتيوب**
الجودة High ينصح بها; الجودة Medium جيدة للفيديوهات بجودة 480p والجودة low للفيديوهات بجودة 320p و 240p.
    
إعداداتك الحالية:
جودة الفيديو: **{0}**
نوع الإرسال: **{1}**
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    def remaining_quota_caption(self, chat_id):
        if not ENABLE_VIP:
            return ""
        used, total, ttl = self.return_remaining_quota(chat_id)
        refresh_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ttl + time.time()))
        caption = f"video1new"
        return caption

    @staticmethod
    def return_remaining_quota(chat_id):
        used, total, ttl = VIP().check_remaining_quota(chat_id)
        return used, total, ttl

    @staticmethod
    def get_vip_greeting(chat_id):
        if not ENABLE_VIP:
            return ""
        v = VIP().check_vip(chat_id)
        if v:
            return f"Hello {v[1]}, VIP{v[-2]}☺️\n\n"
        else:
            return ""

    @staticmethod
    def get_receive_link_text():
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"مهام كثيرة جدًا. تمت إضافة مهامك إلى قائمة الانتظار المحجوزة {reserved}."
        else:
            text = "تمت إضافة مهمتك إلى قائمة الانتظار النشطة. \n جاري المعالجة ...\n\n"

        return text

    @staticmethod
    def ping_worker():
        from tasks import app as celery_app
        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
