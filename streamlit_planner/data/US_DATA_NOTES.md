# US historical snapshot

Price source: https://dataset.aethereal.top/datasets/sp500-stock-prices
Source describes prices as split- and dividend-adjusted, free for research and education.
Source prices were supplied by the project owner on 2026-11-08.
Original SHA256: f7d9ceecefb07672f83a52282f7def57b7a547605dd3f26204c07d1f0c13e5fc
Metadata: https://github.com/datasets/s-and-p-500-companies/blob/main/data/constituents.csv
Metadata retrieved 2026-11-08. All 503 source tickers matched.

Frozen three-calendar-year window ending 2026-11-05; stored trading dates
2023-11-06 through 2026-11-05; 753 daily dates and 495 stocks.
Excluded for incomplete histories: FDXF, GEV, HONA, Q, RDDT, SNDK, SOLV, VYLR.
No prices were filled. Industry uses GICS sub-industry; sector retained separately.

Membership represents the source's current-constituent snapshot, not historical
membership on every trading date. This introduces survivorship bias in backtests.
Source prices and corporate-action adjustments have not been independently audited.
A future update must replace BOTH data files together after checking coverage.
Stored data is fixed; the app does not fetch prices or roll the date window forward.
Philippine and Japanese price snapshots are not included yet.
