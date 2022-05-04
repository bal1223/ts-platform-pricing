import streamlit as st
import datetime as dt
import pandas as pd
import json
import toml
import utils.plots as plt
import utils.data_fns as data_fns
from PIL import Image

# st.markdown('<small>test</small>', unsafe_allow_html=True)
SCENARIO_SETTINGS = {}

# Load pricing parameters
with open('pricing_parameters.json') as f:
    PRICING = json.load(f)
    f.close()

# Load config toml and set as dict
readme = dict(toml.load("utils/config_readme.toml"))

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
            SCENARIO_SETTINGS.update({'avg_deposits_balance': st.slider("Deposits Balance:", min_value = 100000, max_value = 500000, value=300000, step=25000, help=readme['tooltips']['avg_deposits'])})
            SCENARIO_SETTINGS.update({'acct_cnt': st.number_input("Accounts", value=2, step=1, help=readme['tooltips']['acct_cnt'])})            

            # Maybe make this fixed?
            SCENARIO_SETTINGS.update({'phy_card_cnt': st.number_input("Physical Cards Issued", value=3, step=1, help=readme['tooltips']['phy_card_cnt'])})
            SCENARIO_SETTINGS.update({'virt_card_cnt': st.number_input("Virtual Cards Issued", value=5, step=1, help=readme['tooltips']['virt_card_cnt'])})
        
        # Inc transaction assumptions
        with st.expander("Incoming Transactions"):
            SCENARIO_SETTINGS.update({'inc_trans_cnt': st.slider("Count:", min_value=10, max_value= 200, value=50, step=10, key="inc_trans_cnt", help=readme['tooltips']['inc_trans_cnt'])})
            SCENARIO_SETTINGS.update({'inc_trans_amt': st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="inc_trans_amt", help=readme['tooltips']['inc_trans_amt'])})
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
            SCENARIO_SETTINGS.update({'out_trans_cnt': st.slider("Count:", min_value=10, max_value= 200, value=100, step=10, key="out_trans_cnt", help=readme['tooltips']['out_trans_cnt'])})
            SCENARIO_SETTINGS.update({'out_trans_amt': st.slider("Total Dollar Volume:", min_value = 50000, max_value=250000, value=100000, step=10000, key="out_trans_amt", help=readme['tooltips']['out_trans_amt'])})
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
            SCENARIO_SETTINGS.update({'net_ic': st.slider("Net Interchange (%):", min_value=1.0, max_value=3.0, value=2.0, step=0.1, key="net_ic", help=readme['tooltips']['net_ic'])})
        
        with st.expander("Interest on Deposits"):
            SCENARIO_SETTINGS.update({'yield_curve_flag': st.checkbox("Use yield curve?", help=readme['tooltips']['yield_curve_flag'])})
            if SCENARIO_SETTINGS.get('yield_curve_flag'): # If yield curve selected, use the values from the csv
                fed_rates = pd.read_csv('fed_rate.csv', index_col=0, parse_dates=[0])
                SCENARIO_SETTINGS.update({'fed_rate': fed_rates.effr.values})
            else:
                SCENARIO_SETTINGS.update({'fed_rate': st.slider("Flat Fed Rate (%):", value=1.00, min_value=0.0, max_value=2.50, step=0.25, key="fed_rate", help=readme['tooltips']['fed_rate'])})
        
        st.markdown("### Other Settings")
        with st.expander("Chart Settings"):
            SCENARIO_SETTINGS.update({'x_axis': st.selectbox("X-axis:", options=["By Date", "By Number of Companies"], index=0, help=readme['tooltips']['x_axis'])})
            SCENARIO_SETTINGS.update({'annualize_flag': st.checkbox("Annualize values?", help=readme['tooltips']['annualize_flag'])})
            SCENARIO_SETTINGS.update({'chart_freq': st.selectbox("Plot Frequency:", options=['Monthly', 'Quarterly'], help=readme['tooltips']['chart_freq'])})
            SCENARIO_SETTINGS.update({'vendor_exc': st.multiselect("Vendor Exclusions:", options=['stripe','unit','treasury_prime'], help=readme['tooltips']['vendor_exc'])})

    ## DATA COMPUATION
    # Load in migration plan and fed rate
    migration_plan = pd.read_csv('migration_assumptions.csv', index_col=0, parse_dates=[0])

    # Get list of vendors for this run
    VENDORS = list(set(PRICING.keys()) - set(SCENARIO_SETTINGS.get('vendor_exc')))

    # Resample data if needed - if quarterly
    if SCENARIO_SETTINGS.get('chart_freq') == 'Quarterly':
        migration_plan = migration_plan.resample('Q').agg({'monthly_under_loi': 'sum', 
                                                           'total_under_loi': 'last',
                                                           'onboarding': 'sum',
                                                           'total_onboarded': 'last'})

    # Key Data
    key_data = data_fns.generate_key_data(migration_plan, SCENARIO_SETTINGS)
    # st.write(key_data["New Accounts"].values[0])

    # platform_rev
    rev_data = data_fns.generate_rev_data(key_data, SCENARIO_SETTINGS, PRICING, VENDORS)

    # platform_costs
    cost_data = data_fns.generate_cost_data(key_data, SCENARIO_SETTINGS, PRICING, VENDORS)
    
    # Main body
    st.title("Platform Economics Comparison")
    # 1. Description and intro
    with st.container():
        with st.expander("About this app"):
            st.markdown(readme['app']['app_description'])

    # 2. Platform growth
    with st.container():
        st.markdown("## Company Onboarding & Platform Growth")
        st.markdown(readme['onboarding']['intro'])

        # Plot onboarding growth
        st.plotly_chart(plt.plot_platform_growth(migration_plan, freq=SCENARIO_SETTINGS.get('chart_freq')), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # Plot deposits growth
            # st.metric("Deposts @ 100", value="${:,.0f}".format(SCENARIO_SETTINGS.get('avg_deposits_balance')*100))
            st.plotly_chart(plt.plot_deposits_growth(key_data), use_container_width=True)

        with col2:
            # Plot Outgoing transactions growth
            st.plotly_chart(plt.plot_outgoing_trans_mix(key_data, freq=SCENARIO_SETTINGS.get('chart_freq')),  use_container_width=True)

        # commentary
        avg_fmt = SCENARIO_SETTINGS.get('avg_deposits_balance')
        avg_mm = SCENARIO_SETTINGS.get('avg_deposits_balance')/1000000
        st.write(readme['onboarding']['comments'] % (avg_fmt, avg_mm*100, avg_mm*250))
    
    # Base Case Results
    st.markdown("---")
    # 3. P/L
    with st.container():
        st.markdown("### Net Income")
        st.write(readme['net_income']['intro'])

        st.plotly_chart(plt.plot_pnl_comparison(rev_data, cost_data, VENDORS, freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                    annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

        st.write(readme['net_income']['by_vendor'])

        # Expander for costs by vendor
        st.markdown('##### By Vendor')
        for v in VENDORS:
            with st.expander(v.title()):
                st.plotly_chart(plt.plot_vendor_pnl(rev_data, cost_data, v, freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                    annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

    # 4. Revenue
    st.markdown("---")
    with st.container():
        st.markdown("### Revenue")
        st.write(readme['revenue']['intro'])

        # Total revenue
        st.plotly_chart(plt.plot_revenue_comparison(rev_data, 
                                                    key_data,
                                                    VENDORS, 
                                                    freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                    annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

        # 1 x 2 - one for deposits, one for interchange
        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(plt.plot_revenue_comparison(rev_data,
                                                            key_data, 
                                                            VENDORS, 
                                                            freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                            annualize_flag=SCENARIO_SETTINGS.get('annualize_flag'),
                                                            type = "Interchange"), use_container_width=True)

            with col2:
                st.plotly_chart(plt.plot_revenue_comparison(rev_data, 
                                                            key_data,
                                                            VENDORS, 
                                                            freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                            annualize_flag=SCENARIO_SETTINGS.get('annualize_flag'),
                                                            type = "Interest"), use_container_width=True)
                
        st.write(readme['revenue']['comments'])
        
        # Effective interchange share and comparison by thresholds
        # st.plotly_chart(plt.plot_interchange_comparison(rev_data, key_data["Card Spend"], VENDORS, SCENARIO_SETTINGS.get('net_ic'), PRICING), use_container_width=True)

        # Columns to have commentary on vendor revenue
        with st.expander("Key Revenue Drivers by Vendor"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("##### Unit")
                st.markdown('###### Interchange')
                st.write(readme['revenue']['unit_ic'])
                st.markdown('###### Interest')
                st.write(readme['revenue']['unit_int'])

            with col2:
                st.markdown("##### Stripe")
                st.markdown('###### Interchange')
                st.write(readme['revenue']['stripe_ic'])
                st.markdown('###### Interest')
                st.write(readme['revenue']['stripe_int'])

            with col3:
                st.markdown("##### Treasury Prime")
                st.markdown('###### Interchange')
                st.write(readme['revenue']['tp_ic'])
                st.markdown('###### Interest')               
                st.write(readme['revenue']['tp_int'])

        # st.markdown('##### By Vendor')
        # for v in VENDORS:
        #     with st.container():
        #         col1, col2 = st.columns([4, 1])
        #         with col1:
        #             st.plotly_chart(plt.plot_vendor_revenue_growth(rev_data, v, freq=SCENARIO_SETTINGS.get('chart_freq'), annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

        #         with col2:
        #             st.write("this is some text on the side") # look up read me by vendor name

            # TP only has debit card program, so this assumes debit spend only

    st.markdown("---")
    # 5. Costs
    with st.container():
        st.markdown("### Costs")
        st.write(readme['costs']['intro'])

        # Total costs by vendor
        st.plotly_chart(plt.plot_cost_comparison(cost_data, 
                                                 VENDORS, 
                                                 freq=SCENARIO_SETTINGS.get('chart_freq'), 
                                                 annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

        st.write(readme['costs']['comments'])


        # Expander for costs by vendor
        st.markdown('##### By Vendor')
        for v in VENDORS:
            with st.expander(v.title()):
                st.plotly_chart(plt.plot_vendor_costs_by_category(cost_data, v, freq=SCENARIO_SETTINGS.get('chart_freq'), annualize_flag=SCENARIO_SETTINGS.get('annualize_flag')), use_container_width=True)

        # Payments (Stripe)

        # Columns to have commentary on vendor revenue
        with st.expander("Key Cost Drivers by Vendor"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("##### Unit")
                st.write(readme['costs']['unit_costs'])

            with col2:
                st.markdown("##### Stripe")
                st.write(readme['costs']['stripe_costs'])

            with col3:
                st.markdown("##### Treasury Prime")
                st.write(readme['costs']['tp_costs'])

    # 6. Scenario Variation: Digital Transition
    # st.markdown("---")
    # with st.container():
    #     st.markdown("### Scenario Variation: Network Digital Transition")

    # 7. Data Tables
    st.markdown("---")
    st.markdown("### Data")
    st.write("Expand to view the raw data.")
    with st.expander("Onboarding Plan"):
        st.dataframe(migration_plan)

    with st.expander("Transactions Growth"):
        st.dataframe(key_data)

    with st.expander("Revenue Data"):
        st.dataframe(rev_data)

    with st.expander("Cost Data"):
        st.dataframe(cost_data)
        pass

if __name__ == '__main__':
    run_app()