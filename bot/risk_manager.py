#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ঝুঁকি ব্যবস্থাপনা
"""

import logging

logger = logging.getLogger(__name__)

class RiskManager:
    """ঝুঁকি নিয়ন্ত্রণ এবং অর্থ ব্যবস্থাপনা"""
    
    def __init__(self):
        self.daily_trades = 0
        self.daily_loss = 0
    
    def can_trade(self, trades_today: int, daily_loss: float, 
                  max_trades: int, max_daily_loss: float) -> bool:
        """ট্রেড করা যাচাই করুন"""
        try:
            # সর্বোচ্চ ট্রেড সংখ্যা চেক করুন
            if trades_today >= max_trades:
                logger.warning(f"⚠️ সর্বোচ্চ দৈনিক ট্রেড ({max_trades}) পৌঁছেছি")
                return False
            
            # সর্বোচ্চ দৈনিক ক্ষতি চেক করুন
            if daily_loss >= max_daily_loss:
                logger.warning(f"⚠️ সর্বোচ্চ দৈনিক ক্ষতি (${max_daily_loss}) পৌঁছেছি")
                return False
            
            return True
        except Exception as e:
            logger.error(f"❌ ঝুঁকি যাচাইতে ত্রুটি: {e}")
            return False
    
    def calculate_position_size(self, account_balance: float, risk_percent: float = 2) -> float:
        """অবস্থান আকার ক্যালকুলেট করুন"""
        try:
            position_size = (account_balance * risk_percent) / 100
            return round(position_size, 2)
        except Exception as e:
            logger.error(f"❌ অবস্থান আকার ক্যালকুলেশন ত্রুটি: {e}")
            return 10.0  # ডিফল্ট
    
    def calculate_stop_loss(self, entry_price: float, risk_amount: float, 
                          direction: str = "long") -> float:
        """স্টপ লস ক্যালকুলেট করুন"""
        try:
            if direction == "long":
                stop_loss = entry_price - risk_amount
            else:
                stop_loss = entry_price + risk_amount
            
            return round(stop_loss, 5)
        except Exception as e:
            logger.error(f"❌ স্টপ লস ক্যালকুলেশন ত্রুটি: {e}")
            return None
    
    def calculate_take_profit(self, entry_price: float, reward_amount: float, 
                             direction: str = "long") -> float:
        """টেক প্রফিট ক্যালকুলেট করুন"""
        try:
            if direction == "long":
                take_profit = entry_price + reward_amount
            else:
                take_profit = entry_price - reward_amount
            
            return round(take_profit, 5)
        except Exception as e:
            logger.error(f"❌ টেক প্রফিট ক্যালকুলেশন ত্রুটি: {e}")
            return None
