---
name: broken-line-app
description: 負責維護與更新「是否破線」股票查詢網頁。包含 GitHub 推送編碼處理、Google Sheet 資料源對應及 UI 樣式管理。使用此技能處理 broken-line-search.html 的任何修改、欄位更新或部署需求。
---

# 是否破線 股票查詢網頁維護指南

本技能整合了多次部署與編碼修正的實戰教訓，旨在確保 `broken-line-search.html` 的穩定性與資料正確性。

## 1. 核心資料來源 (Data Source)

- **唯一指定 URL**: `https://docs.google.com/spreadsheets/d/1Bl9SRtxSp2StQH99wPLn8TyfvSYRlyHu6-tIS2F_UHg/export?format=csv&sheet=%E6%98%AF%E5%90%A6%E7%A0%B4%E7%B7%9A`
- **教訓**: 嚴禁使用 `gviz/tq` (Query API)，因為它在處理凍結窗格時會導致標題列 (A1:H1) 遺失或變為空白。

## 2. 欄位標籤與邏輯 (Column Mapping)

### 查詢系統 (Tab 1: Search System)
- **欄位範圍**: A 到 H 欄 (Index 0-7)。
- **硬編碼標籤**: A:股票名稱, B:代碼, C:買入均價, D:現價, E:多頭回檔到均線, F:損益, G:成本, H:試算報酬率。
- **搜尋邏輯**: 針對 **B 欄 (index 1)** 進行精確比對 (`===`)。
- **注意**: 查詢系統已與 P 欄脫鉤，不再顯示 P 欄警告。

### 名單系統 (Tab 2: List System)
- **欄位範圍**: R 到 V 欄 (Index 17-21)。
- **混合標籤**:
    - **R 欄 (Index 17)**: 動態從試算表第一列抓取 (R1)。
    - **S~V 欄**: 硬編碼為「成本, 買入均價, 減碼賣出股數, 減碼到最小單位賣出股數」。
- **排序功能**: 所有 R~V 表頭必須支援升冪/降冪排序。

## 3. 安全部署與編碼 (Deployment)

### 嚴禁使用 PowerShell 推送 CJK
- **致命錯誤**: PowerShell 的字串處理會導致繁體中文在推送至 GitHub API 時變為亂碼。
- **標準程序**: 必須使用 Python 腳本 `scripts/deploy_to_github.py` 進行部署。

### 部署範例
```powershell
python scripts/deploy_to_github.py $env:GITHUB_TOKEN "AndersonTsai-Android/IOS_App" "broken-line-search.html" "./local_modified.html"
```

## 4. UI/UX 規範
- **顏色**: 主題色為翡翠綠 (`#10ac84`)。
- **數量計數器**: 只有在「遠離均線名單」分頁右上角顯示，字體必須加大至 `2.8rem`。
- **CSV 解析**: 使用狀態機解析器，以處理儲存格內可能包含的逗號與雙引號。
