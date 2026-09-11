#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
সিগনাল জেনারেটর মডিউল
একাধিক সূচক থেকে ট্রেড সিগনাল তৈরি করুন
"""

import logging
from typing import Dict, List
from enum import Enum
from .indicators import IndicatorAnalyzer, TechnicalIndicators

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """সিগনাল প্রকার"""
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


class SignalStrength(Enum):
    """সিগনাল শক্তি"""
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    VERY_STRONG = 4


class SignalGenerator:
    """উন্নত ট্রেডিং সিগনাল জেনারেটর"""
    
    def __init__(self, buy_threshold: float = 0.6, sell_threshold: float = 0.4, min_strength: int = 2):
        """
        সিগনাল জেনারেটর ইনিশিয়ালাইজ করুন
        """
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.min_strength = min_strength
        self.signal_history = []
    
    def generate_signal(self, prices: List[float], highs: List[float] = None, lows: List[float] = None) -> Dict:
        """
        সম্পূর্ণ ট্রেড সিগনাল তৈরি করুন
        """
        if not prices or len(prices) < 20:
            return {
                'signal': SignalType.NEUTRAL.value,
                'strength': SignalStrength.WEAK.value,
                'confidence': 0.0,
                'indicators': {},
                'reasons': ['অপর্যাপ্ত ডেটা']
            }
        
        indicators = IndicatorAnalyzer.get_indicators(prices, highs, lows)
        
        buy_score = 0
        sell_score = 0
        total_score = 0
        reasons = []
        
        # RSI বিশ্লেষণ
        if indicators.get('rsi') is not None:
            rsi = indicators['rsi']
            if rsi < 30:
                buy_score += 2
                reasons.append(f'RSI oversold ({rsi:.2f})')
            elif rsi > 70:
                sell_score += 2
                reasons.append(f'RSI overbought ({rsi:.2f})')
            else:
                total_score += 1
            total_score += 2
        
        # সিম্পল মুভিং এভারেজ
        if indicators.get('sma_10') and indicators.get('sma_20'):
            sma_10 = indicators['sma_10']
            sma_20 = indicators['sma_20']
            if sma_10 > sma_20:
                buy_score += 1.5
                reasons.append('SMA: ঊর্ধ্বমুখী প্রবণতা')
            else:
                sell_score += 1.5
                reasons.append('SMA: নিম্নমুখী প্রবণতা')
            total_score += 1.5
        
        # MACD বিশ্লেষণ
        if indicators.get('macd'):
            macd = indicators['macd']
            if macd['histogram'] is not None:
                if macd['histogram'] > 0:
                    buy_score += 1
                    reasons.append('MACD: ঊর্ধ্বমুখী')
                else:
                    sell_score += 1
                    reasons.append('MACD: নিম্নমুখী')
                total_score += 1
        
        # বলিঞ্জার ব্যান্ডস
        if indicators.get('bollinger_bands'):
            bb = indicators['bollinger_bands']
            current_price = prices[-1]
            if current_price > bb['upper']:
                sell_score += 0.5
                reasons.append('বলিঞ্জার: উপরের ব্যান্ড স্পর্শ')
            elif current_price < bb['lower']:
                buy_score += 0.5
                reasons.append('বলিঞ্জার: নিচের ব্যান্ড স্পর্শ')
            total_score += 0.5
        
        # সিগনাল নির্ধারণ করুন
        if total_score == 0:
            signal_type = SignalType.NEUTRAL
            confidence = 0.0
        else:
            buy_ratio = buy_score / total_score
            sell_ratio = sell_score / total_score
            
            if buy_ratio > self.buy_threshold:
                signal_type = SignalType.BUY
                confidence = buy_ratio
            elif sell_ratio > self.sell_threshold:
                signal_type = SignalType.SELL
                confidence = sell_ratio
            else:
                signal_type = SignalType.NEUTRAL
                confidence = max(buy_ratio, sell_ratio)
        
        # শক্তি নির্ধারণ করুন
        num_reasons = len(reasons)
        if num_reasons >= 4:
            strength = SignalStrength.VERY_STRONG.value
        elif num_reasons >= 3:
            strength = SignalStrength.STRONG.value
        elif num_reasons >= 2:
            strength = SignalStrength.MODERATE.value
        else:
            strength = SignalStrength.WEAK.value
        
        signal_data = {
            'signal': signal_type.value,
            'strength': strength,
            'confidence': round(confidence, 3),
            'indicators': {
                'rsi': round(indicators.get('rsi'), 2) if indicators.get('rsi') else None,
                'sma_10': round(indicators.get('sma_10'), 4) if indicators.get('sma_10') else None,
                'sma_20': round(indicators.get('sma_20'), 4) if indicators.get('sma_20') else None,
                'macd': indicators.get('macd'),
                'bollinger_bands': indicators.get('bollinger_bands'),
                'stochastic': indicators.get('stochastic')
            },
            'reasons': reasons,
            'current_price': prices[-1]
        }
        
        self.signal_history.append(signal_data)
        return signal_data
    
    def should_trade(self, signal: Dict) -> bool:
        """
        সিগনালের উপর ভিত্তি করে ট্রেড করা উচিত কিনা তা নির্ধারণ করুন
        """
        if signal['signal'] == SignalType.NEUTRAL.value:
            return False
        if signal['strength'] < self.min_strength:
            return False
        if signal['confidence'] < 0.5:
            return False
        return True
    
    def get_signal_summary(self) -> Dict:
        """
        সাম্প্রতিক সিগনালের সারসংক্ষেপ পান
        """
        if not self.signal_history:
            return {'total_signals': 0, 'buy_signals': 0, 'sell_signals': 0, 'neutral_signals': 0, 'avg_confidence': 0.0}
        
        recent = self.signal_history[-100:]
        buy_count = sum(1 for s in recent if s['signal'] == SignalType.BUY.value)
        sell_count = sum(1 for s in recent if s['signal'] == SignalType.SELL.value)
        neutral_count = sum(1 for s in recent if s['signal'] == SignalType.NEUTRAL.value)
        avg_confidence = sum(s['confidence'] for s in recent) / len(recent) if recent else 0
        
        return {'total_signals': len(recent), 'buy_signals': buy_count, 'sell_signals': sell_count, 'neutral_signals': neutral_count, 'avg_confidence': round(avg_confidence, 3), 'buy_ratio': round(buy_count / len(recent), 3) if recent else 0}
