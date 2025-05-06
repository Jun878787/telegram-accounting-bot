#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import logging
import os
import json
import datetime
import subprocess
import sys
import signal

app = Flask(__name__)

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("server.log", encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 全局變量
BOT_STATUS = {
    "running": False,
    "last_start": None,
    "pid": None,
    "process": None
}

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# 路由
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Telegram 記帳機器人伺服器</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }
                button:hover { background: #45a049; }
                button.stop { background: #f44336; }
                button.stop:hover { background: #d32f2f; }
                .status { margin-top: 20px; padding: 15px; background: #e7f3fe; border-left: 5px solid #2196F3; }
                .logs { margin-top: 20px; background: #f9f9f9; padding: 15px; border: 1px solid #ddd; max-height: 300px; overflow-y: auto; }
                pre { margin: 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Telegram 記帳機器人管理伺服器</h1>
                <div>
                    <button onclick="startBot()">啟動機器人</button>
                    <button class="stop" onclick="stopBot()">停止機器人</button>
                    <button onclick="checkStatus()">檢查狀態</button>
                </div>
                <div class="status" id="status">
                    <p>機器人狀態：正在檢查...</p>
                </div>
                <h2>最近操作日誌</h2>
                <div class="logs" id="logs">
                    <pre>正在載入日誌...</pre>
                </div>
            </div>

            <script>
                function startBot() {
                    fetch('/start_bot', { method: 'POST' })
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('status').innerHTML = '<p>機器人狀態：' + (data.success ? '運行中' : '啟動失敗') + '</p>';
                            if (data.message) {
                                document.getElementById('status').innerHTML += '<p>' + data.message + '</p>';
                            }
                            checkLogs();
                        });
                }

                function stopBot() {
                    fetch('/stop_bot', { method: 'POST' })
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('status').innerHTML = '<p>機器人狀態：' + (data.success ? '已停止' : '停止失敗') + '</p>';
                            if (data.message) {
                                document.getElementById('status').innerHTML += '<p>' + data.message + '</p>';
                            }
                            checkLogs();
                        });
                }

                function checkStatus() {
                    fetch('/bot_status')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('status').innerHTML = '<p>機器人狀態：' + (data.running ? '運行中' : '未運行') + '</p>';
                            if (data.last_start) {
                                document.getElementById('status').innerHTML += '<p>上次啟動時間：' + data.last_start + '</p>';
                            }
                            if (data.pid) {
                                document.getElementById('status').innerHTML += '<p>進程 ID：' + data.pid + '</p>';
                            }
                            checkLogs();
                        });
                }

                function checkLogs() {
                    fetch('/get_logs')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('logs').innerHTML = '<pre>' + data.logs + '</pre>';
                        });
                }

                // 頁面加載時檢查狀態
                window.onload = function() {
                    checkStatus();
                };
            </script>
        </body>
    </html>
    """

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global BOT_STATUS

    if BOT_STATUS["running"]:
        return jsonify({"success": False, "message": "機器人已經在運行中"})

    try:
        logger.info("嘗試啟動機器人...")
        # 使用更安全的方式啟動機器人
        # 在 Windows 中使用 subprocess.Popen
        if sys.platform.startswith('win'):
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                ["python", "bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=si,
                shell=True
            )
        else:
            # 非 Windows 平台
            process = subprocess.Popen(
                ["python", "bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        # 更新狀態
        BOT_STATUS["running"] = True
        BOT_STATUS["last_start"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        BOT_STATUS["pid"] = process.pid
        BOT_STATUS["process"] = process
        
        logger.info(f"機器人已啟動，PID: {BOT_STATUS['pid']}")
        return jsonify({"success": True, "message": f"機器人已啟動，PID: {BOT_STATUS['pid']}"})
    except Exception as e:
        error_msg = f"啟動機器人時發生錯誤: {str(e)}"
        logger.error(error_msg)
        return jsonify({"success": False, "message": error_msg})

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global BOT_STATUS

    if not BOT_STATUS["running"]:
        return jsonify({"success": False, "message": "機器人未在運行"})

    try:
        logger.info(f"嘗試停止機器人 (PID: {BOT_STATUS['pid']})...")
        if BOT_STATUS["process"]:
            # 安全地終止進程
            if sys.platform.startswith('win'):
                # Windows 平台
                try:
                    import psutil
                    parent = psutil.Process(BOT_STATUS["pid"])
                    for child in parent.children(recursive=True):
                        child.terminate()
                    parent.terminate()
                except ImportError:
                    # 如果沒有安裝 psutil，使用基本方法
                    BOT_STATUS["process"].terminate()
            else:
                # 非 Windows 平台
                os.killpg(os.getpgid(BOT_STATUS["process"].pid), signal.SIGTERM)
        
        BOT_STATUS["running"] = False
        BOT_STATUS["process"] = None
        
        logger.info("機器人已停止")
        return jsonify({"success": True, "message": "機器人已停止"})
    except Exception as e:
        error_msg = f"停止機器人時發生錯誤: {str(e)}"
        logger.error(error_msg)
        return jsonify({"success": False, "message": error_msg})

@app.route('/bot_status')
def bot_status():
    if BOT_STATUS["process"] and BOT_STATUS["process"].poll() is not None:
        # 進程已終止但狀態未更新
        BOT_STATUS["running"] = False
        BOT_STATUS["process"] = None
        logger.info("檢測到機器人進程已終止，更新狀態")

    return jsonify({
        "running": BOT_STATUS["running"],
        "last_start": BOT_STATUS["last_start"],
        "pid": BOT_STATUS["pid"] if BOT_STATUS["running"] else None
    })

@app.route('/get_logs')
def get_logs():
    try:
        log_file = "server.log"
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                # 讀取最後 50 行
                lines = f.readlines()
                last_lines = lines[-50:] if len(lines) > 50 else lines
                logs = ''.join(last_lines)
        else:
            logs = "日誌文件不存在"
        
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"logs": f"讀取日誌時發生錯誤: {str(e)}"})

if __name__ == '__main__':
    logger.info("伺服器啟動中...")
    try:
        # 從環境變數獲取端口，或使用預設值 5000
        port = int(os.environ.get("PORT", 5000))
        # 監聽所有介面 (0.0.0.0)，而不僅僅是本地回環介面
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"伺服器啟動失敗: {str(e)}")
        print(f"伺服器啟動失敗: {str(e)}") 