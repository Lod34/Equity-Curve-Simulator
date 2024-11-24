document.getElementById("startButton").addEventListener("click", function() {
    runSimulation();
});

function runSimulation() {
    // Simula dei dati di trading (esempio)
    const nTrades = 100;
    const probabilities = [0.75, 0.25];
    let equity = 100;
    const equityCurve = [equity];

    for (let i = 0; i < nTrades; i++) {
        const isWin = Math.random() < probabilities[0];
        const profitLoss = isWin ? 3 : -1; // Profitto per vittoria, perdita per sconfitta
        equity += profitLoss;
        equityCurve.push(equity);
    }

    // Crea grafico con Chart.js
    const ctx = document.getElementById("chart").getContext("2d");
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: nTrades + 1}, (_, i) => `Trade ${i}`),
            datasets: [{
                label: 'Equity Curve',
                data: equityCurve,
                borderColor: '#00aaff',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
            },
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    min: 0,
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        }
    });

    // Animazione della transizione dei dati
    animateResults();
    updateStats({
        kelly: "0.67",
        expectation: "2.00",
        maxDrawdown: "6.8% (€25.00)",
        avgMaxDrawdown: "5.5%",
        minEquity: "€50.00",
        maxEquity: "€200.00",
        avgPerformance: "50% (€50.00)",
        medianPerformance: "48% (€48.00)",
        returnOnMaxDrawdown: "2.5",
        maxConsecutiveWinner: 10,
        maxConsecutiveLoser: 5
    });
}

// Funzione per animare i risultati
function animateResults() {
    anime({
        targets: '#kelly',
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 1500,
        easing: 'easeOutQuad'
    });

    anime({
        targets: '#expectation',
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 2000,
        easing: 'easeOutQuad'
    });

    anime({
        targets: '#maxDrawdown',
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 2500,
        easing: 'easeOutQuad'
    });
}

function updateStats(stats) {
    document.getElementById('kelly').innerText = `Kelly: ${stats.kelly}`;
    document.getElementById('expectation').innerText = `Expectancy: ${stats.expectation}`;
    document.getElementById('maxDrawdown').innerText = `Max Drawdown: ${stats.maxDrawdown}`;
    document.getElementById('avgMaxDrawdown').innerText = `Avg. Max Drawdown: ${stats.avgMaxDrawdown}`;
    document.getElementById('minEquity').innerText = `Min Equity: ${stats.minEquity}`;
    document.getElementById('maxEquity').innerText = `Max Equity: ${stats.maxEquity}`;
    document.getElementById('avgPerformance').innerText = `Avg. Performance: ${stats.avgPerformance}`;
    document.getElementById('medianPerformance').innerText = `Median Performance: ${stats.medianPerformance}`;
    document.getElementById('returnOnMaxDrawdown').innerText = `Return on Max Drawdown: ${stats.returnOnMaxDrawdown}`;
    document.getElementById('maxConsecutiveWinner').innerText = `Max Consecutive Winner: ${stats.maxConsecutiveWinner}`;
    document.getElementById('maxConsecutiveLoser').innerText = `Max Consecutive Loser: ${stats.maxConsecutiveLoser}`;
}

// Animazione dei trades simulati
function animateTrades() {
    const trades = document.getElementById("simulatedTrades");
    const trade = document.createElement("div");
    trade.style.height = "20px";
    trade.style.backgroundColor = "#00aaff";
    trade.style.width = "20px";
    trade.style.position = "absolute";
    trade.style.bottom = "0";
    trades.appendChild(trade);

    anime({
        targets: trade,
        translateX: 100,
        translateY: 100,
        duration: 1500,
        easing: 'easeInOutQuad',
        complete: () => {
            trades.removeChild(trade);
        }
    });
}
