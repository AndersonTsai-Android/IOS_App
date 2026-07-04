---
name: stock-tools-portal
description: 負責維護與更新「股票查詢工具箱」入口網頁 (index.html)。當需要新增工具連結、調整卡片樣式或修改入口說明時使用。
---
# 股票查詢工具箱 入口網頁維護指南

本技能用於維護 `index.html`。此網頁作為所有股票工具（Amanda, 破線, 群益庫存）的中央門戶。

## 核心設計規範

### 1. 介面樣式 (CSS)
- **色調**: 使用紫色漸層 (`#6c5ce7` 到 `#a29bfe`)。
- **佈局**: 採用 Responsive Grid，在桌機顯示多欄，手機自動切換為單欄卡片。
- **互動**: 卡片需有 Hover 位移與陰影加深效果。

### 2. 卡片結構
每張工具卡片包含：
- **Icon**: 使用 Emoji (如 📊, 📈, 📋)。
- **Title**: 工具名稱。
- **Description**: 簡短的功能描述。
- **Link**: 指向 GitHub Pages 的完整 URL。

## 維護流程

### 新增工具
1. 開啟 `index.html`。
2. 在 `<div class="grid">` 內複製一個 `<a>` 區塊。
3. 更新連結 URL、Icon、標題與描述。

### 擴充性建議
- 若未來工具超過 6 個，考慮在 CSS 中加入分組標籤（Category Tags）。
- 確保所有連結都指向 `https://andersontsai-android.github.io/IOS_App/` 下的路徑。
