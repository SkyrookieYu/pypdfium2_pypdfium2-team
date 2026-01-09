# Changelog

此檔案記錄 sovereign_ai 模組的重要變更。

## [0.2.0] - 2026-01-10

### Added
- 新增頁面尺寸資訊 (`width`, `height`) 到 JSON 輸出
- 圖片檔名加上 PDF 名稱前綴，避免批次處理時檔案覆蓋
  - 格式: `{pdf名稱}_page{頁碼}_img{順序}.{格式}`
  - 例如: `mydoc_page1_img1.png`

### Changed
- 簡化輸出格式，移除文字中的圖片連結 (`[IMAGE: ...]`)
- `words` 欄位現在只包含純文字
- 圖片資訊完整保留在 `images` 欄位

### Removed
- 移除 `include_image_links` 參數
- 移除 `use_position_merge` 參數
- 移除 `position_merger.py` 模組
- 移除 CLI 選項: `--no-links`, `--no-position-merge`

### JSON 輸出格式

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

---

## [0.1.0] - 2026-01-10

### Added
- 初始版本
- PDF 文字擷取（使用 pypdfium2 textpage API）
- PDF 圖片擷取（支援智慧格式保留）
- 位置感知圖片連結插入（已在 0.2.0 移除）
- CLI 介面 (`python -m sovereign_ai.cli`)
- MinerU 相容的 JSON 輸出格式
