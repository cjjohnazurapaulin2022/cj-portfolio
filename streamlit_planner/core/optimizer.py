"""Two-stage academic optimizer. Input: aligned daily returns, NOT prices.
Risk is mean absolute deviation (MAD); cash return is zero.
No market retrieval, fees, or share rounding is performed here.
"""
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp, linprog


def optimize(returns, tickers, industries, selected_industries, count=5,
             capital=100000., objective='balanced', minimum=.01,
             maximum=.35, cash_limit=.10, preference=.5, cash_reserve=None):
    r = np.asarray(returns, dtype=float)
    tickers, industries = list(tickers), list(industries)
    sectors = list(selected_industries)
    if r.ndim != 2 or r.shape[0] < 2 or r.shape[1] != len(tickers):
        raise ValueError('Provide at least two aligned return observations per ticker.')
    if len(industries) != len(tickers) or len(set(tickers)) != len(tickers):
        raise ValueError('Tickers must be unique and have one industry each.')
    if not np.isfinite(r).all() or (r < -1).any():
        raise ValueError('Returns must be finite decimal simple returns, no missing values.')
    if objective not in {'return', 'risk', 'balanced'}:
        raise ValueError('Objective must be return, risk, or balanced.')
    if not isinstance(count, int) or isinstance(count, bool) or count < 3:
        raise ValueError('Stock count must be an integer of at least three.')
    if len(set(sectors)) != len(sectors) or not 3 <= len(sectors) <= count:
        raise ValueError('Choose between three and count distinct industries.')
    if not all(np.isfinite(x) for x in [capital,minimum,maximum,cash_limit,preference]):
        raise ValueError('Settings must be finite.')
    if capital <= 0 or not 0 < minimum <= maximum <= 1 or not 0 <= cash_limit <= 1 or not 0 <= preference <= 1:
        raise ValueError('Invalid capital, weight bounds, cash limit, or preference.')
    if count*minimum > 1+1e-10 or count*maximum+cash_limit < 1-1e-10:
        raise ValueError('Infeasible stock weights and cash limit.')
    # None preserves the original optional-cash API; the UI supplies a fixed reserve.
    if cash_reserve is not None:
        if not np.isfinite(cash_reserve) or not 0 <= cash_reserve <= cash_limit:
            raise ValueError('Cash reserve must be between zero and the cash limit.')
        if count*minimum > 1-cash_reserve+1e-10 or count*maximum < 1-cash_reserve-1e-10:
            raise ValueError('Stock weight bounds cannot allocate the capital remaining after the cash reserve.')
    eligible = [i for i,s in enumerate(industries) if s in sectors]
    if len(eligible) < count or any(s not in industries for s in sectors):
        raise ValueError('Insufficient eligible stocks or missing industry.')
    # Sort tickers for repeatable input ordering. Exact selection ties are solver ties.
    eligible.sort(key=lambda i: tickers[i])
    a = r[:,eligible]; mu=a.mean(axis=0); mad=np.abs(a-mu).mean(axis=0)
    def scaled(v):
        return (v-v.min())/np.ptp(v) if np.ptp(v)>1e-12 else np.zeros_like(v)
    score = mu if objective=='return' else -mad if objective=='risk' else preference*scaled(mu)-(1-preference)*scaled(mad)
    rows=[np.ones(len(eligible))]; lower=[count]; upper=[count]
    for s in sectors:
        rows.append(np.array([industries[i]==s for i in eligible],float));lower.append(1);upper.append(np.inf)
    selection=milp(-score,integrality=np.ones(len(eligible)),bounds=Bounds(0,1),
                   constraints=LinearConstraint(np.array(rows),lower,upper),options={'time_limit':60})
    if not selection.success:
        raise ValueError('Selection optimality not established: '+selection.message)
    chosen=[eligible[j] for j in np.flatnonzero(selection.x>.5)]
    a=r[:,chosen]; mu=a.mean(axis=0); dev=a-mu; T,K=a.shape; size=K+1+T
    # variables: stock weights, cash, absolute-deviation auxiliaries
    A=np.zeros((2*T,size)); A[:T,:K]=dev; A[T:,:K]=-dev
    A[:T,K+1:]=-np.eye(T); A[T:,K+1:]=-np.eye(T)
    eq=np.zeros((1,size));eq[0,:K+1]=1
    cash_bounds = (0,cash_limit) if cash_reserve is None else (cash_reserve,cash_reserve)
    bounds=[(minimum,maximum)]*K+[cash_bounds]+[(0,None)]*T
    ret=np.zeros(size);ret[:K]=mu
    risk=np.zeros(size);risk[K+1:]=1/T
    def solve(cost,extra=None):
        mat=A if extra is None else np.vstack([A,extra[0]])
        rhs=np.zeros(2*T) if extra is None else np.r_[np.zeros(2*T),extra[1]]
        sol=linprog(cost,A_ub=mat,b_ub=rhs,A_eq=eq,b_eq=[1],bounds=bounds,method='highs')
        if not sol.success:raise ValueError('Allocation failed: '+sol.message)
        return sol.x
    tol=1e-10
    high=solve(-ret); high=solve(risk,(-ret,-ret@high+tol))
    low=solve(risk); low=solve(-ret,(risk,risk@low+tol))
    def metrics(x):return float(ret@x),float(np.abs(dev@x[:K]).mean())
    rh,dh=metrics(high);rl,dl=metrics(low)
    if objective=='return' or (objective=='balanced' and preference==1):x=high
    elif objective=='risk' or (objective=='balanced' and preference==0):x=low
    else:
        cost=np.zeros(size)
        if rh-rl>1e-9:cost-=preference*ret/(rh-rl)
        if dh-dl>1e-9:cost+=(1-preference)*risk/(dh-dl)
        x=solve(cost) if np.any(cost) else low
    expected,actual_mad=metrics(x)
    if abs(x[:K+1].sum()-1)>1e-7 or (x[:K]<minimum-1e-7).any() or (x[:K]>maximum+1e-7).any() or not -1e-7<=x[K]<=cash_limit+1e-7:
        raise RuntimeError('Post-solve constraint verification failed.')
    if cash_reserve is not None and abs(x[K]-cash_reserve)>1e-7:
        raise RuntimeError('Cash reserve verification failed.')
    return {'status':'optimal','objective':objective,'daily_return':expected,'daily_mad':actual_mad,
            'cash_weight':float(x[K]),'cash_amount':float(capital*x[K]),'candidate_count':len(eligible),
            'allocation':[{'ticker':tickers[i],'industry':industries[i],'weight':float(x[j]),
                           'amount':float(capital*x[j])} for j,i in enumerate(chosen)]}
