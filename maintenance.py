#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বট আপডেট এবং রক্ষণাবেক্ষণ ইউটিলিটি
বট সংস্করণ, ডেটা এবং অ্যাকাউন্ট পরিচালনা করুন
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class BotMaintenance:
    """বট রক্ষণাবেক্ষণ সরঞ্জাম"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
    
    def backup_data(self, backup_dir='backups'):
        """ট্রেড ডেটা ব্যাকআপ করুন"""
        print("💾 ডেটা ব্যাকআপ করছি...")
        
        backup_path = self.root_dir / backup_dir
        backup_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_folder = backup_path / backup_name
        backup_folder.mkdir(exist_ok=True)
        
        files_to_backup = [
            'trading_log.csv',
            'bot_stats.json',
            'bot.log'
        ]
        
        for file in files_to_backup:
            file_path = self.root_dir / file
            if file_path.exists():
                import shutil
                shutil.copy(file_path, backup_folder / file)
                print(f"  ✅ {file}")
        
        print(f"✅ ব্যাকআপ সংরক্ষিত: {backup_folder}")
    
    def clean_logs(self):
        """পুরানো লগ ফাইল সাফ করুন"""
        print("🧹 লগ ফাইল সাফ করছি...")
        
        log_file = self.root_dir / 'bot.log'
        if log_file.exists():
            # ফাইল সাইজ চেক করুন (>50MB হলে)
            if log_file.stat().st_size > 50 * 1024 * 1024:
                archive_name = f"bot_old_{datetime.now().strftime('%Y%m%d')}.log"
                import shutil
                shutil.move(str(log_file), str(self.root_dir / archive_name))
                print(f"  ✅ পুরানো লগ সংরক্ষিত: {archive_name}")
    
    def show_stats(self):
        """বর্তমান পরিসংখ্যান দেখান"""
        print("\n📊 বর্তমান পরিসংখ্যান:")
        print("="*50)
        
        stats_file = self.root_dir / 'bot_stats.json'
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
                print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print("ℹ️ কোনও পরিসংখ্যান উপলব্ধ নেই")
    
    def check_dependencies(self):
        """নির্ভরতা সংস্করণ চেক করুন"""
        print("\n📦 নির্ভরতা সংস্করণ:")
        print("="*50)
        
        packages = ['pandas', 'numpy', 'requests', 'python-telegram-bot']
        
        for package in packages:
            try:
                result = subprocess.run(
                    ['pip', 'show', package],
                    capture_output=True,
                    text=True
                )
                if 'Version' in result.stdout:
                    version = [line.split(': ')[1] for line in result.stdout.split('\n') if 'Version' in line][0]
                    print(f"  ✅ {package}: {version}")
            except:
                print(f"  ❌ {package}: অনুপস্থিত")
    
    def update_bot(self):
        """বট আপডেট করুন (Git থেকে)"""
        print("🔄 বট আপডেট করছি...")
        
        try:
            os.chdir(self.root_dir)
            subprocess.run(['git', 'pull'], check=True)
            print("✅ বট সফলভাবে আপডেট হয়েছে")
        except Exception as e:
            print(f"❌ আপডেট ব্যর্থ: {e}")
    
    def run_menu(self):
        """ইন্টারঅ্যাক্টিভ মেনু"""
        while True:
            print("\n" + "="*50)
            print("🤖 বট রক্ষণাবেক্ষণ মেনু")
            print("="*50)
            print("1. ডেটা ব্যাকআপ করুন")
            print("2. লগ ফাইল সাফ করুন")
            print("3. পরিসংখ্যান দেখান")
            print("4. নির্ভরতা চেক করুন")
            print("5. বট আপডেট করুন (Git)")
            print("6. প্রস্থান করুন")
            print("="*50)
            
            choice = input("\nপছন্দ নির্বাচন করুন (1-6): ").strip()
            
            if choice == '1':
                self.backup_data()
            elif choice == '2':
                self.clean_logs()
            elif choice == '3':
                self.show_stats()
            elif choice == '4':
                self.check_dependencies()
            elif choice == '5':
                self.update_bot()
            elif choice == '6':
                print("\n👋 বিদায়!")
                break
            else:
                print("❌ অবৈধ পছন্দ। আবার চেষ্টা করুন।")


if __name__ == '__main__':
    maintenance = BotMaintenance()
    maintenance.run_menu()
