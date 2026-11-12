# Philippine PSEi historical snapshot

Source: project owner's PSEI_DATAS.xlsx, manually exported from Investing.com.
Original workbook SHA256: 07bcd37fb94470998a7e3952082b46b0db287075c514b5adff6a71b8becdd1ba.
Currency: PHP. Stored daily dates: 2023-11-06 through 2026-11-06.
29 stocks, 734 common daily price dates, 156 completed weekly returns.

Price is the workbook's original Price column. Adjustment conventions are
undocumented; these are source-price returns, not verified dividend-adjusted
or total returns. No dividends, splits, prices or missing dates were invented.
The source's Change% column is not used in calculations. Five RCR reported
changes differ from changes recomputed from Price by over 0.1 percentage point;
prices are preserved unchanged. Rounding or source adjustments may explain
these discrepancies; they have not been independently resolved.

MYNLD is excluded because its supplied history starts 2025-11-10 (243 dates),
shorter than the three-year common window. Its first supplied date is not a
claim about its listing date. Original workbook remains unchanged.

Industry choices use the five PSE sectors represented in the supplied universe:
Financials, Holding Firms, Industrial, Property, Services. No Mining and Oil
constituent is included. These sectors are broader than US GICS sub-industries.
Membership is a supplied constituent snapshot, not historical membership at
every date. Survivorship bias applies. No automatic price or membership updates.

Source date/price uniqueness, finite positive prices and identical common dates
were checked. Independent market-price verification has not been completed.
Data availability is not a claim of redistribution rights or a licence grant.
