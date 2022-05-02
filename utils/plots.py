import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio

BASIC_LAYOUT = go.Layout(
    # autosize=True,
    margin=go.layout.Margin(t=35),
    # hovermode='closest',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font=dict(size=14)
)
OPACITY=0.85

def plot_platform_growth(mp, freq):
    """Take the migration plan and scenario settings to plot
        - the number of companies onboarded in a given period
        - total number of companies onboarded
    """
    total_onboarded_trace = go.Scatter(
        x=mp.index,
        y=mp.total_onboarded,
        name="Total Onboarded",
        marker=dict(size=10),
        line=dict(width=2, dash='dot'), 
        yaxis='y2',
    )

    onboarding_trace = go.Bar(
        x=mp.index,
        y=mp.onboarding,
        name="Onboarding",
        opacity=OPACITY,
    )

    data = [onboarding_trace, total_onboarded_trace]
    fig = go.Figure(data=data, layout=BASIC_LAYOUT)
    fig.update_layout(
        yaxis1=dict(title=f"{freq} Onboarded"),
        yaxis2=dict(side='right', overlaying='y', showgrid=False, title="Total Companies"),
        title="Companies Onboarded Over Time",
        hovermode="x unified"
    )
    return fig

def plot_deposits_growth(kd):
    """Plot the total deposits over time given the assumptions"""
    total_deposits = go.Scatter(
        x=kd.index,
        y=kd["Deposits"],
        name="Total Deposits",
        marker=dict(size=10),
        line=dict(width=2), 
    )

    fig = go.Figure(data=[total_deposits], layout=BASIC_LAYOUT)
    fig.update_layout(
        yaxis=dict(title="$"),
        title="Total Deposits on Platform"
    )
    return fig

def plot_outgoing_trans_mix(kd, freq):
    """Area chart for the volume of outgoing payment mmix, based on the assumptions"""
    data = []
    for p in ["Card Spend", "Checks Issued", "ACH Out", "Wire Out", "Bill Pay", "Cash Out"]:
        tmp_trace = go.Scatter(
            x=kd.index,
            y=kd[p],
            name=p,
            stackgroup='one'
        )

        data.append(tmp_trace)

    fig=go.Figure(data=data, layout=BASIC_LAYOUT)
    fig.update_layout(
        yaxis=dict(title="$"),
        hovermode="x unified",
        title=f"{freq} Spend by Transaction Type"
    )
    return fig

def plot_vendor_revenue_growth(rd, vendor, freq, annualize_flag):
    """Area plot for specific vendor, showing revenue growth by type and number of companies
        Maybe include toggle for "by date" or "by number companies"
    """
    ic_trace = go.Scatter(
            x=rd.index,
            y=rd[f"{vendor}_ic_rev"],
            name="IC",
            stackgroup='one'
        )

    deposits_trace = go.Scatter(
            x=rd.index,
            y=rd[f"{vendor}_int_on_dep_rev"],
            name="Int.",
            stackgroup='one'
        )

    data = [ic_trace, deposits_trace]
    fig=go.Figure(data=data, layout=BASIC_LAYOUT)

    title = f"{vendor.title()} {freq} Revenue Breakdown"
    if annualize_flag:
        title += " (Annualized)"
    
    fig.update_layout(
        yaxis=dict(title="$"),
        hovermode="x unified",
        title=title
    )
    return fig

def plot_interchange_comparison(rd, card_spend, vendors, net_ic, pricing):
    """Comparison by tiers and effective interchange over time, but spend"""
    

    # Share of net interchange this could also be a table that is dynamic?

    # Interchange as % of
    # for v in vendors:
    #     fig.add_trace(go.Scatter(
    #         x=card_spend,
    #         y=rd[f"{v}_ic_rev"] / card_spend * 100.,
    #         name=v,
    #         marker=dict(size=10),
    #         line=dict(width=2, dash='dot'), 
    #         ), row=1, col=2
    #     )

    return fig

def plot_revenue_comparison(rd, kd, vendors, freq, annualize_flag, type="Total"):
    """Total revenue on platforms"""
    data = []
    # fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2])
    for v in vendors:
        if type == "Total":
            tmp_y = rd[f"{v}_total"]
        if type == "Interchange":
            tmp_y = rd[f"{v}_ic_rev"]
        if type == "Interest":
            tmp_y = rd[f"{v}_int_on_dep_rev"]

        tmp_trace = go.Scatter(
            x=rd.index,
            y=tmp_y,
            name=v,
            marker=dict(size=10),
            line=dict(width=2), 
        )
        data.append(tmp_trace)

        # fig.add_trace(
        #     go.Scatter(
        #          x=rd.index,
        #          y=tmp_y,
        #          name=v,
        #          marker=dict(size=10),
        #          line=dict(width=2), 
        #     ), row=1, col=1
        # )

    fig = go.Figure(data=data, layout=BASIC_LAYOUT)

    title = f"{type} {freq} Revenue By Vendor"
    if annualize_flag:
        title += " (Annualized)"

    fig.update_layout(
        yaxis=dict(title="$"),
        title=title,
        hovermode="x unified"
    )
    return fig

def plot_cost_comparison(cd, vendors, freq, annualize_flag):
    """Total costs by vendor"""
    data = []
    for v in vendors:
        tmp_trace = go.Scatter(
            x=cd.index,
            y=cd[f"{v}_total"],
            name=v,
            marker=dict(size=10),
            line=dict(width=2), 
        )
        data.append(tmp_trace)

    fig = go.Figure(data=data, layout=BASIC_LAYOUT)

    title = f"Total {freq} Cost By Vendor"
    if annualize_flag:
        title += " (Annualized)"

    fig.update_layout(
        yaxis=dict(title="$"),
        title=title,
        hovermode="x unified"
    )
    return fig

def plot_vendor_costs_by_category(cd, vendor, freq, annualize_flag):
    """Plot an individual vendor cost breakdown"""
    data = []
    cols = [c for c in cd.columns if vendor in c and 'total' not in c]
    for c in cols:
        tmp_trace = go.Scatter(
            x=cd.index,
            y=cd[c],
            name=c.replace(vendor, "").replace("_", " ").title(),
            stackgroup='one'
        )
        data.append(tmp_trace)

    fig=go.Figure(data=data, layout=BASIC_LAYOUT)

    title = f"{vendor.title()} {freq} Cost Breakdown"
    if annualize_flag:
        title += " (Annualized)"
    
    fig.update_layout(
        yaxis=dict(title="$"),
        hovermode="x unified",
        title=title
    )
    return fig

def plot_pnl_comparison(rd, cd, vendors, freq, annualize_flag):
    """Net cost/profit for each vendor"""
    data = []
    for v in vendors:
        tmp_trace = go.Scatter(
            x=rd.index,
            y=rd[f"{v}_total"] - cd[f"{v}_total"] ,
            name=v,
            marker=dict(size=10),
            line=dict(width=2), 
        )
        data.append(tmp_trace)

    fig = go.Figure(data=data, layout=BASIC_LAYOUT)

    title = f"Total {freq} Net Income By Vendor"
    if annualize_flag:
        title += " (Annualized)"

    fig.update_layout(
        yaxis=dict(title="$"),
        title=title,
        hovermode="x unified"
    )
    return fig

def plot_vendor_pnl(rd, cd, vendor, freq, annualize_flag):
    """Stacked bar chart for costs and revenue and total"""
    data = []
    # add revenue traces
    rev_cols = [c for c in rd.columns if vendor in c and 'total' not in c]
    for c in rev_cols:
        tmp_trace = go.Bar(
            x=rd.index,
            y=rd[c],
            name=c.replace(vendor, "").replace("_", " ").title()
        )
        data.append(tmp_trace)

    # add cost traces
    cost_cols = [c for c in cd.columns if vendor in c and 'total' not in c]
    for c in cost_cols:
        tmp_trace = go.Bar(
            x=rd.index,
            y=cd[c] * -1.,
            name=c.replace(vendor, "").replace("_", " ").title()
        )
        data.append(tmp_trace)

    total_trace = go.Scatter(
            x=rd.index,
            y=rd[f"{vendor}_total"] - cd[f"{vendor}_total"] ,
            name='Net',
            marker=dict(size=10),
            line=dict(width=4), 
        )

    data.append(total_trace)

    fig = go.Figure(data=data, layout=BASIC_LAYOUT)
    fig.update_layout(barmode = 'relative')

    title = f"Total {freq} Net Income By Vendor"
    if annualize_flag:
        title += " (Annualized)"

    fig.update_layout(
        yaxis=dict(title="$"),
        title=title,
        hovermode="x unified"
    )
    return fig
