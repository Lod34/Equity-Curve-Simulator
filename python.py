import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
from IPython.display import display, HTML

class TradingSimulator:
    def __init__(self, 
                 start_equity: float = 100,
                 win_probability: float = 0.75,
                 win_loss_ratio: float = 3,
                 risk_per_trade: float = 0.01,
                 n_trades: int = 100,
                 n_simulations: int = 100):
        self.start_equity = start_equity
        self.win_probability = win_probability
        self.win_loss_ratio = win_loss_ratio
        self.risk_per_trade = risk_per_trade
        self.n_trades = n_trades
        self.n_simulations = n_simulations
        self.paths = []
        self.stats = {}

    def run_simulation(self) -> None:
        self.paths = []
        final_equities = []
        max_drawdowns = []

        for _ in range(self.n_simulations):
            equity_curve = self._simulate_single_path()
            self.paths.append(equity_curve)
            final_equities.append(equity_curve[-1])
            max_drawdowns.append(self._calculate_max_drawdown(equity_curve))

        self.paths = np.array(self.paths)
        mean_equity = np.mean(self.paths, axis=0)
        median_equity = np.median(self.paths, axis=0)

        # Calcola statistiche
        self.stats = {
            "Kelly": self._calculate_kelly(),
            "Expectation": self.win_probability * self.win_loss_ratio - (1 - self.win_probability),
            "Biggest max drawdown": f"{np.max(max_drawdowns) * 100:.2f}% (€{np.max(max_drawdowns) * self.start_equity:.2f})",
            "Avg. max drawdown": f"{np.mean(max_drawdowns) * 100:.2f}%",
            "Min Equity": f"€{np.min(final_equities):.2f}",
            "Max Equity": f"€{np.max(final_equities):.2f}",
            "Avg. performance": f"{((np.mean(final_equities) / self.start_equity) - 1) * 100:.2f}% (€{np.mean(final_equities) - self.start_equity:.2f})",
            "Median performance": f"{((np.median(final_equities) / self.start_equity) - 1) * 100:.2f}% (€{np.median(final_equities) - self.start_equity:.2f})",
            "Return on max drawdown": f"{(np.mean(final_equities) - self.start_equity) / (np.max(max_drawdowns) * self.start_equity):.2f}",
            "Max consecutive winner": np.max([self._calculate_consecutive_wins_or_losses(path, True) for path in self.paths]),
            "Max consecutive loser": np.max([self._calculate_consecutive_wins_or_losses(path, False) for path in self.paths]),
        }

        self._plot_results(mean_equity, median_equity)
        self._display_results()

    def _simulate_single_path(self) -> np.ndarray:
        equity = self.start_equity
        equity_curve = [equity]

        for _ in range(self.n_trades):
            risk_amount = equity * self.risk_per_trade
            
            if np.random.random() < self.win_probability:
                profit = risk_amount * self.win_loss_ratio
                equity += profit
            else:
                equity -= risk_amount

            equity_curve.append(equity)

        return np.array(equity_curve)

    def _calculate_max_drawdown(self, equity_curve: np.ndarray) -> float:
        peak = equity_curve[0]
        max_drawdown = 0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown

    def _calculate_kelly(self) -> float:
        return self.win_probability - (1 - self.win_probability) / self.win_loss_ratio

    def _calculate_consecutive_wins_or_losses(self, path, is_wins: bool) -> int:
        consecutive = max_consecutive = 0
        for i in range(1, len(path)):
            if (path[i] > path[i - 1]) == is_wins:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0
        return max_consecutive

    def _plot_results(self, mean_equity: np.ndarray, median_equity: np.ndarray) -> None:
        plt.figure(figsize=(12, 8))
        colors = np.random.rand(len(self.paths), 3)
        for path, color in zip(self.paths, colors):
            plt.plot(path, alpha=0.5, color=color)
        plt.plot(mean_equity, color='black', linewidth=2, label='Media')
        plt.plot(median_equity, color='white', linewidth=2, label='Mediana')
        plt.grid(True)
        plt.xlabel('# trade', fontsize=14, color='white')
        plt.ylabel('equity', fontsize=14, color='white')
        plt.legend()
        plt.title('Simulazione Trading System', fontsize=16, color='white')
        plt.tight_layout()
        plt.show()

    def _display_results(self):
        html_table = "<table style='width:70%;border:1px solid #444;background-color:#222;color:#fff;border-collapse:collapse;margin-top:20px;'>"
        html_table += "<tr style='background-color:#333;'><th style='border:1px solid #444;padding:8px;text-align:left;'>Statistica</th><th style='border:1px solid #444;padding:8px;text-align:left;'>Valore</th></tr>"
        for stat, value in self.stats.items():
            html_table += f"<tr><td style='border:1px solid #444;padding:8px;'>{stat}</td><td style='border:1px solid #444;padding:8px;'>{value}</td></tr>"
        html_table += "</table>"
        display(HTML(html_table))


def run_interactive_simulation(start_equity, win_probability_percent, risk_percent, profit_loss_ratio, n_trades, n_simulations):
    win_probability = win_probability_percent / 100
    risk_per_trade = risk_percent / 100

    simulator = TradingSimulator(
        start_equity=start_equity,
        win_probability=win_probability,
        win_loss_ratio=profit_loss_ratio,
        risk_per_trade=risk_per_trade,
        n_trades=n_trades,
        n_simulations=n_simulations
    )
    simulator.run_simulation()


# Eseguiamo l'interfaccia interattiva
interact(
    run_interactive_simulation,
    start_equity=widgets.FloatSlider(
        value=100, min=10, max=1000, step=10,
        description='Capitale Iniziale (€):',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    ),
    win_probability_percent=widgets.IntSlider(
        value=75, min=10, max=99, step=1,
        description='Probabilità Vincita (%):',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    ),
    risk_percent=widgets.FloatSlider(
        value=1, min=0.1, max=10, step=0.1,
        description='Rischio (%):',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    ),
    profit_loss_ratio=widgets.FloatSlider(
        value=3, min=1, max=10, step=0.1,
        description='Rapporto Profitto/Rischio:',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    ),
    n_trades=widgets.IntSlider(
        value=100, min=10, max=500, step=10,
        description='Numero Trade:',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    ),
    n_simulations=widgets.IntSlider(
        value=100, min=10, max=500, step=10,
        description='Numero Simulazioni:',
        style={'description_width': '200px'},
        layout=widgets.Layout(width='80%'),
        continuous_update=True
    )
)
