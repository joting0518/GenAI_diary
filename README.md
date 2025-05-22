# 📝 GenAI_diary

**GenAI_diary** 是一個整合多種 text-to-image 模型的日記應用程式，使用者可以將每日的日記文字作為 prompt，選擇喜愛的圖片風格，AI 即會自動生成對應風格的圖像並附加於日記中。
系統設計上會在啟動 Flask 服務時預先載入所有模型，避免使用者在生成圖片時長時間的等待。
---

## 🌟 專案架構

- `templates/`：存放前端 HTML 頁面（封面、日曆、日記編輯畫面）
- `static/`：預設圖片（如 miffy.png）、CSS/JS 等檔案
- `app.py`：使用 Flask 建立 API 串接生成模型
- `localStorage`：前端以 localStorage 儲存日記文字與圖片，無需後端資料庫
- CORS 支援：解決跨網域請求問題，前後端可分開部署

---

## 🧠 使用模型與風格

啟動 Flask API 服務時會預先載入五種模型以避免使用者等待過久：

| 模型代號 | 模型 ID | 擅長風格           | 顯示名稱（下拉選單）    |
|----------|---------|--------------------|--------------------------|
| `pipe1`  | `xyn-ai/anything-v4.0` | 可愛動漫風         | `可愛動漫風`            |
| `pipe2`  | `nitrosocke/mo-di-diffusion` | 迪士尼風格       | `迪士尼風`              |
| `pipe3`  | `CompVis/stable-diffusion-v1-4` | 寫實照片風格     | `寫實照片風`            |
| `pipe4`  | `Fictiverse/Stable_Diffusion_PaperCut_Model` | 剪紙插畫風 | `剪紙插畫風`            |
| `pipe5`  | `prompthero/openjourney-v4` | 藝術奇幻風格     | `藝術、奇幻風`          |

### 🎯 Prompt 加強說明

在後端根據模型自動加上關鍵字以強化風格，例如：

```python
if model_id == 1:
    prompt = "Use Cute Anime Style to generate" + prompt
elif model_id == 2:
    prompt = "Use modern Disney Style to generate" + prompt
elif model_id == 3:
    prompt = "Use Photorealistic Style to generate" + prompt
elif model_id == 4:
    prompt = "Use Papercut Illustration to generate" + prompt
else:
    prompt = "Use Master Painting Style to generate" + prompt

## 🖼️ 使用流程

1. **首頁（封面頁）**  
   點擊 `Start` 按鈕，導向日曆頁面。
![首頁畫面](https://github.com/joting0518/GenAI_diary/blob/main/sample/cover.png?raw=true)
2. **日曆頁（calendar.html）**  
   使用者選擇某一天來撰寫日記。
![日曆畫面](https://github.com/joting0518/GenAI_diary/blob/main/sample/calendar.png?raw=true)

3. **日記頁（diary.html）**  
   - 選擇想要的圖片生成風格（右上角下拉選單）  
   - 撰寫日記內容  
   - 點擊「AI 生成圖片」按鈕，後端會根據內容產圖並顯示在右上角圖片框中。
![日記畫面](https://github.com/joting0518/GenAI_diary/blob/main/sample/diary_content.png?raw=true)
![日記範例](https://github.com/joting0518/GenAI_diary/blob/main/sample/diary_sample.png?raw=true)
---

## 🚀 安裝與執行

```bash
git clone https://github.com/joting0518/GenAI_diary.git
cd GenAI_diary
pip install -r requirements.txt   # 安裝所需套件
python3 app.py                    # 啟動 Flask 服務

### ✅ 啟動成功時會看到：

所有模型準備完成，啟動 Flask server，日記開始使用

Running on http://127.0.0.1:5000
Running on http://<你的IP>:5000

請打開瀏覽器進入網址開始使用服務

---

## 🔒 模型安全說明

由於 `anything-v4.0`（pipe1）有內建 **NSFW 安全檢查機制**，若生成結果疑似為不當內容將會回傳黑圖。

目前為了測試方便，已將 safety checker 關閉：

```python
pipe1.safety_checker = lambda images, clip_input: (images, [False] * len(images))
⚠️ 若部署至正式環境，建議開啟 safety checker 以避免生成不當圖像。
```
