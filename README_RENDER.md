# 在 Render 上部署 Telegram 記帳機器人

本文檔提供將 Telegram 記帳機器人部署到 Render 平台的指南。

## 準備工作

1. 在 [Render](https://render.com/) 上創建帳戶
2. 確保您的 Telegram Bot Token 已準備好

## 部署步驟

### 方法一：使用 GitHub 儲存庫

1. 將專案推送到 GitHub 儲存庫
   ```bash
   git add .
   git commit -m "準備 Render 部署"
   git push origin main
   ```

2. 在 Render 儀表板中：
   - 點擊 "New" > "Blueprint"
   - 連接您的 GitHub 帳戶並選擇包含機器人代碼的儲存庫
   - Render 將自動檢測 `render.yaml` 並據此設置服務

3. 設置環境變數：
   - 在 Blueprint 部署頁面中，為 Telegram Bot 添加所需的環境變數：
     - `TOKEN`: 您的 Telegram Bot Token

4. 點擊 "Apply" 開始部署

### 方法二：手動設置服務

如果您不想使用 Blueprint，可以手動設置 Web 服務和 Worker 服務：

#### Web 服務 (管理界面)

1. 在 Render 儀表板中選擇 "New" > "Web Service"
2. 連接您的 GitHub 儲存庫
3. 填寫以下資訊：
   - Name: telegram-bot-server
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn server:app`
4. 點擊 "Create Web Service"

#### Worker 服務 (機器人)

1. 在 Render 儀表板中選擇 "New" > "Background Worker"
2. 連接您的 GitHub 儲存庫
3. 填寫以下資訊：
   - Name: telegram-bot-worker
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
4. 添加環境變數：
   - `TOKEN`: 您的 Telegram Bot Token
5. 點擊 "Create Background Worker"

## 注意事項

### 持久性存儲

Render 的免費和付費實例都提供臨時磁盤空間，這意味著在部署更新或服務重啟時，本地存儲的數據可能會丟失。考慮以下選項：

1. 使用 Render 的 Disk 服務（僅適用於付費方案）
2. 使用外部數據存儲服務，如：
   - MongoDB Atlas
   - Firebase
   - PostgreSQL
   - Redis

### 監控與日誌

- Render 提供了內置的日誌查看器
- 您可以在每個服務的儀表板中查看日誌
- 考慮設置通知以在服務停止時收到提醒

### 成本控制

- Render 提供免費層級，但有使用限制
- Web 服務免費層級在一段不活動後會休眠
- 付費方案從 $7/月起，提供更好的性能和更長的正常運行時間 