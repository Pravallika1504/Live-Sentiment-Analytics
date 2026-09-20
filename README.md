# Live-Sentiment-Analytics
 
> **AI-Powered Real-Time Sentiment Analysis & Trend Intelligence Platform** 
 
A real-time NLP dashboard that collects news and social media content, analyzes sentiment, identifies trending topics, and presents actionable insights through an interactive dashboard. 
 
## 📖 Table of Contents 
 
- [Overview](#-overview) 
- [Features](#-features) 
- [Tech Stack](#-tech-stack) 
- [Architecture](#-architecture) 
- [Installation](#-installation) 
- [Project Structure](#-project-structure) 
- [Dashboard](#-dashboard) 
- [Future Enhancements](#-future-enhancements) 
- [Author](#-author) 
 
--- 
 
## 🌟 Overview 
 
The **Real-Time Sentiment & Trend Dashboard** is designed to transform continuously changing online content into meaningful insights. 
 
The system collects data from sources such as **News APIs and Reddit**, processes the text, performs sentiment analysis, detects important keywords and trends, and displays the results using interactive visualizations. 
 
### Key Goals 
 
- Analyze real-time online content 
- Identify positive, negative, and neutral sentiment 
- Detect trending topics and keywords 
- Track changes in sentiment 
- Store historical analysis results 
- Provide an interactive intelligence dashboard 
 
--- 
 
## ✨ Features 
 
### 📰 Data Collection 
- Real-time news collection using News API 
- Reddit data integration 
- Source-based content analysis 
 
### 🧹 NLP Processing 
- Text cleaning and preprocessing 
- Removal of unnecessary characters and noise 
- Sentiment classification using VADER 
 
### 🧠 Sentiment Intelligence 
- Positive, Negative, and Neutral classification 
- Compound sentiment scoring 
- Overall sentiment overview 
- Sentiment trend analysis 
 
### 🔥 Trend Analysis 
- Trending keyword detection 
- Topic-based analysis 
- Sentiment changes and spikes 
- Top positive and negative stories 
 
### 📊 Interactive Dashboard 
- KPI cards 
- Interactive Plotly charts 
- Latest intelligence feed 
- Source comparison 
- Sentiment distribution 
- Trend visualization 
 
### 💾 Data Management 
- Historical data storage using SQLite 
- Processed sentiment results 
- Exportable analysis data 
 
--- 
 
## 🛠 Tech Stack 
 
| Category | Technologies | 
|----------|--------------| 
| Language | Python | 
| Dashboard | Streamlit | 
| Data Processing | Pandas | 
| NLP | VADER, NLTK | 
| Visualization | Plotly | 
| Data Sources | News API, Reddit API | 
| Database | SQLite | 
| Version Control | Git, GitHub | 
 
--- 
 
## 🏗 Architecture 
 
```text
┌───────────────────────────────┐ 
│       News API / Reddit       │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│       Data Collection         │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│   Text Cleaning & Processing  │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│     VADER Sentiment NLP       │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│  Trend & Keyword Analysis     │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│       SQLite Database         │ 
└───────────────┬───────────────┘ 
                ↓ 
┌───────────────────────────────┐ 
│    Streamlit Dashboard        │ 
└───────────────────────────────┘
