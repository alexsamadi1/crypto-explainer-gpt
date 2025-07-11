"""
Token Explainer GPT – Future Use Case Edition
------------------------------------------------------------
A Streamlit app that explains what each crypto project *could* enable in the real world —
focusing on future utility and relatable, real-world comparisons for non-crypto users.

Audience: Curious adults who want to understand what crypto projects might *actually do*.

Author: Alex (with ChatGPT co-pilot)
"""

import os
import streamlit as st
from openai import OpenAI

# -----------------------------
# 🔧 Configuration
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

COMMON_CRYPTOS = [
    "Bitcoin (BTC)",
    "Ethereum (ETH)",
    "Solana (SOL)",
    "Avalanche (AVAX)",
    "Chainlink (LINK)",
    "Polygon (MATIC)",
    "Arbitrum (ARB)",
    "Optimism (OP)",
    "Wormhole (W)",
    "Pyth (PYTH)",
    "Render (RNDR)",
    "Starknet (STRK)",
    "Celestia (TIA)"
]

# -----------------------------
# 🧠 GPT SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = (
    """You are TokenExplainerGPT, an expert in translating advanced crypto projects
into practical, real-world future use cases that anyone can understand.

Your job is to explain what each crypto project could enable in the real world —
and why it matters — to an adult who doesn’t use crypto but wants to understand what’s coming.

Avoid crypto-specific jargon. No blockchain, tokens, or smart contracts.
Instead, focus on:

• **What future it enables** – What this project might make possible, faster, or better.
• **Who benefits** – The types of industries, people, or problems it could improve.
• **What it replaces or automates** – Current systems or companies it could change.
• **Analogy** – End with one comparison to a well-known product or infrastructure (e.g., "like Bloomberg, but for global data anyone can tap into").

Think of this like explaining the internet to someone in the 1990s. You’re showing them what this could become, in terms they already understand.
Use friendly, plain English. No hype.
"""
)

# -----------------------------
# 🧠 GPT helper
# -----------------------------

def explain_crypto(name: str) -> str:
    """Return future-oriented, analogy-driven explanation string from GPT"""
    if not name:
        return "Please enter or select a crypto to explore."

    user_prompt = f"Explain what the crypto project '{name}' could enable in the future, without any crypto jargon, for someone who doesn't use crypto."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=650,
            temperature=0.65,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# -----------------------------
# 🎨 Streamlit UI
# -----------------------------

st.set_page_config(page_title="Crypto Explainer GPT", page_icon="🪙", layout="centered")
st.title("🪙 Crypto Explainer GPT")
st.markdown(
    "Curious about crypto? Select a popular one or enter your own, and we’ll explain what it could actually *do* in the real world — in plain English."
)

with st.form("crypto_form"):
    selected = st.selectbox("Or pick a popular crypto:", options=["(None)"] + COMMON_CRYPTOS)
    custom_input = st.text_input("Or type your own:", placeholder="e.g. Uniswap, Arweave, dYdX")
    submitted = st.form_submit_button("Explain")

crypto_name = custom_input.strip() or (selected if selected != "(None)" else "")

if submitted:
    with st.spinner("Thinking..."):
        result = explain_crypto(crypto_name)
    st.markdown(result)

st.markdown("---")
st.caption("Built to help everyday people understand the future — one crypto at a time.")