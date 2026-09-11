#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
টেকনিক্যাল সূচক
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """টেকনিক্যাল বিশ্লেষণ সূচক"""
    
    @staticmethod
    def sma_signal(prices: pd.Series, short_period: int, long_period: int) -> str:
        """সিম্পল মুভিং এভারেজ সিগনাল"""
        try:
            sma_short = prices.rolling(window=short_period).mean()
            sma_long = prices.rolling(window=long_period).mean()
            
            if sma_short.iloc[-1] > sma_long.iloc[-1]:
                return "UP"
            elif sma_short.iloc[-1] < sma_long.iloc[-1]:
                return "DOWN"
            else:
                return "NEUTRAL"
        except Exception as e:
            logger.error(f"❌ SMA সিগনাল ত্রুটি: {e}")
            return "NEUTRAL"
    
    @staticmethod
    def rsi_signal(prices: pd.Series, period: int) -> str:
        """আপেক্ষিক শক্তি সূচক (RSI) সিগনাল"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_rsi = rsi.iloc[-1]
            
            if current_rsi > 70:
                return "DOWN"  # ওভারবট
            elif current_rsi < 30:
                return "UP"    # ওভারসোল্ড
            else:
                return "NEUTRAL"
        except Exception as e:
            logger.error(f"❌ RSI সিগনাল ত্রুটি: {e}")
            return "NEUTRAL"
    
    @staticmethod
    def macd_signal(prices: pd.Series, fast: int, slow: int, signal: int = 9) -> str:
        """MACD সিগনাল"""
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal).mean()
            
            if macd.iloc[-1] > signal_line.iloc[-1]:
                return "UP"
            elif macd.iloc[-1] < signal_line.iloc[-1]:
                return "DOWN"
            else:
                return "NEUTRAL"
        except Exception as e:
            logger.error(f"❌ MACD সিগনাল ত্রুটি: {e}")
            return "NEUTRAL"
    
    @staticmethod
    def bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2) -> dict:
        """বলিঞ্জার ব্যান্ডস"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return {
                'upper': upper_band.iloc[-1],
                'middle': sma.iloc[-1],
                'lower': lower_band.iloc[-1],
                'price': prices.iloc[-1]
            }
        except Exception as e:
            logger.error(f"❌ Bollinger Bands ত্রুটি: {e}")
            return None
    
    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> dict:
        """স্টোকাস্টিক সূচক"""
        try:
            lowest_low = low.rolling(window=period).min()
            highest_high = high.rolling(window=period).max()
            
            k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d = k.rolling(window=3).mean()
            
            return {
                'k': k.iloc[-1],
                'd': d.iloc[-1]
            }
        except Exception as e:
            logger.error(f"❌ Stochastic ত্রুটি: {e}")
            return None
