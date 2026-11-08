"""Academic portfolio demo with synthetic or user-supplied daily prices."""
from pathlib import Path
import sys
import hashlib
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import streamlit as st
from core.optimizer import optimize
from core.returns import weekly_returns
from core.csv_data import load_csv, aligned_prices

st.set_page_config(page_title='Portfolio Planner | Demo', page_icon='📊', layout='wide')
st.title('Portfolio Investment Planner')
st.caption('Explore stock selection and capital allocation with mathematical optimization.')


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
                        rng.normal(.00015+i*.00003, .004+(i%4)*.002, 756)
                        for i in range(20)])
    return r, [f'DEMO{i+1:02d}' for i in range(20)], sectors

daily_returns, tickers, industries = demo_data()
# Artificial calendar is solely a demonstration of daily-to-weekly conversion.
# Includes a baseline price before the first generated daily return.
demo_dates = pd.bdate_range('2023-01-06', periods=len(daily_returns)+1)
daily_prices = pd.DataFrame(
    np.vstack([np.ones((1, len(tickers))), np.cumprod(1+daily_returns, axis=0)])*100,
    index=demo_dates, columns=tickers,
)
weekly = weekly_returns(daily_prices)
returns = weekly.to_numpy()
st.caption('Optimization frequency: weekly. Returns are calculated from daily prices at completed week ends.')
with st.sidebar:
    st.header('Portfolio settings')
    country = st.selectbox('Country / display currency', list(MARKETS), key='country')
    currency, low, high, default, step = MARKETS[country]
    custom = st.checkbox('Use a custom capital amount', key='custom')
    capital = st.number_input(f'Capital ({currency})', min_value=1. if custom else low,
                              max_value=None if custom else high, value=default, step=step,
                              key=f'capital_{currency}_{custom}')
    count = st.number_input('Number of stocks desired', min_value=3, max_value=20, value=5, step=1, key='count')
    label = st.selectbox('Objective', list(OBJECTIVES), key='objective')
    mode = st.radio('Data source', ['Synthetic demo', 'Upload daily-price CSV'])
    uploaded = None
    imported = None
    data_error = None
    data_id = 'synthetic'
    options = SECTORS
    if mode == 'Upload daily-price CSV':
        uploaded = st.file_uploader('Daily adjusted prices (.csv)', type=['csv'])
        st.caption('Required columns: date, ticker, company, industry, currency, adjusted_close. Dates: YYYY-MM-DD.')
        st.download_button('Download CSV header template',
                           'date,ticker,company,industry,currency,adjusted_close\n',
                           file_name='daily_prices_template.csv', mime='text/csv')
        if uploaded is not None:
            raw = uploaded.getvalue()
            data_id = hashlib.sha256(raw).hexdigest()
            try:
                imported = load_csv(raw, currency)
                options = sorted(imported['industry'].unique())
            except ValueError as exc:
                data_error = str(exc)
                options = []
        else:
            options = []
    selected = st.multiselect('Industries (at least 3)', options, default=options[:3],
                              key=f'industries_{mode}_{country}_{data_id}')
    with st.expander('Advanced settings'):
        minimum = st.number_input('Minimum stock weight (%)', .1, 100., 1., .1, key='minimum')
        maximum = st.number_input('Maximum stock weight (%)', .1, 100., 35., .5, key='maximum')
        cash = st.number_input('Fixed cash reserve (%)', 0., 10., 10., 1., key='cash_reserve')
        preference = st.slider('Return emphasis for balanced objective (%)', 0, 100, 50, key='preference')
        st.caption('0 = risk emphasis; 100 = return emphasis. Cash earns 0% in this model.')
        st.caption('The chosen reserve is held exactly. Default: 10%; choose 0% only to disable it. Stock weights use total capital.')
        filter_on = st.checkbox('Limit individual stock risk', key='filter_on')
        stock_limit_pct = st.number_input('Maximum stock weekly standard deviation (%)',
                                         0., 100., 5., .1, disabled=not filter_on, key='stock_limit')
        ceiling_on = st.checkbox('Limit portfolio risk', key='ceiling_on')
        portfolio_limit_pct = st.number_input('Maximum portfolio weekly MAD (%)',
                                             0., 100., 2., .1, disabled=not ceiling_on, key='portfolio_limit')
        st.caption('Optional historical risk limits. Example values are demo settings, not recommended risk levels. These limits do not cap future losses.')
