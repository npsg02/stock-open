#!/usr/bin/env python3
"""
Test script for VN Stock Visualizer
Tests the visualizer with mock data to ensure all functions work correctly
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys


def create_mock_stock_data(symbol='TEST', days=180):
    """
    Create mock stock data for testing
    
    Args:
        symbol (str): Stock symbol
        days (int): Number of days of data to generate
    
    Returns:
        pandas.DataFrame: Mock stock data
    """
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate realistic-looking stock price data
    np.random.seed(42)
    
    # Starting price
    base_price = 50000
    
    # Generate random walk for prices
    returns = np.random.randn(len(dates)) * 0.02  # 2% daily volatility
    price_multipliers = np.exp(returns.cumsum())
    close_prices = base_price * price_multipliers
    
    # Generate OHLC data
    data = []
    for i, date in enumerate(dates):
        close = close_prices[i]
        # Generate realistic OHLC values
        daily_range = close * np.random.uniform(0.01, 0.05)
        high = close + np.random.uniform(0, daily_range)
        low = close - np.random.uniform(0, daily_range)
        open_price = low + np.random.uniform(0, high - low)
        
        # Generate volume
        volume = np.random.randint(1000000, 10000000)
        
        data.append({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data, index=dates)
    return df


def test_visualizer_with_mock_data():
    """Test the visualizer with mock data"""
    print("="*60)
    print("Testing VN Stock Visualizer with Mock Data")
    print("="*60)
    
    try:
        # Import after modifying path
        sys.path.insert(0, '/home/runner/work/stock-open/stock-open')
        from vn_stock_visualizer import VNStockVisualizer
        
        # Create visualizer instance
        print("\n1. Creating visualizer instance...")
        visualizer = VNStockVisualizer('TEST', start_date='2024-01-01', end_date='2024-12-31')
        print("✓ Visualizer created successfully")
        
        # Inject mock data
        print("\n2. Generating mock stock data...")
        visualizer.data = create_mock_stock_data('TEST', days=180)
        print(f"✓ Generated {len(visualizer.data)} data points")
        
        # Test summary
        print("\n3. Testing summary statistics...")
        visualizer.print_summary()
        print("✓ Summary statistics generated successfully")
        
        # Test saving charts
        import os
        output_dir = '/tmp/test_charts'
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n4. Testing chart generation and saving...")
        
        print("   a. Generating candlestick chart...")
        visualizer.plot_candlestick_chart(save_path=f"{output_dir}/test_candlestick.html")
        print("   ✓ Candlestick chart saved")
        
        print("   b. Generating moving average chart...")
        visualizer.plot_price_and_moving_averages(save_path=f"{output_dir}/test_ma.png")
        print("   ✓ Moving average chart saved")
        
        print("   c. Generating volume analysis chart...")
        visualizer.plot_volume_analysis(save_path=f"{output_dir}/test_volume.png")
        print("   ✓ Volume analysis chart saved")
        
        print("   d. Generating daily returns chart...")
        visualizer.plot_daily_returns(save_path=f"{output_dir}/test_returns.png")
        print("   ✓ Daily returns chart saved")
        
        # Verify files exist
        print("\n5. Verifying generated files...")
        expected_files = [
            'test_candlestick.html',
            'test_ma.png',
            'test_volume.png',
            'test_returns.png'
        ]
        
        all_files_exist = True
        for filename in expected_files:
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"   ✓ {filename} exists ({size:,} bytes)")
            else:
                print(f"   ✗ {filename} not found")
                all_files_exist = False
        
        print("\n" + "="*60)
        if all_files_exist:
            print("✓ All tests passed successfully!")
            print(f"✓ Charts saved to: {output_dir}")
        else:
            print("✗ Some tests failed")
        print("="*60)
        
        return all_files_exist
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_visualizer_with_mock_data()
    sys.exit(0 if success else 1)
