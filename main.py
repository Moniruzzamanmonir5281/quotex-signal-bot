#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quotex Trading Signal Bot
উন্নত সূচক সহ স্বয়ংক্রিয় ট্রেডিং বট
"""

import logging
import sys
from bot.quotex_bot import QuotexSignalBot
from config import DEBUG

# লগিং সেটআপ
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("🤖 Quotex Signal Bot শুরু হচ্ছে...")
        
        bot = QuotexSignalBot()
        
        # বট চালু করুন
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("⛔ বট ব্যবহারকারীদ্বারা বন্ধ করা হয়েছে")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ ত্রুটি: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
