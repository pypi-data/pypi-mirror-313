import datetime as dt
import os
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from pydantic import BaseModel
from streamlit_autorefresh import st_autorefresh

from rumorz.client import RumorzClient
from smartpy.utility import dt_util



rumorz = RumorzClient(api_url="http://localhost:8000")

import re

def remove_enum_mentions(input: str) -> str:
    return re.sub(r'(\w+)_([a-z])', lambda m: f"{m.group(1)} {m.group(2)}", input)

def get_log_content(log):
    ignore = ['FinishedCurrentTask']
    tools_emojis = {
        "Reasoning": "🤔",
        "UpdatePlan": "✅",
        "AlertUser": "👋",
        "Trader": "🗣️",
        "UpdateWatchlist": "📋",
        "UpdateMemory": "💾",
        "Sleep": "😴",
        "GetRealTimeUpdate": "🌐",
    }
    tool_descriptions = {
        "Reasoning": "Thinking",
        "AlertUser": "Alerting user",
        "UpdatePlan": "Ready to work",
        "Trader": "Trading desk",
        "UpdateWatchlist": "Updating watchlist",
        "UpdateMemory": "Updating memory",
        "Sleep": "Waiting...",
        "FinishedCurrentTask": "Subtask completed",
        "GetRealTimeUpdate": "Querying Rumorz Graph",
    }

    content = None
    match log['tool_name']:
        case 'GetRealTimeUpdate':
            content = f"Fetching real-time updates for {log['arguments']}"
        case 'Reasoning':
            content = f"{log['arguments']['reasoning']}"
        case 'UpdatePlan':
            content = f""
        case 'UpdateMemory':
            content = f"updated {log['arguments']['key']}"
        case 'Sleep':
            content = f"{log['arguments']['message']}"
        case 'AlertUser':
            content = f"{log['arguments']['message']}"
        case 'Trader':
            content = f"message to the desk: {log['arguments']['message']}"
        case 'SearchEntities':
            content = f"Searching entities: {log['arguments']}"
        case 'GetTokensSocialRanking':
            arguments = ", ".join([f"{k}: {v}" for k, v in log['arguments'].items()])
            content = f"Fetching Graph ranking by : {arguments}"
        case 'UpdateWatchlist':
            content = f"Updating Feed with: {log['arguments']}"
        case 'GetEntitySummaryUpdate':
            content = f"Entity summary update: {log['arguments']}"
        case 'GetFeed':
            content = f"Entity Feed: {log['arguments']}"
        case 'GetPriceSummary':
            content = f"Fetched price summary fpr {log['arguments']}"
        case 'SendEmail':
            content = "Sending email to your inbox"

    if content is None:
        content = f""


    content = content.replace('the missing fields', 'my memory',)
    content = content.replace('memory.', '')



    if log['tool_name'] in ignore:
        return None

    return {
        "timestamp": log["timestamp"],
        "content": f'<b style="color:white;">[ {tools_emojis.get(log["tool_name"], "🔧")} {tool_descriptions.get(log["tool_name"], log["tool_name"])} ]</b> {content}'
    }


st.set_page_config(layout="wide")
st_autorefresh(interval=5000, key="data_refresh")

if 'last_agent_refresh_timestamp' not in st.session_state:
    st.session_state.last_agent_refresh_timestamp = (datetime.utcnow() - timedelta(days=19)).isoformat()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'page' not in st.session_state:
    st.session_state.page = 1

st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: gray;
        margin-top: -50px;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px;
        border: 2px solid #1d222b;
        margin-bottom:30px;
        border-radius: 10px;
    }
    .no-border {
        border: none!important;
    }
    .header img {
        border-radius: 50%;
        width: 80px;
        height: 80px;
    }
    .header .info {
        flex-grow: 1;
        margin-left: 20px;
    }
    .header .info h1 {
        margin: 0;
        font-size: 24px;
        color: white;
    }
    .header .info p {
        margin: 5px 0;
        font-size: 16px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
    .log-box {
        border: 1px solid #1d222b;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        word-wrap: break-word;
        color:gray;
    }
    .divider {
        border-top: 2px solid 1d222b;
        margin: 10px 0;
    }
    .scrollable-container {
        max-height: 400px;
        overflow-y: auto;
    }
    .padded-container {
        padding: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header no-border">
        <img src="https://i.postimg.cc/s2P93CGN/blue-logo-no-text-svg.png" alt="Logo" />
        <div class="info">
            <h4>rumorz.io</h4>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

agent_id = 'fcbae6ae-acd9-4cfe-8a9e-cfbc1fe669a7'
st.session_state.agent_id = agent_id


def format_tool_calls(task):
    markdowns = []
    for tool_call in task['tool_calls']:
        markdowns.append(f"[{tool_call['tool_name'].replace('functions.','')}] {task['title']}\n")
    return markdowns


if 'agent_id' in st.session_state:
    data = rumorz.agent.get_state(id=st.session_state.agent_id)
    new_logs = rumorz.agent.get_logs(
        id=st.session_state.agent_id,
        from_timestamp=st.session_state.last_agent_refresh_timestamp,
        to_timestamp=datetime.utcnow().isoformat(),
        limit=10,
        page=1
    )
    st.session_state.logs = [get_log_content(log) for log in new_logs if log] + st.session_state.logs
    st.session_state.last_agent_refresh_timestamp = datetime.utcnow().isoformat()

    brain = data['brain']
    memory = brain.get("memory", {})
    positioning = memory.get("positioning", "")
    portfolio = brain.get("portfolio_summary", {})
    watch_list = brain.get("watch_list", {}).get("entities", [])
    session_start = brain.get("session_start", "N/A")
    session_duration = brain.get("session_duration", "N/A")
    risk_tolerance = memory.get("risk_tolerance", "N/A")
    initial_goal = brain.get("initial_goal", "N/A")
    name = data.get("name", "N/A")
    personality = brain.get("personality", "N/A")
    plan = brain.get("plan", {}).get("tasks", [])

    st.markdown(
        f"""
        <div class="header">
            <img src="https://i.postimg.cc/wxbw3H3t/kai-avatar.png" alt="Kai" className="w-12 h-12 rounded-full mr-4" />
            <div class="info"> <h1>{name}</h1>
        <p>Function: <span style="color:gray;">Portfolio Manager</span></p>
        <p>Asset class: <span style="color:gray;">Digital Assets</span></p>
        <p>Coverage: <span style="color:gray;">Bitcoin</span></p>
        </div>
        """.format(risk_tolerance),
        unsafe_allow_html=True
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="padded-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Activity")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            for log in st.session_state.logs:
                if log:
                    st.markdown(f'<div class="log-box">{log["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Load more"):
            older_logs = rumorz.agent.get_logs(
                id=st.session_state.agent_id,
                from_timestamp=str(dt_util.toDatetime(st.session_state.logs[-1]['timestamp']) - dt.timedelta(days=10)),
                to_timestamp=str(st.session_state.logs[-1]['timestamp']),
                limit=10,
                page=st.session_state.page * 10
            )
            st.session_state.logs.extend([get_log_content(log) for log in older_logs])
            st.session_state.page += 1
            st.rerun()
    with col2:
        tabs = st.tabs(["Market summary", "Portfolio", "Profile"])

        with tabs[0]:
            st.write(memory.get("market_conditions", ""))

        with tabs[1]:
            if type(portfolio) == dict:
                st.subheader("Trades")
                if 'trades' in portfolio:
                    st.write(pd.DataFrame(portfolio['trades']).to_html(index=False), unsafe_allow_html=True)
                st.subheader("Summary")
                if 'summary' in portfolio:
                    df = pd.DataFrame(list(portfolio['summary'].items()), columns=['stat', 'value'])
                    st.write(df.to_html(index=False), unsafe_allow_html=True)

            else:
                st.write("No trades yet")

        with tabs[2]:
            st.write(f"- **Initial goal**:  50% monthly return")
            st.write(f"- **Starting capital**: $100k")
            st.write(f"- **Risk tolerance**: {risk_tolerance.lower().capitalize() if risk_tolerance else ''}")


    st.markdown('</div>', unsafe_allow_html=True)
