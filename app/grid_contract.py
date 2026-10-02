"""Saved grid contract: per-period limits and rolling three-period import cap."""
from .solver import Solution, solve

def solve_contract(params, limits, window_budget=None):
    result=solve(params)
    if (limits is None and window_budget is None) or not result.feasible:return result
    violations=[]
    for i,row in enumerate(result.periods):
        if limits is not None and row.purchase>limits[i]:violations.append(i)
        if window_budget is not None:
            amount=sum(r.purchase for r in result.periods[max(0,i-2):i+1])
            if amount>window_budget:violations.append(i)
    if violations:
        return Solution(False,(),0,0,None,
            'grid contract exceeded at periods '+str(violations),
            purchase_budget=params.purchase_budget,
            required_min_purchase=result.total_purchase)
    return result
