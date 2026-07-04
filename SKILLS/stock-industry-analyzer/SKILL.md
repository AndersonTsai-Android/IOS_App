---
name: stock-industry-analyzer
description: 負責維護「股票產業與投資價值分析報告」(Investment_Report.html)。包含管理 170+ 檔股票的產業分類、核心產品與專業投資建議。使用此技能更新報表數據、新增個股分析或調整報表 UI。
---

# 股票產業與投資分析 技能指南

本技能專用於維護 `Investment_Report.html`，這是一個基於「是否破線」清單的動態研報系統。

## 1. 資料管理 (Data Management)

- **核心數據庫**: `references/stock_analysis.json`
- **欄位定義**:
    - `id`: 股票代碼 (String)
    - `name`: 股票名稱 (String)
    - `industry`: 產業類別 (例如: CoWoS 設備, 矽光子)
    - `product`: 主要產品 (String)
    - `analysis`: 專業投資分析建議 (String)

## 2. 更新流程 (Workflow)

### 新增或修改分析
1. 編輯 `references/stock_analysis.json`。
2. 確保資料格式正確 (JSON 陣列)。

### 產生 HTML 報表
執行 `scripts/update_report.py` 腳本，將 JSON 數據注入 `assets/report_template.html` 並輸出至目標路徑。

```powershell
python scripts/update_report.py
```

## 3. UI/UX 規範
- **外觀**: 採用現代簡潔風格，卡片式佈局。
- **互動**: 支援即時搜尋與產業過濾。
- **狀態標記**: 
    - 綠色: 具備「龍頭」、「強勁」、「爆發」等關鍵字。
    - 紅色: 具備「關注」、「挑戰」、「低位階」等關鍵字。
    - 黃色: 其他中性評價。

## 4. 參考資料
- 資料來源為 Google 試算表「是否破線」分頁。
- 投資分析應保持客觀專業，結合 AI 伺服器、強韌電網、先進封裝等市場熱點。
