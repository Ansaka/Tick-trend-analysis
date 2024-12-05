import React, { useState, useEffect } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import axios from 'axios';

const StockChart = ({ symbol, startDate, endDate, showEma38, showEma100 }) => {
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [buySignals, setBuySignals] = useState([]);
    const [sellSignals, setSellSignals] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await axios.get(
                    `${process.env.REACT_APP_BACKEND_URL}/api/stock-data/${symbol}?start_date=${startDate}&end_date=${endDate}`
                );
                //console.log(response.data)
                const data = response.data.ema_rows.map(point => ({
                    datetime: new Date(point.datetime).getTime(),
                    price: point.price,
                    ema_38: point.ema_38,
                    ema_100: point.ema_100
                }));
                // Filter signals to include only "BUY"
                const response_signals_buy = response.data.signals.filter(point => point.signal === "BUY").map(point => [
                    new Date(point.datetime).getTime(),
                    point.price
                ]);
                const response_signals_sell = response.data.signals.filter(point => point.signal === "SELL").map(point => [
                    new Date(point.datetime).getTime(),
                    point.price
                ]);
                //console.log(data);
                setChartData(data);
                setBuySignals(response_signals_buy);
                setSellSignals(response_signals_sell);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Error loading chart data. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        if (symbol && startDate && endDate) {
            fetchData();
        }
    }, [symbol, startDate, endDate]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!chartData.length) return <div>No data available for the selected date range.</div>;

    const options = {
        chart: {
            backgroundColor: '#1a1a1a',
            style: {
                color: '#ffffff'
            },
            marginLeft: 25,
            marginRight: 25,
            spacingLeft: 10,
            spacingRight: 10
            
        },
        title: {
            text: `Stock Price: ${symbol}`,
            style: {
                color: '#ffffff'
            }
        },
        rangeSelector: {
            selected: 4,  // 'All' option
            buttons: [{
                type: 'hour',
                count: 1,
                text: '1h'
            }, {
                type: 'hour',
                count: 3,
                text: '3h'
            }, {
                type: 'hour',
                count: 6,
                text: '6h'
            }, {
                type: 'day',
                count: 1,
                text: '1d'
            }, {
                type: 'all',
                text: 'All'
            }],
            buttonTheme: {
                fill: '#2d2d2d',
                stroke: '#444',
                style: {
                        color: '#ffffff'
                },
                states: {
                    hover: {
                        fill: '#444'
                    },
                    select: {
                        fill: '#00ffff',
                        style: {
                            color: '#000000'
                        }
                    }
                }
            },
            inputStyle: {
                color: '#ffffff',
                backgroundColor: '#2d2d2d'
            },
            labelStyle: {
                color: '#ffffff'
            }
        },
        series: [
            {
                name: symbol,
                data: chartData.map(point => [point.datetime, point.price]),
                type: 'line',
                color: '#00ffff',
                lineWidth: 2,
                yAxis: 0,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                tooltip: {
                    pointFormat: 'Price: <b>{point.y:.2f}</b><br/>'
                }
            },
            {
                name: 'Sell signals',
                type: 'scatter',
                color: 'red',
                data: sellSignals,
                marker: {
                    enabled: true,
                    color: 'red',
                    radius: 10,
                    symbol: 'triangle',
                    states: {
                        hover: {
                            enabled: true,
                            fillColor: 'rgba(255, 0, 0, 0.8)',
                            radius: 10,
                            zIndex: 10
                        }
                    }
                },
                tooltip: {
                    pointFormat: 'Signal: <b>Sell</b> at <b>{point.y:.2f}</b><br/>'
                },
            },
            {
                name: 'Buy signals',
                type: 'scatter',
                color: 'green',
                data: buySignals,
                marker: {
                    enabled: true,
                    color: 'green',
                    radius: 8, // Increase the radius for a larger hitbox
                    symbol: 'circle',
                    states: {
                        hover: {
                            enabled: true,
                            fillColor: 'rgba(0, 255, 0, 0.8)',
                            radius: 10,
                            zIndex: 10
                        }
                    }
                },
                tooltip: {
                    pointFormat: 'Signal: <b>Buy</b> at <b>{point.y:.2f}</b><br/>'
                },
            },
            showEma38 ? {
                name: 'EMA 38',
                data: chartData.map(point => [point.datetime, point.ema_38]),
                type: 'line',
                color: '#ffd700',
                lineWidth: 2,
                yAxis: 1,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                tooltip: {
                    pointFormat: 'EMA 38: <b>{point.y:.2f}</b><br/>'
                }
            } : null,
            showEma100 ? {
                name: 'EMA 100',
                data: chartData.map(point => [point.datetime, point.ema_100]),
                type: 'line',
                color: '#f5f5dc',
                lineWidth: 2,
                yAxis: 1,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                tooltip: {
                    pointFormat: 'EMA 100: <b>{point.y:.2f}</b><br/>'
                }
            } : null
        ].filter(Boolean),
        xAxis: {
            type: 'datetime',
            labels: {
                style: {
                    color: '#ffffff'
                },
                format: '{value:%H:%M}'
            },
            gridLineColor: '#333',
            lineColor: '#444',
            tickColor: '#444'
        },
        yAxis: [
            {
                title: {
                    text: 'Price',
                    style: { color: '#ffffff' }
                },
                labels: { style: { color: '#ffffff' } },
                gridLineColor: '#333',
                opposite: true,
                height: '100%', // Full chart height
            },
            {
                title: {
                    text: null // No title for secondary axis
                },
                labels: { style: { color: '#ffffff' }, enabled: false },
                gridLineWidth: '#333',
                opposite: true,
                linkedTo: 0,
            }
        ],
        navigator: {
            maskFill: 'rgba(0, 255, 255, 0.1)',
            handles: {
                backgroundColor: '#00ffff',
                borderColor: '#00ffff'
            },
            series: {
                color: '#00ffff',
                lineWidth: 1
            },
            xAxis: {
                gridLineColor: '#333',
                labels: {
                    style: {
                        color: '#ffffff'
                    }
                }
            },
            outlineColor: '#444',
            outlineWidth: 1
        },
        scrollbar: {
            barBackgroundColor: '#2d2d2d',
            barBorderColor: '#00ffff',
            barBorderWidth: 1,
            buttonBackgroundColor: '#2d2d2d',
            buttonBorderColor: '#00ffff',
            buttonBorderWidth: 1,
            trackBackgroundColor: '#1a1a1a',
            trackBorderColor: '#444',
            trackBorderWidth: 1,
            rifleColor: '#00ffff',
            buttonArrowColor: '#00ffff'
        }
    };

    return (
        <div className="chart-container">
            <HighchartsReact
                highcharts={Highcharts}
                constructorType={'stockChart'}
                options={options}
            />
        </div>
    );
};

export default StockChart;