#!/usr/bin/env python3
"""
Web-based Vietnamese Stock Market Data Visualization Tool
Flask web application for visualizing VN stock market data
"""

from flask import Flask, render_template, request, jsonify, send_file
from vn_stock_visualizer import VNStockVisualizer
import os
import json
from datetime import datetime, timedelta
import io
import base64

app = Flask(__name__)

# Create output directory for charts
CHART_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'charts')
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """Analyze stock and return data"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not symbol:
            return jsonify({'error': 'Stock symbol is required'}), 400
        
        # Create visualizer
        visualizer = VNStockVisualizer(symbol, start_date, end_date)
        
        # Fetch data
        if not visualizer.fetch_data():
            return jsonify({'error': f'Failed to fetch data for {symbol}'}), 400
        
        # Get summary statistics
        if visualizer.data is None or visualizer.data.empty:
            return jsonify({'error': 'No data available'}), 400
        
        latest = visualizer.data.iloc[-1]
        first = visualizer.data.iloc[0]
        
        price_change = latest['close'] - first['close']
        price_change_pct = (price_change / first['close']) * 100
        
        daily_returns = visualizer.data['close'].pct_change()
        volatility = daily_returns.std() * 100
        
        summary = {
            'symbol': symbol,
            'latest_price': float(latest['close']),
            'latest_date': visualizer.data.index[-1].strftime('%Y-%m-%d'),
            'highest_price': float(visualizer.data['high'].max()),
            'lowest_price': float(visualizer.data['low'].min()),
            'price_change': float(price_change),
            'price_change_pct': float(price_change_pct),
            'avg_volume': float(visualizer.data['volume'].mean()),
            'max_volume': float(visualizer.data['volume'].max()),
            'volatility': float(volatility),
            'data_points': len(visualizer.data)
        }
        
        # Generate charts
        chart_id = f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        candlestick_path = os.path.join(CHART_OUTPUT_DIR, f'{chart_id}_candlestick.html')
        ma_path = os.path.join(CHART_OUTPUT_DIR, f'{chart_id}_ma.png')
        volume_path = os.path.join(CHART_OUTPUT_DIR, f'{chart_id}_volume.png')
        returns_path = os.path.join(CHART_OUTPUT_DIR, f'{chart_id}_returns.png')
        
        visualizer.plot_candlestick_chart(save_path=candlestick_path)
        visualizer.plot_price_and_moving_averages(save_path=ma_path)
        visualizer.plot_volume_analysis(save_path=volume_path)
        visualizer.plot_daily_returns(save_path=returns_path)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'charts': {
                'candlestick': f'/static/charts/{chart_id}_candlestick.html',
                'moving_average': f'/static/charts/{chart_id}_ma.png',
                'volume': f'/static/charts/{chart_id}_volume.png',
                'returns': f'/static/charts/{chart_id}_returns.png'
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/stocks')
def get_popular_stocks():
    """Return list of popular Vietnamese stocks"""
    stocks = [
        {'symbol': 'VNM', 'name': 'Vinamilk', 'sector': 'Consumer'},
        {'symbol': 'VCB', 'name': 'Vietcombank', 'sector': 'Banking'},
        {'symbol': 'HPG', 'name': 'Hoa Phat Group', 'sector': 'Industrial'},
        {'symbol': 'VHM', 'name': 'Vinhomes', 'sector': 'Real Estate'},
        {'symbol': 'VIC', 'name': 'Vingroup', 'sector': 'Conglomerate'},
        {'symbol': 'MSN', 'name': 'Masan Group', 'sector': 'Consumer'},
        {'symbol': 'FPT', 'name': 'FPT Corporation', 'sector': 'Technology'},
        {'symbol': 'GAS', 'name': 'PetroVietnam Gas', 'sector': 'Energy'},
        {'symbol': 'TCB', 'name': 'Techcombank', 'sector': 'Banking'},
        {'symbol': 'MWG', 'name': 'Mobile World', 'sector': 'Retail'},
    ]
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
