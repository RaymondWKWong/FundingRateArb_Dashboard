# FundingRateArb Dashboard

Real-time dashboard for monitoring funding rate arbitrage opportunities across 9 major cryptocurrency exchanges.

## Features

- **Real-time Data**: Live funding rates from 9 major exchanges (Binance, Bybit, OKX, Gate.io, KuCoin, MEXC, Bitget, BingX, WhiteBit)
- **Multi-Cryptocurrency Tracking**: Monitor 10 popular cryptocurrencies simultaneously
- **Arbitrage Opportunities**: Automatic detection of profitable long/short positions
- **Professional Interface**: Bloomberg-style dark theme with purple gradients
- **Interactive Charts**: Real-time rate visualization with Plotly
- **Performance Optimized**: 5-minute caching for efficient API usage

## Supported Exchanges

- Binance
- Bybit
- OKX
- Gate.io
- KuCoin
- MEXC
- Bitget
- BingX
- WhiteBit

## Tracked Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)
- Cardano (ADA)
- Polygon (MATIC)
- Avalanche (AVAX)
- Chainlink (LINK)
- Polkadot (DOT)
- Litecoin (LTC)
- Bitcoin Cash (BCH)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the dashboard locally:
```bash
streamlit run funding_rate_dashboard.py
```

## Deployment

This dashboard is optimized for deployment on Streamlit Community Cloud.

## How It Works

The dashboard fetches real-time funding rates from multiple exchanges and calculates arbitrage opportunities by:

1. **Data Collection**: Fetching current funding rates from 9 exchanges
2. **Opportunity Detection**: Finding the highest and lowest rates for each cryptocurrency
3. **Profit Calculation**: Computing potential profit from rate differences
4. **Visual Display**: Presenting opportunities with color-coded Long/Short positions

## API Rate Limits

The dashboard respects exchange API rate limits with:
- 5-minute data caching
- Error handling for failed requests
- Graceful degradation when exchanges are unavailable

## License

This project is for educational and research purposes.
