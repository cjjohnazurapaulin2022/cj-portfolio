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
    country = st.selectbox('Country / display currency', list(MARKETS), index=1, key='country')
    currency, low, high, default, step = MARKETS[country]
    custom = st.checkbox('Use a custom capital amount', key='custom')
    capital = st.number_input(f'Capital ({currency})', min_value=1. if custom else low,
                              max_value=None if custom else high, value=default, step=step,
                              key=f'capital_{currency}_{custom}')
    count = st.number_input('Number of stocks desired', min_value=3, max_value=20, value=5, step=1, key='count')
    label = st.selectbox('Objective', list(OBJECTIVES), key='objective')
    mode = st.radio('Data source', ['Built-in historical data', 'Synthetic demo'])
    imported = None
    data_error = None
    data_id = 'synthetic'
    options = SECTORS
    if mode == 'Built-in historical data':
        if country == 'Japan':
            data_error = 'Built-in data for this country is still being prepared. Choose United States or Philippines to use an available historical snapshot.'
            options = []
        else:
            try:
                folder = Path(__file__).resolve().parent / 'data'
                prefix = 'ph' if country == 'Philippines' else 'us'
                price_path = folder / f'{prefix}_prices.csv'
                meta_path = folder / f'{prefix}_companies.csv'
                data_id = hashlib.sha256(price_path.read_bytes() + meta_path.read_bytes()).hexdigest()
                prices = pd.read_csv(price_path, index_col='date', parse_dates=True)
                info = pd.read_csv(meta_path).set_index('ticker')
                imported = prices.rename_axis(columns='ticker').stack().rename('adjusted_close').reset_index()
                imported = imported.merge(info[['company','industry']], on='ticker', validate='many_to_one')
                imported['currency'] = currency
                options = sorted(imported['industry'].unique())
            except (OSError, ValueError, KeyError) as exc:
                data_error = f'Cannot load the built-in {country} data. Upload data/{prefix}_prices.csv and data/{prefix}_companies.csv together.'
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
    start = st.button('Start Computation', type='primary', key='compute')

is_csv = mode == 'Built-in historical data'
if is_csv:
    st.info('BUILT-IN HISTORICAL SNAPSHOT — stored daily prices. No automatic updates.')
    if data_error:
        st.error(data_error)
    elif imported is not None:
        st.caption(f"{country} snapshot: {imported['date'].min().date()} to {imported['date'].max().date()} · {imported['ticker'].nunique()} candidates with complete daily histories.")
        if country == 'Philippines':
            st.caption('PSE sector choices. Maynilad excluded because its supplied history is shorter than three years. Membership is a fixed constituent snapshot, not historical membership at every date.')
            st.warning('Philippine calculations use the workbook’s Price column. Dividend and split adjustments are unverified, so results are source-price returns, not verified total returns. Prices are preserved; the reported Change% column is not used.')
        else:
            st.caption('Eight shorter-history stocks excluded. Industry choices use GICS sub-industries. Current constituent snapshot; historical index membership and source adjustments have not been independently audited.')
        try:
            daily_prices, metadata = aligned_prices(imported, selected)
            weekly = weekly_returns(daily_prices)
            tickers = list(daily_prices.columns)
            industries = metadata['industry'].tolist()
            returns = weekly.to_numpy()
        except ValueError as exc:
            data_error = str(exc)
            st.error(data_error)
else:
    st.warning('SYNTHETIC DATA DEMO — invented companies and returns. No live prices or actual index constituents. Country changes currency only.')

names = dict(zip(tickers, metadata['company'])) if is_csv and imported is not None and not data_error else {t: f'Synthetic company {t[-2:]}' for t in tickers}
source_label = f'BUILT-IN {country.upper()} SNAPSHOT' if is_csv else 'SYNTHETIC DEMO'
signature = ('builtin-v7', mode, data_id, filter_on, stock_limit_pct, ceiling_on, portfolio_limit_pct, country, capital, count, label, tuple(selected), minimum, maximum, cash, preference)
if st.session_state.get('signature') != signature:
    st.session_state.pop('result', None)

if start:
    st.session_state.pop('result', None)
    errors = []
    if is_csv and (imported is None or data_error):
        errors.append(data_error or 'Built-in data is unavailable.')
    if not 3 <= len(selected) <= count:
        errors.append('Select at least three industries and no more industries than stocks.')
    eligible = sum(s in selected for s in industries)
    if eligible < count:
        errors.append(f'Only {eligible} candidate stocks are eligible. Select more industries or fewer stocks.')
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
                                  cash_limit=.10, preference=preference/100, cash_reserve=cash/100,
                                  stock_risk_limit=stock_limit_pct/100 if filter_on else None,
                                  portfolio_mad_limit=portfolio_limit_pct/100 if ceiling_on else None)
            st.session_state.result = result
            st.session_state.signature = signature
        except (ValueError, RuntimeError) as exc:
            st.error(str(exc))

result = st.session_state.get('result')
if result:
    st.success('Optimization completed — ' + ('built-in historical sample' if is_csv else 'synthetic demonstration results'))
    for heading, value in [
        ('Capital', f'{currency} {capital:,.2f}'),
        ('Stock allocation', f'{currency} {capital-result["cash_amount"]:,.2f}'),
        ('Cash reserved', f'{currency} {result["cash_amount"]:,.2f} ({cash:g}%)'),
        ('Stocks selected', str(len(result['allocation']))),
    ]:
        st.markdown(f'**{heading}:** {value}')
    st.caption(f'{result["candidate_count"]} eligible stocks after screening; {result["excluded_by_risk"]} excluded by the stock-risk filter.')
    st.subheader('Target allocation')
    rows = [{'Company':names[x['ticker']], 'Ticker':x['ticker'],
             'Industry':x['industry'], 'Weight (%)':100*x['weight'],
             f'Amount ({currency})':x['amount']} for x in result['allocation']]
    rows.append({'Company':'Cash retained','Ticker':'CASH','Industry':'Cash',
                 'Weight (%)':100*result['cash_weight'],f'Amount ({currency})':result['cash_amount']})
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, width="stretch",
                 column_config={'Weight (%)':st.column_config.NumberColumn(format='%.2f'),
                                f'Amount ({currency})':st.column_config.NumberColumn(format='%.2f')})
    st.caption(f'Total allocation: {df["Weight (%)"].sum():.2f}% · Amounts are targets before fees and share/lot rounding.')
    st.subheader('Allocation by stock and cash')
    chart_data = df.assign(Label=df['Company'] + ' (' + df['Ticker'] + ')')
    st.vega_lite_chart(chart_data, {
        'mark': {'type': 'bar', 'cornerRadiusEnd': 3},
        'height': max(220, len(df)*36),
        'encoding': {
            'x': {'field': 'Weight (%)', 'type': 'quantitative',
                  'title': 'Portfolio weight (%)', 'scale': {'zero': True}},
            'y': {'field': 'Label', 'type': 'nominal', 'sort': '-x',
                  'title': None, 'axis': {'labelLimit': 300}},
            'color': {'condition': {'test': "datum.Ticker === 'CASH'", 'value': '#d99518'},
                      'value': '#1674b8'},
            'tooltip': [{'field': 'Company', 'type': 'nominal'},
                        {'field': 'Weight (%)', 'type': 'quantitative', 'format': '.2f'},
                        {'field': f'Amount ({currency})', 'type': 'quantitative', 'format': ',.2f'}],
        },
    }, use_container_width=True)
    a,b=st.columns(2)
    a.metric('Mean weekly return — ' + ('historical sample' if is_csv else 'synthetic sample'), f'{result["period_return"]:.4%}')
    b.metric('Weekly portfolio MAD — ' + ('historical sample' if is_csv else 'synthetic sample'), f'{result["period_mad"]:.4%}')
    export=df.assign(Data_source=source_label, Price_start=str(daily_prices.index.min().date()), Price_end=str(daily_prices.index.max().date()), Objective=label, Currency=currency, Return_frequency='weekly', Weekly_observations=len(weekly),
                     Price_basis=('Source Price; adjustments unverified' if country == 'Philippines' else 'Source-described adjusted prices; unaudited') if is_csv else 'Synthetic prices',
                     Stock_weekly_SD_limit_pct=stock_limit_pct if filter_on else 'Disabled',
                     Portfolio_weekly_MAD_limit_pct=portfolio_limit_pct if ceiling_on else 'Disabled')
    st.download_button('Download allocation CSV', export.to_csv(index=False).encode('utf-8-sig'),
                       file_name=f'allocation_{currency}.csv', mime='text/csv')
    with st.expander('Calculation details'):
        if is_csv:
            st.write(f'{len(daily_prices)} daily price dates converted to {len(weekly)} weekly return observations. Price range: {daily_prices.index.min().date()} to {daily_prices.index.max().date()}. Weekly return range: {weekly.index.min().date()} to {weekly.index.max().date()}.')
            if country == 'Philippines':
                st.caption('Price source: project-owner workbook, manually exported from Investing.com. Source Price used unchanged; adjustment conventions unverified. Five RCR reported changes differ by over 0.1 percentage point from changes recomputed from Price. Stored snapshot, no automatic updates.')
            else:
                st.caption('Price source: Aethereal S&P 500 Stock Prices; company metadata: datasets/s-and-p-500-companies. Stored snapshot, no automatic updates. Source adjustments are not independently audited.')
        else:
            st.write(f'{len(daily_returns)} synthetic daily returns converted to {len(weekly)} weekly return observations; fixed random seed 2026.')
        st.write('Selection: binary MILP. Allocation: LP with mean absolute deviation. Each stage is optimal for its own problem; joint global optimality is not claimed.')
        st.write('Weekly return = this week-end stored price / previous week-end stored price - 1. Incomplete final weeks are excluded. Weekly returns are compounded, not averaged daily returns.')
        if not is_csv: st.write('The demo uses invented prices and an artificial weekday calendar beginning January 2023. These dates are not real market history. Live three-year data is not connected yet.')
else:
    st.info('Choose your settings, then click Start Computation.')
    if not is_csv: st.write('This demonstration tests the mathematical workflow before market data is connected. Each industry contains four invented stocks.')
