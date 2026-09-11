#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ট্রেডিং লগ এবং বিশ্লেষণ মডিউল
CSV এবং JSON এ লগ সংরক্ষণ, পরিসংখ্যান ট্র্যাকিং
"""

import csv
import json
import logging
from typing import Dict, List
from datetime import datetime, date
import os

logger = logging.getLogger(__name__)


class TradingLogger:
    """ট্রেডিং লগিং সিস্টেম"""
    
    def __init__(self, log_file: str = 'trading_log.csv', stats_file: str = 'bot_stats.json'):
        """লগার ইনিশিয়ালাইজ করুন"""
        self.log_file = log_file
        self.stats_file = stats_file
        self.trades_buffer = []
        self.session_trades = []
        self.csv_headers = ['timestamp', 'asset', 'direction', 'entry_price', 'exit_price', 'position_size', 'stop_loss', 'take_profit', 'profit_loss', 'profit_percent', 'duration_minutes', 'exit_reason']
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
        """একটি ট্রেড লগ করুন"""
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
            self.trades_buffer.append(row)
            self.session_trades.append(trade_data)
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
    
    def get_statistics(self) -> Dict:
        """ট্রেড পরিসংখ্যান পান"""
        if not self.session_trades:
            return {'total_trades': 0, 'winning_trades': 0, 'losing_trades': 0, 'win_rate': 0.0, 'total_profit': 0.0, 'avg_profit_per_trade': 0.0}
        
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
        
        return {'total_trades': total_trades, 'winning_trades': winning_trades, 'losing_trades': losing_trades, 'win_rate': round(win_rate, 3), 'total_profit': round(total_profit, 2), 'avg_profit_per_trade': round(avg_profit, 2)}
