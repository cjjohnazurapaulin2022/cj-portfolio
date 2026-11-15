# Japan Nikkei 225 candidate snapshot

Source: project-owner JP225DATAS.xlsx, manually downloaded from Investing.com.
Original workbook SHA256: 245856fda33df7e76323962f5233a4bccb13aa0c1ae1833d70bd79d4b0de0c8c.
Source workbook remains unchanged. Original sheets: 30, with 733 dates each.
Stored sample: 30 stocks, 732 common daily price dates, 2023-11-06 to 2026-11-06.
Daily source Price column used unchanged on retained dates. Currency: JPY.
Weekly Friday-ending closes produce 156 weekly returns.

Cleaning: exclude 2026-11-03 from all stocks, a confirmed Japanese cash-equity
market holiday (Culture Day). All 30 supplied rows on this date also have
inconsistent OHLC ranges. The supplied Nippon Yusen sheet has 15 empty leading
columns; these are ignored. No prices are filled, interpolated or winsorized.
The supplied Change % column is not used to calculate returns.

Dividend and split adjustment conventions are undocumented. These are source-
price returns, not independently verified total returns. The internal shared
loader field named adjusted_close does not verify the underlying adjustments.
All retained prices were checked for finite positive values, unique dates and
complete common coverage. Source reported daily changes match recomputed Price
changes within 0.1 percentage point. This is internal consistency checking,
not independent price or corporate-action verification. Entire exchange
calendar and every market price have not been independently audited.

Industry: Nikkei industry classification, with broad sector retained separately.
Universe is a selected 30-stock subset, NOT all 225 constituents or an investment
ranking. Membership checked against official Nikkei list on 2026-11-13.
Historical membership changes are not reconstructed; survivorship bias applies.

References:
https://indexes.nikkei.co.jp/en/nkave/index/component
https://www.jpx.co.jp/english/corporate/about-jpx/calendar/index.html

Fixed historical snapshot: no automatic data fetching or date-window changes.
Replace prices and metadata together after validating any future update.
Public availability does not establish redistribution permission or a licence.
