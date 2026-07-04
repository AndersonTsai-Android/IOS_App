---
name: gooaye-analyzer
description: 專門用於抓取並分析《股癌 Gooaye》最新 Podcast 單集，產出包含內容摘要與台股 AI 投資分析的互動式網頁。當用戶要求更新股癌筆記或查詢最新集數時使用。
---

# Gooaye Analyzer

## 核心工作流 (Workflow)

當用戶觸發此技能時，請依序執行以下步驟：

### 1. 抓取最新集數資訊
使用 `web_fetch` 抓取 [股癌 Apple Podcast 頁面](https://podcasts.apple.com/tw/podcast/gooaye-%E8%82%A1%E7%99%8C/id1500839292)。
- 提取最新的 **集數編號 (EPxxx)**、**標題** 及 **發布日期**。

### 2. 檢查是否已存在
在 `D:\gemini\Stock\` 目錄下使用 `glob` 搜尋檔案 `EPxxx_Gooaye_Investment_Summary.html`。
- 如果檔案已存在，請直接告知用戶：「EPxxx 已是最新版本，無需更新。」並停止後續動作。
- 如果檔案不存在，請繼續執行步驟 3。

### 3. 深度研究單集內容
使用 `google_web_search` 搜尋該單集的詳細筆記與總結。
- 重點關注：產業趨勢（如被動元件、AI 伺服器）、個股技術面/籌碼面觀察、孟恭的投資心態。
- 確保提取到具體的技術細節（如 MLCC 料號、電容規格等）。

### 4. AI 投資分析
根據單集內容，結合當前台股盤勢，分析具備投資機會的標的。
- 提供股票代碼 (Ticker)。
- 解釋推薦邏輯（為什麼現在有機會）。

### 5. 生成互動網頁
使用 `D:\gemini\Stock\Gooaye\gooaye-analyzer\assets\template.html` 作為模板，產生包含以下兩部分的 `EPxxx_Gooaye_Investment_Summary.html`：
- **PART 1: 節目內容摘要** (包含產業細節、操作心態)。
- **PART 2: AI 深度分析** (包含具體台股標的、邏輯評價)。
- 確保網頁風格為現代深色模式 (Dark Mode)，且具備響應式導航。

### 6. 開啟與交付
- 將生成的 HTML 檔案寫入 `D:\gemini\Stock\`。
- 使用 `cmd.exe /c start ""` 配合檔案路徑（或在 PowerShell 中使用 `Start-Process` 開啟 HTML 檔案）來確保瀏覽器能正確開啟。
- 告知用戶完成更新，並在對話中提供可點擊的 `file:///` 連結作為備份方案。

## 注意事項
- 檔案命名必須嚴謹遵循 `EPxxx_Gooaye_Investment_Summary.html` 格式。
- 若搜尋不到詳細內容，應告知用戶目前資訊不足，詢問是否由你根據標題進行推理。

