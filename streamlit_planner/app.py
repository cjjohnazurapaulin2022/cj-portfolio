
"""Academic portfolio demo with built-in historical or synthetic daily prices."""
from pathlib import Path
import sys
import hashlib
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import streamlit as st
from core.optimizer import optimize
from core.returns import weekly_returns
from core.csv_data import aligned_prices

st.set_page_config(page_title='Portfolio Planner | Demo', page_icon='📊', layout='wide')
st.markdown("""
<style>
.stApp, .stApp input, .stApp textarea, .stApp button {
    font-family: Arial, Helvetica, sans-serif;
}
[data-testid="stMainBlockContainer"] {
    max-width: 1200px;
    padding-top: 3rem;
}
.planner-intro {
    max-width: 900px;
    margin: 0 0 1.6rem;
}
.planner-intro h1 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.025em;
    padding: 0;
    margin: 0 0 1rem;
}
.planner-intro .intro-subtitle {
    font-size: clamp(1.2rem, 2.5vw, 1.5rem);
    font-weight: 600;
    line-height: 1.45;
    margin: 0 0 1.2rem;
}
.planner-intro p {
    font-size: 18px;
    line-height: 1.7;
    margin: 0 0 1rem;
}
.planner-intro .intro-start {
    font-size: 18px;
    font-weight: 600;
    margin-top: 1.4rem;
}
.planner-intro .intro-note {
    font-size: 14px;
    line-height: 1.6;
    opacity: 0.8;
    margin: 1rem 0 0;
}
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding-top: 2rem; }
    .planner-intro p { font-size: 17px; }
}
</style>
<section class="planner-intro" aria-label="About the portfolio planner">
    <h1>Portfolio Investment Planner</h1>
    <p class="intro-subtitle">Choose stocks and plan your investment across three countries.</p>
    <p>This free planner uses mathematical optimization to help you explore stock portfolios
    in the <strong>United States, Philippines, and Japan</strong>. Choose whether to prioritize
    historical returns, reduce historical risk, or balance both.</p>
    <p>Personalize your portfolio by setting your <strong>capital, number of stocks,
    and preferred sectors or industries</strong>. You can also adjust allocation limits,
    risk settings, and your cash reserve.</p>
    <p>See the selected stocks and how your capital is allocated in a simple
    <strong>table and chart</strong>.</p>
    <p class="intro-start">To begin, open Portfolio settings in the sidebar and click
    “Start Computation.”</p>
    <p class="intro-note">Educational demonstration using stored historical data.
    Prices do not update automatically. Historical results do not guarantee future performance.</p>
</section>
""", unsafe_allow_html=True)


MARKETS = {
    'Philippines': ('PHP', 10000., 10000000., 100000., 1000.),
    'United States': ('USD', 1000., 1000000., 10000., 100.),
    'Japan': ('JPY', 500000., 100000000., 3000000., 10000.),
}
SECTORS = ['Banking', 'Technology', 'Utilities', 'Consumer goods', 'Property']
OBJECTIVES = {'Balance return and risk':'balanced', 'Maximize estimated return':'return', 'Minimize risk (MAD)':'risk'}

@st.cache_data
def demo_data():
    rng = np.random.default_rng(2026)
    market = rng.normal(0, .006, (756, 1))
    sectors = np.repeat(SECTORS, 4).tolist()
    factors = rng.normal(0, .004, (756, len(SECTORS)))
    r = np.column_stack([market[:,0] * (.5+i*.025) + factors[:,i//4] +




