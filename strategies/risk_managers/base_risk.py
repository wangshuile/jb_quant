# coding=utf-8
from typing import Dict, Tuple, Any

from core.base import PositionRecord, IRiskManager
from utils.data_converter import DataConverter
from utils.logger import default_logger as logger


class BaseRiskManager(IRiskManager):
    """基础风险管理器"""

    def update_position_all(self, context):
        account = context.account()
        positions = account.positions()
        self.position_records = {}
        for pos in positions:
            symbol = pos['symbol']
            volume = pos['volume']
            avg_cost = pos['vwap']
            update_time = pos['updated_at']
            self.update_position_record(context=context, symbol=symbol, avg_cost=avg_cost, volume=volume,update_time=update_time)

    def __init__(self, config):
        self.config = config
        self.position_records: Dict[str, PositionRecord] = {}
        self.today_bought = set()

    def check_position_limits(self, context, symbol: str, plan_amount: float) -> bool:
        """检查仓位限制"""
        try:
            account = context.account()
            cash = DataConverter.safe_float(account.cash)

            positions = account.positions()
            total_position_value = 0
            position_count = 0

            for pos in positions:
                volume = DataConverter.safe_float(pos['volume'])
                price = DataConverter.safe_float(pos['price'])
                position_value = volume * price
                total_position_value += position_value

                if volume > 0:
                    position_count += 1

            total_assets = cash + total_position_value

            if total_assets <= 0:
                return False

            current_position_value = 0
            for pos in positions:
                if pos['symbol'] == symbol:
                    volume = DataConverter.safe_float(pos['volume'])
                    price = DataConverter.safe_float(pos['price'])
                    current_position_value = volume * price
                    break

            # 检查单只股票仓位限制
            if (current_position_value + plan_amount) > total_assets * self.config.max_position_ratio:
                logger.debug(f"单只股票仓位限制: {symbol}")
                return False

            # 检查总仓位限制
            if (total_position_value + plan_amount) > total_assets * self.config.total_position_ratio:
                logger.debug("总仓位限制")
                return False

            # 检查最大持仓数量限制
            if position_count >= self.config.max_positions and current_position_value == 0:
                logger.debug("最大持仓数量限制")
                return False

            return True

        except Exception as e:
            logger.error(f"仓位检查失败: {e}")
            return False

    def check_stop_loss_profit(self, context, symbol: str, current_price: float) -> Tuple[bool, str]:
        """检查止盈止损"""
        if symbol not in self.position_records:
            return False, ""

        if not self.can_sell_today(context, symbol):
            return False, "T+1限制"

        record = self.position_records[symbol]
        avg_cost = record.avg_cost

        if avg_cost <= 0:
            return False, ""

        returns = (current_price - avg_cost) / avg_cost

        # 止损检查
        if returns <= self.config.stop_loss_rate:
            return True, f"止损,收益率:{returns:.2%}"

        # 止盈检查
        if returns >= self.config.stop_profit_rate:
            return True, f"止盈,收益率:{returns:.2%}"

        # 移动止盈
        if current_price > record.highest_price:
            record.highest_price = current_price

        trailing_stop_price = record.highest_price * (1 - self.config.trailing_stop_rate)
        if current_price < trailing_stop_price:
            return True, f"移动止盈,收益率:{returns:.2%}"

        return False, ""

    def can_sell_today(self, context, symbol: str) -> bool:
        """检查是否可以当日卖出"""
        if symbol in self.today_bought:
            return False
        if symbol in self.position_records:
            buy_date = self.position_records[symbol].buy_date
            current_date = context.now.strftime('%Y-%m-%d')
            return buy_date != current_date
        return True

    def update_position_record(self, context, symbol: str, avg_cost: float, volume: int, update_time: Any):
        """更新持仓记录"""
        self.position_records[symbol] = PositionRecord(
            symbol=symbol,
            avg_cost=avg_cost,
            highest_price=avg_cost,
            update_time=update_time,
            buy_date=update_time.strftime('%Y-%m-%d'),
            volume=volume
        )
        if update_time.strftime('%Y-%m-%d') == context.now.strftime('%Y-%m-%d'):
            self.today_bought.add(symbol)

    def reset_daily_flags(self):
        """每日重置标志"""
        self.today_bought.clear()
