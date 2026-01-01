# coding=utf-8
import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TradingConfig:
    """交易配置数据类"""
    # 基础配置【BACKTEST:回测模式, MODE_LIVE:模拟盘实盘模式】
    mode: str = 'BACKTEST'
    strategy_id: str = "策略id"
    token: str = os.getenv('GM_TOKEN', '掘金量化token')
    benchmark: str = "SHSE.000300"
    strategy_name: str = "策略名称"
    # AI-token
    ai_token: str = "deepseek服务token"

    # 选股配置
    stock_pool_size: int = 300  # 股票池大小
    max_positions: int = 3  # 最大持仓

    # 仓位配置
    max_position_ratio: float = 0.34  # 单只股票的最大持仓
    total_position_ratio: float = 1  # 总持仓比率

    # 风险控制
    stop_loss_rate: float = -0.08  # 止损
    stop_profit_rate: float = 0.15  # 止盈
    trailing_stop_rate: float = 0.05  # 高点回测百分之5止盈
    trade_pe_value: float = 30.0  # 买入前pe大小

    # 择时配置
    timing_enabled: bool = True
    trading_start_time: str = "09:30:00"
    trading_end_time: str = "14:55:00"

    # 回测配置
    backtest_start: str = "2019-01-01 08:00:00"
    backtest_end: str = "2025-12-23 16:00:00"
    initial_cash: float = 1000000
    commission_ratio: float = 0.0003
    slippage_ratio: float = 0.0001
    # 回测成交比例, 默认 1.0, 即下单 100%成交
    backtest_transaction_ratio: float = 1.0

    # 策略组件选择
    data_manager_type: str = "fixed"  # fixed, index 1.选择股票池【】
    stock_selection_type: str = "momentum"  # momentum, mean_reversion,volatility  2.选择股票评分系统【】
    timing_strategy_type: str = "ma"  # ma, momentum, rsi  3.计算交易信号【】
    trade_executor_type: str = "base"  # base, limit,vwap   4.执行交易指令【】
    risk_manager_type: str = "base"  # base, conservative, 5.风控系统【】
    black_list: list = None  # 黑名单

    def __post_init__(self):
        self.black_list = [
        ]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'TradingConfig':
        """从字典创建配置"""
        return cls(**config_dict)
