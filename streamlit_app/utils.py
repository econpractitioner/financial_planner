import numpy as np

def simulate_option1(years_joint, years_single, discount_rate, inflation_rate, starting_expense, payment_joint, payment_single):
    """
    Simulate Option 1 (Pension with saving):
    For each year, you receive a pension payment (depending on joint or one-survivor period)
    and incur an expense (starting_expense, growing with inflation).
    The net cash flow is reinvested at the discount rate.
    
    Returns:
      - net_cashflows: list of net cash flows for each year.
      - cumulative_savings: list of the reinvested balance at the end of each year.
    """
    total_years = years_joint + years_single
    net_cashflows = []
    cumulative_savings = []
    savings = 0.0
    
    for year in range(1, total_years + 1):
        pension = payment_joint if year <= years_joint else payment_single
        expense = starting_expense * ((1 + inflation_rate) ** (year - 1))
        net = pension - expense
        net_cashflows.append(net)
        savings = (savings + net) * (1 + discount_rate)
        cumulative_savings.append(savings)
    
    return net_cashflows, cumulative_savings

def simulate_option2_allow_negative(principal, starting_expense, r, total_years, inflation_rate):
    """
    Simulate Option 2:
    Withdraw the full inflation-adjusted expense each year from the principal (even if that results in a negative balance).
    The remaining balance accrues interest at rate r.
    
    Returns:
      - withdrawals: list of expenses withdrawn each year.
      - balance_history: list of account balance at the end of each year (can be negative).
    """
    balance = principal
    withdrawals = []
    balance_history = []
    
    for year in range(1, total_years + 1):
        expense = starting_expense * ((1 + inflation_rate) ** (year - 1))
        withdrawals.append(expense)
        balance = (balance - expense) * (1 + r)
        balance_history.append(balance)
    
    return withdrawals, balance_history

def present_value_of_series(cashflows, r):
    """
    Compute the present value of a series of cash flows discounted at rate r.
    """
    pv = sum(cf / ((1 + r) ** (i+1)) for i, cf in enumerate(cashflows))
    return pv