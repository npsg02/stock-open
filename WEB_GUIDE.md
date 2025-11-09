# Web Application Guide

## Getting Started

### Starting the Web Server

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python web_app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Web Interface

#### Analyzing a Stock

1. **Enter Stock Symbol**: Type the stock symbol (e.g., VNM, VCB, HPG) in the input field
   - Click "Popular Stocks" to see a list of common Vietnamese stocks

2. **Select Date Range**: Choose start and end dates for your analysis
   - Default is the last 6 months
   - Use "Quick Analyze" button for instant 6-month analysis

3. **Click "Analyze Stock"**: The application will:
   - Fetch stock data from vnstock
   - Generate all visualizations
   - Display comprehensive summary statistics

#### Understanding the Results

The web interface displays:

1. **Summary Statistics Card**
   - Latest Price and Date
   - Price Change (amount and percentage)
   - Price Range (High/Low)
   - Volume Statistics (Average and Maximum)
   - Volatility Measure
   - Number of Data Points

2. **Interactive Candlestick Chart**
   - Fully interactive chart you can zoom and pan
   - Hover over any point for detailed information
   - View both price action and volume

3. **Moving Averages Chart**
   - Price trends with MA20, MA50, and MA100
   - Helps identify trend direction

4. **Volume Analysis Chart**
   - Trading volume with color coding
   - Volume moving average overlay

5. **Daily Returns Chart**
   - Time series of daily percentage returns
   - Distribution histogram

## Popular Vietnamese Stocks

The web interface includes quick access to these popular stocks:

### Banking
- **VCB** - Vietcombank
- **TCB** - Techcombank

### Consumer & Retail
- **VNM** - Vinamilk
- **MSN** - Masan Group
- **MWG** - Mobile World

### Industrial
- **HPG** - Hoa Phat Group

### Technology
- **FPT** - FPT Corporation

### Energy
- **GAS** - PetroVietnam Gas

### Real Estate & Conglomerates
- **VHM** - Vinhomes
- **VIC** - Vingroup

## Features

### Quick Analysis
Click the "Quick Analyze (6 months)" button for instant analysis with default 6-month period.

### Popular Stocks Browser
Click "Popular Stocks" to view and select from a curated list of major Vietnamese stocks organized by sector.

### Responsive Design
The web interface works on:
- Desktop computers
- Tablets
- Mobile phones (responsive layout)

### Real-time Data
All data is fetched in real-time from the vnstock library, ensuring you always get the latest market information.

## Technical Details

### Architecture
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Flask (Python web framework)
- **Data Source**: vnstock library
- **Visualization**: Plotly (interactive), Matplotlib (static)

### API Endpoints

#### `GET /`
Returns the main web interface

#### `POST /api/analyze`
Analyzes a stock and returns data and charts

Request body:
```json
{
  "symbol": "VNM",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

Response:
```json
{
  "success": true,
  "summary": {
    "symbol": "VNM",
    "latest_price": 85000,
    "price_change": 2500,
    "price_change_pct": 3.03,
    ...
  },
  "charts": {
    "candlestick": "/static/charts/...",
    "moving_average": "/static/charts/...",
    ...
  }
}
```

#### `GET /api/stocks`
Returns list of popular Vietnamese stocks

Response:
```json
[
  {
    "symbol": "VNM",
    "name": "Vinamilk",
    "sector": "Consumer"
  },
  ...
]
```

## Deployment

### Local Development
```bash
python web_app.py
```
Server runs on `http://localhost:5000` with debug mode enabled.

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web_app:app"]
```

Build and run:
```bash
docker build -t vn-stock-visualizer .
docker run -p 5000:5000 vn-stock-visualizer
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port
```

### Charts Not Loading
- Ensure the `static/charts/` directory exists and is writable
- Check browser console for errors
- Verify vnstock library is properly installed

### Data Fetch Errors
- Verify internet connectivity
- Check if the stock symbol is valid
- Ensure vnstock library is working: `python -c "import vnstock"`

### Slow Performance
- The first analysis may take longer as data is fetched
- Subsequent analyses of the same stock are faster
- Consider implementing caching for production use

## Customization

### Changing Colors
Edit `static/css/style.css` to customize the color scheme:
```css
/* Change gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding More Stocks
Edit `web_app.py` in the `get_popular_stocks()` function:
```python
stocks = [
    {'symbol': 'YOURSYMBOL', 'name': 'Company Name', 'sector': 'Sector'},
    ...
]
```

### Custom Moving Average Periods
Edit `web_app.py` in the `analyze_stock()` function to change MA periods:
```python
visualizer.plot_price_and_moving_averages(
    ma_periods=[10, 30, 60],  # Custom periods
    save_path=ma_path
)
```

## Support

For issues or questions:
1. Check this guide
2. Review the main README.md
3. Check the USAGE_GUIDE.md for CLI usage
4. Open an issue on GitHub
