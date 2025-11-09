# Vietnamese Stock Market Data Visualization Tool

A comprehensive tool for visualizing Vietnamese stock market data using the `vnstock` library. Available as both a **web application** and **command-line tool** with various visualization options including candlestick charts, moving averages, volume analysis, and returns distribution.

## Features

- 🌐 **Web Application** - Modern, user-friendly web interface for analyzing stocks
- 📊 **Interactive Candlestick Charts** - View OHLC data with volume in an interactive Plotly chart
- 📈 **Moving Averages** - Visualize price trends with customizable moving averages (MA20, MA50, MA100)
- 📉 **Volume Analysis** - Analyze trading volume with color-coded bars and moving averages
- 💹 **Daily Returns** - View daily returns over time and distribution histogram
- 📋 **Summary Statistics** - Get comprehensive statistics including price range, volatility, and volume metrics
- 🚀 **Quick Analysis** - One-click analysis for popular Vietnamese stocks

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

Start the web server:

```bash
python web_app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The web interface allows you to:
- Select from popular Vietnamese stocks or enter any stock symbol
- Choose custom date ranges or use quick 6-month analysis
- View all charts and statistics in one interactive dashboard
- Export and save analysis results

### Command Line Interface

#### Basic Usage

Visualize a stock for the last 6 months (default):

```bash
python vn_stock_visualizer.py VNM
```

#### Custom Date Range

Specify custom start and end dates:

```bash
python vn_stock_visualizer.py VCB --start 2023-01-01 --end 2023-12-31
```

#### Save Charts to Files

Generate and save all charts to files:

```bash
python vn_stock_visualizer.py HPG --save-charts
```

Specify custom output directory:

```bash
python vn_stock_visualizer.py VNM --save-charts --output-dir ./my_charts
```

### Python API

You can also use the tool programmatically in your Python scripts:

```python
from vn_stock_visualizer import VNStockVisualizer

# Create visualizer instance
visualizer = VNStockVisualizer('VNM', start_date='2023-01-01', end_date='2023-12-31')

# Fetch data
visualizer.fetch_data()

# Print summary statistics
visualizer.print_summary()

# Generate visualizations
visualizer.plot_candlestick_chart()  # Interactive chart
visualizer.plot_price_and_moving_averages(ma_periods=[20, 50, 100])
visualizer.plot_volume_analysis()
visualizer.plot_daily_returns()

# Save charts to files
visualizer.plot_candlestick_chart(save_path='vnm_candlestick.html')
visualizer.plot_price_and_moving_averages(save_path='vnm_ma.png')
```

## Popular Vietnamese Stock Symbols

Here are some popular Vietnamese stock symbols you can analyze:

- **VNM** - Vinamilk (Dairy products)
- **VCB** - Vietcombank (Banking)
- **HPG** - Hoa Phat Group (Steel)
- **VHM** - Vinhomes (Real estate)
- **VIC** - Vingroup (Conglomerate)
- **MSN** - Masan Group (Consumer goods)
- **FPT** - FPT Corporation (Technology)
- **GAS** - PetroVietnam Gas (Gas distribution)
- **TCB** - Techcombank (Banking)
- **MWG** - Mobile World (Retail electronics)

## Output Examples

The tool generates four types of visualizations:

1. **Candlestick Chart (HTML)** - Interactive chart showing OHLC data and volume
2. **Moving Averages (PNG)** - Line chart with price and multiple moving averages
3. **Volume Analysis (PNG)** - Price and volume charts with color-coded bars
4. **Daily Returns (PNG)** - Time series of daily returns and distribution histogram

## Command Line Arguments

```
positional arguments:
  symbol                Stock symbol (e.g., VNM, VCB, HPG)

optional arguments:
  -h, --help            show this help message and exit
  --start START         Start date (YYYY-MM-DD)
  --end END             End date (YYYY-MM-DD)
  --save-charts         Save charts to files instead of displaying
  --output-dir OUTPUT_DIR
                        Directory to save charts (default: ./charts)
```

## Dependencies

- **vnstock** (>=3.2.6) - Vietnamese stock data library
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **matplotlib** (>=3.7.0) - Static chart generation
- **plotly** (>=5.17.0) - Interactive chart generation
- **numpy** (>=1.24.0) - Numerical computing

## Troubleshooting

### Installation Issues

If you encounter issues installing vnstock, try these alternatives:

```bash
# Option 1: Install with specific version
pip install vnstock==3.2.6

# Option 2: Install latest version
pip install vnstock

# Option 3: Install with no cache (if download issues)
pip install --no-cache-dir vnstock
```

### Testing Without vnstock

To test the visualization functionality without installing vnstock (useful for development):

```bash
python test_visualizer.py
```

This will run tests using mock data to verify all visualization functions work correctly.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.