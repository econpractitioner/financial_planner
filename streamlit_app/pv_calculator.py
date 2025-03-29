import streamlit as st

st.set_page_config(page_title="Present Value Calculator", layout="wide")

st.title("Present Value (PV) Calculator")

st.sidebar.header("Input Parameters")

future_value = st.sidebar.number_input("Future Value (FV)", value=1000000, step=10000)
interest_rate = st.sidebar.slider("Annual Discount Rate (%)", min_value=0.0, max_value=0.10, value=0.03, step=0.005)
years = st.sidebar.number_input("Number of Years", value=10, step=1)

# Calculate Present Value
pv = future_value / ((1 + interest_rate) ** years)

st.markdown("### Result")
st.write(f"**Present Value (PV):** {pv:,.2f}")

st.markdown(
    """
    **Formula Used:**  
    \[
    PV = \frac{FV}{(1 + r)^t}
    \]
    where:
    - \( PV \) = Present Value  
    - \( FV \) = Future Value  
    - \( r \) = Interest Rate  
    - \( t \) = Number of Years  
    """
)
