# CLAUDE_zh.md

本文件為 Claude Code (claude.ai/code) 在此儲存庫中工作時提供指引。

## 專案概述

pypdfium2 是 PDFium 的 ABI 級 Python 3 綁定，PDFium 是一個強大的 PDF 渲染、檢視、操作和建立函式庫。使用 ctypesgen（pypdfium2-team 分支）和來自 pdfium-binaries 的外部 PDFium 二進位檔案建構。

## 指令

使用 `just` 指令執行器（make 的現代替代方案）。執行 `just -l` 列出所有指令。

### 測試
```bash
just test                              # 執行所有測試
just test -sv                          # 詳細輸出含 stdout
just test tests/test_document.py       # 單一模組
just test tests/test_document.py::test_open_path  # 單一測試
just test -k "test_open"               # 模式匹配
just coverage                          # 測試含覆蓋率報告
```

設定 `DEBUG_AUTOCLOSE=1` 可除錯自動物件終結。

### 程式碼品質
```bash
just check      # autoflake（未使用的匯入）、codespell、reuse lint（SPDX）
just distcheck  # 對 dist/* 執行 twine check + check-wheel-contents
```

### 建構/打包
```bash
just build-native [args]      # 原生建構 PDFium（精簡，系統相依性）
just build-toolchained [args] # 使用 Google 工具鏈建構 PDFium
just update [args]            # 從 pdfium-binaries 下載二進位檔
just emplace [args]           # 暫存檔案以供打包
just craft [args]             # 建立 wheel 套件
just packaging-pypi           # 完整發布：clean, check, update-verify, craft, distcheck
just clean                    # 清理建構產物
```

### 文件
```bash
just docs-build   # 使用 Sphinx 建構 HTML 文件
just docs-open    # 在瀏覽器開啟文件
just docs-clean   # 清理文件建構
```

## 架構

### 雙層 API 設計

1. **高階輔助類別**（`src/pypdfium2/_helpers/`）- 使用者友善的 Python 類別：
   - `PdfDocument` - 開啟/建立 PDF 的主要入口點
   - `PdfPage` - 頁面操作（渲染、文字擷取）
   - `PdfBitmap` - 圖像渲染和轉換
   - `PdfTextPage` - 文字擷取和搜尋
   - `PdfObject` - 頁面物件處理
   - `PdfMatrix` - 轉換矩陣

2. **原始 ctypes API**（`src/pypdfium2_raw/`）- 透過自動產生的綁定直接存取 C API

```python
import pypdfium2 as pdfium           # 輔助 API
import pypdfium2.raw as pdfium_c     # 原始 ctypes API
import pypdfium2.internal as pdfium_i  # 內部工具
```

### 重要目錄

- `src/pypdfium2/_helpers/` - 高階封裝類別
- `src/pypdfium2/_cli/` - 命令列介面子指令
- `src/pypdfium2/internal/` - 基礎類別（`AutoCloseable`、`AutoCastable`）、常數、工具
- `src/pypdfium2_raw/` - 自動產生的 ctypes 綁定
- `setupsrc/` - 建構基礎設施（update.py、build_native.py、build_toolchained.py、craft.py、autorelease.py）
- `tests/resources/` - 測試用 PDF 檔案
- `tests/expectations/` - 預期測試輸出

### 資源管理

使用 `AutoCloseable` 基礎類別搭配 `weakref.finalize()` 進行自動清理。支援上下文管理器（`with` 陳述式）。輔助類別透過 `.raw` 屬性暴露其底層原始物件，傳遞給原始 API 函式時會自動解析。

## 建構系統

透過 `PDFIUM_PLATFORM` 環境變數控制：
- `auto` - 自動偵測平台，使用預建二進位檔（預設）
- `system-search` - 使用系統安裝的 PDFium
- `sourcebuild` - 使用 `data/sourcebuild/` 中預暫存的檔案
- `sourcebuild-native` / `sourcebuild-toolchained` - 觸發建構腳本

其他重要環境變數：`BUILD_PARAMS`（原生建構選項）、`PYPDFIUM_MODULES`（要包含的模組）、`PDFIUM_BINDINGS=reference`（使用參考綁定）。

## 開發環境

Conda/虛擬環境名稱：`pypdfium2`

## 開發注意事項

- **不硬換行**：程式碼庫不對長行進行硬換行。請使用編輯器自動換行（建議：100 欄）
- **執行緒安全**：PDFium 不是執行緒安全的
- **可選相依性**：Pillow、NumPy、opencv-python 用於圖像操作（延遲匯入）
