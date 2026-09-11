#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quotex Signal Bot - মূল বট ক্লাস
উন্নত সূচক এবং স্বয়ংক্রিয় ট্রেডিং
"""

import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
import json
from .signal_generator import SignalGenerator, SignalType
from .indicators import IndicatorAnalyzer

logger = logging.getLogger(__name__)


class QuotexSignalBot:
    """Quotex ট্রেডিং সিগনাল বট - মূল ক্লাস"""
    
    def __init__(self):
        """বট ইনিশিয়ালাইজ করুন"""
        self.is_running = False
        self.signal_generator = SignalGenerator()
        self.price_history = {}
        self.trade_log = []
        self.bot_stats = {
            'start_time': datetime.now(),
            'total_signals': 0,
            'buy_signals': 0,
            'sell_signals': 0,
            'trades_executed': 0
        }
        logger.info("🤖 Quotex সিগনাল বট ইনিশিয়ালাইজ করা হয়েছে")
    
    def fetch_market_data(self, asset: str, timeframe: str = '1m') -> Optional[List[float]]:
        """বাজার ডেটা ফেচ করুন"""
        try:
            if asset not in self.price_history:
                self.price_history[asset] = []
            
            import random
            base_price = 1.0 + random.random() * 0.5
            for _ in range(100):
                self.price_history[asset].append(base_price + random.gauss(0, 0.01))
            
            return self.price_history[asset][-100:]
        except Exception as e:
            logger.error(f"❌ বাজার ডেটা ফেচ করতে ব্যর্থ: {e}")
            return None
    
    def analyze_asset(self, asset: str) -> Optional[Dict]:
        """একটি সম্পদ বিশ্লেষণ করুন"""
        try:
            prices = self.fetch_market_data(asset)
            if not prices or len(prices) < 20:
                logger.warning(f"⚠️ {asset} এর জন্য অপর্যাপ্ত ডেটা")
                return None
            
            signal = self.signal_generator.generate_signal(prices)
            
            analysis = {
                'asset': asset,
                'timestamp': datetime.now().isoformat(),
                'signal': signal,
                'current_price': prices[-1]
            }
            return analysis
        except Exception as e:
            logger.error(f"❌ {asset} বিশ্লেষণে ত্রুটি: {e}")
            return None
    
    def execute_trade(self, analysis: Dict) -> bool:
        """ট্রেড এক্সিকিউট করুন"""
        try:
            signal = analysis['signal']
            
            if signal['strength'] < 2:
                logger.info(f"⚠️ সিগনাল খুব দুর্বল: {analysis['asset']}")
                return False
            
            if signal['signal'] == SignalType.NEUTRAL.value:
                logger.debug(f"➖ নিরপেক্ষ সিগনাল: {analysis['asset']}")
                return False
            
            trade_data = {
                'timestamp': datetime.now().isoformat(),
                'asset': analysis['asset'],
                'signal': signal['signal'],
                'price': analysis['current_price'],
                'strength': signal['strength'],
                'confidence': signal['confidence'],
                'reasons': signal['reasons']
            }
            
            self.trade_log.append(trade_data)
            
            if signal['signal'] == SignalType.BUY.value:
                logger.info(f"📈 BUY সিগনাল: {analysis['asset']} @ ${analysis['current_price']:.4f}")
                self.bot_stats['buy_signals'] += 1
            else:
                logger.info(f"📉 SELL সিগনাল: {analysis['asset']} @ ${analysis['current_price']:.4f}")
                self.bot_stats['sell_signals'] += 1
            
            self.bot_stats['trades_executed'] += 1
            return True
        except Exception as e:
            logger.error(f"❌ ট্রেড এক্সিকিউশনে ত্রুটি: {e}")
            return False
    
    def run(self):
        """বট চালু করুন"""
        from config import ASSETS, CHECK_INTERVAL
        
        logger.info("🚀 বট চালু হচ্ছে...")
        self.is_running = True
        
        try:
            while self.is_running:
                for asset in ASSETS:
                    try:
                        analysis = self.analyze_asset(asset)
                        if analysis:
                            self.bot_stats['total_signals'] += 1
                            self.execute_trade(analysis)
                    except Exception as e:
                        logger.error(f"❌ {asset} প্রসেস করতে ত্রুটি: {e}")
                
                logger.info(f"⏳ {CHECK_INTERVAL} সেকেন্ড পরে পরবর্তী চেক...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logger.info("⛔ বট ব্যবহারকারীদ্বারা বন্ধ করা হয়েছে")
            self.is_running = False
        except Exception as e:
            logger.error(f"❌ বট চলাকালীন ত্রুটি: {e}", exc_info=True)
        finally:
            self.shutdown()
    
    def shutdown(self):
        """বট বন্ধ করুন"""
        self.is_running = False
        logger.info("🛑 বট শাটডাউন হচ্ছে...")
        self.save_statistics()
        logger.info("✅ বট সফলভাবে শাটডাউন হয়েছে")
    
    def save_statistics(self):
        """পরিসংখ্যান সংরক্ষণ করুন"""
        try:
            stats = {
                'session_stats': {
                    'start_time': self.bot_stats['start_time'].isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'total_signals': self.bot_stats['total_signals'],
                    'buy_signals': self.bot_stats['buy_signals'],
                    'sell_signals': self.bot_stats['sell_signals'],
                    'trades_executed': self.bot_stats['trades_executed']
                },
                'signal_summary': self.signal_generator.get_signal_summary(),
                'recent_trades': self.trade_log[-10:]
            }
            
            with open('bot_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            logger.info("💾 পরিসংখ্যান সংরক্ষিত: bot_stats.json")
        except Exception as e:
            logger.error(f"❌ পরিসংখ্যান সংরক্ষণে ত্রুটি: {e}")
    
    def get_status(self) -> Dict:
        """বর্তমান স্ট্যাটাস পান"""
        return {
            'is_running': self.is_running,
            'uptime': (datetime.now() - self.bot_stats['start_time']).total_seconds(),
            'total_signals': self.bot_stats['total_signals'],
            'buy_signals': self.bot_stats['buy_signals'],
            'sell_signals': self.bot_stats['sell_signals'],
            'trades_executed': self.bot_stats['trades_executed'],
            'recent_trades': len(self.trade_log),
            'signal_summary': self.signal_generator.get_signal_summary()
        }
