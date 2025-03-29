import streamlit as st

st.set_page_config(page_title="Financial Planning Tools", layout="wide")

st.title("📊 Financial Planning Tools")
st.write(
    """
    Welcome to the **Financial Planning App Suite**!  
    This site provides various calculators to help with retirement and investment planning.
    
    Select an app from the sidebar or click the buttons below to explore.
    """
)

st.markdown("## 📌 Available Apps")

# Retirement Simulator
st.subheader("🏦 Retirement Simulator")
st.write(
    """
    Compare two retirement options:
    - **Option 1:** Fixed pension payments with savings.
    - **Option 2:** Fixed principal investment with withdrawals.
    
    **🔹 Helps you decide which retirement plan is best!**
    """
)
if st.button("Go to Retirement Simulator"):
    st.switch_page("pages/retirement_simulator.py")

# Present Value Calculator
st.subheader("📉 Present Value Calculator")
st.write(
    """
    Calculate the **Present Value (PV)** of a future amount using a discount rate.
    
    **🔹 Useful for evaluating investments and retirement plans.**
    """
)
if st.button("Go to PV Calculator"):
    st.switch_page("pages/pv_calculator.py")

st.markdown("---")
st.write("📌 **Use the sidebar to navigate or click the buttons above.**")

