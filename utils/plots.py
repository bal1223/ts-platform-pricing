import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

BASIC_LAYOUT = go.Layout(
    autosize=True,
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