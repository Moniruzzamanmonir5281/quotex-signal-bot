import os
from dotenv import load_dotenv

load_dotenv()

# Quotex API কনফিগারেশন
QUOTEX_EMAIL = os.getenv('QUOTEX_EMAIL', 'your_email@example.com')
QUOTEX_PASSWORD = os.getenv('QUOTEX_PASSWORD', 'your_password')
QUOTEX_API_KEY = os.getenv('QUOTEX_API_KEY', 'your_api_key')

# ট্রেডিং সেটিংস
TRADE_AMOUNT = int(os.getenv('TRADE_AMOUNT', 10))  # ডলারে
ASSETS = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))  # সেকেন্ডে
TIMEFRAME = '1m'  # 1 মিনিট

# সিগনাল সেটিংস
SMA_SHORT = 10
SMA_LONG = 20
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ঝুঁকি ব্যবস্থাপনা
MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 100))  # সর্বোচ্চ দৈনিক ক্ষতি
MAX_TRADES_PER_DAY = int(os.getenv('MAX_TRADES_PER_DAY', 10))
WIN_RATE_THRESHOLD = 0.55  # লাভের হার 55% এর উপরে

# টেলিগ্রাম নোটিফিকেশন
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
SEND_NOTIFICATIONS = os.getenv('SEND_NOTIFICATIONS', 'true').lower() == 'true'

# ডেটাবেস সেটিংস
LOG_FILE = 'trading_log.csv'
STATS_FILE = 'bot_stats.json'

# ডেবাগ মোড
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
