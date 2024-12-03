import React, { useState } from 'react';
import StockChart from './StockChart';

const StockChartCard = ({ symbol, startDate, endDate }) => {
    const [showPrice, setShowPrice] = useState(true); // State for price line visibility
    const [showEma38, setShowEma38] = useState(true); // State for EMA 38 visibility
    const [showEma100, setShowEma100] = useState(true); // State for EMA 100 visibility

    return (
        <>
            <div className="stock-chart-card">
                <div className="line-selector">
                    <div className="line-option">
                        <input
                            type="checkbox"
                            checked={showPrice}
                            onChange={() => setShowPrice(!showPrice)}
                        />
                        <span className="color-box" style={{ backgroundColor: '#00ffff' }}></span>
                        <label>Price</label>
                    </div>
                    <div className="line-option">
                        <input
                            type="checkbox"
                            checked={showEma38}
                            onChange={() => setShowEma38(!showEma38)}
                        />
                        <span className="color-box" style={{ backgroundColor: '#ffd700' }}></span>
                        <label>EMA 38</label>
                    </div>
                    <div className="line-option">
                        <input
                            type="checkbox"
                            checked={showEma100}
                            onChange={() => setShowEma100(!showEma100)}
                        />
                        <span className="color-box" style={{ backgroundColor: '#f5f5dc' }}></span>
                        <label>EMA 100</label>
                    </div>
                </div>
                
            </div>
            <StockChart 
                symbol={symbol} 
                startDate={startDate} 
                endDate={endDate} 
                showPrice={showPrice}
                showEma38={showEma38}
                showEma100={showEma100}
            />
        </>
    );
}

export default StockChartCard;