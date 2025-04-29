import streamlit as st
import pandas as pd
from utils import data, metrics
from utils.plots import create_peer_comparison_chart, create_metric_gauge

# Page configuration
st.set_page_config(
    page_title="BankStax 2.0",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🏦 BankStax 2.0")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        df = data.load_financial_data("Line items latest (1).xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

df = load_data()

if df is not None:
    # Sidebar for bank selection
    st.sidebar.header("Bank Selection")
    selected_bank = st.sidebar.selectbox(
        "Choose a bank",
        data.get_bank_list(df)
    )

    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "Key Financials", 
        "Key Metrics", 
        "CCAR Stress Test Analysis"
    ])

    # Tab 1: Key Financials
    with tab1:
        st.header("Key Financials")
        
        # Financial metrics dropdown
        financial_metrics = [
            'PAT', 'Total Liabilities', 'Cash',
            'Total Assets', 'Current Assets', 'Current Liabilities',
            'Accounts Receivables', 'Marketable Securities', 'Core Deposits',
            'Total Deposits', 'Loans', 'Non Performing Assets',
            'Tier 1 Capital', 'Tier 2 Capital', 'Risk Weighted Assets'
        ]
        
        selected_financial_metric = st.selectbox(
            "Select Financial Metric",
            financial_metrics,
            key="financial_metric_dropdown"
        )
        
        fig = create_peer_comparison_chart(
            df, selected_bank, selected_financial_metric,
            f"{selected_financial_metric} - Peer Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Key Metrics
    with tab2:
        st.header("Key Metrics")
        
        # Calculate metrics for selected bank
        bank_metrics = metrics.calculate_key_metrics(df, selected_bank)
        
        # Mock market benchmarks
        market_benchmarks = {
            'core_deposits_ratio': 85.0,
            'npa_ratio': 2.0,
            'liquidity_ratio': 25.0,
            'capital_adequacy_ratio': 12.0,
            'solvency_ratio': 20.0,
            'loan_deposit_ratio': 80.0
        }
        
        # Create 2x3 grid for metrics
        metric_titles = {
            'core_deposits_ratio': 'Core Deposits/Total Deposits',
            'npa_ratio': 'NPAs/Total Loans',
            'liquidity_ratio': 'Liquidity Ratio',
            'capital_adequacy_ratio': 'Capital Adequacy Ratio',
            'solvency_ratio': 'Solvency Ratio',
            'loan_deposit_ratio': 'Loan-Deposit Ratio'
        }
        
        # Display metrics in a grid
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_metric_gauge(
                bank_metrics['core_deposits_ratio'],
                metric_titles['core_deposits_ratio'],
                market_benchmarks['core_deposits_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig = create_metric_gauge(
                bank_metrics['liquidity_ratio'],
                metric_titles['liquidity_ratio'],
                market_benchmarks['liquidity_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig = create_metric_gauge(
                bank_metrics['solvency_ratio'],
                metric_titles['solvency_ratio'],
                market_benchmarks['solvency_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_metric_gauge(
                bank_metrics['npa_ratio'],
                metric_titles['npa_ratio'],
                market_benchmarks['npa_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig = create_metric_gauge(
                bank_metrics['capital_adequacy_ratio'],
                metric_titles['capital_adequacy_ratio'],
                market_benchmarks['capital_adequacy_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig = create_metric_gauge(
                bank_metrics['loan_deposit_ratio'],
                metric_titles['loan_deposit_ratio'],
                market_benchmarks['loan_deposit_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

        # Metrics explanation expander
        with st.expander("Metrics Explanation"):
            st.markdown("""
            - **Core Deposits Ratio**: Measures the stability of funding sources
            - **NPA Ratio**: Indicates asset quality and credit risk
            - **Liquidity Ratio**: Measures ability to meet short-term obligations
            - **Capital Adequacy Ratio**: Shows bank's capital strength
            - **Solvency Ratio**: Indicates long-term financial stability
            - **Loan-Deposit Ratio**: Shows efficiency in converting deposits to loans
            """)
        
        st.markdown("---")
        st.header("📊 Peer-to-Peer Comparison for Key Metrics")

        # Define key metrics list BEFORE selectbox
        key_metrics_list = [
            'Core Deposits/Total Deposits',
            'NPAs/Total Loans',
            'Liquidity Ratio',
            'Capital Adequacy Ratio',
            'Solvency Ratio',
            'Loan-Deposit Ratio'
        ]

        selected_key_metric = st.selectbox(
            "Select Key Metric for Peer Comparison",
            key_metrics_list,
            key="peer_key_metric_dropdown"
        )

        metric_mapping = {
            'Core Deposits/Total Deposits': 'core_deposits_ratio',
            'NPAs/Total Loans': 'npa_ratio',
            'Liquidity Ratio': 'liquidity_ratio',
            'Capital Adequacy Ratio': 'capital_adequacy_ratio',
            'Solvency Ratio': 'solvency_ratio',
            'Loan-Deposit Ratio': 'loan_deposit_ratio'
        }

        # Create peer comparison DataFrame
        peer_df = pd.DataFrame({
            'Bank Name': df['Company'],
            'Metric Value': df.apply(lambda row: metrics.calculate_key_metrics(df, row['Company'])[metric_mapping[selected_key_metric]], axis=1)
        })

        # Use Streamlit native bar chart
        peer_df = peer_df.set_index('Bank Name')
        st.bar_chart(peer_df)

    with tab3:
        st.header("CCAR Stress Test Analysis")
    
        # Calculate stress test metrics
        stress_metrics = metrics.calculate_stress_test_metrics(
        df[df['Company'] == selected_bank].iloc[0]
        )
    
        # Mock market benchmarks for stress tests
        stress_benchmarks = {
        'cet1_ratio': 4.5,
        'tier1_capital_ratio': 6,
        'total_capital_ratio': 8,
        'leverage_ratio': 4.0,
        'supplementary_tier1_ratio': 3   # 
        }
    
        # Create 2x3 grid (instead of 2x2) for 5 metrics
        col1, col2 = st.columns(2)

        with col1:
            fig = create_metric_gauge(
            stress_metrics['cet1_ratio'],
            'CET1 Ratio',
            stress_benchmarks['cet1_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = create_metric_gauge(
            stress_metrics['total_capital_ratio'],
            'Total Capital Ratio',
            stress_benchmarks['total_capital_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = create_metric_gauge(
            stress_metrics['supplementary_tier1_ratio'],
            'Supplementary Tier 1 Ratio',
            stress_benchmarks['supplementary_tier1_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = create_metric_gauge(
            stress_metrics['tier1_capital_ratio'],
            'Tier 1 Capital Ratio',
            stress_benchmarks['tier1_capital_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = create_metric_gauge(
            stress_metrics['leverage_ratio'],
            'Leverage Ratio',
            stress_benchmarks['leverage_ratio']
            )
            st.plotly_chart(fig, use_container_width=True)

            # Stress test explanation expander
        with st.expander("Stress Test Metrics Explanation"):
             st.markdown("""
             - **CET1 Ratio**: Core measure of bank's financial strength
             - **Tier 1 Capital Ratio**: Measures bank's core equity capital
             - **Total Capital Ratio**: Overall capital adequacy measure
             - **Leverage Ratio**: Indicates bank's ability to meet financial obligations
             - **Supplementary Tier 1 Ratio**: Additional Tier 1 capital strength beyond core CET1
            """)
