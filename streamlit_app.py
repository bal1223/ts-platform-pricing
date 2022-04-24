import streamlit as st
import datetime as dt
import pandas as pd
import utils.plots as plt
import utils.data_fns as data_fns
from PIL import Image

# st.markdown('<small>test</small>', unsafe_allow_html=True)

def run_app():
    # Page settings
    st.set_page_config(page_title="Pricing Scenarios", layout="wide")

    # Teamshares logo on sidebar
    st.sidebar.image(Image.open('teamshares-logo.png'), use_column_width=True)

    # Set up Sidebar
    with st.sidebar:
        run_scenario = st.button("Run") # may need to update to form later. Disable if checksums not satisfied

        st.title("Scenario Assumptions")
        st.markdown("### Average Company Monthly Settings")
        with st.expander("Accounts"):
            deposits_balance = st.slider("Deposits Balance:", min_value = 100000, max_value = 500000, value=300000, step=25000)
            acct_count = st.number_input("Accounts", value=2.5, step=0.5, help="Ex: company could have an account for each store location.")

        with st.expander("Incoming Transactions"):
            inc_trans_cnt = st.slider("Count:", min_value=10, max_value= 200, value=50, step=10, key="inc_trans_cnt")
            inc_trans_amt = st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="inc_trans_amt")
            st.write("##### Implied Avg. Transaction Size:", inc_trans_amt/inc_trans_cnt)
            
            st.write("### Breakdown by Type (%):")
            ach_in = st.slider("ACH:", value=10, key="ach_in")
            checks_in = st.slider("Checks:", value=70, key="checks_in")
            cc_in = st.slider("Cards:", value=15, key="cc_in")
            cash_in = st.slider("Cash:", value=5, key="cash_in")
            wires_in = st.slider("Wires:", value=0, key="wires_in")

            inc_checksum = ach_in + checks_in + cc_in + cash_in + wires_in
            st.write("##### checksum:", inc_checksum)

        with st.expander("Outgoing Transactions"):
            out_trans_cnt = st.slider("Count:", min_value=10, max_value= 200, value=100, step=10, key="out_trans_cnt")
            out_trans_amt = st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="out_trans_amt")
            st.write("##### Implied Avg. Transaction Size:", out_trans_amt/out_trans_cnt)
            
            st.write("### Breakdown by Type (%):")
            ach_out = st.slider("ACH:", value=15, key="ach_out")
            checks_out = st.slider("Checks:", value=70, key="checks_out")
            cc_out = st.slider("Cards:", value=10, key="cc_out")
            cash_out = st.slider("Cash:", value=0, key="cash_out")
            bill_pay_out = st.slider("Bill Pay:", value=4, key="cash_out")
            wires_out = st.slider("Wires:", value=1, key="wires_out")

            outc_checksum = ach_out + checks_out + cc_out + cash_out + wires_out + bill_pay_out
            st.write("##### checksum:", outc_checksum)

        st.markdown("### Revenue Settings")
        with st.expander("Interchange"):
            net_ic = st.slider("Net Interchange:", min_value=1.0, max_value=3.0, value=2.0, step=0.1, key="net_ic")
        
        with st.expander("Interest on Deposits"):
            yield_curve_flag = st.checkbox("Use current yield curve?")
            if not yield_curve_flag:
                fed_rate = st.number_input("Flat Fed Rate (bps):", value=50, min_value=0, max_value=200, step=25, key="fed_rate")
        
        st.markdown("### Other Settings")
        with st.expander("Chart Settings"):
            annualize_flag = st.checkbox("Annualize monthly values?")
            chart_freq = st.selectbox("Plot Frequency:", options=['Monthly', 'Quarterly'])
            vendor_exc = st.multiselect("Vendor Exclusions:", options=['Stripe','Unit','Treasury Prime','Column'])

    # Main body
    # 1. Description and intro
    with st.container():
        st.markdown("### Description")


    # 2. Platform growth
    with st.container():
        st.markdown("### Company Onboard & Platform Growth")


    # Base Case Results
    st.markdown("### Platform Base Case")
    st.write("Some comments here about what the base case is")
    # 3. P/L
    with st.container():
        st.markdown("##### Net Income")

    # 4. Revenue
    with st.container():
        st.markdown("##### Revenue")

    # 5. Costs
    with st.container():
        st.markdown("##### Costs")

    # 6. Scenario Variation: Digital Transition
    with st.container():
        st.markdown("### Scenario Variation: Network Digital Transition")

if __name__ == '__main__':
    run_app()