// Vietnamese Stock Market Visualizer - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysisForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const quickAnalyzeBtn = document.getElementById('quickAnalyzeBtn');
    const showStocksBtn = document.getElementById('showStocksBtn');
    const resultsSection = document.getElementById('resultsSection');
    const errorMessage = document.getElementById('errorMessage');
    const modal = document.getElementById('stocksModal');
    const closeModal = document.getElementsByClassName('close')[0];

    // Set default dates
    const today = new Date();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(today.getMonth() - 6);
    
    document.getElementById('end_date').valueAsDate = today;
    document.getElementById('start_date').valueAsDate = sixMonthsAgo;

    // Load popular stocks
    loadPopularStocks();

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeStock();
    });

    // Quick analyze button
    quickAnalyzeBtn.addEventListener('click', function() {
        const symbol = document.getElementById('symbol').value.trim();
        if (!symbol) {
            showError('Please enter a stock symbol');
            return;
        }
        
        // Set dates to last 6 months
        document.getElementById('end_date').valueAsDate = today;
        document.getElementById('start_date').valueAsDate = sixMonthsAgo;
        
        analyzeStock();
    });

    // Show stocks modal
    showStocksBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Close modal
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    function loadPopularStocks() {
        fetch('/api/stocks')
            .then(response => response.json())
            .then(stocks => {
                const stocksList = document.getElementById('stocksList');
                stocksList.innerHTML = '';
                
                stocks.forEach(stock => {
                    const stockItem = document.createElement('div');
                    stockItem.className = 'stock-item';
                    stockItem.innerHTML = `
                        <div class="stock-symbol">${stock.symbol}</div>
                        <div class="stock-name">${stock.name}</div>
                        <div class="stock-sector">${stock.sector}</div>
                    `;
                    stockItem.addEventListener('click', function() {
                        document.getElementById('symbol').value = stock.symbol;
                        modal.style.display = 'none';
                    });
                    stocksList.appendChild(stockItem);
                });
            })
            .catch(error => {
                console.error('Error loading stocks:', error);
            });
    }

    function analyzeStock() {
        const symbol = document.getElementById('symbol').value.trim().toUpperCase();
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        if (!symbol) {
            showError('Please enter a stock symbol');
            return;
        }

        // Show loading state
        setLoading(true);
        hideError();
        resultsSection.style.display = 'none';

        // Make API request
        fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbol: symbol,
                start_date: startDate,
                end_date: endDate
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to analyze stock');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'Failed to analyze stock');
            }
        })
        .catch(error => {
            showError(error.message);
        })
        .finally(() => {
            setLoading(false);
        });
    }

    function displayResults(data) {
        const summary = data.summary;
        const charts = data.charts;

        // Update summary statistics
        document.getElementById('summarySymbol').textContent = summary.symbol;
        document.getElementById('latestPrice').textContent = formatNumber(summary.latest_price) + ' VND';
        document.getElementById('latestDate').textContent = summary.latest_date;
        
        // Price change with color
        const priceChangeEl = document.getElementById('priceChange');
        const priceChangePctEl = document.getElementById('priceChangePct');
        const changeSign = summary.price_change >= 0 ? '+' : '';
        
        priceChangeEl.textContent = changeSign + formatNumber(summary.price_change) + ' VND';
        priceChangePctEl.textContent = changeSign + summary.price_change_pct.toFixed(2) + '%';
        
        if (summary.price_change >= 0) {
            priceChangeEl.classList.add('positive');
            priceChangeEl.classList.remove('negative');
            priceChangePctEl.classList.add('positive');
            priceChangePctEl.classList.remove('negative');
        } else {
            priceChangeEl.classList.add('negative');
            priceChangeEl.classList.remove('positive');
            priceChangePctEl.classList.add('negative');
            priceChangePctEl.classList.remove('positive');
        }

        document.getElementById('highPrice').textContent = formatNumber(summary.highest_price) + ' VND';
        document.getElementById('lowPrice').textContent = formatNumber(summary.lowest_price) + ' VND';
        document.getElementById('avgVolume').textContent = formatNumber(summary.avg_volume);
        document.getElementById('maxVolume').textContent = formatNumber(summary.max_volume);
        document.getElementById('volatility').textContent = summary.volatility.toFixed(2) + '%';
        document.getElementById('dataPoints').textContent = summary.data_points;

        // Update charts
        document.getElementById('candlestickChart').src = charts.candlestick;
        document.getElementById('maChart').src = charts.moving_average;
        document.getElementById('volumeChart').src = charts.volume;
        document.getElementById('returnsChart').src = charts.returns;

        // Show results
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function setLoading(isLoading) {
        const btnText = analyzeBtn.querySelector('.btn-text');
        const spinner = analyzeBtn.querySelector('.spinner');
        
        if (isLoading) {
            btnText.textContent = 'Analyzing...';
            spinner.style.display = 'inline-block';
            analyzeBtn.disabled = true;
            quickAnalyzeBtn.disabled = true;
        } else {
            btnText.textContent = 'Analyze Stock';
            spinner.style.display = 'none';
            analyzeBtn.disabled = false;
            quickAnalyzeBtn.disabled = false;
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function formatNumber(num) {
        return num.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
});
