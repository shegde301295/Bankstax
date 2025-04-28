import plotly.graph_objects as go

def create_peer_comparison_chart(df, bank_name, metric, title):
    """
    Create a bar chart comparing a bank's metric with peer average
    """
    bank_value = df[df['Company'] == bank_name][metric].values[0]
    peer_avg = df[df['Company'] != bank_name][metric].mean()
    
    fig = go.Figure()
    
    # Add bar for selected bank
    fig.add_trace(go.Bar(
        x=['Selected Bank'],
        y=[bank_value],
        name=bank_name,
        marker_color='#1f77b4'
    ))
    
    # Add bar for peer average
    fig.add_trace(go.Bar(
        x=['Peer Average'],
        y=[peer_avg],
        name='Peer Average',
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title=metric,
        showlegend=True,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_metric_gauge(value, title, benchmark):
    """
    Create a single gauge chart for a metric
    """
    if value is None:
        value = 0
    
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, max(value, benchmark) * 1.2]},
            'threshold': {
                'line': {'color': 'red', 'width': 2},
                'thickness': 0.75,
                'value': benchmark
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=50, b=30),
        template='plotly_white'
    )
    
    return fig
