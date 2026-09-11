#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
স্বয়ংক্রিয় সেটআপ এবং ইনস্টলেশন স্ক্রিপ্ট
সমস্ত প্রয়োজনীয় ফাইল এবং ডিরেক্টরি তৈরি করে
"""

import os
import shutil
import sys
from pathlib import Path

class BotSetup:
    """বট সেটআপ এবং ইনিশিয়ালাইজেশন"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.bot_dir = self.root_dir / 'bot'
        self.logs_dir = self.root_dir / 'logs'
        self.data_dir = self.root_dir / 'data'
    
    def create_directories(self):
        """প্রয়োজনীয় ডিরেক্টরি তৈরি করুন"""
        print("📁 ডিরেক্টরি তৈরি করছি...")
        
        for directory in [self.bot_dir, self.logs_dir, self.data_dir]:
            directory.mkdir(exist_ok=True)
            print(f"  ✅ {directory.name}/")
    
    def create_env_file(self):
        """পরিবেশ ফাইল তৈরি করুন"""
        print("\n⚙️ পরিবেশ ফাইল তৈরি করছি...")
        
        env_file = self.root_dir / '.env'
        env_example = self.root_dir / '.env.example'
        
        if not env_file.exists() and env_example.exists():
            shutil.copy(env_example, env_file)
            print(f"  ✅ {env_file.name} তৈরি করা হয়েছে")
            print(f"  📝 অনুগ্রহ করে {env_file.name} ফাইলে আপনার শংসাপত্র যোগ করুন")
        else:
            print(f"  ℹ️ {env_file.name} ইতিমধ্যে বিদ্যমান")
    
    def create_log_files(self):
        """লগ ফাইল তৈরি করুন"""
        print("\n📋 লগ ফাইল তৈরি করছি...")
        
        log_file = self.root_dir / 'bot.log'
        trading_log = self.root_dir / 'trading_log.csv'
        
        # bot.log
        if not log_file.exists():
            log_file.touch()
            print(f"  ✅ {log_file.name} তৈরি করা হয়েছে")
        
        # trading_log.csv
        if not trading_log.exists():
            with open(trading_log, 'w', encoding='utf-8') as f:
                f.write('timestamp,asset,direction,entry_price,exit_price,position_size,stop_loss,take_profit,profit_loss,profit_percent,duration_minutes,exit_reason\n')
            print(f"  ✅ {trading_log.name} তৈরি করা হয়েছে")
    
    def install_dependencies(self):
        """নির্ভরতা ইনস্টল করুন"""
        print("\n📦 নির্ভরতা ইনস্টল করছি...")
        
        requirements_file = self.root_dir / 'requirements.txt'
        
        if requirements_file.exists():
            print("  🔄 pip থেকে প্যাকেজ ইনস্টল করছি...")
            os.system(f"{sys.executable} -m pip install -r {requirements_file}")
            print("  ✅ নির্ভরতা ইনস্টল সম্পূর্ণ")
        else:
            print(f"  ⚠️ {requirements_file.name} পাওয়া যায়নি")
    
    def verify_installation(self):
        """ইনস্টলেশন যাচাই করুন"""
        print("\n✅ ইনস্টলেশন যাচাই করছি...")
        
        required_files = [
            'main.py',
            'config.py',
            'requirements.txt',
            '.env.example',
            'bot/__init__.py',
            'bot/quotex_bot.py',
            'bot/indicators.py',
            'bot/signal_generator.py',
            'bot/telegram_notifier.py',
            'bot/logger.py'
        ]
        
        missing_files = []
        for file in required_files:
            file_path = self.root_dir / file
            if file_path.exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file}")
                missing_files.append(file)
        
        return len(missing_files) == 0
    
    def run(self):
        """সম্পূর্ণ সেটআপ চালান"""
        print("="*50)
        print("🤖 Quotex Signal Bot - সেটআপ শুরু")
        print("="*50)
        
        self.create_directories()
        self.create_env_file()
        self.create_log_files()
        
        print("\n" + "="*50)
        print("💡 পরবর্তী পদক্ষেপ:")
        print("="*50)
        print("\n1. .env ফাইলে আপনার শংসাপত্র যোগ করুন:")
        print("   - QUOTEX_EMAIL")
        print("   - QUOTEX_PASSWORD")
        print("   - QUOTEX_API_KEY")
        print("   - TELEGRAM_TOKEN (ঐচ্ছিক)")
        print("   - TELEGRAM_CHAT_ID (ঐচ্ছিক)")
        
        print("\n2. নির্ভরতা ইনস্টল করুন:")
        print(f"   pip install -r requirements.txt")
        
        print("\n3. বট চালু করুন:")
        print(f"   python main.py")
        
        print("\n" + "="*50)
        
        if self.verify_installation():
            print("\n✅ সেটআপ সফল!")
        else:
            print("\n⚠️ কিছু ফাইল অনুপস্থিত। অনুগ্রহ করে ম্যানুয়ালি যোগ করুন।")


if __name__ == '__main__':
    setup = BotSetup()
    setup.run()
