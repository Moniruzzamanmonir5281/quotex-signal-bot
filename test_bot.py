#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
বট পরীক্ষা স্ক্রিপ্ট
সমস্ত উপাদান সঠিকভাবে কাজ করছে কিনা যাচাই করুন
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """সমস্ত ইমপোর্ট পরীক্ষা করুন"""
    print("🧪 ইমপোর্ট পরীক্ষা করছি...")
    print("="*50)
    
    tests = [
        ('config', 'কনফিগারেশন মডিউল'),
        ('bot.indicators', 'সূচক মডিউল'),
        ('bot.signal_generator', 'সিগনাল জেনারেটর মডিউল'),
        ('bot.quotex_bot', 'কোটেক্স বট মডিউল'),
        ('bot.telegram_notifier', 'টেলিগ্রাম নোটিফায়ার মডিউল'),
        ('bot.logger', 'লগার মডিউল'),
    ]
    
    passed = 0
    failed = 0
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name}")
            passed += 1
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed += 1
    
    print("="*50)
    print(f"ফলাফল: {passed} সফল, {failed} ব্যর্থ\n")
    
    return failed == 0

def test_config():
    """কনফিগারেশন পরীক্ষা করুন"""
    print("⚙️ কনফিগারেশন পরীক্ষা করছি...")
    print("="*50)
    
    try:
        from config import (
            QUOTEX_EMAIL, QUOTEX_PASSWORD, TRADE_AMOUNT,
            MAX_DAILY_LOSS, MAX_TRADES_PER_DAY, ASSETS
        )
        
        print(f"✅ Quotex ইমেল: {QUOTEX_EMAIL[:10]}...")
        print(f"✅ ট্রেড পরিমাণ: ${TRADE_AMOUNT}")
        print(f"✅ সর্বোচ্চ দৈনিক ক্ষতি: ${MAX_DAILY_LOSS}")
        print(f"✅ সর্বোচ্চ দৈনিক ট্রেড: {MAX_TRADES_PER_DAY}")
        print(f"✅ ট্রেড সম্পদ: {', '.join(ASSETS)}")
        print("="*50)
        print("✅ কনফিগারেশন সফল\n")
        return True
    
    except Exception as e:
        print(f"❌ কনফিগারেশন ত্রুটি: {e}")
        print("="*50 + "\n")
        return False

def test_indicators():
    """সূচক কার্যকারিতা পরীক্ষা করুন"""
    print("📊 সূচক পরীক্ষা করছি...")
    print("="*50)
    
    try:
        from bot.indicators import TechnicalIndicators
        
        # নমুনা ডেটা
        prices = [100 + i*0.5 for i in range(50)]
        
        # SMA
        sma = TechnicalIndicators.calculate_sma(prices, 20)
        print(f"✅ SMA (20): {sma:.4f}")
        
        # RSI
        rsi = TechnicalIndicators.calculate_rsi(prices, 14)
        print(f"✅ RSI (14): {rsi:.2f}")
        
        # MACD
        macd = TechnicalIndicators.calculate_macd(prices)
        print(f"✅ MACD: {macd['macd']:.4f}")
        
        # Bollinger Bands
        bb = TechnicalIndicators.calculate_bollinger_bands(prices)
        print(f"✅ Bollinger Bands: {bb['upper']:.4f} - {bb['lower']:.4f}")
        
        print("="*50)
        print("✅ সূচক পরীক্ষা সফল\n")
        return True
    
    except Exception as e:
        print(f"❌ সূচক ত্রুটি: {e}")
        print("="*50 + "\n")
        return False

def test_signal_generator():
    """সিগনাল জেনারেটর পরীক্ষা করুন"""
    print("🎯 সিগনাল জেনারেটর পরীক্ষা করছি...")
    print("="*50)
    
    try:
        from bot.signal_generator import SignalGenerator
        
        generator = SignalGenerator()
        prices = [100 + i*0.5 for i in range(50)]
        
        signal = generator.generate_signal(prices)
        
        print(f"✅ সিগনাল: {signal['signal']}")
        print(f"✅ শক্তি: {signal['strength']}")
        print(f"✅ আস্থা: {signal['confidence']}")
        print(f"✅ কারণ সংখ্যা: {len(signal['reasons'])}")
        
        print("="*50)
        print("✅ সিগনাল জেনারেটর পরীক্ষা সফল\n")
        return True
    
    except Exception as e:
        print(f"❌ সিগনাল জেনারেটর ত্রুটি: {e}")
        print("="*50 + "\n")
        return False

def run_all_tests():
    """সমস্ত পরীক্ষা চালান"""
    print("\n" + "="*50)
    print("🤖 বট সিস্টেম পরীক্ষা")
    print("="*50 + "\n")
    
    results = [
        ("ইমপোর্ট পরীক্ষা", test_imports()),
        ("কনফিগারেশন পরীক্ষা", test_config()),
        ("সূচক পরীক্ষা", test_indicators()),
        ("সিগনাল জেনারেটর পরীক্ষা", test_signal_generator()),
    ]
    
    print("="*50)
    print("📊 পরীক্ষার ফলাফল:")
    print("="*50)
    
    for test_name, result in results:
        status = "✅ সফল" if result else "❌ ব্যর্থ"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("="*50)
    if all_passed:
        print("\n✅ সমস্ত পরীক্ষা সফল!")
        print("আপনি এখন বট চালাতে পারেন: python main.py\n")
    else:
        print("\n❌ কিছু পরীক্ষা ব্যর্থ হয়েছে।")
        print("অনুগ্রহ করে ত্রুটিগুলি সমাধান করুন এবং আবার চেষ্টা করুন।\n")
    
    return all_passed


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
