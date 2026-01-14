# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 目錄說明

這是 pypdfium2 專案的 `sovereign_ai/` 目錄，為主權AI專案提供 PDF 文字和圖片擷取功能。

## 快速開始

### 使用 CLI

```bash
# 基本擷取
python -m sovereign_ai.cli input.pdf -o output/

# 強制 PNG 格式
python -m sovereign_ai.cli input.pdf -o output/ --image-format png

# 擷取特定頁面
python -m sovereign_ai.cli input.pdf -o output/ --pages 1,3,5

# 只擷取文字（不擷取圖片）
python -m sovereign_ai.cli input.pdf -o output/ --no-images
```

### 使用 Python API

```python
from sovereign_ai import extract_pdf_to_json
from pathlib import Path

result = extract_pdf_to_json(
    pdf_path=Path("input.pdf"),
    output_dir=Path("output"),
    image_format="auto",  # 自動保留原始格式
    save_images=True      # 設為 False 可跳過圖片擷取
)
```

## 輸出格式

文字和圖片分開存放，不會在文字中插入圖片連結：

```json
[
  {
    "pageNo": 1,
    "width": 595.3,
    "height": 841.9,
    "words": "純文字內容...",
    "images": [
      {
        "index": 0,
        "path": "images/mydoc_page1_img1.png",
        "bounds": [100.0, 200.0, 300.0, 400.0]
      }
    ]
  }
]
```

- `width`/`height`: 頁面尺寸（PDF 點數，72 點 = 1 英寸）
- `bounds`: 圖片座標 `[left, bottom, right, top]`（PDF 座標系，原點在左下角）
- 圖片檔名格式: `{pdf名稱}_page{頁碼}_img{順序}.{格式}`

## 核心檔案

| 檔案 | 說明 |
|------|------|
| `pdf_extractor.py` | 核心擷取邏輯，主要 API |
| `text_utils.py` | 文字擷取工具（使用 pypdfium2 textpage API）|
| `image_utils.py` | 圖片擷取工具（支援智慧格式保留）|
| `cli.py` | 命令列介面 |

## 功能特點

1. **純文字擷取**：`words` 欄位只包含純文字
2. **圖片資訊獨立**：圖片路徑和座標存放在 `images` 欄位
3. **智慧圖片擷取**：優先保留原始格式（JPEG/PNG），fallback 到 bitmap 擷取
4. **MinerU 相容格式**：輸出 JSON 格式與 MinerU 的 client_json 相似

## 輸出目錄結構

```
output/
├── mydoc.json          # 擷取結果 JSON
└── images/
    ├── mydoc_page1_img1.png
    ├── mydoc_page1_img2.jpg
    └── mydoc_page2_img1.png
```

## 環境設定

此模組使用 pypdfium2 環境：
```bash
conda activate pypdfium2
```

## 參數說明

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `image_format` | `"auto"` | 圖片格式：`auto`/`png`/`jpg` |
| `pages` | `None` | 指定頁碼（1-based），None 表示所有頁面 |
| `save_json` | `True` | 是否儲存 JSON 檔案 |
| `save_images` | `True` | 是否擷取並儲存圖片 |
