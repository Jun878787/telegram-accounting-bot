# Telegram 記帳機器人

這是一個功能強大的 Telegram 記帳機器人，專為管理個人和群組財務而設計。

## 主要功能

- 💰 記錄 TWD 和 CNY 貨幣交易
- 📊 生成月度報表
- 📚 查看歷史報表
- 💱 匯率設置與轉換
- 🔧 強大的群組管理功能
- ⚙️ 可自定義的管理員權限
- 🖥️ 網頁管理界面

## 安裝與設置

1. 克隆此儲存庫
```bash
git clone https://github.com/Jun878787/telegram-accounting-bot.git
cd telegram-accounting-bot
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 配置機器人
   - 從 BotFather 獲取 Telegram API 令牌
   - 創建 `config.py` 文件並配置必要參數

4. 啟動機器人
```bash
python bot.py
```

5. 連接到 GitHub
```bash
git remote add origin https://github.com/Jun878787/telegram-accounting-bot.git
```

## 使用網頁管理界面

本專案包含一個網頁管理界面，可以更方便地管理機器人：

1. 啟動管理伺服器
```bash
python server.py
```

2. 打開瀏覽器訪問
```
http://127.0.0.1:5000
```

3. 在網頁界面中，您可以：
   - 啟動/停止機器人
   - 查看機器人狀態
   - 查看運行日誌

## 使用方法

### 基本指令
- `/start` - 啟動機器人
- `/help` 或 `幫助` - 顯示幫助信息
- `📋指令說明` - 顯示詳細指令列表

### 記帳格式
- `TW+100` - 新增 100 TWD
- `TW-50` - 減少 50 TWD
- `CN+200` - 新增 200 CNY
- `CN-30` - 減少 30 CNY
- `2023/01/01 TW+100` - 指定日期的交易

### 管理員指令
- `💱設置匯率` - 設置當前匯率
- `⚙️群管設定` - 管理群組設置
- `🔒 權限管理` - 管理用戶權限

## 部署到雲端
本專案可以部署到各種雲服務商，包括：
- Google Cloud Platform
- DigitalOcean
- AWS
- Heroku

詳細部署指南請參考 [部署文檔](docs/deployment.md)。

## 貢獻

歡迎提交 Pull Requests 和 Issues。

## 授權

[MIT License](LICENSE)
