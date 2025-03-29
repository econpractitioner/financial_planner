import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Retirement Options Simulator", layout="wide")

st.title("Retirement Options Simulator")

st.markdown("""
This app compares two retirement options:
- **Option 1:** A pension that pays a fixed amount (600,000 during the joint period and 300,000 thereafter). 
  Any surplus (pension minus expenses) is reinvested at the discount rate.
- **Option 2:** An investment of a fixed principal (6,000,000) from which you withdraw an expense (growing with inflation) every year.
  In this simulation, withdrawals are taken in full—even if that leads to a negative balance.
  
The starting annual expense is common for both options. Adjust the parameters below to see how your retirement options compare.
""")

st.sidebar.header("Possible Options")

# Option 1 parameters
st.sidebar.subheader("Option 1: Pension")
payment_joint = st.sidebar.number_input("Annual Pension Payment (Joint period)", value=600000, step=10000)
payment_single = st.sidebar.number_input("Annual Pension Payment (One-survivor period)", value=300000, step=10000)
years_joint = st.sidebar.number_input("Years both spouses are alive", value=12, step=1)
years_single = st.sidebar.number_input("Years one spouse is alive", value=3, step=1)
total_years = years_joint + years_single

# Common Starting Expense for both options.
starting_expense = st.sidebar.number_input("Starting Annual Expense", value=360000, step=5000)

# Common parameters
st.sidebar.subheader("Option 2: Invest in fixed income security")
principal = st.sidebar.number_input("Principal available", value=6000000, step=100000)
discount_rate = st.sidebar.slider("Interest rate", min_value=0.0, max_value=0.10, value=0.07, step=0.005)
inflation_rate = st.sidebar.number_input("Inflation Rate", value=0.05, step=0.005, format="%.3f")



st.markdown("### Simulation Functions")

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

# Run simulations for both options.
net_cashflows1, savings_history = simulate_option1(years_joint, years_single, discount_rate, inflation_rate, starting_expense, payment_joint, payment_single)
withdrawals2, balance_history2 = simulate_option2_allow_negative(principal, starting_expense, discount_rate, total_years, inflation_rate)

# Compute Present Values.
pv_option1 = present_value_of_series(net_cashflows1, discount_rate)
pv_option2_withdrawals = present_value_of_series(withdrawals2, discount_rate)
pv_option2_final = balance_history2[-1] / ((1 + discount_rate) ** total_years)
pv_option2 = pv_option2_withdrawals + pv_option2_final

st.markdown("### Results")
st.write(f"**Option 1 (Pension with Saving) Present Value:** {pv_option1:,.0f}")
st.write(f"**Option 2 (Fixed Instrument) Present Value:** {pv_option2:,.0f}")

# Prepare data for plotting
years = np.arange(1, total_years+1)
# Convert values to millions for plotting.
savings_lakhs = np.array(savings_history) / 1e5
balance_lakhs = np.array(balance_history2) / 1e5

st.markdown("### Year-by-Year Evolution")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(years, savings_lakhs, label="Option 1: savings", marker='o')
ax.plot(years, balance_lakhs, label="Option 2: remaining balance", marker='s')
ax.set_xlabel("Year")
ax.set_ylabel("Value (Lakhs)")
ax.set_title("Year-by-Year Evolution: Option 1 vs Option 2")
ax.legend()
ax.grid(True)

st.pyplot(fig)