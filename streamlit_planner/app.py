"""Academic demo UI. All returns and companies are synthetic."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import streamlit as st
from core.optimizer import optimize
from core.returns import weekly_returns

st.set_page_config(page_title='Portfolio Planner | Demo', page_icon='📊', layout='wide')
st.title('Portfolio Investment Planner')
st.caption('Explore stock selection and capital allocation with mathematical optimization.')
st.warning('SYNTHETIC DATA DEMO — invented companies and returns. No live prices or actual index constituents. Country changes currency only.')

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
    selected = st.multiselect('Industries (at least 3)', SECTORS, default=SECTORS[:3], key='industries')
    with st.expander('Advanced settings'):
        minimum = st.number_input('Minimum stock weight (%)', .1, 100., 1., .1, key='minimum')
        maximum = st.number_input('Maximum stock weight (%)', .1, 100., 35., .5, key='maximum')
        cash = st.number_input('Fixed cash reserve (%)', 0., 10., 10., 1., key='cash_reserve')
        preference = st.slider('Return emphasis for balanced objective (%)', 0, 100, 50, key='preference')
        st.caption('0 = risk emphasis; 100 = return emphasis. Cash earns 0% in this model.')
        st.caption('The chosen reserve is held exactly. Default: 10%; choose 0% only to disable it. Stock weights use total capital.')
    start = st.button('Start Computation', type='primary', key='compute')

signature = ('weekly-reserve-v3', country, capital, count, label, tuple(selected), minimum, maximum, cash, preference)
if st.session_state.get('signature') != signature:
    st.session_state.pop('result', None)

if start:
    st.session_state.pop('result', None)
    errors = []
    if not 3 <= len(selected) <= count:
        errors.append('Select at least three industries and no more industries than stocks.')
    eligible = sum(s in selected for s in industries)
    if eligible < count:
        errors.append(f'Only {eligible} demo stocks are eligible. Select more industries or fewer stocks.')
    if minimum > maximum:
        errors.append('Minimum stock weight cannot exceed the maximum.')
    if count * minimum > 100-cash+1e-9:
        errors.append('Minimum stock weights exceed the capital available after reserving cash. Reduce the minimum or stock count.')
    if count * maximum + cash < 100-1e-9:
        errors.append(f'Increase maximum stock weight to at least {(100-cash)/count:.2f}%, or increase the stock count or reserve.')
    if errors:
        for error in errors: st.error(error)
    else:
        try:
            with st.spinner('Selecting stocks and optimizing allocations…'):
                result = optimize(returns, tickers, industries, selected, count=int(count), capital=capital,
                                  objective=OBJECTIVES[label], minimum=minimum/100, maximum=maximum/100,
                                  cash_limit=.10, preference=preference/100, cash_reserve=cash/100)
            st.session_state.result = result
            st.session_state.signature = signature
        except (ValueError, RuntimeError) as exc:
            st.error(str(exc))
