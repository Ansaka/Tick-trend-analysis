import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SymbolSearch = ({ onSymbolSelect }) => {
    const [search, setSearch] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [userClick, setUserClick] = useState(false);
    useEffect(() => {
        const fetchSymbols = async () => {
            if (search.length < 1 || userClick) {
                setSuggestions([]);
                return;
            }

            setLoading(true);
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/symbols?search=${search}`
                );
                setSuggestions(response.data);
            } catch (error) {
                console.error('Error fetching symbols:', error);
            } finally {
                setLoading(false);
            }
        };

        const timeoutId = setTimeout(fetchSymbols, 300);
        return () => clearTimeout(timeoutId);
    }, [search, userClick]);

    const handleSuggestionClick = (symbol) => {
        onSymbolSelect(symbol);
        setSearch(symbol);
        setUserClick(true);
        setSuggestions([]);
    };

    const handleInputChange = (e) => {
        const value = e.target.value.toUpperCase();
        setSearch(value);
        if (userClick) {
            setUserClick(false)
        }
    };

    return (
        <div className="symbol-search">
            <input
                type="text"
                placeholder="Enter stock symbol"
                value={search}
                onChange={handleInputChange}
                required
            />
            {suggestions.length > 0 && (
                <ul className="suggestions">
                    {suggestions.map((symbol) => (
                        <li 
                            key={symbol}
                            onClick={() => handleSuggestionClick(symbol)}
                        >
                            {symbol}
                        </li>
                    ))}
                </ul>
            )}
            {loading && <div className="loading">Loading...</div>}
        </div>
    );
};

export default SymbolSearch;