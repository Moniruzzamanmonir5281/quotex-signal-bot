#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quotex বট মূল মডিউল
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from config import (
    QUOTEX_EMAIL, QUOTEX_PASSWORD, QUOTEX_API_KEY,
    TRADE_AMOUNT, ASSETS, CHECK_INTERVAL, TIMEFRAME,
    SMA_SHORT, SMA_LONG, RSI_PERIOD, MACD_FAST, MACD_SLOW,
    MAX_DAILY_LOSS, MAX_TRADES_PER_DAY, LOG_FILE
)
from bot.indicators import TechnicalIndicators
from bot.risk_manager import RiskManager
from bot.notifications import Notifier

logger = logging.getLogger(__name__)

class QuotexSignalBot:
    def __init__(self):
        self.email = QUOTEX_EMAIL
        self.password = QUOTEX_PASSWORD
        self.api_key = QUOTEX_API_KEY
        self.base_url = "https://api.quotex.io"
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        
        # অবজেক্ট তৈরি করুন
        self.indicators = TechnicalIndicators()
        self.risk_manager = RiskManager()
        self.notifier = Notifier()
        
        # ট্রেডিং পরিসংখ্যান
        self.trades_today = 0
        self.daily_loss = 0
        self.today_date = datetime.now().date()
    
    def login(self) -> bool:
        """Quotex এ লগইন করুন"""
        try:
            logger.info("🔐 Quotex এ লগইন করছি...")
            login_url = f"{self.base_url}/login"
            payload = {
                "email": self.email,
                "password": self.password
            }
            response = self.session.post(login_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.user_id = data.get('user_id')
                logger.info("✓ সফলভাবে Quotex এ লগইন হয়েছে")
                return True
            else:
                logger.error(f"❌ লগইন ব্যর্থ: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ লগইন ত্রুটি: {e}")
            return False
    
    def get_market_data(self, asset: str, limit: int = 100) -> pd.DataFrame:
        """বাজারের ডেটা পান"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/markets/{asset}?limit={limit}&timeframe={TIMEFRAME}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['candles'])
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                return df
            else:
                logger.warning(f"⚠️ {asset} এর ডেটা পেতে ব্যর্থ")
                return None
                
        except Exception as e:
            logger.error(f"❌ ডেটা পেতে ত্রুটি: {e}")
            return None
    
    def calculate_signals(self, df: pd.DataFrame) -> dict:
        """সমস্ত সিগনাল ক্যালকুলেট করুন"""
        try:
            signals = {}
            
            # SMA সিগনাল
            sma_signal = self.indicators.sma_signal(
                df['close'], SMA_SHORT, SMA_LONG
            )
            signals['SMA'] = sma_signal
            
            # RSI সিগনাল
            rsi_signal = self.indicators.rsi_signal(
                df['close'], RSI_PERIOD
            )
            signals['RSI'] = rsi_signal
            
            # MACD সিগনাল
            macd_signal = self.indicators.macd_signal(
                df['close'], MACD_FAST, MACD_SLOW
            )
            signals['MACD'] = macd_signal
            
            return signals
            
        except Exception as e:
            logger.error(f"❌ সিগনাল ক্যালকুলেট করতে ত্রুটি: {e}")
            return {}
    
    def generate_trade_signal(self, signals: dict) -> str:
        """চূড়ান্ত ট্রেড সিগনাল তৈরি করুন"""
        try:
            up_votes = sum(1 for s in signals.values() if s == "UP")
            down_votes = sum(1 for s in signals.values() if s == "DOWN")
            
            total_votes = up_votes + down_votes
            
            if total_votes == 0:
                return "NEUTRAL"
            
            if up_votes > down_votes:
                confidence = (up_votes / total_votes) * 100
                return f"UP ({confidence:.0f}%)"
            elif down_votes > up_votes:
                confidence = (down_votes / total_votes) * 100
                return f"DOWN ({confidence:.0f}%)"
            else:
                return "NEUTRAL"
                
        except Exception as e:
            logger.error(f"❌ সিগনাল তৈরিতে ত্রুটি: {e}")
            return "NEUTRAL"
    
    def place_trade(self, asset: str, signal: str, amount: float) -> bool:
        """ট্রেড রাখুন"""
        try:
            # ঝুঁকি ব্যবস্থাপনা চেক করুন
            if not self.risk_manager.can_trade(
                self.trades_today,
                self.daily_loss,
                MAX_TRADES_PER_DAY,
                MAX_DAILY_LOSS
            ):
                logger.warning("⚠️ ঝুঁকি সীমা অতিক্রম করা হয়েছে")
                return False
            
            # সিগনাল পার্স করুন
            direction = "call" if "UP" in signal else "put"
            
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/trades"
            
            payload = {
                "asset": asset,
                "direction": direction,
                "amount": amount,
                "expiration": 60  # ১ মিনিট
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                trade_id = response.json().get('trade_id')
                logger.info(f"✓ ট্রেড রাখা হয়েছে: {signal} - {asset} - ID: {trade_id}")
                
                # পরিসংখ্যান আপডেট করুন
                self.trades_today += 1
                
                # বিজ্ঞপ্তি পাঠান
                self.notifier.send_trade_notification(
                    asset, direction, signal, amount, trade_id
                )
                
                return True
            else:
                logger.error(f"❌ ট্রেড ব্যর্থ: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ ট্রেড রাখতে ত্রুটি: {e}")
            return False
    
    def check_daily_reset(self):
        """দৈনিক রিসেট চেক করুন"""
        current_date = datetime.now().date()
        if current_date != self.today_date:
            logger.info("📊 দৈনিক পরিসংখ্যান রিসেট করছি")
            self.trades_today = 0
            self.daily_loss = 0
            self.today_date = current_date
    
    def run(self):
        """বট চালু করুন"""
        if not self.login():
            logger.error("❌ লগইন ব্যর্থ, বট বন্ধ করছি")
            return
        
        logger.info("🚀 বট চলছে...")
        logger.info(f"📊 সম্পদ: {ASSETS}")
        logger.info(f"⏱️ চেক ইন্টারভাল: {CHECK_INTERVAL} সেকেন্ড")
        
        while True:
            try:
                # দৈনিক রিসেট চেক করুন
                self.check_daily_reset()
                
                for asset in ASSETS:
                    logger.info(f"📈 {asset} বিশ্লেষণ করছি...")
                    
                    # ডেটা পান
                    df = self.get_market_data(asset)
                    
                    if df is not None and len(df) > 0:
                        # সিগনাল ক্যালকুলেট করুন
                        signals = self.calculate_signals(df)
                        
                        # চূড়ান্ত সিগনাল তৈরি করুন
                        trade_signal = self.generate_trade_signal(signals)
                        logger.info(f"🔔 {asset} সিগনাল: {trade_signal}")
                        
                        # শক্তিশালী সিগনাল হলে ট্রেড করুন
                        if "UP" in trade_signal or "DOWN" in trade_signal:
                            confidence = int(trade_signal.split('(')[1].rstrip(')'))
                            if confidence >= 66:  # 66% এর উপরে
                                self.place_trade(asset, trade_signal, TRADE_AMOUNT)
                
                # পরবর্তী চেকের জন্য অপেক্ষা করুন
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("\n⛔ বট ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে")
                break
            except Exception as e:
                logger.error(f"❌ অপ্রত্যাশিত ত্রুটি: {e}", exc_info=True)
                time.sleep(CHECK_INTERVAL)
