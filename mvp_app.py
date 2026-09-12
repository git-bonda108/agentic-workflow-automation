#!/usr/bin/env python3
"""
Dragonfruit Media — Proposal & MVP Demo
Dashboard: time allocations, pipeline, proposal summary, Producer agent (OpenAI Agents SDK + ClickUp).
Run: streamlit run mvp_app.py
"""
import asyncio
import json
import os
import re
from pathlib import Path

# Load .env so credentials (ClickUp, Slack, etc.) are available when you add them
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Paths
BASE = Path(__file__).resolve().parent
MOCK = BASE / "mock_data"

# Chart colors — Dragonfruit website–inspired (dragonfruitmedia.co)
PALETTE = {
    "primary": "#E85D75",
    "accent": "#E85D75",
    "success": "#0d9488",
    "warning": "#f59e0b",
    "error": "#dc2626",
}


def load_json(name: str):
    path = MOCK / f"{name}.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Page config
st.set_page_config(
    page_title="Dragonfruit AI Proposal & MVP",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — Dragonfruit Media: premium, divine, full Streamlit polish
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    :root {
        --df-bg: #FAFAFA;
        --df-bg-warm: #FFF9F6;
        --df-surface: #FFFFFF;
        --df-text: #1a1a1a;
        --df-text-muted: #64748B;
        --df-accent: #E85D75;
        --df-accent-dark: #C94B62;
        --df-accent-glow: rgba(232, 93, 117, 0.25);
        --df-success: #0d9488;
        --df-success-bg: rgba(13, 148, 136, 0.08);
        --df-border: #E2E8F0;
        --df-shadow: 0 1px 3px rgba(0,0,0,0.06);
        --df-shadow-card: 0 4px 24px rgba(0,0,0,0.06);
        --df-shadow-card-hover: 0 8px 32px rgba(0,0,0,0.08);
        --df-radius: 16px;
        --df-radius-sm: 12px;
    }
    * { font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important; }
    .stApp { max-width: 1600px; margin: 0 auto; background: linear-gradient(180deg, var(--df-bg-warm) 0%, var(--df-bg) 100%) !important; }
    main { background: transparent !important; padding: 2rem 2.5rem 4rem !important; }
    main .stMarkdown, main p, main li { color: var(--df-text) !important; }
    h1 { font-weight: 800 !important; letter-spacing: -0.04em !important; color: var(--df-text) !important; font-size: 2.5rem !important; line-height: 1.15 !important; }
    h2 { font-weight: 700 !important; color: var(--df-text) !important; font-size: 1.45rem !important; margin-top: 1.75rem !important; letter-spacing: -0.02em !important; }
    h3 { font-weight: 600 !important; color: var(--df-text) !important; font-size: 1.15rem !important; }
    [data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 800 !important; color: var(--df-accent) !important; letter-spacing: -0.02em !important; }
    [data-testid="stMetricDelta"] { font-weight: 600 !important; }
    [data-testid="stMetricLabel"] { color: var(--df-text-muted) !important; font-weight: 500 !important; font-size: 0.9rem !important; }
    [data-testid="stMetric"] {
        background: var(--df-surface) !important; padding: 1.5rem !important; border-radius: var(--df-radius) !important;
        box-shadow: var(--df-shadow-card) !important; border: 1px solid var(--df-border) !important;
        border-left: 4px solid var(--df-accent) !important; transition: box-shadow 0.2s ease, transform 0.2s ease !important;
    }
    [data-testid="stMetric"]:hover { box-shadow: var(--df-shadow-card-hover) !important; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: var(--df-surface); padding: 8px; border-radius: 999px; box-shadow: var(--df-shadow);
        border: 1px solid var(--df-border);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px; font-weight: 600; border-radius: 999px; color: var(--df-text-muted) !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--df-text) !important; background: var(--df-bg) !important; }
    .stTabs [aria-selected="true"] { background: var(--df-accent) !important; color: white !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--df-surface) 0%, var(--df-bg-warm) 100%) !important;
        border-right: 1px solid var(--df-border) !important; box-shadow: 4px 0 24px rgba(0,0,0,0.03) !important;
    }
    [data-testid="stSidebar"] .stMarkdown { color: var(--df-text) !important; }
    [data-testid="stSidebar"] label { color: var(--df-text-muted) !important; }
    [data-testid="stSidebar"] [data-baseweb="radio"] label { padding: 10px 14px !important; border-radius: var(--df-radius-sm) !important; transition: background 0.2s !important; }
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover { background: var(--df-bg) !important; }
    .stButton > button {
        border-radius: 999px !important; font-weight: 600 !important; background: var(--df-accent) !important;
        color: white !important; border: none !important; padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important; box-shadow: 0 2px 8px var(--df-accent-glow) !important;
    }
    .stButton > button:hover {
        background: var(--df-accent-dark) !important; box-shadow: 0 6px 20px var(--df-accent-glow) !important;
        transform: translateY(-1px) !important;
    }
    .streamlit-expanderHeader { font-weight: 600 !important; color: var(--df-text) !important; }
    [data-testid="stExpander"] {
        background: var(--df-surface) !important; border-radius: var(--df-radius) !important;
        box-shadow: var(--df-shadow) !important; border: 1px solid var(--df-border) !important;
    }
    [data-testid="stDataFrame"] { border-radius: var(--df-radius) !important; overflow: hidden !important; box-shadow: var(--df-shadow) !important; }
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMetric"]) { gap: 1rem !important; }
    .df-hero {
        padding: 2.5rem 0 2rem; margin-bottom: 1.5rem; text-align: left;
        border-bottom: 3px solid var(--df-accent); background: linear-gradient(135deg, rgba(232,93,117,0.04) 0%, transparent 50%);
        border-radius: var(--df-radius); padding-left: 1.5rem; padding-right: 1.5rem;
    }
    .df-hero h1 { margin-bottom: 0.5rem !important; }
    .df-hero p { font-size: 1.15rem !important; line-height: 1.5 !important; color: var(--df-text-muted) !important; }
    .df-card {
        background: var(--df-surface); border-radius: var(--df-radius); padding: 1.75rem;
        box-shadow: var(--df-shadow-card); border: 1px solid var(--df-border); margin: 1.25rem 0;
    }
    .df-pill { display: inline-block; padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; margin-right: 0.5rem; margin-bottom: 0.5rem; }
    .df-pill-ok { background: var(--df-success-bg); color: var(--df-success); border: 1px solid rgba(13,148,136,0.3); }
    .df-pill-demo { background: rgba(245,158,11,0.12); color: #b45309; border: 1px solid rgba(245,158,11,0.35); }
    .df-footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--df-border); color: var(--df-text-muted); font-size: 0.9rem; text-align: center; }
    blockquote { border-left: 4px solid var(--df-accent); padding-left: 1rem; margin: 1rem 0; color: var(--df-text-muted); font-style: italic; }
    main table { border-radius: var(--df-radius); overflow: hidden; box-shadow: var(--df-shadow); }
    main table th { background: var(--df-accent) !important; color: white !important; font-weight: 600 !important; padding: 14px 18px !important; }
    main table td { padding: 14px 18px !important; }
    main table tr:nth-child(even) { background: var(--df-bg) !important; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
        border-radius: var(--df-radius-sm) !important; border: 1px solid var(--df-border) !important;
    }
    [data-testid="stSelectbox"] > div { border-radius: var(--df-radius-sm) !important; }
    .js-plotly-plot .plotly { border-radius: var(--df-radius) !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar — premium, clear hierarchy
st.sidebar.markdown("### 🥭 Dragonfruit Media")
st.sidebar.markdown("**#1 Global YouTube Agency**")
st.sidebar.caption("AI & Automation · EOY 2026")
st.sidebar.markdown("Scale **4 → 7** clients per pod")
st.sidebar.divider()
st.sidebar.markdown("**Navigate**")

nav = st.sidebar.radio(
    "Navigate",
    [
        "🎬 Run Demo",
        "📊 Time Allocations (Current vs Dream)",
        "🔄 Pipeline Overview",
        "📋 Proposal Summary",
        "🤖 Producer Agent (ClickUp)",
        "📁 Wish List & Tools",
    ],
    label_visibility="collapsed",
)

# Connector status (used in Run Demo + sidebar)
def _connector_status():
    out = {"clickup": False, "slack": False, "frameio": False, "notion": False}
    try:
        from connectors.clickup_client import is_clickup_configured
        out["clickup"] = is_clickup_configured()
    except Exception:
        pass
    try:
        from connectors.slack_client import is_slack_configured
        out["slack"] = is_slack_configured()
    except Exception:
        pass
    try:
        from connectors import is_frameio_configured, is_notion_configured
        out["frameio"] = is_frameio_configured()
        out["notion"] = is_notion_configured()
    except Exception:
        pass
    return out

_conn = _connector_status()
st.sidebar.divider()
st.sidebar.markdown("**Connections**")
conn_text = "Mock ✅  ClickUp " + ("✅" if _conn["clickup"] else "○") + "  Slack " + ("✅" if _conn["slack"] else "○") + "  Frame.io " + ("✅" if _conn["frameio"] else "○") + "  Notion " + ("✅" if _conn["notion"] else "○")
st.sidebar.caption(conn_text)
st.sidebar.divider()
st.sidebar.caption("[Demo script](DEMO_SCRIPT.md) · [Plan](AGENTIC_PLAN.md)")
st.sidebar.caption("[Connect data](CONNECT_YOUR_DATA.md) · [HITL](HUMAN_IN_THE_LOOP_GATES.md)")

# --- Run Demo (all 8 high-priority tools, tabbed) ---
if nav == "🎬 Run Demo":
    has_openai_demo = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    has_clickup_demo = _conn["clickup"]
    has_slack_demo = _conn["slack"]
    has_frameio_demo = _conn["frameio"]
    has_notion_demo = _conn["notion"]

    wish = load_json("wishlist_tools")
    high = wish.get("high_priority", [])
    alloc = load_json("time_allocations").get("roles", {})
    pipeline = load_json("pipeline_stages")
    pods_data = load_json("pods_and_clients")
    pod_names = [p["name"] for p in pods_data.get("pods", [])]

    n_connected = sum([has_clickup_demo, has_slack_demo, has_frameio_demo, has_notion_demo])
    st.markdown("""
    <div class="df-hero">
        <h1>Your environment. Faster.</h1>
        <p>Same pipeline, same pods, same tools — with agentic workflow so you deliver best value and coordination runs itself.</p>
        <div style="margin-top:1.25rem;">
            <span class="df-pill df-pill-ok">Mock data</span>
            <span class="df-pill """ + ("df-pill-ok" if has_clickup_demo else "df-pill-demo") + """">ClickUp</span>
            <span class="df-pill """ + ("df-pill-ok" if has_slack_demo else "df-pill-demo") + """">Slack</span>
            <span class="df-pill """ + ("df-pill-ok" if has_frameio_demo else "df-pill-demo") + """">Frame.io</span>
            <span class="df-pill """ + ("df-pill-ok" if has_notion_demo else "df-pill-demo") + """">Notion</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if n_connected > 0:
        st.success(f"**{n_connected} of 4** integrations active (from .env). Use real data in your flows.")
    st.markdown("---")

    tab_overview, tab_cd1, tab_cd2, tab_cd3, tab_cd4, tab_ed1, tab_ed2, tab_ed3, tab_pr4 = st.tabs([
        "Overview",
        "CD-1 Retention",
        "CD-2 Outlier Ideation",
        "CD-3 Packaging",
        "CD-4 A/B Monitor",
        "ED-1 Sentiment",
        "ED-2 QC",
        "ED-3 Assignment",
        "PR-4 ClickUp",
    ])

    # ---------- Overview ----------
    with tab_overview:
        st.markdown('<div class="df-card"><h3 style="margin-top:0;">Your current environment — with agents and MCP</h3></div>', unsafe_allow_html=True)
        with st.container():
            st.markdown("""
            This demo uses **your** pipeline, **your** pods, **your** time allocations, and **your** wish list.  
            Nothing is generic. We're showing how each of your **8 high-priority tools** lives inside the same workflow you use today — ClickUp, Notion, Frame.io, Slack — but **faster**, with **agentic workflows** handling coordination so your team can focus on strategy and creative.
            """)
            st.markdown("**Coordination today:** Producers and PCs spend the majority of their time on admin (ClickUp, Slack, meetings). We're addressing that with agents + MCP so tasks, statuses, and feedback flow without manual handoffs.")
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Clients per pod today", pods_data.get("current_clients_per_pod", 4), None)
        with c2:
            st.metric("Target EOY 2026", pods_data.get("target_clients_per_pod_eoy2026", 7), "+3")
        with c3:
            prod = alloc.get("Producers", {})
            coord = (prod.get("current") or {}).get("ClickUp Administration (Total)", 0) * 100
            st.metric("Producer ClickUp time (today)", f"{coord:.0f}%", "→ ~18% with PR-4")
        st.markdown("**Your pipeline:** " + pipeline.get("pipeline_name", "Production Pipeline") + f" — {len(pipeline.get('phases', []))} phases. **Your pods:** " + ", ".join(pod_names) + ".")
        st.markdown("---")
        st.subheader("Connections (MCP / APIs)")
        clickup_status = "✅ Connected" if has_clickup_demo else "🔶 Demo mode"
        slack_status = "✅ Connected" if has_slack_demo else "🔶 Not configured"
        frameio_status = "✅ Configured" if has_frameio_demo else "🔜 Not set"
        notion_status = "✅ Configured" if has_notion_demo else "🔜 Not set"
        st.markdown(f"""
        | System | Status | Notes |
        |--------|--------|-------|
        | **Mock Data** | ✅ | Pipeline, pods, wish list from `mock_data/` (same as Dragonfruit MCP). |
        | **ClickUp** | {clickup_status} | PR-4 creates real tasks when `CLICKUP_*` in `.env`. |
        | **Slack** | {slack_status} | List channels / send when `SLACK_BOT_TOKEN` in `.env`. |
        | **Frame.io** | {frameio_status} | ED-1 sentiment when `FRAMEIO_ACCESS_TOKEN` set. |
        | **Notion** | {notion_status} | CD-6 / context when `NOTION_API_KEY` set. |
        """)
        if has_slack_demo:
            try:
                from connectors.slack_client import slack_list_channels
                chans = slack_list_channels(limit=10)
                if chans:
                    with st.expander("Slack channels (first 10)"):
                        for c in chans:
                            st.markdown(f"- `#{c['name']}` — `{c['id']}`")
                else:
                    st.caption("Slack connected; add scope `channels:read` to list channels.")
            except Exception:
                pass
        st.caption("Credentials from `.env`. See **CONNECT_YOUR_DATA.md** and **MCP_SERVERS_AND_DATA.md**.")

    # ---------- CD-1 Predictive Retention ----------
    with tab_cd1:
        t = next((x for x in high if x.get("id") == "CD-1"), {})
        st.subheader(t.get("name", "CD-1 Predictive Retention Scoring"))
        st.caption("Creative Director · " + t.get("category", "") + " — Your script, your channel context.")
        st.markdown(t.get("description", ""))
        script_input = st.text_area("Paste script (or use sample)", value="[Intro hook 0:00-0:15]\nWhy most people get this wrong...\n[Main point 1]\n[Main point 2]\n[Main point 3]\n[CTA and outro]", height=140, key="cd1_script")
        col_cd1a, col_cd1b = st.columns([1, 3])
        with col_cd1a:
            run_cd1 = st.button("Run retention prediction", key="run_cd1")
        if run_cd1:
            # Mock retention curve (100% at start, dip mid, decline)
            x = [i * 100 / 49 for i in range(50)]
            y = [max(22, min(100, 100 - 0.4 * xi - 15 * (2.718 ** (-((xi - 35) ** 2) / 80)))) for xi in x]
            fig = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=PALETTE["success"], width=2), name="Predicted retention %"))
            fig.update_layout(title="Predicted audience retention", xaxis_title="% through video", yaxis_title="Retention %", height=320, margin=dict(t=40, b=40))
            st.plotly_chart(fig, width="stretch")
            st.markdown("**Drop-off flags**")
            st.markdown("- **~35%** — Main point 1 may feel long; consider tightening or adding a visual hook.")
            st.markdown("- **~65%** — Retention dip; script could use a clear transition or payoff before point 3.")
            st.markdown("**Improvement suggestions**")
            st.markdown("- Shorten intro to 10–12 seconds; move hook earlier. Add a curiosity gap in the first 5 seconds.")
            st.markdown("- Add a mid-video recap or \"what you’ll learn\" to re-engage before point 3.")
            st.success("In production: model uses your channel context and format (longform/shortform). Simulated above.")

    # ---------- CD-2 Outlier Ideation ----------
    with tab_cd2:
        t = next((x for x in high if x.get("id") == "CD-2"), {})
        st.subheader(t.get("name", "CD-2 Competitive Outlier Ideation Engine"))
        st.caption("Creative Director · " + t.get("category", "") + " — ~20 competitor channels per client.")
        st.markdown(t.get("description", ""))
        clients_flat = []
        for p in pods_data.get("pods", []):
            for c in p.get("clients", []):
                clients_flat.append({"client": c["name"], "pod": p["name"], "id": c["id"]})
        client_option = st.selectbox("Select client (your pods)", [f"{x['client']} ({x['pod']})" for x in clients_flat], key="cd2_client")
        if st.button("Generate weekly digest", key="run_cd2"):
            st.markdown("**Outlier videos this week** — themes, format, why they outperformed")
            df_outlier = pd.DataFrame([
                {"Video title": "The One Mistake That Cost Me 6 Figures", "Theme": "Mistake / lesson", "Format": "Story + takeaway", "Why outlier": "CTR 12% vs channel avg 6%; strong curiosity gap"},
                {"Video title": "Why Nobody Talks About This", "Theme": "Underrated topic", "Format": "List + opinion", "Why outlier": "Retention 58% at 2 min; hook repeated at 1:30"},
                {"Video title": "I Tried X for 30 Days (Results)", "Theme": "Experiment / results", "Format": "Challenge + data", "Why outlier": "Thumbnail A/B: face + number beat text-only by 40%"},
            ])
            st.dataframe(df_outlier, width="stretch", hide_index=True)
            st.caption("Data from your configured competitor channels. In production: continuous monitoring; digest via Slack or Notion.")
            st.success("Simulated with your client list. Mock Data MCP can feed competitor config per client.")

    # ---------- CD-3 Visual Packaging ----------
    with tab_cd3:
        t = next((x for x in high if x.get("id") == "CD-3"), {})
        st.subheader(t.get("name", "CD-3 Visual Packaging & Thumbnail Intelligence"))
        st.caption("Creative Director · " + t.get("category", ""))
        st.markdown(t.get("description", ""))
        packaging_input = st.text_input("Script snippet or thumbnail concept", value="Why most people get this wrong — and what to do instead", key="cd3_input")
        if st.button("Score packaging + suggest thumbnail text", key="run_cd3"):
            st.metric("Packaging score", "7.2 / 10", "Curiosity gap strong; clarity could improve")
            st.markdown("**Thumbnail text suggestions** (from script + competitor patterns)")
            st.markdown("- **\"Most people get this wrong\"** — high curiosity; matches top performers in your niche.")
            st.markdown("- **\"What to do instead\"** — clear value; consider pairing with a number (e.g. \"3 steps\").")
            st.markdown("- **\"The one mistake\"** — alternative angle; test A/B vs current.")
            st.caption("In production: competitor thumbnail analysis + Google Trends/SEO cross-check. Your channel shelf strategy.")
            st.success("Simulated. Production uses your competitor thumbnails and script library.")

    # ---------- CD-4 A/B Test Monitor ----------
    with tab_cd4:
        t = next((x for x in high if x.get("id") == "CD-4"), {})
        st.subheader(t.get("name", "CD-4 Competitor A/B Test Monitor"))
        st.caption("Creative Director · " + t.get("category", "") + " — Slack DM in production.")
        st.markdown(t.get("description", ""))
        st.markdown("**Recent alerts** (simulated — your competitor set)")
        alerts = [
            {"Competitor": "Channel A", "Change": "Title + thumbnail", "Before": "How I did X", "After": "The $0 Method That Changed Everything", "Δ CTR": "+42%", "Slack": "✅ Alert sent"},
            {"Competitor": "Channel B", "Change": "Thumbnail", "Before": "Text-only", "After": "Face + number", "Δ CTR": "+28%", "Slack": "✅ Alert sent"},
            {"Competitor": "Channel C", "Change": "Description", "Before": "Short blurb", "After": "Timestamped chapters", "Δ Retention": "+12%", "Slack": "✅ Alert sent"},
        ]
        for a in alerts:
            with st.expander(f"{a['Competitor']} — {a['Change']}", expanded=True):
                st.markdown(f"**Before:** {a['Before']}  \n**After:** {a['After']}  \n**Performance:** {a.get('Δ CTR', a.get('Δ Retention', '—'))}  \n{a['Slack']}")
        st.caption("In production: automated detection + Slack DM to CD with before/after and performance delta. Your competitor list from config.")
        st.success("Simulated. Connects to same competitor pipeline as CD-2 and CD-3.")

    # ---------- ED-1 (Frame.io Sentiment) ----------
    with tab_ed1:
        t = next((x for x in high if x.get("id") == "ED-1"), {})
        st.subheader(t.get("name", "ED-1 Frame.io Comment Sentiment Analyzer"))
        st.caption("Editor / PPM · " + t.get("category", "") + " · " + ("Frame.io connected" if has_frameio_demo else "Demo mode (mock comments)"))
        st.markdown(t.get("description", ""))
        # Build client + video options from pods
        all_clients = []
        for pod in pods_data.get("pods", []):
            for c in pod.get("clients", []):
                all_clients.append({"client": c["name"], "client_id": c["id"], "pod": pod["name"]})
        client_names = [x["client"] for x in all_clients]
        ed1_client_sel = st.selectbox("Client", client_names, key="ed1_client")
        mock_videos = ["V1 — Intro cut (Mar 5)", "V2 — B-roll pass (Mar 4)", "V3 — Color (Mar 3)", "V4 — Final review (Mar 2)"]
        ed1_video_sel = st.selectbox("Video / asset", mock_videos, key="ed1_video")
        alert_threshold = st.slider("Alert when sentiment score below", 0.0, 1.0, 0.4, 0.1, key="ed1_threshold")
        if st.button("Run sentiment analysis", key="ed1_run"):
            st.session_state["ed1_ran"] = True
        if st.session_state.get("ed1_ran"):
            st.markdown("---")
            st.markdown("**Video-level sentiment** (" + ed1_video_sel + ")")
            sent_scores = {"Positive": 0.62, "Neutral": 0.28, "Negative": 0.10}
            fig_ed1 = go.Figure(data=[go.Bar(x=list(sent_scores.keys()), y=list(sent_scores.values()), marker_color=[PALETTE["success"], PALETTE["warning"], PALETTE["error"]])])
            fig_ed1.update_layout(title="Comment sentiment (this asset)", yaxis_title="Proportion", height=280, margin=dict(t=40))
            st.plotly_chart(fig_ed1, width="stretch")
            overall = 0.72
            if overall < alert_threshold:
                st.warning(f"⚠️ Score {overall:.2f} is below alert threshold ({alert_threshold}). Consider PPM follow-up.")
            else:
                st.success(f"Overall sentiment score: **{overall:.2f}** (above threshold).")
            st.markdown("**Client-level trend** (" + ed1_client_sel + ")")
            weeks = ["W-4", "W-3", "W-2", "W-1", "This week"]
            trend_scores = [0.58, 0.61, 0.65, 0.68, overall]
            fig_trend = go.Figure(data=[go.Scatter(x=weeks, y=trend_scores, mode="lines+markers", line=dict(color=PALETTE["accent"], width=2), marker=dict(size=10))])
            fig_trend.update_layout(yaxis_title="Sentiment score", height=260, margin=dict(t=30), yaxis=dict(range=[0, 1]))
            st.plotly_chart(fig_trend, width="stretch")
        st.caption("Connects to Frame.io MCP/API for real comments when configured. Your clients, your assets.")

    # ---------- ED-2 (Automated QC) ----------
    with tab_ed2:
        t = next((x for x in high if x.get("id") == "ED-2"), {})
        st.subheader(t.get("name", "ED-2 Automated Video QC Checker"))
        st.caption("Editor / PPM · " + t.get("category", ""))
        st.markdown(t.get("description", ""))
        all_clients_ed2 = []
        for pod in pods_data.get("pods", []):
            for c in pod.get("clients", []):
                all_clients_ed2.append(c["name"])
        ed2_client = st.selectbox("Client", all_clients_ed2, key="ed2_client")
        ed2_videos = ["V1 — Intro cut", "V2 — B-roll pass", "V3 — Color", "V4 — Final review"]
        ed2_video = st.selectbox("Video / asset", ed2_videos, key="ed2_video")
        if st.button("Run checklist", key="ed2_run"):
            st.session_state["ed2_report"] = [
                {"Timestamp": "00:00:12", "Rule": "Safe zone / title safe", "Status": "Pass", "Severity": "—"},
                {"Timestamp": "00:01:45", "Rule": "Audio levels (-14 LUFS)", "Status": "Fail", "Severity": "High"},
                {"Timestamp": "00:02:30", "Rule": "Color consistency (client LUT)", "Status": "Pass", "Severity": "—"},
                {"Timestamp": "00:03:00", "Rule": "Lower-third duration", "Status": "Warning", "Severity": "Medium"},
                {"Timestamp": "00:05:15", "Rule": "End card / CTA", "Status": "Pass", "Severity": "—"},
            ]
        if st.session_state.get("ed2_report"):
            st.markdown("---")
            st.markdown("**Timestamped QC report** — " + ed2_client + " · " + ed2_video)
            df_qc = pd.DataFrame(st.session_state["ed2_report"])
            st.dataframe(df_qc, width="stretch", hide_index=True)
            fails = sum(1 for r in st.session_state["ed2_report"] if r["Status"] == "Fail")
            if fails > 0:
                st.warning(f"**{fails}** item(s) need attention before delivery.")
            st.caption("Client-specific checklist from your SOPs. In production: automated against exported frame/audio.")
        else:
            st.caption("Select client and video, then **Run checklist**. Uses your client SOPs and QC rules.")

    # ---------- ED-3 (Capacity Assignment) ----------
    with tab_ed3:
        t = next((x for x in high if x.get("id") == "ED-3"), {})
        st.subheader(t.get("name", "ED-3 Automated Capacity-Based Task Assignment"))
        st.caption("Producer / PC · " + t.get("category", "") + " · " + ("ClickUp connected" if has_clickup_demo else "Demo mode (mock tasks)"))
        st.markdown(t.get("description", ""))
        st.markdown("**Batch ready** — tasks awaiting assignment:")
        mock_batch_tasks = [
            {"Task": "Longform edit — Client Alpha", "Type": "Longform", "Due": "Fri Mar 14", "Est. hrs": 8},
            {"Task": "Shortform batch — Client Gamma", "Type": "Shortform", "Due": "Mon Mar 10", "Est. hrs": 4},
            {"Task": "Color pass — Client Beta", "Type": "Longform", "Due": "Wed Mar 12", "Est. hrs": 3},
        ]
        st.dataframe(pd.DataFrame(mock_batch_tasks), width="stretch", hide_index=True)
        if st.button("Suggest assignees", key="ed3_run"):
            st.session_state["ed3_suggestions"] = [
                {"Editor": "Editor 1", "Current workload (hrs)": 24, "Skill match": "Longform", "Suggested": "Yes", "Notes": "Best fit for Alpha"},
                {"Editor": "Editor 2", "Current workload (hrs)": 18, "Skill match": "Shortform", "Suggested": "Yes", "Notes": "Capacity + Gamma experience"},
                {"Editor": "Editor 3", "Current workload (hrs)": 32, "Skill match": "Longform", "Suggested": "No", "Notes": "At capacity"},
            ]
        if st.session_state.get("ed3_suggestions"):
            st.markdown("---")
            st.markdown("**Suggested assignees** (workload, skill, pod)")
            st.dataframe(pd.DataFrame(st.session_state["ed3_suggestions"]), width="stretch", hide_index=True)
            st.caption("Uses ClickUp + editor availability when connected. Producer/PC confirms assignment (human-in-the-loop).")
        else:
            st.caption("Click **Suggest assignees** to see workload-aware suggestions. Uses ClickUp tasks and editor capacity.")

    # ---------- PR-4 (full UI + Human-in-the-loop) ----------
    with tab_pr4:
        t = next((x for x in high if x.get("id") == "PR-4"), {})
        st.subheader(t.get("name", "PR-4 Claude-to-ClickUp Agent"))
        st.caption("Producer · " + t.get("category", "") + " · " + ("Connected to ClickUp" if has_clickup_demo else "Demo mode (mock ClickUp)"))
        st.markdown(t.get("description", ""))
        st.markdown("Ask in your own words; the Producer agent **proposes** a task. You **confirm** before it is created (human-in-the-loop at critical gate).")
        demo_cmd = st.text_area("Natural language command", value="Create a new task for Mango Pod: longform edit for Client Alpha, due Friday, assign to Editor 1", height=70, key="demo_cmd")
        col_run, _ = st.columns([1, 3])
        with col_run:
            run_clicked = st.button("Run Producer agent", key="demo_run")
        if run_clicked:
            if not has_openai_demo:
                # Mock: propose task and store for HITL
                st.session_state["pr4_pending"] = {"list_id": "list_mango", "name": "Longform edit — Client Alpha", "due_date": "Friday", "assignee": "Editor 1", "_demo": True, "reply": "Proposed task based on your request. Confirm below to create in ClickUp."}
            else:
                try:
                    from agents import Runner
                    from role_agents.producer_agent import get_producer_agent
                    async def run_demo():
                        agent = get_producer_agent()
                        return await Runner.run(agent, demo_cmd)
                    with st.spinner("Producer agent running…"):
                        result_demo = asyncio.run(run_demo())
                    proposal = {"list_id": "list_mango", "name": "Longform edit — Client Alpha", "due_date": "Friday", "assignee": "Editor 1", "_demo": False, "reply": getattr(result_demo, "final_output", str(result_demo))}
                    st.session_state["pr4_pending"] = proposal
                except ImportError:
                    st.warning("OpenAI Agents SDK not available (e.g. Python 3.10+ required). Using mock proposal.")
                    st.session_state["pr4_pending"] = {"list_id": "list_mango", "name": "Longform edit — Client Alpha", "due_date": "Friday", "assignee": "Editor 1", "_demo": True, "reply": "Mock proposal — set up Python 3.10+ and openai-agents to run the real agent."}
                except Exception as e:
                    st.error(f"Run failed: {e}")
                    st.session_state.pop("pr4_pending", None)
        # Human-in-the-loop: show pending proposal and Confirm / Cancel
        if st.session_state.get("pr4_pending"):
            pending = st.session_state["pr4_pending"]
            st.markdown("---")
            st.markdown("**Human-in-the-loop — confirm before creating**")
            st.markdown("Review the proposed task. Only **Confirm** will create it in ClickUp.")
            st.json({k: v for k, v in pending.items() if k != "reply"})
            if pending.get("reply"):
                with st.expander("Agent reply"):
                    st.write(pending["reply"])
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button("Confirm create task", key="pr4_confirm", type="primary"):
                    # Actually create (or show success in mock)
                    if pending.get("_demo"):
                        st.success("Task created in ClickUp (demo mode): *" + pending.get("name", "") + "*")
                    else:
                        try:
                            from connectors.clickup_client import clickup_create_task
                            clickup_create_task(list_id=pending.get("list_id", "list_mango"), name=pending.get("name", "Task"), description=None, due_date_ms=None)
                            st.success("Task created in ClickUp.")
                        except Exception as e:
                            st.error(f"Create failed: {e}")
                    st.session_state.pop("pr4_pending", None)
                    st.rerun()
            with c2:
                if st.button("Cancel", key="pr4_cancel"):
                    st.session_state.pop("pr4_pending", None)
                    st.rerun()
        st.caption("ClickUp: " + ("connected (real API or MCP)" if has_clickup_demo else "demo mode (mock lists/tasks)") + " · Critical gate: HUMAN_IN_THE_LOOP_GATES.md")
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

# --- Time Allocations ---
elif nav == "📊 Time Allocations (Current vs Dream)":
    st.markdown("""
    <div class="df-hero">
        <h1>Current vs Dream Time Allocation</h1>
        <p>By role — source: DFM Current vs. Dream Time Allocations (50h week).</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_json("time_allocations")
    roles_data = data.get("roles", {})

    role_select = st.selectbox(
        "Select role",
        list(roles_data.keys()),
        index=0,
    )

    role = roles_data.get(role_select, {})
    current = role.get("current", {})
    dream = role.get("dream", {})

    if current or dream:
        # Build comparison: top-level categories only for clarity
        current_items = [(k, v, "Current") for k, v in sorted(current.items(), key=lambda x: -x[1])[:12]]
        dream_items = [(k, v, "Dream") for k, v in sorted(dream.items(), key=lambda x: -x[1])[:12]]

        # Unified categories that appear in both
        all_keys = set(current.keys()) | set(dream.keys())
        rows = []
        for k in sorted(all_keys, key=lambda x: -(current.get(x, 0) + dream.get(x, 0) / 2)):
            c = current.get(k, 0)
            d = dream.get(k, 0)
            if c > 0 or d > 0:
                rows.append({"Category": k[:45] + ("..." if len(k) > 45 else ""), "Current %": round(c * 100, 1), "Dream %": round(d * 100, 1)})

        df = pd.DataFrame(rows)
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Current", x=df["Category"], y=df["Current %"], marker_color=PALETTE["error"]))
            fig.add_trace(go.Bar(name="Dream", x=df["Category"], y=df["Dream %"], marker_color=PALETTE["success"]))
            fig.update_layout(
                barmode="group",
                title=f"{role_select} — Current vs Dream",
                xaxis_tickangle=-35,
                yaxis_title="% of capacity",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500,
            )
            st.plotly_chart(fig, width="stretch")

        if role.get("key_notes"):
            st.info(f"**Key notes:** {role['key_notes']}")
        st.markdown(f"**People:** {role.get('people', '—')} | **Capacity (h/week):** {role.get('capacity_hours_per_week', '—')}")
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

# --- Pipeline ---
elif nav == "🔄 Pipeline Overview":
    st.markdown("""
    <div class="df-hero">
        <h1>Production Pipeline Overview</h1>
        <p>Source: DFM Current Pipeline (with Feedback).</p>
    </div>
    """, unsafe_allow_html=True)

    data = load_json("pipeline_stages")
    phases = data.get("phases", [])

    for p in phases:
        with st.expander(f"**{p['phase']}** ({len(p['steps'])} steps)", expanded=(p["order"] <= 2)):
            for s in p["steps"]:
                st.markdown(f"- **{s['step']}** — *{s['role']}* · {s['tool']}")

    pods = load_json("pods_and_clients")
    st.subheader("Pods & capacity")
    st.metric("Current clients per pod", pods.get("current_clients_per_pod", 4))
    st.metric("Target (EOY 2026) clients per pod", pods.get("target_clients_per_pod_eoy2026", 7))
    for pod in pods.get("pods", [])[:2]:
        st.markdown(f"**{pod['name']}**: {len(pod['clients'])} clients, {pod['editors_count']} editors")
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

# --- Proposal Summary ---
elif nav == "📋 Proposal Summary":
    st.markdown("""
    <div class="df-hero">
        <h1>Proposal Summary</h1>
        <p>Full document: proposal_contract/Dragonfruit_Proposal_EOY2026.html (export to PDF).</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Objective")
    st.markdown("Scale from **4 → 7 clients per pod** by EOY 2026 without proportional headcount increase.")

    st.subheader("Three levers")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. Workflow automation**  \nClickUp, Slack, Notion, Dropbox — reduce coordination overhead.")
    with col2:
        st.markdown("**2. Agentic infrastructure**  \nAI agents for task routing, status updates, feedback distribution.")
    with col3:
        st.markdown("**3. Right-fit AI toolkit**  \nWish list tools by role (predictive retention, QC, capacity assignment, etc.).")

    st.subheader("Target outcomes (from your materials)")
    st.markdown("""
    | Role | Current → Dream |
    |------|-----------------|
    | Producers | Coordination 74.5% → 41% |
    | Production Coordinators | Coordination 70% → 40% |
    | Creative Directors | Preproduction 29% → 50%; V1/ClickUp admin → 0% |
    | Post Production Managers | Reactive 1:1s → intentional editor management |
    | Editors | Core editing 66% → 80%; idle 6.5% → 2% |
    """)

    st.subheader("Implementation roadmap (high level)")
    st.markdown("""
    - **Phase 1 (Days 1–30):** Slack templates, ClickUp↔Slack notifications, timeline calculator.
    - **Phase 2 (Months 1–2):** Claude-to-ClickUp pilot, capacity assignment v1, Frame.io sentiment beta.
    - **Phase 3 (Months 2–4):** Automated QC, Claude Projects per client, first CD tools.
    - **Phase 4 (Months 4–6):** Rollout to all pods; CD-2/CD-3/CD-4; 7 clients per pod.
    """)

    st.subheader("Costs (indicative)")
    st.markdown("""
    - **Labour:** ~80–120 days (phased + retainer).
    - **New system/tooling:** ~$3–7K/month (licenses + APIs + hosting).
    """)
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

# --- Producer Agent (OpenAI Agents SDK + ClickUp) ---
elif nav == "🤖 Producer Agent (ClickUp)":
    st.markdown("""
    <div class="df-hero">
        <h1>Producer Agent — ClickUp</h1>
        <p>OpenAI Agents SDK + ClickUp connector. Natural language → task create/update (real API or demo mode).</p>
    </div>
    """, unsafe_allow_html=True)

    has_openai = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    has_clickup = False
    try:
        from connectors.clickup_client import is_clickup_configured
        has_clickup = is_clickup_configured()
    except Exception:
        pass

    col1, col2 = st.columns(2)
    with col1:
        st.metric("OpenAI API key", "Set" if has_openai else "Not set (agent disabled)")
    with col2:
        st.metric("ClickUp", "Connected" if has_clickup else "Demo mode")

    default_cmd = "Create a new task for Mango Pod: longform edit for Client Alpha, due Friday, assign to Editor 1"
    command = st.text_area(
        "Natural language command",
        value=default_cmd,
        height=80,
        placeholder="e.g. Create task for Mango Pod, longform edit for Client Alpha, due Friday, assign to Editor 1",
    )

    if st.button("Run Producer agent"):
        if not has_openai:
            st.warning("Set OPENAI_API_KEY to run the real agent. Showing mock result below.")
            # Fallback: simple mock
            pod = "Mango Pod"
            client = "Client Alpha"
            task_type = "longform edit"
            if "Lemon" in command or "lemon" in command:
                pod = "Lemon Pod"
            for c in ["Client Alpha", "Client Beta", "Client Gamma"]:
                if c.lower() in command.lower():
                    client = c
                    break
            if "shortform" in command.lower():
                task_type = "shortform edit"
            st.success("Mock result (no API key).")
            st.markdown("**Would create in ClickUp:**")
            st.json({
                "space": pod,
                "task_name": f"{task_type} — {client}",
                "type": task_type,
                "client": client,
                "due_date": "Friday",
                "assignee": "Editor 1",
                "status": "To Do",
            })
        else:
            try:
                from agents import Runner
                from role_agents.producer_agent import get_producer_agent
            except Exception as import_err:
                st.error(f"Could not load OpenAI Agents SDK (need Python 3.10+): {import_err}")
                st.stop()

            try:
                async def run():
                    agent = get_producer_agent()
                    return await Runner.run(agent, command)

                with st.spinner("Producer agent running…"):
                    result = asyncio.run(run())

                st.success("Agent finished.")
                st.markdown("**Reply:**")
                st.write(result.final_output)
                if getattr(result, "run_items", None):
                    with st.expander("Tool calls"):
                        for item in result.run_items:
                            name = getattr(item, "tool_name", None) or getattr(item, "name", str(item))
                            out = getattr(item, "result", None) or getattr(item, "output", "")
                            st.text(f"{name}: {out}")
            except Exception as e:
                st.error(f"Agent run failed: {e}")
                st.code(str(e), language="text")
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

# --- Wish List & Tools ---
elif nav == "📁 Wish List & Tools":
    st.markdown("""
    <div class="df-hero">
        <h1>AI Wish List & Tool Stack</h1>
        <p>High- and medium-priority tools by role; current stack spend.</p>
    </div>
    """, unsafe_allow_html=True)
    wish = load_json("wishlist_tools")
    tools_stack = load_json("tool_stack")

    st.subheader("High-priority wish list tools (8)")
    for t in wish.get("high_priority", []):
        st.markdown(f"- **{t['id']}** — *{t['name']}* ({t['role']}, {t['category']})  \n  {t['description']}")

    st.subheader("Medium-priority wish list tools (8)")
    for t in wish.get("medium_priority", []):
        st.markdown(f"- **{t['id']}** — *{t['name']}* ({t['role']}, {t['category']})  \n  {t['description']}")

    st.subheader("Current tool stack (top 10 by spend)")
    total = tools_stack.get("total_monthly_usd", 0)
    st.metric("Total monthly spend (all tools)", f"${total:,.0f}")
    for t in tools_stack.get("tools", [])[:10]:
        st.markdown(f"- **{t['name']}** — ${t['monthly_usd']:,.0f}/mo · {t['plan']}")
    st.markdown("---")
    st.markdown('<p class="df-footer">Your pipeline · Your pods · Your wish list · Running faster.</p>', unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.caption("Proposal due March 13th · Confidential")
