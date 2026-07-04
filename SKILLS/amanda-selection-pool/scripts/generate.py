import pandas as pd
import json
import re
import requests
import io
import datetime
import sys
import os

def generate(output_path):
    url = 'https://docs.google.com/spreadsheets/d/1Bl9SRtxSp2StQH99wPLn8TyfvSYRlyHu6-tIS2F_UHg/gviz/tq?tqx=out:csv&sheet=Amanda'

    try:
        print(f"Fetching data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        csv_text = response.content.decode('utf-8')
        
        df = pd.read_csv(io.StringIO(csv_text))
        data_df = df.iloc[:, :6].copy()
        
        def clean_code(x):
            if pd.isna(x): return ""
            s = str(x).strip()
            s = re.sub(r'\.0$', '', s)
            s = re.sub(r'[^A-Z0-9]', '', s.upper())
            return s

        def clean_name(x):
            if pd.isna(x): return ""
            return str(x).strip()

        def process_val(val):
            if pd.isna(val): return "N/A"
            s = str(val).strip()
            if s == "" or s.lower() == "#n/a" or s.lower() == "nan" or s == "#N/A":
                return "N/A"
            return s

        stock_map = {}
        for _, row in data_df.iterrows():
            code = clean_code(row.iloc[0])
            name = clean_name(row.iloc[1])
            if code and name:
                stock_map[code] = {
                    "name": name,
                    "date": process_val(row.iloc[2]),
                    "last_close": process_val(row.iloc[3]),
                    "avg_price": process_val(row.iloc[4]),
                    "cost": process_val(row.iloc[5])
                }

        update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        html_content = r"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Amanda 選股池查詢</title>
    <style>
        * { -webkit-tap-highlight-color: transparent; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 450px;
            text-align: center;
        }
        h1 {
            color: #1a73e8;
            margin: 0 0 5px 0;
            font-size: 26px;
        }
        .update-time {
            font-size: 11px;
            color: #9aa0a6;
            margin-bottom: 25px;
        }
        .input-group {
            position: relative;
            margin-bottom: 25px;
        }
        input {
            width: 100%;
            padding: 18px;
            font-size: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            box-sizing: border-box;
            outline: none;
            transition: all 0.3s;
            background-color: #f8f9fa;
        }
        input:focus {
            border-color: #1a73e8;
            background-color: #fff;
            box-shadow: 0 0 0 4px rgba(26, 115, 232, 0.1);
        }
        .result-container {
            min-height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .result {
            padding: 20px;
            border-radius: 15px;
            display: none;
            flex-direction: column;
            text-align: left;
            animation: fadeIn 0.3s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result.found {
            display: flex;
            background-color: #f1f8ff;
            border: 1px solid #c8e1ff;
        }
        .result.not-found {
            display: flex;
            background-color: #fff5f5;
            border: 1px solid #feb2b2;
            text-align: center;
            justify-content: center;
        }
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 2px solid #d1e3fa;
            padding-bottom: 12px;
        }
        .stock-name {
            font-size: 26px;
            font-weight: 800;
            color: #174ea6;
        }
        .stock-date {
            font-size: 13px;
            color: #5f6368;
            background: #e1effe;
            padding: 4px 8px;
            border-radius: 6px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }
        .info-item {
            display: flex;
            flex-direction: column;
        }
        .info-label {
            color: #70757a;
            font-size: 13px;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 18px;
            font-weight: 600;
            color: #202124;
        }
        .status {
            font-size: 20px;
            color: #d93025;
            font-weight: bold;
        }
        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #9aa0a6;
        }
        .empty-msg {
            color: #9aa0a6;
            font-size: 16px;
            padding: 40px 0;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Amanda 選股池</h1>
        <div class="update-time">最後同步: UPDATE_TIME_PLACEHOLDER</div>
        <div class="input-group">
            <input type="text" id="stockInput" placeholder="請輸入股票代碼" autocomplete="off" inputmode="numeric">
        </div>
        <div class="result-container">
            <div id="resultArea" class="result"></div>
            <div id="emptyMsg" class="empty-msg">💡 請輸入 4 位數代碼查詢</div>
        </div>
        <div class="footer">系統資料與 Google 試算表即時同步</div>
    </div>

    <script>
        const stockData = DATA_PLACEHOLDER;

        const stockInput = document.getElementById('stockInput');
        const resultArea = document.getElementById('resultArea');
        const emptyMsg = document.getElementById('emptyMsg');

        function updateDisplay(code) {
            const cleanCode = code.toUpperCase().replace(/[^A-Z0-9]/g, '');
            
            if (cleanCode === '') {
                resultArea.style.display = 'none';
                emptyMsg.style.display = 'block';
                return;
            }

            emptyMsg.style.display = 'none';
            const stock = stockData[cleanCode];

            if (stock) {
                resultArea.className = 'result found';
                const showDate = stock.date && stock.date !== "N/A";
                resultArea.innerHTML = `
                    <div class="stock-header">
                        <span class="stock-name">${stock.name}</span>
                        ${showDate ? `<span class="stock-date">選入: ${stock.date}</span>` : ''}
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">昨收</div>
                            <div class="info-value">${stock.last_close}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">均價</div>
                            <div class="info-value">${stock.avg_price}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">成本</div>
                            <div class="info-value">${stock.cost}</div>
                        </div>
                    </div>
                `;
            } else {
                resultArea.className = 'result not-found';
                resultArea.innerHTML = `<div class="status">⚠️ 不在Amanda選股池</div>`;
            }
            resultArea.style.display = 'flex';
        }

        stockInput.addEventListener('input', (e) => updateDisplay(e.target.value));
        window.addEventListener('load', () => {
            if (window.innerWidth > 768) stockInput.focus();
        });
    </script>
</body>
</html>
"""
        
        final_html = html_content.replace("DATA_PLACEHOLDER", json.dumps(stock_map, ensure_ascii=False))
        final_html = final_html.replace("UPDATE_TIME_PLACEHOLDER", update_time)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"Success: Generated Amanda_Search.html with {len(stock_map)} stocks at {output_path}.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <output_path>")
        sys.exit(1)
    generate(sys.argv[1])
