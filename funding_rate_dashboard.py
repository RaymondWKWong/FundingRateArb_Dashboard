import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Crypto Funding Rate Arbitrage Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #0a0a0a !important;
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }
    
    .main > div {
        background: #0a0a0a !important;
        padding: 0 !important;
    }
    
    .block-container {
        background: #0a0a0a !important;
        padding: 1rem 1rem 0rem 1rem !important;
        max-width: 100% !important;
    }
    
    /* Fix white bar at top */
    .stApp > header {
        background: #0a0a0a !important;
        height: 0px !important;
    }
    
    /* Fix sidebar styling */
    .css-1d391kg, .css-1lcbmhc, .css-1cypcdb, .css-17eq0hr {
        background: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] {
        background: #0a0a0a !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: #0a0a0a !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Fix slider styling */
    .stSlider {
        background: #0a0a0a !important;
    }
    
    .stSlider > div {
        background: #0a0a0a !important;
    }
    
    .stSlider label {
        color: #ffffff !important;
    }
    
    .stSlider [data-testid="stSlider"] {
        background: #1a1a2e !important;
    }
    
    /* Fix number input styling */
    .stNumberInput label {
        color: #ffffff !important;
    }
    
    .stNumberInput input {
        background: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #3a3a52 !important;
    }
    
    /* Make number input text white */
    .stNumberInput input::placeholder {
        color: #ffffff !important;
    }
    
    .stNumberInput div[data-baseweb="input"] {
        background: #1a1a2e !important;
        color: #ffffff !important;
    }
    
    .stNumberInput div[data-baseweb="input"] input {
        color: #ffffff !important;
    }
    
    /* Fix number input buttons */
    .stNumberInput button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: 1px solid #3a3a52 !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stNumberInput button:active {
        transform: translateY(0px) !important;
    }
    
    /* Fix number input container */
    .stNumberInput > div {
        background: #1a1a2e !important;
        border-radius: 8px !important;
        border: 1px solid #3a3a52 !important;
    }
    
    /* Fix selectbox styling */
    .stSelectbox label {
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div {
        background: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #3a3a52 !important;
    }
    
    /* Fix checkbox styling */
    .stCheckbox label {
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
    }
    
    /* Add glow to all headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Specific header styling */
    .stSubheader {
        color: #ffffff !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Section headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff !important;
        margin: 1.5rem 0 1rem 0;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%) !important;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #3a3a5a;
        color: #ffffff;
        text-align: center;
        margin: 0.3rem;
        box-shadow: 0 4px 20px rgba(74, 93, 215, 0.4);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .opportunity-card {
        background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%) !important;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #3a3a5a;
        color: #ffffff;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 6px 30px rgba(74, 93, 215, 0.5);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        height: 230px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Analysis section styling */
    .analysis-section {
        background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%) !important;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #3a3a5a;
        margin: 1rem 0;
        box-shadow: 0 6px 30px rgba(74, 93, 215, 0.5);
    }
    
    .analysis-section h2 {
        color: #ffffff !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
        margin-bottom: 1rem;
    }
    
    /* Summary card with same size as opportunity card */
    .summary-card {
        background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%) !important;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #3a3a5a;
        color: #ffffff;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 6px 30px rgba(74, 93, 215, 0.5);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        height: 230px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Tracker styling */
    .tracker-container {
        background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%) !important;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #3a3a5a;
        margin: 1rem 0;
        box-shadow: 0 6px 30px rgba(74, 93, 215, 0.5);
        min-height: 400px;
    }
    
    .tracker-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .tracker-title {
        color: #ffffff !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Override Streamlit metric styling */
    [data-testid="metric-container"] {
        background: transparent !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 20px rgba(74, 93, 215, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="metric-container"] > div {
        background: transparent !important;
    }
    
    /* Add glow to metric text */
    [data-testid="metric-container"] * {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Add glow to all text within purple boxes */
    .analysis-section * {
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
    }
    
    .opportunity-card * {
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
    }
    
    .exchange-matrix {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .exchange-pair {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #3a3a52;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .exchange-pair:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border-color: #667eea;
    }
    
    .exchange-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .rate-display {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
        font-family: 'Inter', monospace;
    }
    
    .rate-positive { color: #00ff88; }
    .rate-negative { color: #ff4757; }
    .rate-neutral { color: #feca57; }
    
    .opportunity-details {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #3a3a52;
    }
    
    .profit-amount {
        font-size: 1.3rem;
        font-weight: 700;
        color: #00ff88;
    }
    
    /* Exchange Table Styling */
    .exchange-table {
        display: flex;
        flex-direction: column;
        margin: 1rem 0;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #3a3a52;
    }
    
    .table-header {
        display: flex;
        background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
        padding: 0.8rem 0;
        border-bottom: 2px solid #3a3a52;
    }
    
    .header-cell {
        flex: 1;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 600;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0 0.5rem;
    }
    
    .table-row {
        display: flex;
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        padding: 1rem 0;
        border-bottom: 1px solid #3a3a52;
        transition: all 0.3s ease;
    }
    
    .table-row:hover {
        background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
        transform: translateX(2px);
    }
    
    .table-row:last-child {
        border-bottom: none;
    }
    
    .table-cell {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 0 0.5rem;
        text-align: center;
    }
    
    .ticker-cell {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 0.5rem;
    }
    
    .star-icon {
        font-size: 1.2rem;
        color: #feca57;
    }
    
    .ticker-info {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    
    .ticker-symbol {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    
    .position-type {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        text-transform: uppercase;
    }
    
    .long-position {
        background: rgba(0, 255, 136, 0.2);
        color: #00ff88;
    }
    
    .short-position {
        background: rgba(255, 71, 87, 0.2);
        color: #ff4757;
    }
    
    .rates-cell {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .funding-rate {
        font-size: 1rem;
        font-weight: 700;
        font-family: 'Inter', monospace;
        margin-bottom: 0.2rem;
    }
    
    .rate-comparison {
        font-size: 0.8rem;
        color: #888;
        font-family: 'Inter', monospace;
    }
    
    .countdown-cell {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
    }
    
    .countdown-number {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        font-family: 'Inter', monospace;
    }
    
    .countdown-time {
        font-size: 0.9rem;
        color: #feca57;
        font-family: 'Inter', monospace;
    }
    
    .profit-cell {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .profit-pct {
        font-size: 1rem;
        font-weight: 700;
        font-family: 'Inter', monospace;
    }
    
    .lifetime-cell {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
    }
    
    .lifetime-value {
        font-size: 1rem;
        font-weight: 700;
        color: #00ff88;
        font-family: 'Inter', monospace;
    }
    
    .lifetime-time {
        font-size: 0.7rem;
        color: #888;
    }
    
    .profit-positive {
        color: #00ff88;
    }
    
    .profit-negative {
        color: #ff4757;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .custom-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid #1a1a2e;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff !important;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Ensure all text is white */
    .stApp, .stApp * {
        color: #ffffff !important;
    }
    
    /* Specific fixes for metric values */
    [data-testid="metric-container"] * {
        color: #ffffff !important;
    }
    
    /* Fix subheader colors */
    .stSubheader {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header[data-testid="stHeader"] {display:none;}
    
    /* Remove toolbar and deploy button */
    .stActionButton {display:none;}
    div[data-testid="stDecoration"] {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    
    /* Force all containers to dark background */
    .stApp .main .block-container {
        background: #0a0a0a !important;
        padding-top: 1rem !important;
    }
    
    .stApp .main {
        background: #0a0a0a !important;
    }
    
    .stApp {
        background: #0a0a0a !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# EXCHANGE API FUNCTIONS (Optimized for dashboard)
# =============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_binance_funding(symbol, days=7):
    try:
        url = "https://fapi.binance.com/fapi/v1/fundingRate"
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = end_time - (days * 24 * 60 * 60 * 1000)
        
        params = {
            'symbol': f"{symbol}USDT",
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        df['funding_time'] = pd.to_datetime(df['fundingTime'], unit='ms')
        df['funding_rate'] = df['fundingRate'].astype(float)
        df['exchange'] = 'binance'
        df['symbol'] = symbol
        
        return df[['funding_time', 'funding_rate', 'exchange', 'symbol']]
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_bybit_funding(symbol, days=7):
    try:
        url = "https://api.bybit.com/v5/market/funding/history"
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = end_time - (days * 24 * 60 * 60 * 1000)
        
        params = {
            'category': 'linear',
            'symbol': f"{symbol}USDT",
            'startTime': start_time,
            'endTime': end_time,
            'limit': 200
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('retCode') != 0 or not data.get('result', {}).get('list'):
            return pd.DataFrame()
        
        records = []
        for item in data['result']['list']:
            records.append({
                'funding_time': pd.to_datetime(int(item['fundingRateTimestamp']), unit='ms'),
                'funding_rate': float(item['fundingRate']),
                'exchange': 'bybit',
                'symbol': symbol
            })
        
        return pd.DataFrame(records)
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_okx_funding(symbol, days=7):
    try:
        url = "https://www.okx.com/api/v5/public/funding-rate-history"
        
        params = {
            'instId': f"{symbol}-USDT-SWAP",
            'limit': 100
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') != '0' or not data.get('data'):
            return pd.DataFrame()
        
        records = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for item in data['data']:
            funding_time = pd.to_datetime(int(item['fundingTime']), unit='ms')
            if funding_time >= cutoff_date:
                records.append({
                    'funding_time': funding_time,
                    'funding_rate': float(item['fundingRate']),
                    'exchange': 'okx',
                    'symbol': symbol
                })
        
        return pd.DataFrame(records)
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_gate_funding(symbol, days=7):
    try:
        url = "https://api.gateio.ws/api/v4/futures/usdt/funding_rate"
        
        params = {
            'contract': f"{symbol}_USDT",
            'limit': 100
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        records = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for item in data:
            funding_time = pd.to_datetime(int(item['t']), unit='s')
            if funding_time >= cutoff_date:
                records.append({
                    'funding_time': funding_time,
                    'funding_rate': float(item['r']),
                    'exchange': 'gate',
                    'symbol': symbol
                })
        
        return pd.DataFrame(records)
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_kucoin_funding(symbol, days=7):
    try:
        contracts_url = "https://api-futures.kucoin.com/api/v1/contracts/active"
        contracts_response = requests.get(contracts_url, timeout=10)
        
        if contracts_response.status_code != 200:
            return pd.DataFrame()
        
        contracts_data = contracts_response.json()
        if contracts_data.get('code') != '200000':
            return pd.DataFrame()
        
        contracts = contracts_data.get('data', [])
        target_base = 'XBT' if symbol == 'BTC' else symbol
        btc_contract = None
        
        for contract in contracts:
            base_currency = contract.get('baseCurrency', '')
            quote_currency = contract.get('quoteCurrency', '')
            
            if (base_currency == target_base and 
                quote_currency == 'USDT' and 
                contract.get('status') == 'Open'):
                btc_contract = contract.get('symbol', '')
                break
        
        if not btc_contract:
            return pd.DataFrame()
        
        funding_url = f"https://api-futures.kucoin.com/api/v1/funding-rate/{btc_contract}/current"
        response = requests.get(funding_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') != '200000':
            return pd.DataFrame()
        
        funding_data = data.get('data', {})
        current_time = datetime.now()
        funding_rate = funding_data.get('value', 0)
        
        # Only return data if we have a funding rate
        if funding_rate and funding_rate != 0:
            records = [{
                'funding_time': current_time,
                'funding_rate': float(funding_rate),
                'exchange': 'kucoin',
                'symbol': symbol
            }]
            return pd.DataFrame(records)
        
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_mexc_funding(symbol):
    """MEXC API - Fixed with working endpoint"""
    try:
        url = f"https://contract.mexc.com/api/v1/contract/funding_rate/{symbol}_USDT"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            url = "https://contract.mexc.com/api/v1/contract/funding_rate"
            params = {'symbol': f"{symbol}_USDT"}
            response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return pd.DataFrame()
        
        data = response.json()
        funding_rate = None
        
        if isinstance(data, dict):
            if 'fundingRate' in data:
                funding_rate = float(data['fundingRate'])
            elif 'data' in data and isinstance(data['data'], dict):
                funding_rate = float(data['data'].get('fundingRate', 0))
        elif isinstance(data, list) and len(data) > 0:
            funding_rate = float(data[0].get('fundingRate', 0))
        
        # Only return data if we have a funding rate
        if funding_rate is not None and funding_rate != 0:
            current_time = datetime.now()
            records = [{
                'funding_time': current_time,
                'funding_rate': funding_rate,
                'exchange': 'mexc',
                'symbol': symbol
            }]
            return pd.DataFrame(records)
        
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_bitget_funding(symbol):
    """Bitget API - Fixed with correct symbol format"""
    try:
        url = "https://api.bitget.com/api/v2/mix/market/funding-rate"
        params = {
            'symbol': f"{symbol}USDT",
            'productType': 'USDT-FUTURES'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            params['symbol'] = f"{symbol}USDT_UMCBL"
            response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            url = "https://api.bitget.com/api/mix/v1/market/current-fundRate"
            params = {
                'symbol': f"{symbol}USDT_UMCBL",
                'productType': 'umcbl'
            }
            response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return pd.DataFrame()
        
        data = response.json()
        current_time = datetime.now()
        funding_rate = None
        
        if data.get('code') == '00000' and 'data' in data:
            funding_info = data['data']
            if isinstance(funding_info, dict):
                funding_rate = float(funding_info.get('fundingRate', 0))
            elif isinstance(funding_info, list) and len(funding_info) > 0:
                funding_rate = float(funding_info[0].get('fundingRate', 0))
        
        # Only return data if we have a funding rate
        if funding_rate is not None and funding_rate != 0:
            records = [{
                'funding_time': current_time,
                'funding_rate': funding_rate,
                'exchange': 'bitget',
                'symbol': symbol
            }]
            return pd.DataFrame(records)
        
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_bingx_funding(symbol):
    """BingX API - Fixed data parsing for list responses"""
    try:
        url = f"https://open-api.bingx.com/openApi/swap/v2/quote/fundingRate"
        params = {'symbol': f"{symbol}-USDT"}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return pd.DataFrame()
        
        data = response.json()
        current_time = datetime.now()
        funding_rate = None
        
        if data.get('code') == 0 and 'data' in data:
            funding_data = data['data']
            
            if isinstance(funding_data, dict):
                funding_rate = float(funding_data.get('fundingRate', 0))
            elif isinstance(funding_data, list) and len(funding_data) > 0:
                first_item = funding_data[0]
                if isinstance(first_item, dict):
                    funding_rate = float(first_item.get('fundingRate', 0))
                elif isinstance(first_item, (int, float)):
                    funding_rate = float(first_item)
        
        # Only return data if we have a funding rate
        if funding_rate is not None and funding_rate != 0:
            records = [{
                'funding_time': current_time,
                'funding_rate': funding_rate,
                'exchange': 'bingx',
                'symbol': symbol
            }]
            return pd.DataFrame(records)
        
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_whitebit_funding(symbol):
    """WhiteBit API"""
    try:
        url = "https://whitebit.com/api/v4/public/futures"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return pd.DataFrame()
        
        data = response.json()
        current_time = datetime.now()
        funding_rate = None
        
        if data and 'result' in data:
            futures_data = data['result']
            symbol_key = f"{symbol}_USDT"
            
            if isinstance(futures_data, dict):
                for market, info in futures_data.items():
                    if market.upper() == symbol_key.upper() and isinstance(info, dict):
                        rate = info.get('funding_rate', 0)
                        if rate and rate != 0:
                            funding_rate = float(rate)
                            break
        
        # Only return data if we have a funding rate
        if funding_rate is not None and funding_rate != 0:
            records = [{
                'funding_time': current_time,
                'funding_rate': funding_rate,
                'exchange': 'whitebit',
                'symbol': symbol
            }]
            return pd.DataFrame(records)
        
        return pd.DataFrame()
        
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_current_rates_other_exchanges(symbol):
    """Fetch current rates from additional exchanges"""
    exchanges_data = []
    
    additional_exchanges = [
        ('MEXC', fetch_mexc_funding),
        ('Bitget', fetch_bitget_funding),
        ('BingX', fetch_bingx_funding),
        ('WhiteBit', fetch_whitebit_funding)
    ]
    
    for name, fetch_func in additional_exchanges:
        try:
            data = fetch_func(symbol)
            if not data.empty:
                exchanges_data.append(data)
        except Exception as e:
            continue
    
    if exchanges_data:
        return pd.concat(exchanges_data, ignore_index=True)
    else:
        return pd.DataFrame()

# =============================================================================
# DATA COLLECTION AND ANALYSIS
# =============================================================================

@st.cache_data(ttl=300)
def collect_funding_data(symbol, days=7):
    """Collect funding rate data from all exchanges"""
    
    exchanges = [
        ('Binance', fetch_binance_funding),
        ('Bybit', fetch_bybit_funding),
        ('OKX', fetch_okx_funding),
        ('Gate.io', fetch_gate_funding),
        ('KuCoin', fetch_kucoin_funding)
    ]
    
    all_data = []
    
    # Fetch from major exchanges
    for name, fetch_func in exchanges:
        try:
            data = fetch_func(symbol, days)
            if not data.empty:
                all_data.append(data)
        except Exception as e:
            st.warning(f"Failed to fetch data from {name}: {str(e)}")
    
    # Fetch from other exchanges (current rates only)
    try:
        other_data = fetch_current_rates_other_exchanges(symbol)
        if not other_data.empty:
            all_data.append(other_data)
    except:
        pass
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

def analyze_arbitrage_opportunities(data):
    """Analyze arbitrage opportunities from funding rate data"""
    if data.empty:
        return pd.DataFrame(), {}
    
    # Get latest rate for each exchange
    latest_rates = data.groupby('exchange')['funding_rate'].last().reset_index()
    
    # Calculate statistics
    stats = {
        'avg_rate': latest_rates['funding_rate'].mean(),
        'max_rate': latest_rates['funding_rate'].max(),
        'min_rate': latest_rates['funding_rate'].min(),
        'spread': latest_rates['funding_rate'].max() - latest_rates['funding_rate'].min(),
        'exchanges_count': len(latest_rates)
    }
    
    # Find arbitrage opportunities
    arbitrage_opportunities = []
    
    for i, row1 in latest_rates.iterrows():
        for j, row2 in latest_rates.iterrows():
            if i < j:
                rate_diff = abs(row1['funding_rate'] - row2['funding_rate'])
                daily_diff = rate_diff * 3  # 8-hour to daily
                
                if daily_diff > 0.00005:  # 0.005% threshold
                    arbitrage_opportunities.append({
                        'exchange_1': row1['exchange'],
                        'exchange_2': row2['exchange'],
                        'rate_1': row1['funding_rate'],
                        'rate_2': row2['funding_rate'],
                        'rate_diff': rate_diff,
                        'daily_diff': daily_diff,
                        'potential_daily_profit_100': daily_diff * 100,
                        'potential_monthly_profit_100': daily_diff * 100 * 30,
                        'direction': f"Long {row1['exchange']}, Short {row2['exchange']}" if row1['funding_rate'] < row2['funding_rate'] else f"Long {row2['exchange']}, Short {row1['exchange']}",
                        'success_probability': 'High' if daily_diff > 0.0002 else 'Medium'
                    })
    
    return pd.DataFrame(arbitrage_opportunities), stats

def create_funding_rate_chart(data):
    """Create historical funding rate chart with dark theme"""
    if data.empty:
        return None
    
    fig = go.Figure()
    
    exchanges = data['exchange'].unique()
    # Professional color palette for dark theme
    colors = ['#00d4ff', '#ff6b6b', '#4ecdc4', '#45b7d1', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43']
    
    for i, exchange in enumerate(exchanges):
        exchange_data = data[data['exchange'] == exchange].sort_values('funding_time')
        
        if len(exchange_data) > 1:
            fig.add_trace(go.Scatter(
                x=exchange_data['funding_time'],
                y=exchange_data['funding_rate'] * 100,
                mode='lines+markers',
                name=exchange.upper(),
                line=dict(color=colors[i % len(colors)], width=2.5),
                marker=dict(size=5, line=dict(width=1, color='white')),
                hovertemplate=f'<b>{exchange.upper()}</b><br>' +
                            'Time: %{x}<br>' +
                            'Rate: %{y:.4f}%<br>' +
                            '<extra></extra>'
            ))
    
    fig.update_layout(
        title={
            'text': 'Historical Funding Rates (7 Days)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#ffffff', 'family': 'Inter'}
        },
        xaxis_title='Date',
        yaxis_title='Funding Rate (%)',
        hovermode='x unified',
        height=450,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Inter'),
        legend=dict(
            bgcolor='rgba(30, 30, 46, 0.8)',
            bordercolor='#3a3a52',
            borderwidth=1,
            font=dict(color='#ffffff')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        )
    )
    
    return fig

def create_exchange_list(data, capital, symbol):
    """Create exchange list similar to the reference image"""
    if data.empty:
        return None
    
    # Get latest rates for all exchanges
    latest_data = data.groupby('exchange').last().reset_index()
    
    # Sort by funding rate (descending for best opportunities)
    latest_data = latest_data.sort_values('funding_rate', ascending=False)
    
    # Create table header
    list_html = '''
    <div class="exchange-table">
        <div class="table-header">
            <div class="header-cell">Ticker Markets</div>
            <div class="header-cell">Funding Rates</div>
            <div class="header-cell">Countdown</div>
            <div class="header-cell">% Profit Interval</div>
            <div class="header-cell">24 hours</div>
            <div class="header-cell">Life time</div>
        </div>
    '''
    
    for idx, row in latest_data.iterrows():
        exchange = row['exchange']
        funding_rate = row['funding_rate']
        
        # Calculate profit potential (funding rate * 3 payments per day * capital)
        daily_profit_pct = funding_rate * 3 * 100
        
        # Determine position type based on rate
        if funding_rate > 0:
            position_type = "SHORT"
            position_color = "short-position"
        else:
            position_type = "LONG"  
            position_color = "long-position"
        
        # Color coding for funding rate
        rate_color = 'rate-positive' if funding_rate > 0 else 'rate-negative'
        
        # Profit color
        profit_color = 'profit-positive' if daily_profit_pct > 0 else 'profit-negative'
        
        # Calculate countdown to next funding (8 hours cycle)
        import datetime
        now = datetime.datetime.now()
        next_funding_hours = 8 - (now.hour % 8)
        next_funding_minutes = 60 - now.minute
        
        if next_funding_minutes == 60:
            next_funding_minutes = 0
            next_funding_hours += 1
        
        countdown = f"{next_funding_hours:02d}:{next_funding_minutes:02d}"
        
        # Calculate lifetime profit (example: 30 days)
        lifetime_profit_pct = daily_profit_pct * 30
        
        list_html += f'''
        <div class="table-row">
            <div class="table-cell ticker-cell">
                <div class="star-icon">⭐</div>
                <div class="ticker-info">
                    <div class="ticker-symbol">{symbol}USDT</div>
                    <div class="position-type {position_color}">{position_type} {exchange.title()}</div>
                </div>
            </div>
            
            <div class="table-cell rates-cell">
                <div class="funding-rate {rate_color}">{funding_rate*100:.3f}%</div>
                <div class="rate-comparison">+{abs(funding_rate)*100:.3f}%</div>
            </div>
            
            <div class="table-cell countdown-cell">
                <div class="countdown-number">1</div>
                <div class="countdown-time">{countdown}</div>
            </div>
            
            <div class="table-cell profit-cell">
                <div class="profit-pct {profit_color}">{daily_profit_pct:+.3f}%</div>
            </div>
            
            <div class="table-cell profit-cell">
                <div class="profit-pct {profit_color}">{daily_profit_pct:+.3f}%</div>
            </div>
            
            <div class="table-cell lifetime-cell">
                <div class="lifetime-value">{abs(lifetime_profit_pct):.1f}%</div>
                <div class="lifetime-time">Real-time</div>
            </div>
        </div>
        '''
    
    list_html += '</div>'
    return list_html

def create_arbitrage_chart(arb_df):
    """Create arbitrage opportunities chart with dark theme"""
    if arb_df.empty:
        return None
    
    # Sort by profit potential and take top 10
    arb_df = arb_df.sort_values('potential_daily_profit_100', ascending=True).tail(10)
    
    fig = go.Figure()
    
    # Color scheme based on profit potential
    colors = []
    for profit in arb_df['potential_daily_profit_100']:
        if profit > 0.05:
            colors.append('#2ed573')  # Green for high profit
        elif profit > 0.03:
            colors.append('#ffa502')  # Orange for medium profit
        elif profit > 0.01:
            colors.append('#3742fa')  # Blue for low profit
        else:
            colors.append('#747d8c')  # Gray for very low profit
    
    fig.add_trace(go.Bar(
        x=arb_df['potential_daily_profit_100'],
        y=[f"{row['exchange_1']} → {row['exchange_2']}" for _, row in arb_df.iterrows()],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[f"${profit:.3f}" for profit in arb_df['potential_daily_profit_100']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                     'Daily Profit: $%{x:.3f}<br>' +
                     'Monthly: $%{customdata:.2f}<br>' +
                     '<extra></extra>',
        customdata=arb_df['potential_monthly_profit_100']
    ))
    
    fig.update_layout(
        title={
            'text': 'Top Arbitrage Opportunities',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#ffffff', 'family': 'Inter'}
        },
        xaxis_title='Daily Profit ($)',
        yaxis_title='Exchange Pairs',
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Inter'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        )
    )
    
    return fig

def create_current_rates_chart(data):
    """Create current rates comparison chart with dark theme"""
    if data.empty:
        return None
    
    latest_rates = data.groupby('exchange')['funding_rate'].last().reset_index()
    latest_rates = latest_rates.sort_values('funding_rate')
    
    fig = go.Figure()
    
    # Color scheme for rates: red for negative, green for positive, yellow for neutral
    colors = []
    for rate in latest_rates['funding_rate']:
        if rate < 0:
            colors.append('#ff6b6b')  # Red for negative
        elif rate > 0.0001:
            colors.append('#4ecdc4')  # Teal for high positive
        elif rate > 0.00005:
            colors.append('#00d4ff')  # Blue for medium positive
        else:
            colors.append('#feca57')  # Yellow for low positive
    
    fig.add_trace(go.Bar(
        x=latest_rates['funding_rate'] * 100,
        y=latest_rates['exchange'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[f"{rate:.4f}%" for rate in latest_rates['funding_rate'] * 100],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                     'Rate: %{x:.4f}%<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Current Funding Rates by Exchange',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#ffffff', 'family': 'Inter'}
        },
        xaxis_title='Funding Rate (%)',
        yaxis_title='Exchange',
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Inter'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.3)',
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            color='#ffffff',
            title=dict(font=dict(color='#ffffff')),
            tickfont=dict(color='#ffffff')
        )
    )
    
    return fig

def get_current_rates_for_crypto(symbol):
    """Get current funding rates for a specific crypto from all exchanges"""
    
    exchanges = [
        ('Binance', fetch_binance_funding),
        ('Bybit', fetch_bybit_funding),
        ('OKX', fetch_okx_funding),
        ('Gate.io', fetch_gate_funding),
        ('KuCoin', fetch_kucoin_funding)
    ]
    
    current_rates = {}
    
    # Fetch from major exchanges
    for name, fetch_func in exchanges:
        try:
            data = fetch_func(symbol, days=1)  # Get recent data
            if not data.empty:
                # Get the most recent funding rate
                latest_rate = data['funding_rate'].iloc[-1]
                current_rates[name] = latest_rate
        except Exception as e:
            print(f"Error fetching {name} data for {symbol}: {str(e)}")
            continue
    
    # Fetch from additional exchanges
    additional_exchanges = [
        ('MEXC', fetch_mexc_funding),
        ('Bitget', fetch_bitget_funding),
        ('BingX', fetch_bingx_funding),
        ('WhiteBit', fetch_whitebit_funding)
    ]
    
    for name, fetch_func in additional_exchanges:
        try:
            data = fetch_func(symbol)
            if not data.empty:
                latest_rate = data['funding_rate'].iloc[-1]
                current_rates[name] = latest_rate
        except Exception as e:
            print(f"Error fetching {name} data for {symbol}: {str(e)}")
            continue
    
    return current_rates

def get_best_opportunities_for_all_cryptos(capital_amount):
    """Get best arbitrage opportunities for all cryptocurrencies with correct min/max logic"""
    predefined_cryptos = ['BTC', 'ETH', 'SOL', 'DOGE', 'MATIC', 'AVAX', 'PEPE', 'LINK', 'DOT', 'ADA']
    opportunities = []
    
    for crypto in predefined_cryptos:
        try:
            # Get current rates for this crypto from all exchanges
            current_rates = get_current_rates_for_crypto(crypto)
            
            if len(current_rates) >= 2:
                # Find min and max rates across all exchanges
                min_rate = min(current_rates.values())
                max_rate = max(current_rates.values())
                
                # Find exchanges with min and max rates
                min_exchange = [ex for ex, rate in current_rates.items() if rate == min_rate][0]
                max_exchange = [ex for ex, rate in current_rates.items() if rate == max_rate][0]
                
                # Calculate arbitrage opportunity using correct min/max logic
                # Long position on exchange with LOWER funding rate (you pay less funding)
                # Short position on exchange with HIGHER funding rate (you receive more funding)
                # Profit = difference in funding rates
                
                if max_rate > min_rate:
                    profit_percentage = (max_rate - min_rate) * 100
                    rate_spread = max_rate - min_rate
                    
                    opportunity = {
                        'crypto': crypto,
                        'long_exchange': min_exchange,  # Long on lower rate (pay less funding)
                        'short_exchange': max_exchange,  # Short on higher rate (receive more funding)
                        'long_rate': min_rate,
                        'short_rate': max_rate,
                        'profit_percentage': profit_percentage,
                        'daily_profit': (capital_amount * profit_percentage / 100),
                        'min_rate': min_rate,
                        'max_rate': max_rate,
                        'rate_spread': rate_spread,
                        'direction': f"Long {min_exchange}, Short {max_exchange}"  # Match Best Opportunity format
                    }
                    
                    opportunities.append(opportunity)
                    
        except Exception as e:
            print(f"Error processing {crypto}: {str(e)}")
            continue
    
    return opportunities

def render_opportunities_tracker(opportunities, sort_order='desc'):
    """Render the opportunities tracker with real live data"""
    
    if not opportunities:
        st.markdown('<div style="color: #ffffff; text-align: center; padding: 2rem;">Loading opportunities...</div>', unsafe_allow_html=True)
        return
    
    # Sort opportunities by profit percentage
    sorted_opportunities = sorted(opportunities, 
                                key=lambda x: x['profit_percentage'], 
                                reverse=(sort_order == 'desc'))
    
    # Create header row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown('<div style="color: #ffffff; font-weight: 600; text-align: center; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);">Ticker Markets</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="color: #ffffff; font-weight: 600; text-align: center; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);">Funding Rates</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="color: #ffffff; font-weight: 600; text-align: center; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);">% Profit</div>', unsafe_allow_html=True)
    
    # Display opportunities
    for opp in sorted_opportunities:
        profit_color = "#00ff88" if opp['profit_percentage'] > 0 else "#ff4757"
        
        # Create opportunity row
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f'''
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.3rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                min-height: 100px;
                max-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-weight: 700; color: #ffffff; font-size: 1.1rem; margin-bottom: 0.4rem; text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);">
                    {opp['crypto']}USDT
                </div>
                <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8); line-height: 1.4;">
                    <span style="color: #00ff88; font-weight: 600;">Long {opp['long_exchange']}</span><br>
                    <span style="color: #ff4757; font-weight: 600;">Short {opp['short_exchange']}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.3rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                min-height: 100px;
                max-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="color: #00ff88; font-weight: 600; font-size: 0.95rem; text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);">
                    {opp['long_exchange']}: {opp['long_rate']*100:.4f}%
                </div>
                <div style="color: #ff4757; font-weight: 600; font-size: 0.95rem; text-shadow: 0 0 8px rgba(255, 71, 87, 0.4);">
                    {opp['short_exchange']}: {opp['short_rate']*100:.4f}%
                </div>
                <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.7rem; margin-top: 0.2rem;">
                    Spread: {opp.get('rate_spread', 0)*100:.4f}%
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            daily_profit_usd = opp['daily_profit']
            st.markdown(f'''
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.3rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                min-height: 100px;
                max-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="color: {profit_color}; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 10px {profit_color};">
                    {opp['profit_percentage']:.3f}%
                </div>
                <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.7rem; margin-top: 0.2rem;">
                    ${daily_profit_usd:.2f}/day
                </div>
            </div>
            ''', unsafe_allow_html=True)

# =============================================================================
# STREAMLIT DASHBOARD
# =============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">Crypto Funding Rate Arbitrage Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # Symbol selection
    symbol = st.sidebar.selectbox(
        "Select Cryptocurrency",
        ["BTC", "ETH", "SOL", "DOGE", "MATIC", "PEPE", "AVAX", "LINK", "DOT", "ADA"],
        index=0
    )
    
    # Capital amount
    capital = st.sidebar.number_input(
        "Capital Amount ($)",
        min_value=10,
        max_value=100000,
        value=100,
        step=10
    )
    
    # Days for historical data
    days = st.sidebar.slider(
        "Historical Data (Days)",
        min_value=1,
        max_value=14,
        value=7
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5 minutes)", value=True)
    
    # Refresh button
    if st.sidebar.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Loading state with custom spinner
        loading_placeholder = st.empty()
        with loading_placeholder:
            st.markdown('''
            <div class="custom-spinner">
                <div class="spinner"></div>
            </div>
            <p style="text-align: center; color: #ffffff; margin-top: 1rem;">Fetching live data...</p>
            ''', unsafe_allow_html=True)
            
            data = collect_funding_data(symbol, days)
            
        loading_placeholder.empty()
        
        if data.empty:
            st.error(f"No data available for {symbol}. Please try another symbol.")
            return
        
        # Analyze opportunities
        arb_df, stats = analyze_arbitrage_opportunities(data)
        
        # Title
        st.markdown(f"<h2 style='color: #ffffff; text-shadow: 0 0 15px rgba(255, 255, 255, 0.7); margin-bottom: 1rem;'>{symbol} Funding Rate Analysis</h2>", unsafe_allow_html=True)
        
        # Key metrics
        col1_1, col1_2, col1_3, col1_4 = st.columns(4)
        
        with col1_1:
            st.metric(
                "Active Exchanges",
                stats['exchanges_count'],
                delta=None
            )
        
        with col1_2:
            st.metric(
                "Average Rate",
                f"{stats['avg_rate']*100:.4f}%",
                delta=None
            )
        
        with col1_3:
            st.metric(
                "Rate Spread",
                f"{stats['spread']*100:.4f}%",
                delta=None
            )
        
        with col1_4:
            st.metric(
                "Arbitrage Opportunities",
                len(arb_df),
                delta=None
            )
        
        # Best Opportunity and Summary cards below analysis
        card_col1, card_col2 = st.columns(2)
        
        with card_col1:
            if not arb_df.empty:
                # Best opportunity card - using original logic for min/max rates
                best_opportunity = arb_df.loc[arb_df['potential_daily_profit_100'].idxmax()]
                
                st.markdown(f"""
                <div class="opportunity-card">
                    <h3>Best Opportunity</h3>
                    <p><strong>{best_opportunity['exchange_1'].upper()} → {best_opportunity['exchange_2'].upper()}</strong></p>
                    <p>Daily Profit: <strong>${best_opportunity['potential_daily_profit_100']*(capital/100):.2f}</strong></p>
                    <p>Monthly: <strong>${best_opportunity['potential_monthly_profit_100']*(capital/100):.2f}</strong></p>
                    <p>Strategy: {best_opportunity['direction']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="opportunity-card">
                    <h3>Best Opportunity</h3>
                    <p>No opportunities found</p>
                </div>
                """, unsafe_allow_html=True)
        
        with card_col2:
            if not arb_df.empty:
                total_daily_profit = arb_df['potential_daily_profit_100'].sum() * (capital/100)
                avg_daily_profit = arb_df['potential_daily_profit_100'].mean() * (capital/100)
                
                st.markdown(f"""
                <div class="summary-card">
                    <h3>Summary</h3>
                    <p>Total Daily Potential: <strong>${total_daily_profit:.2f}</strong></p>
                    <p>Average per Pair: <strong>${avg_daily_profit:.2f}</strong></p>
                    <p>Active Pairs: <strong>{len(arb_df)}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="summary-card">
                    <h3>Summary</h3>
                    <p>No data available</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        st.subheader("Historical Funding Rates")
        hist_chart = create_funding_rate_chart(data)
        if hist_chart:
            st.plotly_chart(hist_chart, use_container_width=True)
        
        st.subheader("Current Rates Comparison")
        rates_chart = create_current_rates_chart(data)
        if rates_chart:
            st.plotly_chart(rates_chart, use_container_width=True)
    
    with col2:
        # Opportunities tracker
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        
        # Get opportunities for all cryptos
        with st.spinner("Fetching real-time funding rates..."):
            opportunities = get_best_opportunities_for_all_cryptos(capital)
        
        # Add some summary stats at the top
        if opportunities:
            total_opportunities = len(opportunities)
            avg_profit = sum(opp['profit_percentage'] for opp in opportunities) / len(opportunities)
            best_profit = max(opp['profit_percentage'] for opp in opportunities)
            
            st.markdown(f'''
            <div style="
                background: linear-gradient(135deg, #4a5dd7 0%, #5c4a99 100%);
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
                box-shadow: 0 6px 30px rgba(74, 93, 215, 0.5);
            ">
                <div style="color: #ffffff; font-size: 0.9rem; text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);">
                    <strong>{total_opportunities}</strong> opportunities found | 
                    Avg: <strong>{avg_profit:.3f}%</strong> | 
                    Best: <strong style="color: #00ff88;">{best_profit:.3f}%</strong>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Render tracker
        render_opportunities_tracker(opportunities, 'desc')
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()
