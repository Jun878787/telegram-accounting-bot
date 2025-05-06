#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Telegram API 令牌
# 從 https://t.me/BotFather 獲取
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# 管理員用戶 ID
# 這些用戶將擁有機器人的完全控制權
ADMIN_IDS = [123456789, 987654321]

# 預設匯率 (CNY 到 TWD)
DEFAULT_RATE = 4.3

# 數據文件路徑
DATA_FILE = 'data/accounting_data.json'
RATE_FILE = 'data/rate_data.json'
FUND_FILE = 'data/fund_data.json'
SETTINGS_FILE = 'data/settings.json'

# 機器人設置
CLEAN_INTERVAL = 30  # 清理舊數據的間隔（天）
HEARTBEAT_INTERVAL = 60  # 心跳檢測間隔（秒）
MAX_ERROR_COUNT = 5  # 允許的最大連續錯誤數
ERROR_RESET_TIME = 600  # 錯誤計數器重置時間（秒）

# 歡迎詞
DEFAULT_WELCOME_MESSAGE = "歡迎使用記帳機器人！\n使用 /help 或 '幫助' 獲取使用說明。" 