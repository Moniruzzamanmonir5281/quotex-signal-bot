#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Notification Module
টেলিগ্রাম নোটিফিকেশন সিস্টেম
"""

import logging
from typing import Dict, Optional
import requests
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """টেলিগ্রাম নোটিফিকেশন সিস্টেম"""
    
    def __init__(self, token: str, chat_id: str, enabled: bool = True):
        """নোটিফায়ার ইনিশিয়ালাইজ করুন"""
        self.token = token
        self.chat_id = chat_id
        self.enabled = enabled
        self.api_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """টেলিগ্রাম বার্তা পাঠান"""
        if not self.enabled or not self.token or not self.chat_id:
            logger.debug("⚠️ টেলিগ্রাম নোটিফিকেশন অক্ষম")
            return False
        
        try:
            url = f"{self.api_url}/sendMessage"
            data = {'chat_id': self.chat_id, 'text': message, 'parse_mode': parse_mode}
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                logger.debug("✅ টেলিগ্রাম বার্তা পাঠানো হয়েছে")
                return True
            else:
                logger.error(f"❌ টেলিগ্রাম ত্রুটি: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ টেলিগ্রাম বার্তা পাঠাতে ব্যর্থ: {e}")
            return False
    
    def send_signal_alert(self, signal: Dict) -> bool:
        """ট্রেডিং সিগনাল সতর্কতা পাঠান"""
        try:
            message = f"""
<b>🚨 ট্রেডিং সিগনাল সতর্কতা</b>

<b>সিগনাল:</b> {signal.get('signal', 'N/A')}
<b>সম্পদ:</b> {signal.get('asset', 'N/A')}
<b>মূল্য:</b> ${signal.get('price', 0):.4f}
<b>শক্তি:</b> {signal.get('strength', 'N/A')}
<b>আস্থা:</b> {signal.get('confidence', 0):.1%}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            return self.send_message(message)
        except Exception as e:
            logger.error(f"❌ সিগনাল সতর্কতা পাঠাতে ব্যর্থ: {e}")
            return False
    
    def test_connection(self) -> bool:
        """টেলিগ্রাম সংযোগ পরীক্ষা করুন"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                logger.info("✅ টেলিগ্রাম সংযোগ সফল")
                return True
            else:
                logger.error(f"❌ টেলিগ্রাম সংযোগ ব্যর্থ: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ টেলিগ্রাম পরীক্ষায় ত্রুটি: {e}")
            return False
