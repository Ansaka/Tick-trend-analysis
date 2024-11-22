import React, { useState } from 'react';
import StockChart from './components/StockChart';
import './App.css';

function App() {
    const [symbol, setSymbol] = useState('');
    const [date, setDate] = useState('');
    const [showChart, setShowChart] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setShowChart(true);
    };

    return (
        <div className="App">
            <h1>Stock Trend Analysis</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter stock symbol"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                    required
                />
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                />
                <button type="submit">Show Chart</button>
            </form>
            {showChart && <StockChart symbol={symbol} date={date} />}
        </div>
    );
}

export default App;