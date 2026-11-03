# Portfolio calculation engine — stage 1

Not yet a Streamlit application. No market data, network calls, fees, or share-lot purchase plan.

Install requirements, then run `python -m unittest discover -s streamlit_planner` from the repository root.

`core/optimizer.py` accepts a T-by-N matrix of aligned daily simple returns (decimal units), unique tickers, industries, selected industries, count and capital. Objectives: `return`, `risk`, `balanced`.

Defaults: 5 stocks, 1% minimum stock weight, 35% maximum, 10% maximum cash, zero cash return, 50/50 balanced preference. All selected industries must be represented; at least three are required. Missing returns must be handled upstream, not silently filled here.

Stage A is binary MILP stock selection. Stage B is LP allocation using portfolio mean absolute deviation. These stages do not guarantee the global joint optimum. Allocation return/risk ties use secondary objectives within numerical tolerance. Selection ties retain solver tie-breaking on sorted ticker input; this is not a guarantee of identical tied selections across solver versions.

Balanced allocation scales against the maximum-return and minimum-MAD reference portfolios. Degenerate trade-off terms are omitted. Metrics are daily historical estimates. Cash and stock amounts are target allocations before fees, not executable orders.

Tests use invented data only. Selection is independently checked by exhaustive enumeration; analytical allocation fixtures check a known maximum-return solution and minimum-risk cash usage. Other tests cover constraints, identical returns, invalid settings, and capital scaling.

No deployment or GitHub commit has been performed. Upload these files under the same paths when instructed. Suggested commit: Add tested two-stage portfolio optimization engine.

