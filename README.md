# 📈 Chart Service

A lightweight Flask microservice that generates chart images from matplotlib Python code. Designed as a companion service for [claude-discord-bot](https://github.com/hzw0813/claude-discord-bot).

一個輕量的 Flask 微服務，將 matplotlib Python 程式碼渲染成圖片，作為 [claude-discord-bot](https://github.com/hzw0813/claude-discord-bot) 的配套服務使用。

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-blueviolet?style=flat)

-----

## ✨ Features / 功能

- 📊 Executes matplotlib Python code and returns a PNG image
- 🔢 Renders LaTeX math formulas as images
- 🚀 Ready to deploy on Railway

-----

## 🛠️ Tech Stack

|Component      |Technology                |
|---------------|--------------------------|
|Web framework  |Flask                     |
|Chart rendering|matplotlib + numpy + scipy|
|Server         |Gunicorn                  |
|Hosting        |Railway                   |

-----

## 📡 API Endpoints / API 端點

### `POST /generate`

Executes matplotlib Python code and returns a PNG image.
執行 matplotlib Python 程式碼並回傳 PNG 圖片。

**Request body:**

```json
{
  "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3],[4,5,6])"
}
```

**Response:** PNG image (`image/png`)

**Rules for the code / 程式碼規則：**

- Must `import` at the top
- Do NOT call `plt.show()`
- Do NOT save files

-----

### `POST /latex`

Renders LaTeX math formulas as a PNG image.
將 LaTeX 數學公式渲染成 PNG 圖片。

**Request body:**

```json
{
  "formulas": ["E = mc^2", "\\frac{a}{b}"]
}
```

**Response:** PNG image (`image/png`)

-----

### `GET /`

Health check — returns `Chart service is running!`

-----

## 🚀 Deployment / 部署

### Deploy on Railway / 部署到 Railway

1. Fork this repo
1. Create a new project on [Railway](https://railway.app) and connect the repo
1. Railway will auto-detect the Python service and deploy it
1. Copy the public URL and set it as `CHART_SERVICE_URL` in your [claude-discord-bot](https://github.com/hzw0813/claude-discord-bot) environment variables

### Run Locally / 本地執行

```bash
pip install -r requirements.txt
python app.py
```

The service will start on `http://localhost:8000`.

-----

## 📁 Project Structure / 專案結構

```
chart-service/
├── app.py            # Main Flask app / 主程式
├── requirements.txt  # Python dependencies
├── Procfile          # Gunicorn start command
└── railway.toml      # Railway deployment config
```

-----

## 🤝 Contributing / 貢獻

Pull requests are welcome!
歡迎送 PR！

-----

## 📄 License

MIT
