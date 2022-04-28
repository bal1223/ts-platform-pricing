import datetime as dt
import pandas as pd
import numpy as np
import streamlit as st

# monthly_under_loi	total_under_loi	onboarding	total_onboarded
def generate_key_data(mp, scenario_settings):
    """
        Function to take a migration growth plan and scenario settings to 
        create a dataframe of assumed growth in accounts, deposits, spend volume, etc.
        to be used in plots and dynamic text.
    """
    # if scenario_settings.get('x_axis') == 'By Date':
    key_data = pd.DataFrame(index=mp.index)

    #Add number of companies
    key_data["No. of Companies"] = mp.total_onboarded
    
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

    if scenario_settings.get('x_axis') == "By Number of Companies":
        key_data.set_index("No. of Companies", inplace=True)

    return key_data


def generate_rev_data(kd, scenario_settings, pricing_settings, vendors):
    """Function to generate the dataframe of revenue values by vendor to be plotted"""
    rev_data = pd.DataFrame(index=kd.index)

    for k, v in pricing_settings.items():
        # Skip if not selected to evaluate
        if k in vendors:
            # Interest on Deposits
            rev_data[f"{k}_int_on_dep_rev"] = rev_interest_on_deposits(kd.Deposits, scenario_settings.get("fed_rate"), v['revenue']['partner_bank'])

            # Interchange Revenue
            rev_data[f"{k}_ic_rev"] = rev_interchange(kd["Card Spend"], scenario_settings.get("net_ic"), v['revenue']['interchange'])

    if scenario_settings.get('annualize_flag'):
        rev_data = annualize(rev_data, scenario_settings.get('chart_freq'))
        
    return rev_data

def annualize(df, freq):
    """helper function to annualize the data"""
    if freq == 'Monthly':
        df *= 12

    if freq == 'Quarterly':
        df *= 4
    
    return df
    
def rev_interchange(card_spend, net_ic, vendor_settings):
    """Computes a series of interchange revenue values based on assumed card spend, net interchange on that spend, and vendor price settings
        Returns a list of values.
    """
    ic_rev = []
    for spend in card_spend:
        tmp_total = 0
        # Loop through the tiers
        for tier in vendor_settings:
            tmp_low = tier.get("low_threshold")
            tmp_high = tier.get("high_threshold")

            # Compute the amount of rev share considered for the tier
            if not tmp_high:
                tier_share = max(spend - tmp_low, 0) * tier.get("value")
            else:
                tier_share = max(min(spend - tmp_low, tmp_high - tmp_low), 0) * tier.get("value")

            # If it is variable, multiply times net_ic assumption
            if tier.get("type") == "variable":
                tier_share *= (net_ic / 100.)

            # Add the tier share to the total for that period's card spend
            tmp_total += tier_share

        # Add the total rev share for the period to the list
        ic_rev.append(tmp_total)
    return ic_rev


def rev_interest_on_deposits(deposits_series, effr, vendor_partner_bank):
    """Takes a series of deposit balances, an effective fed rate (single value OR array), and vendor partner bank name
        Returns a series of values of length deposit rates that is the revenue earned from interest on deposits.
        It depends on the vendor, and in turn which bank they are using.
    """
    if isinstance(effr, float):
        effr = [effr] * len(deposits_series)

    interest_rev = []
    for d, r in zip(deposits_series, effr):

        tmp_int = 0.
        # Communicated to be roughly half of the Fed Rate, but Stripe was non-commital. Going to assume a slight haircut, so 40% of the target Fed Rate.
        if vendor_partner_bank == 'Evolve B&T':
            tmp_int = d * 0.4 * r/100.
            
        # Piermont is 50% of the midpoint of the fed target range (if above 2mm). This is assumed to be high: Fed Rate; low: Fed Rate less 25bps.
        # This is what the range has historically been and is equal to r - 0.125)
        if vendor_partner_bank == 'Piermont' and d > 2000000:
            tmp_int = d * 0.5 * (r-0.125)/100.
        
        # Blue Ridge logic is deposits times Fed Rate less 20bps
        if vendor_partner_bank == 'Blue Ridge':
            tmp_int = d * (r-0.20)/100.

        interest_rev.append(tmp_int)
    
    return interest_rev
