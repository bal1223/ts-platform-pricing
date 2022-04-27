import streamlit as st
import datetime as dt
import pandas as pd
import json
import utils.plots as plt
import utils.data_fns as data_fns
from PIL import Image

# st.markdown('<small>test</small>', unsafe_allow_html=True)
SCENARIO_SETTINGS = {}

def run_app():
    # Page settings
    st.set_page_config(page_title="Pricing Scenarios", layout="wide")

    # Teamshares logo on sidebar
    st.sidebar.image(Image.open('teamshares-logo.png'), use_column_width=True)

    # Set up Sidebar
    with st.sidebar:
        st.title("Scenario Assumptions")
        st.markdown("### Average Company Monthly Settings")

        # Avg deposit balance, account count, card counts
        with st.expander("Accounts"):
            SCENARIO_SETTINGS.update({'avg_deposits_balance': st.slider("Deposits Balance:", min_value = 100000, max_value = 500000, value=300000, step=25000)})
            SCENARIO_SETTINGS.update({'acct_cnt': st.number_input("Accounts", value=2.5, step=0.5, help="Ex: company could have an account for each store location.")})            

            # Maybe make this fixed?
            SCENARIO_SETTINGS.update({'phy_card_cnt': st.number_input("Physical Cards Issued", value=3, step=1, help="Physical branded cards issued per company.")})
            SCENARIO_SETTINGS.update({'virt_card_cnt': st.number_input("Virtual Cards Issued", value=5, step=1, help="Virtual cards issued per company.")})
        
        # Inc transaction assumptions
        with st.expander("Incoming Transactions"):
            SCENARIO_SETTINGS.update({'inc_trans_cnt': st.slider("Count:", min_value=10, max_value= 200, value=50, step=10, key="inc_trans_cnt")})
            SCENARIO_SETTINGS.update({'inc_trans_amt': st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="inc_trans_amt")})
            st.write("##### Implied Avg. Transaction Size:", SCENARIO_SETTINGS.get('inc_trans_amt')/SCENARIO_SETTINGS.get('inc_trans_cnt'))
            
            st.write("### Breakdown by Type (%):")
            SCENARIO_SETTINGS.update({'ach_in': st.slider("ACH:", value=10, step=5, key="ach_in")})
            SCENARIO_SETTINGS.update({'checks_in': st.slider("Checks:", value=70, step=5, key="checks_in")})
            SCENARIO_SETTINGS.update({'cc_in': st.slider("Cards:", value=15, step=5, key="cc_in")})
            SCENARIO_SETTINGS.update({'cash_in': st.slider("Cash:", value=5, step=5, max_value= 25, key="cash_in")})
            SCENARIO_SETTINGS.update({'wires_in': st.slider("Wires:", value=0, step=1, max_value=10, key="wires_in")})

            inc_checksum = SCENARIO_SETTINGS.get('ach_in') + SCENARIO_SETTINGS.get('checks_in') + SCENARIO_SETTINGS.get('cc_in') + SCENARIO_SETTINGS.get('cash_in') + SCENARIO_SETTINGS.get('wires_in')
            st.write("##### checksum:", inc_checksum)

        # Outgoing transactions assumptions
        with st.expander("Outgoing Transactions"):
            SCENARIO_SETTINGS.update({'out_trans_cnt': st.slider("Count:", min_value=10, max_value= 200, value=100, step=10, key="out_trans_cnt")})
            SCENARIO_SETTINGS.update({'out_trans_amt': st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="out_trans_amt")})
            st.write("##### Implied Avg. Transaction Size:", SCENARIO_SETTINGS.get('out_trans_amt')/SCENARIO_SETTINGS.get('out_trans_cnt'))
            
            st.write("### Breakdown by Type (%):")
            SCENARIO_SETTINGS.update({'ach_out': st.slider("ACH:", value=15, step=5, key="ach_out")})
            SCENARIO_SETTINGS.update({'checks_out': st.slider("Checks:", value=70, step=5, key="checks_out")})
            SCENARIO_SETTINGS.update({'cc_out': st.slider("Cards:", value=10, step=5, key="cc_out")})
            SCENARIO_SETTINGS.update({'cash_out': st.slider("Cash:", value=0, step=1, max_value=5, key="cash_out")})
            SCENARIO_SETTINGS.update({'bill_pay_out': st.slider("Bill Pay:", value=4, step=1, max_value=10, key="cash_out")})
            SCENARIO_SETTINGS.update({'wires_out': st.slider("Wires:", value=1, step=1, max_value=10, key="wires_out")})

            out_checksum = SCENARIO_SETTINGS.get('ach_out') + SCENARIO_SETTINGS.get('checks_out') + \
                           SCENARIO_SETTINGS.get('cc_out') + SCENARIO_SETTINGS.get('cash_out') + \
                           SCENARIO_SETTINGS.get('wires_out') + SCENARIO_SETTINGS.get('bill_pay_out')
            st.write("##### checksum:", out_checksum)

        st.markdown("### Revenue Settings")
        with st.expander("Interchange"):
            SCENARIO_SETTINGS.update({'net_ic': st.slider("Net Interchange:", min_value=1.0, max_value=3.0, value=2.0, step=0.1, key="net_ic")})
        
        with st.expander("Interest on Deposits"):
            SCENARIO_SETTINGS.update({'yield_curve_flag': st.checkbox("Use current yield curve?")})
            if not SCENARIO_SETTINGS.get('yield_curve_flag'):
                fed_rate = st.number_input("Flat Fed Rate (bps):", value=50, min_value=0, max_value=200, step=25, key="fed_rate")
        
        st.markdown("### Other Settings")
        with st.expander("Chart Settings"):
            SCENARIO_SETTINGS.update({'annualize_flag': st.checkbox("Annualize monthly values?")})
            SCENARIO_SETTINGS.update({'chart_freq': st.selectbox("Plot Frequency:", options=['Monthly', 'Quarterly'])})
            SCENARIO_SETTINGS.update({'vendor_exc': st.multiselect("Vendor Exclusions:", options=['Stripe','Unit','Treasury Prime','Column'])})

    # Data Computation
    migration_plan = pd.read_csv('migration_assumptions.csv', index_col=0, parse_dates=[0])

    # Resample if needed - if quarterly
    if SCENARIO_SETTINGS.get('chart_freq') == 'Quarterly':
        migration_plan = migration_plan.resample('Q').agg({'monthly_under_loi': 'sum', 
                                                           'total_under_loi': 'last',
                                                           'onboarding': 'sum',
                                                           'total_onboarded': 'last'})
    # st.dataframe(migration_plan)

    # Key Data
    key_data = data_fns.generate_key_data(migration_plan, SCENARIO_SETTINGS)
    # st.dataframe(key_data)

    # platform_rev

    # platform_costs

    # platform_pnl

    # Digital transformation scenario
    
    # Main body
    # 1. Description and intro
    with st.container():
        st.markdown("### Description")
        st.write("This is some text to explain what this is.")

    # 2. Platform growth
    with st.container():
        st.markdown("### Company Onboard & Platform Growth")

        # Plot onboarding growth
        st.plotly_chart(plt.plot_platform_growth(migration_plan, freq=SCENARIO_SETTINGS.get('chart_freq')), use_container_width=True)
        
        # Plot deposits growth
        st.plotly_chart(plt.plot_deposits_growth(key_data), use_container_width=True)

        # Plot Outgoing transactions growth
        st.plotly_chart(plt.plot_outgoing_trans_mix(key_data, freq=SCENARIO_SETTINGS.get('chart_freq')),  use_container_width=True)

        
        
        st.write("Have some text here about the assumed migration speed.")
        
        st.markdown("<small>* Assumed 75 companies under LOI by end of Q3.</small>", unsafe_allow_html=True)
        
        
    
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