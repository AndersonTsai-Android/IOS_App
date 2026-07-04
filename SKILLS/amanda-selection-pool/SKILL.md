---
name: amanda-selection-pool
description: 產生與更新 Amanda 選股池的查詢網頁。當使用者需要從指定 Google 試算表擷取股票代碼與資訊，並產出一個手機可用的互動式查詢網頁時使用。
---

# Amanda 選股池查詢網頁產生器

此技能用於從指定的 Google 試算表抓取股票資料（代碼、股名、選入日期、昨收、均價、成本），並產生一個獨立的 HTML 檔案 `Amanda_Search.html`。

## 使用流程

1. **執行產生腳本**：
   使用 Python 執行 `scripts/generate.py` 並指定輸出路徑。

   ```bash
   python scripts/generate.py "C:/Users/Anderson Tsai/Desktop/Amanda_Search.html"
   ```

2. **功能特點**：
   - **自動處理 N/A**：自動過濾試算表中的 `#N/A` 或空值。
   - **編碼校正**：確保中文字元（如「台塑」）正確顯示。
   - **手機優化**：產出的 HTML 具備響應式設計，適合行動裝置查詢。
   - **快速比對**：輸入代碼即時顯示結果，若不在名單內則提示。

## 檔案結構

- `scripts/generate.py`: 核心 Python 腳本，負責抓取資料並生成網頁。
- `Amanda_Search.html`: 產出的最終網頁檔案。

## 注意事項

- 執行腳本需要聯網以存取 Google 試算表。
- 確保環境中已安裝 `pandas`, `requests` 等必要函式庫。
