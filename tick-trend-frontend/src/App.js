import React, { useState } from 'react';
import StockChart from './components/StockChart';
import './App.css';
import SymbolSearch from './components/SymbolSearch';

function App() {
    const [symbol, setSymbol] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [showChart, setShowChart] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!symbol || !startDate || !endDate) {
            return;
        }
        setShowChart(true);
    };

    const handleSymbolSelect = (selectedSymbol) => {
        setSymbol(selectedSymbol);
        setShowChart(false); // Reset chart when new symbol is selected
    };

    return (
        <div className="App">
            <h1>Golden Cross+</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <SymbolSearch onSymbolSelect={handleSymbolSelect} />
                    <div className="date-inputs">
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            required
                        />
                        <input
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" disabled={!symbol || !startDate || !endDate}>
                        Show Chart
                    </button>
                </div>
            </form>
            {showChart && <StockChart symbol={symbol} startDate={startDate} endDate={endDate} />}
        </div>
    );
}

export default App;