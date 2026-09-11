#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
সূচক ক্যালকুলেশন মডিউল
Technical Indicators: SMA, RSI, MACD, Bollinger Bands, Stochastic
"""

import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """উন্নত প্রযুক্তিগত সূচক ক্যালকুলেটর"""
    
    @staticmethod
    def calculate_sma(data: List[float], period: int) -> float:
        """
        Simple Moving Average (সিম্পল মুভিং এভারেজ) গণনা করুন
        
        Args:
            data: মূল্যের তালিকা
            period: সময়কাল
            
        Returns:
            SMA মান
        """
        if len(data) < period:
            return None
        return sum(data[-period:]) / period
    
    @staticmethod
    def calculate_ema(data: List[float], period: int) -> float:
        """
        Exponential Moving Average (ঘাতীয় মুভিং এভারেজ) গণনা করুন
        
        Args:
            data: মূল্যের তালিকা
            period: সময়কাল
            
        Returns:
            EMA মান
        """
        if len(data) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = sum(data[-period:]) / period
        
        for price in data[-period+1:]:
            ema = price * multiplier + ema * (1 - multiplier)
        
        return ema
    
    @staticmethod
    def calculate_rsi(data: List[float], period: int = 14) -> float:
        """
        Relative Strength Index (আপেক্ষিক শক্তি সূচক) গণনা করুন
        
        Args:
            data: মূল্যের তালিকা
            period: সময়কাল (ডিফল্ট: 14)
            
        Returns:
            RSI মান (0-100)
        """
        if len(data) < period + 1:
            return None
        
        deltas = np.diff(data[-period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(data: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        """
        MACD (Moving Average Convergence Divergence) গণনা করুন
        """
        if len(data) < slow + signal:
            return {'macd': None, 'signal': None, 'histogram': None}
        
        ema_fast = TechnicalIndicators.calculate_ema(data, fast)
        ema_slow = TechnicalIndicators.calculate_ema(data, slow)
        
        if ema_fast is None or ema_slow is None:
            return {'macd': None, 'signal': None, 'histogram': None}
        
        macd = ema_fast - ema_slow
        signal_line = macd
        histogram = macd - signal_line
        
        return {'macd': macd, 'signal': signal_line, 'histogram': histogram}
    
    @staticmethod
    def calculate_bollinger_bands(data: List[float], period: int = 20, num_std: float = 2.0) -> Dict[str, float]:
        """
        Bollinger Bands (বলিঞ্জার ব্যান্ডস) গণনা করুন
        """
        if len(data) < period:
            return {'upper': None, 'middle': None, 'lower': None}
        
        prices = data[-period:]
        middle = sum(prices) / period
        variance = sum((x - middle) ** 2 for x in prices) / period
        std_dev = variance ** 0.5
        
        upper = middle + (std_dev * num_std)
        lower = middle - (std_dev * num_std)
        
        return {'upper': upper, 'middle': middle, 'lower': lower}
    
    @staticmethod
    def calculate_stochastic(data: List[float], period: int = 14) -> Dict[str, float]:
        """
        Stochastic Oscillator (স্টোকাস্টিক অসিলেটর) গণনা করুন
        """
        if len(data) < period:
            return {'k': None, 'd': None}
        
        prices = data[-period:]
        highest = max(prices)
        lowest = min(prices)
        
        if highest == lowest:
            k = 50
        else:
            k = 100 * ((prices[-1] - lowest) / (highest - lowest))
        
        return {'k': k, 'd': k}


class IndicatorAnalyzer:
    """সূচক বিশ্লেষণ এবং সিগনাল প্রজন্ম"""
    
    @staticmethod
    def get_indicators(prices: List[float], highs: List[float] = None, lows: List[float] = None) -> Dict:
        """
        সমস্ত সূচক একসাথে গণনা করুন
        """
        indicators = {}
        
        indicators['sma_10'] = TechnicalIndicators.calculate_sma(prices, 10)
        indicators['sma_20'] = TechnicalIndicators.calculate_sma(prices, 20)
        indicators['ema_12'] = TechnicalIndicators.calculate_ema(prices, 12)
        indicators['ema_26'] = TechnicalIndicators.calculate_ema(prices, 26)
        indicators['rsi'] = TechnicalIndicators.calculate_rsi(prices, 14)
        indicators['macd'] = TechnicalIndicators.calculate_macd(prices)
        indicators['stochastic'] = TechnicalIndicators.calculate_stochastic(prices)
        indicators['bollinger_bands'] = TechnicalIndicators.calculate_bollinger_bands(prices)
        
        if highs and lows:
            indicators['atr'] = TechnicalIndicators.calculate_atr(highs, lows, prices)
        
        return indicators
    
    @staticmethod
    def calculate_atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> float:
        """
        Average True Range (গড় সত্য পরিসীমা) গণনা করুন
        """
        if len(high) < period or len(low) < period or len(close) < period:
            return None
        
        tr_values = []
        for i in range(len(high)):
            tr = max(
                high[i] - low[i],
                abs(high[i] - close[i-1]) if i > 0 else 0,
                abs(low[i] - close[i-1]) if i > 0 else 0
            )
            tr_values.append(tr)
        
        return sum(tr_values[-period:]) / period
