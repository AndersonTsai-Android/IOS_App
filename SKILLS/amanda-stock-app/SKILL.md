---
name: amanda-stock-app
description: 負責維護與更新 Amanda 股票查詢網頁。當需要修改 Google Sheet 資料來源 URL、調整網頁 UI 樣式、或更新股票代碼查詢邏輯時使用。
---

# Amanda 股票查詢網頁維護指南

本技能用於維護位在桌面（或指定路徑）的 `amanda-stock-search.html` 檔案。

## 核心資訊

- **資料來源 (Google Sheet CSV)**: `https://docs.google.com/spreadsheets/d/1Bl9SRtxSp2StQH99wPLn8TyfvSYRlyHu6-tIS2F_UHg/gviz/tq?tqx=out:csv&sheet=Amanda`
- **欄位定義**:
    - `[0]` (A欄): 股票代碼 (查詢關鍵字)
    - `[1]` (B欄): 商品名稱
    - `[2]` (C欄): 選入日期
    - `[3]` (D欄): 昨收
    - `[4]` (E欄): 均價
    - `[5]` (F欄): 成本

## 常見任務流程

### 1. 修改 UI 樣式
網頁使用 Vanilla CSS 設計。若要修改顏色、字體或佈局，請搜尋檔案中的 `<style>` 區塊。
- 主色調變數: `--primary-color`, `--accent-color`
- 背景變數: `--bg-color`

### 2. 更新資料來源或工作表名稱
若 Google Sheet 的 ID 或工作表名稱（Sheet Name）變更，請更新 JavaScript 中的 `SHEET_URL` 常數。
- 格式模板: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/gviz/tq?tqx=out:csv&sheet=[SHEET_NAME]`

### 3. 調整查詢邏輯
查詢邏輯位於 `searchStock()` 函式中：
- 使用 `fetch` 取得 CSV。
- 使用 `parseCSV()` 解析資料。
- 使用 `data.find()` 根據代碼比對。

## 注意事項
- 網頁不需後端，直接以瀏覽器開啟。
- 若遇到 CORS 問題，請確認 Google Sheet 是否已設定為「知道連結的人均可檢視」。
- 解析器 `parseCSV` 是簡易實作，若 CSV 結構變得極度複雜（如包含換行符號在儲存格內），可能需要引入專門的解析函式庫。
