import React, { useState, useEffect } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import axios from 'axios';

const StockChart = ({ symbol, startDate, endDate }) => {
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await axios.get(
                    `http://localhost:8000/api/stock-data/${symbol}?start_date=${startDate}&end_date=${endDate}`
                );
                const data = response.data.map(point => [
                    new Date(point.datetime).getTime(),
                    point.price
                ]);
                //console.log('Fetched data:', response.data);
                //console.log('Mapped data:', data);
                setChartData(data);
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
            }
        },
        title: {
            text: `Stock Price: ${symbol}`,
            style: {
                color: '#ffffff'
            }
        },
        rangeSelector: {
            selected: 3,  // 'All' option
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
        series: [{
            name: symbol,
            data: chartData,
            type: 'line',
            color: '#00ffff', // Neon cyan
            lineWidth: 2,
            states: {
                hover: {
                    lineWidth: 3
                }
            }
        }],
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
        yAxis: {
            title: {
                text: 'Price',
                style: {
                    color: '#ffffff'
                }
            },
            labels: {
                style: {
                    color: '#ffffff'
                }
            },
            gridLineColor: '#333'
        },
        tooltip: {
            backgroundColor: 'rgba(45, 45, 45, 0.9)',
            borderColor: '#444',
            style: {
                color: '#ffffff'
            },
            split: false,
            shared: true,
            formatter: function() {
                return `<b>${symbol}</b><br/>
                        Time: ${Highcharts.dateFormat('%H:%M:%S', this.x)}<br/>
                        Price: ${this.y.toFixed(2)}`;
            }
        },
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