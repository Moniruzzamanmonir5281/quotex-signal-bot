#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বিজ্ঞপ্তি সিস্টেম (টেলিগ্রাম)
"""

import logging
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SEND_NOTIFICATIONS

logger = logging.getLogger(__name__)

class Notifier:
    """বিজ্ঞপ্তি পাঠানো হয়"""
    
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = SEND_NOTIFICATIONS and self.token and self.chat_id
    
    def send_message(self, message: str) -> bool:
        """টেলিগ্রাম বার্তা পাঠান"""
        if not self.enabled:
            return False
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ টেলিগ্রাম বার্তা পাঠাতে ত্রুটি: {e}")
            return False
    
    def send_trade_notification(self, asset: str, direction: str, signal: str, 
                               amount: float, trade_id: str) -> bool:
        """ট্রেড বিজ্ঞপ্তি পাঠান"""
        try:
            message = f"""<b>🔔 নতুন ট্রেড</b>
<b>সম্পদ:</b> {asset}
<b>দিক:</b> {direction.upper()}
<b>সিগনাল:</b> {signal}
<b>পরিমাণ:</b> ${amount}
<b>ট্রেড ID:</b> {trade_id}"""
            return self.send_message(message)
        except Exception as e:
            logger.error(f"❌ ট্রেড বিজ্ঞপ্তি ত্রুটি: {e}")
            return False
    
    def send_error_notification(self, error: str) -> bool:
        """ত্রুটি বিজ্ঞপ্তি পাঠান"""
        try:
            message = f"<b>❌ ত্রুটি</b>\n{error}"
            return self.send_message(message)
        except Exception as e:
            logger.error(f"❌ ত্রুটি বিজ্ঞপ্তি ত্রুটি: {e}")
            return False
    
    def send_daily_report(self, trades: int, wins: int, losses: int, 
                         profit: float) -> bool:
        """দৈনিক রিপোর্ট পাঠান"""
        try:
            win_rate = (wins / trades * 100) if trades > 0 else 0
            message = f"""<b>📊 দৈনিক রিপোর্ট</b>
<b>মোট ট্রেড:</b> {trades}
<b>বিজয়:</b> {wins}
<b>ক্ষতি:</b> {losses}
<b>জয়ের হার:</b> {win_rate:.2f}%
<b>লাভ/ক্ষতি:</b> ${profit:,.2f}"""
            return self.send_message(message)
        except Exception as e:
            logger.error(f"❌ দৈনিক রিপোর্ট ত্রুটি: {e}")
            return False
