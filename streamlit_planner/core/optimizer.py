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
    bounds=[(minimum,maximum)]*K+[(0,cash_limit)]+[(0,None)]*T
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
    return {'status':'optimal','objective':objective,'daily_return':expected,'daily_mad':actual_mad,
            'cash_weight':float(x[K]),'cash_amount':float(capital*x[K]),'candidate_count':len(eligible),
            'allocation':[{'ticker':tickers[i],'industry':industries[i],'weight':float(x[j]),
                           'amount':float(capital*x[j])} for j,i in enumerate(chosen)]}
