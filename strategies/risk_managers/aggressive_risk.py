# coding=utf-8
from strategies.risk_managers.base_risk import BaseRiskManager
from utils.logger import default_logger as logger
from utils.data_converter import DataConverter

class AggressiveRiskManager(BaseRiskManager):
    """激进型风险管理器"""

    def check_position_limits(self, context, symbol: str, plan_amount: float) -> bool:
        """更宽松的仓位限制检查"""
        base_result = super().check_position_limits(context, symbol, plan_amount)

        if not base_result:
            return False
        # 允许更高的单只股票仓位（40%）
        account = context.account()
        cash = DataConverter.safe_float(account.cash)
        positions = account.positions()
        total_position_value = 0
        for pos in positions:
            volume = DataConverter.safe_float(pos['volume'])
            price = DataConverter.safe_float(pos['price'])
            total_position_value += volume * price
        total_assets = cash + total_position_value

        current_position_value = 0
        for pos in positions:
            if pos['symbol'] == symbol:
                volume = DataConverter.safe_float(pos['volume'])
                price = DataConverter.safe_float(pos['price'])
                current_position_value = volume * price
                break

        if (current_position_value + plan_amount) > total_assets * 0.4:  # 更宽松的限制
            logger.debug(f"激进型单只股票仓位限制: {symbol}")
            return False

        # 允许更高的总仓位（90%）
        if (total_position_value + plan_amount) > total_assets * 0.9:
            logger.debug("激进型总仓位限制")
            return False

        return True
