<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Flask-Web--App-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Render-Hosting-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/Telebot-TelegramBot-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/RandomForestRegressor-ML-orange?style=flat-square" />
</p>

<p align="center">
  <img src="/Ping_Render/salary-sage-logo.png" width="120" alt="Salary Sage Logo" />
</p>

# 🧙‍♂️ Salary Sage

**Salary Sage** is an intelligent Telegram bot powered by machine learning that predicts salaries based on your role, experience, location, and tech stack. It's a smart, simple, and interactive way for job seekers and professionals to understand salary trends across domains.

---

## 🚀 Start the Bot Server

> The bot is hosted on Render, which may go to sleep when idle. Use the button below to wake the server before starting a conversation.

👉 **[Start Bot Server](https://salary-sage.netlify.app/)**  
(_This site is deployed on **Netlify** and sends a ping to wake the Render server._)

## 💬 Talk to the Bot

🔗 [**Open Salary Sage on Telegram**](https://t.me/salary_sage_bot)

---

## 🤖 About the Bot

Salary Sage is an AI-powered Telegram bot that uses a trained machine learning model to predict salaries. It takes in user inputs like:

- Job Title
- Experience Level
- Company Type
- Location
- Technologies Known

Based on this information, it provides an estimated annual salary.

---

## 🧠 Model Details

**Model Used**: `RandomForestRegressor` (from `sklearn.ensemble`)  
**Dataset Fields**:
- `work_year`
- `experience_level`
- `employment_type`
- `job_title`
- `salary_currency`
- `employee_residence`
- `remote_ratio`
- `company_location`
- `company_size`
- `skills` (derived)

📂 **Dataset**: [Salary Prediction Dataset (Kaggle)](https://www.kaggle.com/datasets/amirmahdiabbootalebi/salary-by-job-title-and-country/data)

📊 **Architecture**:

![Architecture Diagram](/Ping_Render/architecture-diagram.png)

---

## ☁️ Deployment Flow

### 🔌 Telegram Bot Integration

We used the `pyTelegramBotAPI` (`telebot`) library to manage Telegram messaging, command handling, and replies. A conversational flow was created to collect input features from users step-by-step and pass them to the trained ML model.

### 🧪 Flask Server

We wrapped the bot logic inside a lightweight Flask server:

- The Flask route `/` returns a simple response for uptime pings.
- `bot.polling()` runs in a separate thread after the server starts.

This approach ensures the bot is continuously polling Telegram's API while still responding to external HTTP pings (used to keep the server alive).

### 🌐 Hosted on Render

The bot is deployed on **Render** as a web service. Render supports long-running processes and is ideal for hosting Flask + bot apps.

⏳ **Challenge**: Render free tier apps go to sleep after 15 minutes of inactivity.

### 🪄 Solution: Wake-Up Ping Site (Netlify)

We created a separate **static frontend on Netlify**:

- When the **Start Bot** button is clicked, it sends a ping to the Render server.
- A countdown timer gives Render ~50 seconds to start the bot server.
- Once ready, it shows a link to launch the Telegram bot.

This ensures a seamless experience despite Render's auto-sleep feature.

---

## 🛠️ Tech Stack

- Python 3.11
- Flask
- Telebot (pyTelegramBotAPI)
- Scikit-learn
- Netlify (Frontend Ping)
- Render (Backend Hosting)
- Telegram Bot API

---

## 📌 To Run Locally

```bash
git clone https://github.com/VIKNESH1211/Salary-Sage-Telegram-bot.git
cd salary-sage
pip install -r requirements.txt
python bot.py
