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
        """
        নোটিফায়ার ইনিশিয়ালাইজ করুন
        
        Args:
            token: টেলিগ্রাম বট টোকেন
            chat_id: চ্যাট আইডি
            enabled: নোটিফিকেশন সক্ষম여부
        """
        self.token = token
        self.chat_id = chat_id
        self.enabled = enabled
        self.api_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        টেলিগ্রাম বার্তা পাঠান
        
        Args:
            message: বার্তা পাঠানো
            parse_mode: পার্স মোড (HTML বা Markdown)
            
        Returns:
            সাফল্য অবস্থা
        """
        if not self.enabled or not self.token or not self.chat_id:
            logger.debug("⚠️ টেলিগ্রাম নোটিফিকেশন অক্ষম")
            return False
        
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
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
        """
        ট্রেডিং সিগনাল সতর্কতা পাঠান
        
        Args:
            signal: সিগনাল ডেটা
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            message = f"""
<b>🚨 ট্রেডিং সিগনাল সতর্কতা</b>

<b>সিগনাল:</b> {signal.get('signal', 'N/A')}
<b>সম্পদ:</b> {signal.get('asset', 'N/A')}
<b>মূল্য:</b> ${signal.get('price', 0):.4f}
<b>শক্তি:</b> {signal.get('strength', 'N/A')}
<b>আস্থা:</b> {signal.get('confidence', 0):.1%}

<b>কারণ:</b>
{chr(10).join([f"• {reason}" for reason in signal.get('reasons', [])])}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            return self.send_message(message)
        
        except Exception as e:
            logger.error(f"❌ সিগনাল সতর্কতা পাঠাতে ব্যর্থ: {e}")
            return False
    
    def send_trade_notification(self, trade: Dict) -> bool:
        """
        ট্রেড নোটিফিকেশন পাঠান
        
        Args:
            trade: ট্রেড ডেটা
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            emoji = "📈" if trade.get('direction') == 'BUY' else "📉"
            
            message = f"""
<b>{emoji} ট্রেড এক্সিকিউটেড</b>

<b>দিকনির্দেশনা:</b> {trade.get('direction', 'N/A')}
<b>সম্পদ:</b> {trade.get('asset', 'N/A')}
<b>প্রবেশ মূল্য:</b> ${trade.get('entry_price', 0):.4f}
<b>অবস্থান আকার:</b> {trade.get('position_size', 0):.4f} লট
<b>স্টপ লস:</b> ${trade.get('stop_loss', 0):.4f}
<b>টেক প্রফিট:</b> ${trade.get('take_profit', 0):.4f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            return self.send_message(message)
        
        except Exception as e:
            logger.error(f"❌ ট্রেড নোটিফিকেশন পাঠাতে ব্যর্থ: {e}")
            return False
    
    def send_daily_report(self, stats: Dict) -> bool:
        """
        দৈনিক রিপোর্ট পাঠান
        
        Args:
            stats: দৈনিক পরিসংখ্যান
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            message = f"""
<b>📊 দৈনিক রিপোর্ট</b>

<b>অ্যাকাউন্ট ভারসাম্য:</b> ${stats.get('current_balance', 0):.2f}
<b>দৈনিক P&L:</b> ${stats.get('daily_pnl', 0):.2f}
<b>লাভ/ক্ষতি %:</b> {stats.get('pnl_percent', 0):.2f}%

<b>আজকের ট্রেড:</b>
• মোট ট্রেড: {stats.get('total_trades', 0)}
• জয়ী: {stats.get('winning_trades', 0)}
• পরাজিত: {stats.get('losing_trades', 0)}
• জয়ের হার: {stats.get('win_rate', 0):.1%}

<b>সিগনাল ডেটা:</b>
• মোট সিগনাল: {stats.get('total_signals', 0)}
• ক্রয় সিগনাল: {stats.get('buy_signals', 0)}
• বিক্রয় সিগনাল: {stats.get('sell_signals', 0)}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            return self.send_message(message)
        
        except Exception as e:
            logger.error(f"❌ দৈনিক রিপোর্ট পাঠাতে ব্যর্থ: {e}")
            return False
    
    def send_error_alert(self, error_message: str) -> bool:
        """
        ত্রুটি সতর্কতা পাঠান
        
        Args:
            error_message: ত্রুটি বার্তা
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            message = f"""
<b>⚠️ বট ত্রুটি সতর্কতা</b>

<b>ত্রুটি:</b>
<code>{error_message}</code>

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            return self.send_message(message)
        
        except Exception as e:
            logger.error(f"❌ ত্রুটি সতর্কতা পাঠাতে ব্যর্থ: {e}")
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
