import datetime as dt
import pandas as pd
import numpy as np

# monthly_under_loi	total_under_loi	onboarding	total_onboarded
def generate_key_data(mp, scenario_settings):
    """
        Function to take a migration growth plan and scenario settings to 
        create a dataframe of assumed growth in accounts, deposits, spend volume, etc.
        to be used in plots and dynamic text.
    """
    key_data = pd.DataFrame(index=mp.index)
    # Accounts
    key_data['New Accounts'] = mp.onboarding * scenario_settings.get('acct_cnt')
    key_data['Total Accounts'] = mp.total_onboarded * scenario_settings.get('acct_cnt')
    
    # Transaction Out
    key_data['Card Spend'] = mp.total_onboarded * scenario_settings.get('cc_out')/100. * scenario_settings.get('out_trans_amt')
    key_data['Deposits'] = mp.total_onboarded * scenario_settings.get('avg_deposits_balance')
    key_data['Checks Issued'] = mp.total_onboarded * scenario_settings.get('checks_out')/100. * scenario_settings.get('out_trans_amt')
    key_data['ACH Out'] = mp.total_onboarded * scenario_settings.get('ach_out')/100. * scenario_settings.get('out_trans_amt')
    key_data['Wire Out'] = mp.total_onboarded * scenario_settings.get('wires_out')/100. * scenario_settings.get('out_trans_amt')
    key_data['Bill Pay'] = mp.total_onboarded * scenario_settings.get('bill_pay_out')/100. * scenario_settings.get('out_trans_amt')
    key_data['Cash Out'] = mp.total_onboarded * scenario_settings.get('cash_out')/100. * scenario_settings.get('out_trans_amt')
    
    # Cards
    key_data['Physical Cards Issued'] = mp.onboarding * scenario_settings.get('phy_card_cnt')
    key_data['Virtual Cards Issued'] = mp.onboarding * scenario_settings.get('virt_card_cnt')

    return key_data