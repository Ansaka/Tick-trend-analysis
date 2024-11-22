import React, { useState } from 'react';
import StockChart from './components/StockChart';
import './App.css';
import SymbolSearch from './components/SymbolSearch';
import Navbar from './components/Navbar';

function App() {
    const [symbol, setSymbol] = useState('');
    const [startDate, setStartDate] = useState('2021-11-08');
    const [endDate, setEndDate] = useState('2021-11-14');
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
            <Navbar />
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <SymbolSearch onSymbolSelect={handleSymbolSelect} />
                    <div className="date-inputs">
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            min="2021-11-08"
                            max="2021-11-14"
                            required
                        />
                        <input
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            min="2021-11-08"
                            max="2021-11-14"
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