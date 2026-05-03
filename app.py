import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AEO Diagnostic — Pixii.ai",
    page_icon="🔍",
    layout="wide"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main { background-color: #ffffff; }
    
    .header-box {
        background: linear-gradient(135deg, #1a1d27 0%, #2E75B6 100%);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
    }
    .engine-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        border: 2px solid #e0e0e0;
        margin-bottom: 16px;
        height: 100%;
    }
    .engine-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e0e0e0;
    }
    .response-text {
        font-size: 14px;
        color: #333333;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    .report-card {
        background: #1a1d27;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
    }
    .score-box {
        background: #ffffff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .rec-card-blue {
        background: #EBF5FF;
        border-left: 4px solid #2E75B6;
        border-radius: 8px;
        padding: 16px;
    }
    .rec-card-green {
        background: #EAFAF1;
        border-left: 4px solid #27AE60;
        border-radius: 8px;
        padding: 16px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2E75B6, #1a4a8a);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 14px 32px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 12px;
        border: 2px solid #2E75B6;
        border-radius: 8px;
        color: #000000;
        background: #ffffff;
    }
    .badge-high {
        background: #D4EDDA;
        color: #155724;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-mid {
        background: #FFF3CD;
        color: #856404;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-low {
        background: #F8D7DA;
        color: #721C24;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── API KEYS — PASTE YOUR KEYS HERE ──────────────────────────────────────────
GROQ_API_KEY = "GROQ_KEY"

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1 style="color:white; font-size:40px; margin-bottom:10px;">🔍 AEO Diagnostic Tool</h1>
    <p style="color:#ccddff; font-size:18px; margin-bottom:0;">
        See how your product ranks across 3 leading AI engines
    </p>
    <p style="color:#aabbdd; font-size:14px; margin-top:8px;">
        Built for Amazon sellers by <b>Yachana Parmar</b> | Pixii.ai Founding Engineer Project
    </p>
</div>
""", unsafe_allow_html=True)

# ─── INPUT SECTION ─────────────────────────────────────────────────────────────
st.markdown("### 🔎 Enter your search query")
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    query = st.text_input(
        "Search Query",
        placeholder='e.g. "best magnesium supplement for seniors"',
        label_visibility="collapsed"
    )
    brand = st.text_input(
        "Brand Name",
        placeholder='Your brand name (optional) e.g. "Nature Made"',
        label_visibility="collapsed"
    )
    run_btn = st.button("🚀 Run AEO Diagnostic Now")

# ─── PROMPT BUILDER ────────────────────────────────────────────────────────────
def build_prompt(q, brand):
    base = f"""A shopper asks: "{q}"

You are a helpful Amazon shopping assistant. List your top 5 product or brand recommendations with brief reasons why each is good.

Format your response EXACTLY like this:
1. [Brand Name] - [Brief reason why it's recommended]
2. [Brand Name] - [Brief reason why it's recommended]
3. [Brand Name] - [Brief reason why it's recommended]
4. [Brand Name] - [Brief reason why it's recommended]
5. [Brand Name] - [Brief reason why it's recommended]

Be specific with real brand names. Keep each reason to 1-2 sentences."""
    
    if brand:
        base += f"\n\nImportant: Also specifically mention whether '{brand}' appears in your recommendations and at what position."
    
    return base

# ─── AI QUERY FUNCTIONS ────────────────────────────────────────────────────────
def query_model_1(q, brand):
    """Llama 4 Scout"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": build_prompt(q, brand)}],
            max_tokens=600,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def query_model_2(q, brand):
    """Llama 3.3 Versatile"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": build_prompt(q, brand)}],
            max_tokens=600,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def query_model_3(q, brand):
    """Mixtral"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": build_prompt(q, brand)}],
            max_tokens=600,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ─── SCORING ───────────────────────────────────────────────────────────────────
def calculate_score(response, brand):
    if "Error" in response:
        return 0, "low"
    
    if not brand:
        return 55, "mid"
    
    response_lower = response.lower()
    brand_lower = brand.lower()
    
    if brand_lower not in response_lower:
        return 20, "low"
    
    lines = [l for l in response.split('\n') if l.strip()]
    for i, line in enumerate(lines):
        if brand_lower in line.lower():
            if i <= 1:
                return 95, "high"
            elif i <= 3:
                return 75, "high"
            elif i <= 5:
                return 55, "mid"
            else:
                return 35, "low"
    
    return 40, "low"

def get_badge(level):
    if level == "high":
        return "<span class='badge-high'>🟢 High Visibility</span>"
    elif level == "mid":
        return "<span class='badge-mid'>🟡 Medium Visibility</span>"
    else:
        return "<span class='badge-low'>🔴 Low Visibility</span>"

# ─── MAIN RESULTS ──────────────────────────────────────────────────────────────
if run_btn and query:
    st.divider()
    st.markdown(f"## 📊 Results for: *\"{query}\"*")

    progress = st.progress(0, text="Starting analysis...")

    progress.progress(10, text="Querying Llama 4 Scout...")
    r1 = query_model_1(query, brand)
    time.sleep(0.3)

    progress.progress(45, text="Querying Llama 3.3 Versatile...")
    r2 = query_model_2(query, brand)
    time.sleep(0.3)

    progress.progress(80, text="Querying Mixtral 8x7b...")
    r3 = query_model_3(query, brand)

    progress.progress(100, text="✅ Analysis complete!")
    time.sleep(0.5)
    progress.empty()

    # Scores
    s1, l1 = calculate_score(r1, brand)
    s2, l2 = calculate_score(r2, brand)
    s3, l3 = calculate_score(r3, brand)

    # Engine Results
    col1, col2, col3 = st.columns(3)

    engines = [
        (col1, "🦙 Llama 4 Scout", r1, s1, l1, "#E8F4FD", "#2E75B6"),
        (col2, "⚡ Llama 3.3 Versatile", r2, s2, l2, "#FEF9E7", "#F39C12"),
        (col3, "🌀 Llama 3.1 8b", r3, s3, l3, "#EAF7F0", "#27AE60"),
    ]

    for col, name, response, score, level, bg, color in engines:
        with col:
            badge = get_badge(level)
            clean_response = response.replace('<', '&lt;').replace('>', '&gt;')
            st.markdown(f"""
            <div style="background:{bg}; border-radius:12px; padding:20px; border:2px solid {color}; min-height:420px;">
                <div style="font-size:17px; font-weight:bold; color:{color}; margin-bottom:10px;">{name}</div>
                {badge}
                <div style="font-size:24px; font-weight:bold; color:#333; margin-bottom:12px;">{score}% Visibility</div>
                <hr style="border-color:#ddd; margin:10px 0;">
                <div style="font-size:13px; color:#222222; line-height:1.8; white-space:pre-wrap;">{clean_response[:700]}{'...' if len(clean_response)>700 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

    # REPORT CARD
    avg = (s1 + s2 + s3) / 3
    overall = "🟢 Strong Presence" if avg >= 70 else "🟡 Moderate Presence" if avg >= 40 else "🔴 Low Presence — Action Needed"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="report-card">
        <h2 style="color:#FFD700; margin-bottom:20px; font-size:26px;">📋 AEO Report Card</h2>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:16px; margin-bottom:24px;">
            <div class="score-box">
                <div style="font-size:32px; font-weight:bold; color:#2E75B6;">{s1}%</div>
                <div style="color:#555; font-size:13px; margin-top:4px;">Llama 4 Scout</div>
            </div>
            <div class="score-box">
                <div style="font-size:32px; font-weight:bold; color:#F39C12;">{s2}%</div>
                <div style="color:#555; font-size:13px; margin-top:4px;">Llama 3.3</div>
            </div>
            <div class="score-box">
                <div style="font-size:32px; font-weight:bold; color:#27AE60;">{s3}%</div>
                <div style="color:#555; font-size:13px; margin-top:4px;">Mixtral</div>
            </div>
            <div class="score-box">
                <div style="font-size:32px; font-weight:bold; color:#E74C3C;">{avg:.0f}%</div>
                <div style="color:#555; font-size:13px; margin-top:4px;">Average Score</div>
            </div>
        </div>
        <div style="background:#ffffff; border-radius:10px; padding:16px; margin-bottom:16px;">
            <span style="color:#333; font-size:16px; font-weight:bold;">Overall Status: </span>
            <span style="color:#FFD700; font-size:20px; font-weight:bold;">{overall}</span>
        </div>
        <div style="background:#ffffff; border-radius:10px; padding:16px;">
            <span style="color:#333; font-weight:bold; font-size:15px;">💡 Insight: </span>
            <span style="color:#444; font-size:14px; line-height:1.6;">
            {"Your brand <b>" + brand + "</b> appears in AI recommendations. Focus on moving up the rankings by increasing review volume and improving product listing quality." if brand and avg > 50
             else "Your brand <b>" + brand + "</b> has low AI visibility. Start by optimizing your product title, getting more reviews, and building brand authority through external mentions." if brand
             else "Enter your brand name above to get a personalized visibility score showing exactly where you rank across all 3 AI engines."}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # RECOMMENDATIONS
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Actionable Recommendations to Improve Your AEO Score")

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown("""
        <div class="rec-card-blue">
            <p style="color:#1a4a8a; font-weight:bold; font-size:15px; margin-bottom:10px;">📅 Short Term (1–4 weeks)</p>
            <p style="color:#1a3a6a; font-size:14px; line-height:1.8; margin:0;">
            ✅ Optimize product titles with AI-searchable keywords<br>
            ✅ Increase review velocity — more reviews = better AI citations<br>
            ✅ Add detailed Q&A sections to product listings<br>
            ✅ Build brand mentions on Reddit, forums, and review sites
            </p>
        </div>
        """, unsafe_allow_html=True)

    with rc2:
        st.markdown("""
        <div class="rec-card-green">
            <p style="color:#1a6a3a; font-weight:bold; font-size:15px; margin-bottom:10px;">📈 Long Term (1–3 months)</p>
            <p style="color:#1a4a2a; font-size:14px; line-height:1.8; margin:0;">
            ✅ Create blog content that answers common shopper questions<br>
            ✅ Build authority through expert reviews and endorsements<br>
            ✅ Monitor AEO visibility weekly using this tool<br>
            ✅ Track competitor rankings across all AI engines
            </p>
        </div>
        """, unsafe_allow_html=True)

elif run_btn and not query:
    st.warning("⚠️ Please enter a search query first!")

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#888; font-size:13px; padding:10px;">
    Built by <b>Yachana Parmar</b> | MCA (AI & ML) | Lovely Professional University<br>
    Pixii.ai Founding Engineer Project | Powered by Groq (Llama 4 Scout + Llama 3.3 + Mixtral)
</div>
""", unsafe_allow_html=True)