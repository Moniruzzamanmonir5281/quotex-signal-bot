#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ট্রেডিং লগ এবং বিশ্লেষণ মডিউল
CSV এবং JSON এ লগ সংরক্ষণ, পরিসংখ্যান ট্র্যাকিং
"""

import csv
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, date
import os

logger = logging.getLogger(__name__)


class TradingLogger:
    """ট্রেডিং লগিং সিস্টেম"""
    
    def __init__(self, log_file: str = 'trading_log.csv', stats_file: str = 'bot_stats.json'):
        """
        লগার ইনিশিয়ালাইজ করুন
        
        Args:
            log_file: ট্রেড লগ ফাইল
            stats_file: পরিসংখ্যান ফাইল
        """
        self.log_file = log_file
        self.stats_file = stats_file
        self.trades_buffer = []
        self.session_trades = []
        
        # CSV হেডার তৈরি করুন
        self.csv_headers = [
            'timestamp', 'asset', 'direction', 'entry_price', 'exit_price',
            'position_size', 'stop_loss', 'take_profit', 'profit_loss',
            'profit_percent', 'duration_minutes', 'exit_reason'
        ]
        
        self._initialize_csv()
    
    def _initialize_csv(self):
        """CSV ফাইল ইনিশিয়ালাইজ করুন"""
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.csv_headers)
                logger.info(f"✅ নতুন লগ ফাইল তৈরি: {self.log_file}")
        
        except Exception as e:
            logger.error(f"❌ CSV ফাইল তৈরিতে ত্রুটি: {e}")
    
    def log_trade(self, trade_data: Dict) -> bool:
        """
        একটি ট্রেড লগ করুন
        
        Args:
            trade_data: ট্রেড তথ্য
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            row = [
                trade_data.get('timestamp', datetime.now().isoformat()),
                trade_data.get('asset', 'N/A'),
                trade_data.get('direction', 'N/A'),
                f"{trade_data.get('entry_price', 0):.4f}",
                f"{trade_data.get('exit_price', 0):.4f}" if trade_data.get('exit_price') else 'N/A',
                f"{trade_data.get('position_size', 0):.4f}",
                f"{trade_data.get('stop_loss', 0):.4f}",
                f"{trade_data.get('take_profit', 0):.4f}",
                f"{trade_data.get('profit_loss', 0):.2f}" if trade_data.get('profit_loss') is not None else 'N/A',
                f"{trade_data.get('profit_percent', 0):.2f}" if trade_data.get('profit_percent') is not None else 'N/A',
                f"{trade_data.get('duration_minutes', 0):.1f}" if trade_data.get('duration_minutes') is not None else 'N/A',
                trade_data.get('exit_reason', 'N/A')
            ]
            
            # বাফারে যোগ করুন
            self.trades_buffer.append(row)
            self.session_trades.append(trade_data)
            
            # প্রতি ১০টি ট্রেডে লিখুন
            if len(self.trades_buffer) >= 10:
                self._flush_buffer()
            
            return True
        
        except Exception as e:
            logger.error(f"❌ ট্রেড লগিংয়ে ত্রুটি: {e}")
            return False
    
    def _flush_buffer(self):
        """বাফার ফাইলে লিখুন"""
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(self.trades_buffer)
            
            logger.debug(f"✅ {len(self.trades_buffer)} ট্রেড সংরক্ষিত")
            self.trades_buffer = []
        
        except Exception as e:
            logger.error(f"❌ বাফার লেখায় ত্রুটি: {e}")
    
    def flush_all(self):
        """সমস্ত বাফার ফ্লাশ করুন"""
        if self.trades_buffer:
            self._flush_buffer()
    
    def log_signal(self, signal: Dict) -> bool:
        """
        একটি সিগনাল লগ করুন
        
        Args:
            signal: সিগনাল তথ্য
            
        Returns:
            সাফল্য অবস্থা
        """
        try:
            signal_log = {
                'timestamp': datetime.now().isoformat(),
                'asset': signal.get('asset'),
                'signal': signal.get('signal'),
                'strength': signal.get('strength'),
                'confidence': signal.get('confidence'),
                'reasons': signal.get('reasons', [])
            }
            
            logger.debug(f"📝 সিগনাল লগ: {signal_log}")
            return True
        
        except Exception as e:
            logger.error(f"❌ সিগনাল লগিংয়ে ত্রুটি: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        ট্রেড পরিসংখ্যান পান
        
        Returns:
            পরিসংখ্যান অভিধান
        """
        if not self.session_trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_profit': 0.0,
                'avg_profit_per_trade': 0.0,
                'profit_factor': 0.0
            }
        
        total_profit = 0
        winning_trades = 0
        losing_trades = 0
        
        for trade in self.session_trades:
            if trade.get('profit_loss') is not None:
                profit = trade['profit_loss']
                total_profit += profit
                
                if profit >= 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
        
        total_trades = len(self.session_trades)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        avg_profit = total_profit / total_trades if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 3),
            'total_profit': round(total_profit, 2),
            'avg_profit_per_trade': round(avg_profit, 2)
        }
    
    def save_session_stats(self, session_stats: Dict):
        """সেশন পরিসংখ্যান সংরক্ষণ করুন"""
        try:
            stats_data = {
                'session_date': datetime.now().isoformat(),
                'session_stats': session_stats,
                'trading_stats': self.get_statistics(),
                'total_session_trades': len(self.session_trades)
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 সেশন পরিসংখ্যান সংরক্ষিত: {self.stats_file}")
        
        except Exception as e:
            logger.error(f"❌ সেশন পরিসংখ্যান সংরক্ষণে ত্রুটি: {e}")
    
    def get_daily_summary(self) -> Dict:
        """দৈনিক সারসংক্ষেপ পান"""
        today = date.today().isoformat()
        
        today_trades = [t for t in self.session_trades 
                       if t.get('timestamp', '').startswith(today)]
        
        if not today_trades:
            return {
                'date': today,
                'trades': 0,
                'profit': 0.0,
                'win_rate': 0.0
            }
        
        total_profit = sum(t.get('profit_loss', 0) for t in today_trades)
        winning = sum(1 for t in today_trades if t.get('profit_loss', 0) >= 0)
        win_rate = winning / len(today_trades) if today_trades else 0
        
        return {
            'date': today,
            'trades': len(today_trades),
            'profit': round(total_profit, 2),
            'win_rate': round(win_rate, 3)
        }
    
    def export_to_json(self, filename: str = None) -> bool:
        """সমস্ত ট্রেড JSON-এ রপ্তানি করুন"""
        try:
            if filename is None:
                filename = f"trades_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_trades': len(self.session_trades),
                'statistics': self.get_statistics(),
                'trades': self.session_trades
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ ট্রেড রপ্তানি করা হয়েছে: {filename}")
            return True
        
        except Exception as e:
            logger.error(f"❌ ট্রেড রপ্তানিতে ত্রুটি: {e}")
            return False
