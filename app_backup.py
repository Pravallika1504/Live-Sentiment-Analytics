import streamlit as st
import pandas as pd
import plotly.express as px
import re
from src.news import collect_news
from src.sentiment import analyze_sentiment
# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="PulseAI | Real-Time Sentiment Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# =========================================================
# THEME / CSS
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 5% 0%, rgba(99,102,241,.16), transparent 28%),
                radial-gradient(circle at 95% 5%, rgba(168,85,247,.12), transparent 30%),
                #070b12;
            color: #f8fafc;
        }
        .main .block-container {
            max-width: 1450px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }
        [data-testid="stSidebar"] {
            background: #090e17;
            border-right: 1px solid rgba(255,255,255,.08);
        }
        .hero {
            padding: 1.8rem 2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(20,29,49,.96), rgba(12,17,30,.86));
            border: 1px solid rgba(139,92,246,.25);
            box-shadow: 0 20px 60px rgba(0,0,0,.28);
            margin-bottom: 1.2rem;
        }
        .live-pill {
            display: inline-block;
            padding: 5px 11px;
            border-radius: 999px;
            background: rgba(34,197,94,.10);
            border: 1px solid rgba(34,197,94,.28);
            color: #4ade80;
            font-size: .74rem;
            font-weight: 800;
            letter-spacing: .8px;
            margin-bottom: .7rem;
        }
        .brand {
            font-size: 2.7rem;
            line-height: 1;
            font-weight: 850;
            letter-spacing: -1.5px;
        }
        .brand span {
            color: #a78bfa;
        }
        .subtitle {
            color: #94a3b8;
            margin-top: .55rem;
            font-size: 1rem;
        }
        .hero-note {
            color: #64748b;
            margin-top: .8rem;
            font-size: .82rem;
        }
        .section-title {
            font-size: 1.25rem;
            font-weight: 800;
            margin: 1.35rem 0 .75rem;
            color: #f8fafc;
        }
        .section-subtitle {
            color: #64748b;
            font-size: .82rem;
            margin-top: -.45rem;
            margin-bottom: .8rem;
        }
        .kpi {
            padding: 1.1rem 1.15rem;
            min-height: 118px;
            border-radius: 18px;
            background: rgba(15,23,42,.74);
            border: 1px solid rgba(255,255,255,.08);
            box-shadow: 0 10px 30px rgba(0,0,0,.14);
        }
        .kpi-label {
            color: #94a3b8;
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: 850;
            margin-top: .45rem;
        }
        .kpi-note {
            color: #64748b;
            font-size: .73rem;
            margin-top: .25rem;
        }
        .purple { color: #a78bfa; }
        .positive { color: #4ade80; }
        .neutral { color: #facc15; }
        .negative { color: #fb7185; }
        .keyword {
            display: inline-block;
            padding: 7px 12px;
            margin: 3px;
            border-radius: 999px;
            background: rgba(139,92,246,.10);
            border: 1px solid rgba(139,92,246,.23);
            color: #c4b5fd;
            font-size: .78rem;
        }
        .article-shell {
            padding: 1rem 1.1rem;
            border-radius: 17px;
            background: rgba(13,20,34,.70);
            border: 1px solid rgba(255,255,255,.075);
            margin-bottom: .65rem;
        }
        .article-title {
            color: #f8fafc;
            font-size: 1rem;
            font-weight: 750;
            line-height: 1.35;
        }
        .article-source {
            color: #64748b;
            font-size: .76rem;
            margin-top: .35rem;
        }
        .score-pill {
            display: inline-block;
            padding: 4px 9px;
            border-radius: 999px;
            font-size: .73rem;
            font-weight: 800;
        }
        .score-positive {
            color: #4ade80;
            background: rgba(34,197,94,.10);
            border: 1px solid rgba(34,197,94,.18);
        }
        .score-neutral {
            color: #facc15;
            background: rgba(250,204,21,.08);
            border: 1px solid rgba(250,204,21,.17);
        }
        .score-negative {
            color: #fb7185;
            background: rgba(251,113,133,.08);
            border: 1px solid rgba(251,113,133,.17);
        }
        .insight {
            padding: 1rem 1.1rem;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(99,102,241,.10), rgba(168,85,247,.07));
            border: 1px solid rgba(139,92,246,.18);
            color: #cbd5e1;
        }
        .footer {
            text-align: center;
            color: #475569;
            font-size: .74rem;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="live-pill">● LIVE INTELLIGENCE</div>
        <div class="brand">Pulse<span>AI</span></div>
        <div class="subtitle">Real-Time Sentiment & Trend Intelligence</div>
        <div class="hero-note">
            Collect → Clean → Analyze → Visualize • News API + VADER NLP + Plotly
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# SIDEBAR / CONTROL CENTER
# =========================================================
with st.sidebar:
    st.markdown("## 🎛️ Control Center")

    keyword = st.text_input(
        "Topic to monitor",
        value=st.session_state.get("last_keyword", "ChatGPT"),
        placeholder="e.g. OpenAI, AI, Tesla...",
    )
    article_count = st.slider(
        "Articles to analyze",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
    )
    analyze_button = st.button(
        "🔍 Analyze Topic",
        use_container_width=True,
        type="primary",
    )
    refresh_button = st.button(
        "🔄 Refresh Live Data",
        use_container_width=True,
    )
    st.divider()
    st.markdown("### 📡 Data Sources")
    st.success("News API • Connected")
    st.info("VADER NLP • Active")
    st.caption("Current pipeline analyzes article titles + available text.")
    st.divider()
    st.markdown("### 🧠 Pipeline")
    st.markdown(
        """
        **01 · Collect**  
        Live news articles
        **02 · Clean**  
        Text preprocessing
        **03 · Analyze**  
        VADER sentiment
        **04 · Visualize**  
        Interactive Plotly analytics
        """
    )
    st.divider()
    st.caption("Tip: try topics such as `OpenAI`, `Tesla`, `AI`, `Apple`, or `Bitcoin`.")
# =========================================================
# DATA COLLECTION
# =========================================================
should_fetch = (
    analyze_button
    or refresh_button
    or "articles" not in st.session_state
)
if should_fetch:
    with st.spinner(f"📡 Fetching live intelligence for “{keyword}”..."):
        try:
            articles = collect_news(keyword, article_count)
            processed_articles = []
            for article in articles:
                title = article.get("title") or ""
                text = article.get("text") or ""
                combined_text = f"{title} {text}".strip()
                result = analyze_sentiment(combined_text)
                article["sentiment"] = result["label"]
                article["sentiment_score"] = float(result["score"])
                processed_articles.append(article)
            st.session_state["articles"] = processed_articles
            st.session_state["last_keyword"] = keyword
        except Exception as e:
            st.error(f"Unable to collect live data: {e}")
            st.stop()
# =========================================================
# DATAFRAME
# =========================================================
articles = st.session_state.get("articles", [])
if not articles:
    st.warning("No articles found. Try another topic.")
    st.stop()
df = pd.DataFrame(articles)
if "sentiment_score" not in df.columns:
    df["sentiment_score"] = 0.0
df["sentiment_score"] = pd.to_numeric(
    df["sentiment_score"], errors="coerce"
).fillna(0.0)
if "sentiment" not in df.columns:
    df["sentiment"] = "Neutral"
if "title" not in df.columns:
    df["title"] = "Untitled article"
if "url" not in df.columns:
    df["url"] = "#"
if "created" not in df.columns:
    df["created"] = ""
# =========================================================
# TOPIC + STATUS BAR
# =========================================================
active_topic = st.session_state.get("last_keyword", keyword)
st.markdown(
    f'<div class="section-title">📡 Live Intelligence — {active_topic}</div>',
    unsafe_allow_html=True,
)
status_left, status_right = st.columns([4, 1])
with status_left:
    st.caption(
        f"Showing {len(df)} analyzed articles • "
        f"Source: News API • NLP: VADER"
    )
with status_right:
    st.caption("🟢 Pipeline operational")
# =========================================================
# KPI METRICS
# =========================================================
total = len(df)
positive = int((df["sentiment"] == "Positive").sum())
neutral = int((df["sentiment"] == "Neutral").sum())
negative = int((df["sentiment"] == "Negative").sum())
average_score = float(df["sentiment_score"].mean())
positive_pct = (positive / total * 100) if total else 0
negative_pct = (negative / total * 100) if total else 0
if average_score > 0.05:
    score_class = "positive"
    mood = "Bullish / Positive"
elif average_score < -0.05:
    score_class = "negative"
    mood = "Cautious / Negative"
else:
    score_class = "neutral"
    mood = "Mixed / Neutral"
c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "Articles", total, "purple", "Analyzed now"),
    (c2, "Positive", positive, "positive", f"{positive_pct:.0f}% of coverage"),
    (c3, "Neutral", neutral, "neutral", "Balanced coverage"),
    (c4, "Negative", negative, "negative", f"{negative_pct:.0f}% of coverage"),
    (c5, "Avg Sentiment", f"{average_score:.2f}", score_class, mood),
]
for col, label, value, css_class, note in kpis:
    with col:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {css_class}">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
# =========================================================
# QUICK INSIGHT
# =========================================================
st.markdown('<div class="section-title">💡 AI Signal</div>', unsafe_allow_html=True)
if positive > negative and average_score > 0.05:
    insight = (
        f"Overall coverage is leaning positive. "
        f"{positive} of {total} articles are positive, while {negative} are negative."
    )
elif negative > positive and average_score < -0.05:
    insight = (
        f"Overall coverage is leaning negative. "
        f"{negative} of {total} articles are negative, compared with {positive} positive articles."
    )
else:
    insight = (
        f"Coverage is mixed. The average sentiment is {average_score:.2f}, "
        f"with {positive} positive, {neutral} neutral, and {negative} negative articles."
    )
st.markdown(
    f'<div class="insight">📌 <b>{mood}</b> — {insight}</div>',
    unsafe_allow_html=True,
)
# =========================================================
# SENTIMENT FILTER
# =========================================================
st.markdown('<div class="section-title">🔎 Explore Coverage</div>', unsafe_allow_html=True)
filter_col1, filter_col2 = st.columns([2, 1])
with filter_col1:
    search_text = st.text_input(
        "Search within article titles",
        placeholder="Search articles...",
        label_visibility="collapsed",
    )
with filter_col2:
    sentiment_filter = st.selectbox(
        "Sentiment",
        ["All", "Positive", "Neutral", "Negative"],
        label_visibility="collapsed",
    )
display_df = df.copy()
if search_text:
    display_df = display_df[
        display_df["title"]
        .fillna("")
        .str.contains(search_text, case=False, na=False)
    ]
if sentiment_filter != "All":
    display_df = display_df[
        display_df["sentiment"] == sentiment_filter
    ]
# =========================================================
# CHARTS
# =========================================================
st.markdown('<div class="section-title">📊 Sentiment Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Understand the distribution and strength of the current conversation.</div>',
    unsafe_allow_html=True,
)
left, right = st.columns(2)
# ---------- DONUT ----------
with left:
    counts = (
        df["sentiment"]
        .value_counts()
        .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
        .reset_index()
    )
    counts.columns = ["Sentiment", "Count"]
    fig = px.pie(
        counts,
        names="Sentiment",
        values="Count",
        hole=0.68,
        color="Sentiment",
        color_discrete_map={
            "Positive": "#4ade80",
            "Neutral": "#facc15",
            "Negative": "#fb7185",
        },
    )
    fig.update_layout(
        title="Overall Sentiment Mix",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title="",
        margin=dict(l=10, r=10, t=55, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- SCORE DISTRIBUTION ----------
with right:
    fig2 = px.histogram(
        df,
        x="sentiment_score",
        nbins=12,
        title="Sentiment Score Distribution",
        labels={"sentiment_score": "Sentiment Score"},
    )
    fig2.add_vline(
        x=0,
        line_dash="dash",
        line_width=1,
        annotation_text="Neutral",
    )
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)
# =========================================================
# ARTICLE SENTIMENT BAR
# =========================================================
chart_df = df.copy()
chart_df["Short Title"] = (
    chart_df["title"]
    .fillna("")
    .astype(str)
    .str.slice(0, 38)
)
fig3 = px.bar(
    chart_df.sort_values("sentiment_score"),
    x="sentiment_score",
    y="Short Title",
    orientation="h",
    color="sentiment",
    hover_data=["title", "sentiment_score"],
    color_discrete_map={
        "Positive": "#4ade80",
        "Neutral": "#facc15",
        "Negative": "#fb7185",
    },
    title="Sentiment Strength by Article",
)
fig3.add_vline(x=0, line_dash="dash", line_width=1)
fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Sentiment Score",
    yaxis_title="",
    margin=dict(l=10, r=20, t=55, b=20),
)
st.plotly_chart(fig3, use_container_width=True)
# =========================================================
# TREND OVER TIME
# =========================================================
trend_df = df.copy()
trend_df["timestamp"] = pd.to_datetime(
    trend_df["created"],
    errors="coerce",
    utc=True,
)
trend_df = trend_df.dropna(subset=["timestamp"])
if not trend_df.empty:
    trend_df["time"] = trend_df["timestamp"].dt.floor("h")

    hourly = (
        trend_df.groupby("time", as_index=False)
        .agg(
            avg_sentiment=("sentiment_score", "mean"),
            articles=("sentiment_score", "count"),
        )
        .sort_values("time")
    )
    st.markdown(
        '<div class="section-title">📈 Sentiment Trend Over Time</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Average sentiment across the timestamps returned by the live source.</div>',
        unsafe_allow_html=True,
    )
    fig4 = px.line(
        hourly,
        x="time",
        y="avg_sentiment",
        markers=True,
        hover_data=["articles"],
        title="Average Sentiment Timeline",
    )
    fig4.add_hline(y=0, line_dash="dash", line_width=1)
    fig4.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Time",
        yaxis_title="Average Score",
        margin=dict(l=10, r=20, t=55, b=20),
    )
    st.plotly_chart(fig4, use_container_width=True)
# =========================================================
# TRENDING KEYWORDS
# =========================================================
st.markdown('<div class="section-title">🔥 Trending Keywords</div>', unsafe_allow_html=True)
stopwords = {
    "the", "and", "for", "with", "that", "this", "from",
    "about", "into", "after", "have", "has", "will", "are",
    "was", "were", "their", "they", "you", "your", "more",
    "than", "over", "under", "news", "says", "said", "new",
    "what", "when", "where", "which", "while", "could",
    "would", "been", "also", "just", "like", "than",
}
all_titles = " ".join(
    df["title"].fillna("").astype(str).tolist()
).lower()
words = re.findall(r"\b[a-zA-Z]{4,}\b", all_titles)
word_counts = {}
for word in words:
    if word not in stopwords:
        word_counts[word] = word_counts.get(word, 0) + 1
top_words = sorted(
    word_counts.items(),
    key=lambda x: x[1],
    reverse=True,
)[:15]
if top_words:
    keyword_html = "".join(
        f'<span class="keyword">#{word} · {count}</span>'
        for word, count in top_words
    )
    st.markdown(keyword_html, unsafe_allow_html=True)
else:
    st.caption("Not enough text to calculate trending keywords.")
# =========================================================
# LATEST INTELLIGENCE
# =========================================================
st.markdown('<div class="section-title">📰 Latest Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-subtitle">{len(display_df)} articles match the current filters.</div>',
    unsafe_allow_html=True,
)
for _, row in display_df.iterrows():
    title = str(row.get("title", "Untitled article"))
    url = str(row.get("url", "#"))
    created = str(row.get("created", ""))
    sentiment = str(row.get("sentiment", "Neutral"))
    score = float(row.get("sentiment_score", 0))
    if sentiment == "Positive":
        icon = "🟢"
        score_class = "score-positive"
    elif sentiment == "Negative":
        icon = "🔴"
        score_class = "score-negative"
    else:
        icon = "🟡"
        score_class = "score-neutral"
    source = "News"
    try:
        source = re.sub(r"^https?://", "", url).split("/")[0]
    except Exception:
        pass
    with st.container(border=True):
        col_main, col_action = st.columns([5.4, 1.2])
        with col_main:
            st.markdown(
                f'<div class="article-title">{icon} {title}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="article-source">
                    {source} &nbsp;•&nbsp; {created}
                    &nbsp;•&nbsp;
                    <span class="score-pill {score_class}">
                        {sentiment} · {score:.2f}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_action:
            st.link_button(
                "Read Article ↗",
                url,
                use_container_width=True,
            )
# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        PulseAI • Real-Time Sentiment & Trend Intelligence<br>
        Built with Streamlit, News API, VADER NLP & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)