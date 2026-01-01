# coding=utf-8
from typing import Any, Dict, List

import numpy as np


class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self):
        self.trades: List[Dict[str, Any]] = []
        self.daily_returns: List[float] = []
        self.equity_curve: List[Dict[str, Any]] = []

    def add_trade(self, symbol: str, entry_price: float, exit_price: float,
                  entry_time: str, exit_time: str, shares: int, reason: str = ""):
        """记录交易"""
        returns = (exit_price - entry_price) / entry_price
        trade = {
            'symbol': symbol,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'entry_time': entry_time,
            'exit_time': exit_time,
            'shares': shares,
            'returns': returns,
            'reason': reason
        }
        self.trades.append(trade)

    def record_daily_return(self, date: str, daily_return: float):
        """记录每日收益率"""
        self.daily_returns.append(daily_return)

    def record_equity(self, date: str, equity: float):
        """记录权益曲线"""
        self.equity_curve.append({
            'date': date,
            'equity': equity
        })

    def get_summary(self) -> Dict[str, Any]:
        """获取交易总结"""
        if not self.trades:
            return {}

        returns = [trade['returns'] for trade in self.trades]
        total_return = sum(returns)
        win_rate = len([r for r in returns if r > 0]) / len(returns) if returns else 0
        avg_return = total_return / len(returns) if returns else 0
        max_return = max(returns) if returns else 0
        min_return = min(returns) if returns else 0

        # 计算夏普比率（简化版）
        sharpe_ratio = 0
        if self.daily_returns:
            avg_daily_return = np.mean(self.daily_returns)
            std_daily_return = np.std(self.daily_returns)
            if std_daily_return > 0:
                sharpe_ratio = avg_daily_return / std_daily_return * np.sqrt(252)

        # 计算最大回撤
        max_drawdown = 0
        if self.equity_curve:
            equities = [point['equity'] for point in self.equity_curve]
            peak = equities[0]
            for equity in equities:
                if equity > peak:
                    peak = equity
                drawdown = (peak - equity) / peak
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        return {
            'total_trades': len(self.trades),
            'total_return': total_return,
            'win_rate': win_rate,
            'avg_return': avg_return,
            'max_return': max_return,
            'min_return': min_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown
        }
