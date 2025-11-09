#!/usr/bin/env python3
"""
Vietnamese Stock Market Data Visualization Tool
Uses vnstock library to fetch and visualize VN stock market data
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import argparse

try:
    # Try importing from vnstock 3.x
    from vnstock3 import Vnstock
    VNSTOCK_VERSION = 3
except ImportError:
    try:
        # Fallback to vnstock 0.x
        from vnstock import stock_historical_data
        VNSTOCK_VERSION = 0
    except ImportError:
        print("Error: vnstock library not found. Please install it using: pip install vnstock")
        exit(1)


class VNStockVisualizer:
    """A tool to visualize Vietnamese stock market data"""
    
    def __init__(self, symbol, start_date=None, end_date=None):
        """
        Initialize the visualizer with stock symbol and date range
        
        Args:
            symbol (str): Stock symbol (e.g., 'VNM', 'VCB', 'HPG')
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
        """
        self.symbol = symbol.upper()
        
        # Set default date range if not provided
        if end_date is None:
            self.end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.end_date = end_date
            
        if start_date is None:
            # Default to 6 months of data
            self.start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        else:
            self.start_date = start_date
        
        self.data = None
        
    def fetch_data(self):
        """Fetch stock data using vnstock library"""
        try:
            print(f"Fetching data for {self.symbol} from {self.start_date} to {self.end_date}...")
            
            if VNSTOCK_VERSION == 3:
                # Use vnstock 3.x API
                stock = Vnstock().stock(symbol=self.symbol, source='VCI')
                self.data = stock.quote.history(
                    start=self.start_date,
                    end=self.end_date
                )
                
                # Standardize column names to lowercase
                if self.data is not None:
                    self.data.columns = self.data.columns.str.lower()
                    # Set time column as index if present
                    if 'time' in self.data.columns:
                        self.data['time'] = pd.to_datetime(self.data['time'])
                        self.data.set_index('time', inplace=True)
            else:
                # Use vnstock 0.x API
                self.data = stock_historical_data(
                    symbol=self.symbol,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    resolution='1D',
                    type='stock'
                )
            
            if self.data is not None and not self.data.empty:
                print(f"Successfully fetched {len(self.data)} data points")
                return True
            else:
                print("No data retrieved")
                return False
        except Exception as e:
            print(f"Error fetching data: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def plot_candlestick_chart(self, save_path=None):
        """
        Create an interactive candlestick chart with volume
        
        Args:
            save_path (str): Path to save the HTML file (optional)
        """
        if self.data is None or self.data.empty:
            print("No data available. Please fetch data first.")
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{self.symbol} Stock Price', 'Volume'),
            row_heights=[0.7, 0.3]
        )
        
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=self.data.index,
                open=self.data['open'],
                high=self.data['high'],
                low=self.data['low'],
                close=self.data['close'],
                name='OHLC'
            ),
            row=1, col=1
        )
        
        # Add volume bar chart
        colors = ['red' if close < open else 'green' 
                  for close, open in zip(self.data['close'], self.data['open'])]
        
        fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['volume'],
                name='Volume',
                marker_color=colors
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Stock Analysis ({self.start_date} to {self.end_date})',
            yaxis_title='Price (VND)',
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True
        )
        
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        if save_path:
            fig.write_html(save_path)
            print(f"Chart saved to {save_path}")
        else:
            fig.show()
    
    def plot_price_and_moving_averages(self, ma_periods=[20, 50, 100], save_path=None):
        """
        Plot closing price with moving averages
        
        Args:
            ma_periods (list): List of periods for moving averages
            save_path (str): Path to save the image file (optional)
        """
        if self.data is None or self.data.empty:
            print("No data available. Please fetch data first.")
            return
        
        plt.figure(figsize=(14, 7))
        
        # Plot closing price
        plt.plot(self.data.index, self.data['close'], label='Close Price', linewidth=2)
        
        # Calculate and plot moving averages
        for period in ma_periods:
            if len(self.data) >= period:
                ma = self.data['close'].rolling(window=period).mean()
                plt.plot(self.data.index, ma, label=f'MA{period}', alpha=0.7)
        
        plt.title(f'{self.symbol} - Price and Moving Averages', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (VND)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def plot_volume_analysis(self, save_path=None):
        """
        Plot volume analysis with moving average
        
        Args:
            save_path (str): Path to save the image file (optional)
        """
        if self.data is None or self.data.empty:
            print("No data available. Please fetch data first.")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
        
        # Plot price
        ax1.plot(self.data.index, self.data['close'], color='blue', linewidth=2)
        ax1.set_ylabel('Price (VND)', fontsize=12)
        ax1.set_title(f'{self.symbol} - Price and Volume Analysis', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Plot volume with color coding
        colors = ['red' if close < open else 'green' 
                  for close, open in zip(self.data['close'], self.data['open'])]
        ax2.bar(self.data.index, self.data['volume'], color=colors, alpha=0.7)
        
        # Add volume moving average
        volume_ma = self.data['volume'].rolling(window=20).mean()
        ax2.plot(self.data.index, volume_ma, color='orange', linewidth=2, label='Volume MA20')
        
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def plot_daily_returns(self, save_path=None):
        """
        Plot daily returns distribution
        
        Args:
            save_path (str): Path to save the image file (optional)
        """
        if self.data is None or self.data.empty:
            print("No data available. Please fetch data first.")
            return
        
        # Calculate daily returns
        daily_returns = self.data['close'].pct_change() * 100
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot daily returns over time
        ax1.plot(self.data.index[1:], daily_returns[1:], linewidth=1)
        ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax1.set_title(f'{self.symbol} - Daily Returns Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Daily Return (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot histogram of returns
        ax2.hist(daily_returns.dropna(), bins=50, edgecolor='black', alpha=0.7)
        ax2.axvline(x=0, color='r', linestyle='--', linewidth=2)
        ax2.set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Daily Return (%)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    def print_summary(self):
        """Print summary statistics of the stock data"""
        if self.data is None or self.data.empty:
            print("No data available. Please fetch data first.")
            return
        
        print(f"\n{'='*60}")
        print(f"Summary Statistics for {self.symbol}")
        print(f"Period: {self.start_date} to {self.end_date}")
        print(f"{'='*60}")
        
        latest = self.data.iloc[-1]
        first = self.data.iloc[0]
        
        print(f"\nLatest Price (Close): {latest['close']:,.0f} VND")
        print(f"Latest Date: {self.data.index[-1].strftime('%Y-%m-%d')}")
        print(f"\nPrice Range:")
        print(f"  Highest: {self.data['high'].max():,.0f} VND")
        print(f"  Lowest: {self.data['low'].min():,.0f} VND")
        
        price_change = latest['close'] - first['close']
        price_change_pct = (price_change / first['close']) * 100
        print(f"\nPrice Change: {price_change:+,.0f} VND ({price_change_pct:+.2f}%)")
        
        print(f"\nVolume Statistics:")
        print(f"  Average Daily Volume: {self.data['volume'].mean():,.0f}")
        print(f"  Highest Volume: {self.data['volume'].max():,.0f}")
        
        # Calculate volatility
        daily_returns = self.data['close'].pct_change()
        volatility = daily_returns.std() * 100
        print(f"\nVolatility (Daily Std Dev): {volatility:.2f}%")
        
        print(f"{'='*60}\n")


def main():
    """Main function to run the visualizer from command line"""
    parser = argparse.ArgumentParser(
        description='Vietnamese Stock Market Data Visualization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Visualize VNM stock for the last 6 months
  python vn_stock_visualizer.py VNM
  
  # Visualize VCB stock with custom date range
  python vn_stock_visualizer.py VCB --start 2023-01-01 --end 2023-12-31
  
  # Generate all charts and save to files
  python vn_stock_visualizer.py HPG --save-charts
        """
    )
    
    parser.add_argument('symbol', type=str, help='Stock symbol (e.g., VNM, VCB, HPG)')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--save-charts', action='store_true', 
                        help='Save charts to files instead of displaying')
    parser.add_argument('--output-dir', type=str, default='./charts',
                        help='Directory to save charts (default: ./charts)')
    
    args = parser.parse_args()
    
    # Create visualizer instance
    visualizer = VNStockVisualizer(args.symbol, args.start, args.end)
    
    # Fetch data
    if not visualizer.fetch_data():
        print("Failed to fetch data. Exiting.")
        return
    
    # Print summary
    visualizer.print_summary()
    
    # Create output directory if saving charts
    if args.save_charts:
        import os
        os.makedirs(args.output_dir, exist_ok=True)
        symbol = visualizer.symbol
        
        print("\nGenerating charts...")
        visualizer.plot_candlestick_chart(
            save_path=f"{args.output_dir}/{symbol}_candlestick.html"
        )
        visualizer.plot_price_and_moving_averages(
            save_path=f"{args.output_dir}/{symbol}_ma.png"
        )
        visualizer.plot_volume_analysis(
            save_path=f"{args.output_dir}/{symbol}_volume.png"
        )
        visualizer.plot_daily_returns(
            save_path=f"{args.output_dir}/{symbol}_returns.png"
        )
        print(f"\nAll charts saved to {args.output_dir}/")
    else:
        print("\nGenerating interactive candlestick chart...")
        visualizer.plot_candlestick_chart()


if __name__ == "__main__":
    main()
