#!/usr/bin/env python3
"""
Example usage of the VN Stock Visualizer
This script demonstrates various ways to use the visualization tool
"""

from vn_stock_visualizer import VNStockVisualizer
from datetime import datetime, timedelta


def example_basic_usage():
    """Example 1: Basic usage with default settings"""
    print("\n" + "="*60)
    print("Example 1: Basic Usage - VNM stock (last 6 months)")
    print("="*60)
    
    # Create visualizer for VNM stock
    visualizer = VNStockVisualizer('VNM')
    
    # Fetch data
    if visualizer.fetch_data():
        # Print summary
        visualizer.print_summary()
        
        # Show interactive candlestick chart
        visualizer.plot_candlestick_chart()


def example_custom_date_range():
    """Example 2: Custom date range"""
    print("\n" + "="*60)
    print("Example 2: Custom Date Range - VCB stock (2023)")
    print("="*60)
    
    # Create visualizer with specific date range
    visualizer = VNStockVisualizer(
        symbol='VCB',
        start_date='2023-01-01',
        end_date='2023-12-31'
    )
    
    # Fetch and visualize
    if visualizer.fetch_data():
        visualizer.print_summary()
        visualizer.plot_price_and_moving_averages()


def example_multiple_stocks():
    """Example 3: Compare multiple stocks"""
    print("\n" + "="*60)
    print("Example 3: Compare Multiple Stocks")
    print("="*60)
    
    stocks = ['VNM', 'VCB', 'HPG']
    
    # Calculate date range (last 3 months)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    for symbol in stocks:
        print(f"\n--- Analyzing {symbol} ---")
        visualizer = VNStockVisualizer(symbol, start_date, end_date)
        
        if visualizer.fetch_data():
            visualizer.print_summary()


def example_save_all_charts():
    """Example 4: Save all charts to files"""
    print("\n" + "="*60)
    print("Example 4: Save All Charts - HPG stock")
    print("="*60)
    
    import os
    
    # Create output directory
    output_dir = './example_charts'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create visualizer
    visualizer = VNStockVisualizer('HPG')
    
    if visualizer.fetch_data():
        visualizer.print_summary()
        
        # Save all chart types
        print("\nGenerating and saving charts...")
        visualizer.plot_candlestick_chart(
            save_path=f"{output_dir}/hpg_candlestick.html"
        )
        visualizer.plot_price_and_moving_averages(
            save_path=f"{output_dir}/hpg_ma.png"
        )
        visualizer.plot_volume_analysis(
            save_path=f"{output_dir}/hpg_volume.png"
        )
        visualizer.plot_daily_returns(
            save_path=f"{output_dir}/hpg_returns.png"
        )
        
        print(f"\nAll charts saved to {output_dir}/")


def example_custom_moving_averages():
    """Example 5: Custom moving average periods"""
    print("\n" + "="*60)
    print("Example 5: Custom Moving Averages - FPT stock")
    print("="*60)
    
    visualizer = VNStockVisualizer('FPT')
    
    if visualizer.fetch_data():
        visualizer.print_summary()
        
        # Use custom MA periods: 10, 30, 60 days
        visualizer.plot_price_and_moving_averages(
            ma_periods=[10, 30, 60]
        )


def main():
    """Run all examples"""
    print("\n" + "#"*60)
    print("# VN Stock Visualizer - Example Usage Demonstrations")
    print("#"*60)
    
    try:
        # Run examples
        # Uncomment the examples you want to run
        
        # example_basic_usage()
        # example_custom_date_range()
        example_multiple_stocks()
        # example_save_all_charts()
        # example_custom_moving_averages()
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError running examples: {e}")


if __name__ == "__main__":
    main()
