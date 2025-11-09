# Vietnamese Stock Market Visualization Tool - Usage Guide

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```bash
# Visualize VNM stock (Vinamilk) for the last 6 months
python vn_stock_visualizer.py VNM
```

## Detailed Usage Examples

### Command Line Interface

#### Example 1: Quick Visualization
Analyze VNM stock with default settings (last 6 months):
```bash
python vn_stock_visualizer.py VNM
```

#### Example 2: Custom Date Range
Analyze VCB stock for the year 2023:
```bash
python vn_stock_visualizer.py VCB --start 2023-01-01 --end 2023-12-31
```

#### Example 3: Save All Charts
Generate and save all chart types to files:
```bash
python vn_stock_visualizer.py HPG --save-charts
```

#### Example 4: Custom Output Directory
Save charts to a specific directory:
```bash
python vn_stock_visualizer.py FPT --save-charts --output-dir ./my_analysis
```

### Python API

#### Example 1: Basic API Usage
```python
from vn_stock_visualizer import VNStockVisualizer

# Create visualizer for VNM stock
visualizer = VNStockVisualizer('VNM')

# Fetch data
visualizer.fetch_data()

# Display summary statistics
visualizer.print_summary()

# Generate interactive candlestick chart
visualizer.plot_candlestick_chart()
```

#### Example 2: Custom Date Range
```python
from vn_stock_visualizer import VNStockVisualizer

# Create visualizer with specific date range
visualizer = VNStockVisualizer(
    symbol='VCB',
    start_date='2023-01-01',
    end_date='2023-12-31'
)

# Fetch and analyze
visualizer.fetch_data()
visualizer.print_summary()
```

#### Example 3: Generate All Charts
```python
from vn_stock_visualizer import VNStockVisualizer

visualizer = VNStockVisualizer('HPG')
visualizer.fetch_data()

# Generate all chart types
visualizer.plot_candlestick_chart(save_path='hpg_candles.html')
visualizer.plot_price_and_moving_averages(save_path='hpg_ma.png')
visualizer.plot_volume_analysis(save_path='hpg_volume.png')
visualizer.plot_daily_returns(save_path='hpg_returns.png')
```

#### Example 4: Custom Moving Averages
```python
from vn_stock_visualizer import VNStockVisualizer

visualizer = VNStockVisualizer('FPT')
visualizer.fetch_data()

# Use custom MA periods: 10, 30, 60 days
visualizer.plot_price_and_moving_averages(ma_periods=[10, 30, 60])
```

#### Example 5: Compare Multiple Stocks
```python
from vn_stock_visualizer import VNStockVisualizer

stocks = ['VNM', 'VCB', 'HPG']

for symbol in stocks:
    visualizer = VNStockVisualizer(symbol)
    if visualizer.fetch_data():
        visualizer.print_summary()
```

## Chart Types

### 1. Candlestick Chart (Interactive HTML)
- OHLC (Open, High, Low, Close) candlestick visualization
- Volume bars below the price chart
- Color-coded volume (red for down days, green for up days)
- Interactive zoom and pan
- Hover for detailed information

### 2. Moving Averages Chart (PNG)
- Closing price line
- Multiple moving averages (default: MA20, MA50, MA100)
- Customizable MA periods
- Grid for easy reading

### 3. Volume Analysis Chart (PNG)
- Price chart on top
- Volume bars on bottom with color coding
- Volume moving average (20-day by default)
- Shows correlation between price and volume

### 4. Daily Returns Chart (PNG)
- Time series of daily percentage returns
- Histogram showing return distribution
- Zero line reference
- Helps identify volatility and patterns

## Popular Vietnamese Stocks

### Banking Sector
- **VCB** - Vietcombank
- **TCB** - Techcombank
- **BID** - BIDV
- **CTG** - VietinBank

### Consumer & Retail
- **VNM** - Vinamilk (Dairy)
- **MSN** - Masan Group
- **MWG** - Mobile World (Electronics)

### Industrial & Manufacturing
- **HPG** - Hoa Phat Group (Steel)
- **GAS** - PetroVietnam Gas

### Real Estate & Conglomerates
- **VHM** - Vinhomes
- **VIC** - Vingroup

### Technology
- **FPT** - FPT Corporation

## Output Files

When using `--save-charts`, the tool generates:

1. `{SYMBOL}_candlestick.html` - Interactive candlestick chart (4-5 MB)
2. `{SYMBOL}_ma.png` - Moving averages chart (300-500 KB)
3. `{SYMBOL}_volume.png` - Volume analysis chart (300-400 KB)
4. `{SYMBOL}_returns.png` - Daily returns chart (300-500 KB)

## Summary Statistics

The tool provides comprehensive statistics:
- Latest closing price and date
- Price range (highest and lowest)
- Price change and percentage change over the period
- Average daily volume
- Highest volume day
- Daily volatility (standard deviation of returns)

## Tips for Analysis

1. **Trend Identification**: Use moving averages to identify trends
   - Price above MA = Uptrend
   - Price below MA = Downtrend

2. **Volume Confirmation**: High volume on price increases confirms strength

3. **Volatility Assessment**: Check daily returns distribution for risk

4. **Time Periods**: 
   - Short-term: 1-3 months
   - Medium-term: 6 months
   - Long-term: 1+ years

## Troubleshooting

### Issue: vnstock not installing
**Solution**: Try installing with specific version:
```bash
pip install vnstock==3.2.6
```

### Issue: Charts not displaying
**Solution**: Use `--save-charts` to save to files instead:
```bash
python vn_stock_visualizer.py VNM --save-charts
```

### Issue: No data retrieved
**Possible causes**:
- Invalid stock symbol
- No trading on selected dates
- Network connectivity issues

**Solution**: Verify stock symbol and date range, check internet connection

## Testing

To test the tool without fetching real data:
```bash
python test_visualizer.py
```

This generates test charts using mock data to verify all functions work correctly.

## Support

For issues or questions:
1. Check this usage guide
2. Review the main README.md
3. Open an issue on GitHub
