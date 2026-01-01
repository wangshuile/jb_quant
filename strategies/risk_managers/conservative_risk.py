# coding=utf-8
from strategies.risk_managers.base_risk import BaseRiskManager
from utils.logger import default_logger as logger
from utils.data_converter import DataConverter

class ConservativeRiskManager(BaseRiskManager):
    """保守型风险管理器"""

    def check_position_limits(self, context, symbol: str, plan_amount: float) -> bool:
        """更严格的仓位限制检查"""
        base_result = super().check_position_limits(context, symbol, plan_amount)
        if not base_result:
            return False
        # 额外检查：单只股票仓位不超过15%
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
        if (current_position_value + plan_amount) > total_assets * 0.15:  # 更严格的限制
            logger.debug(f"保守型单只股票仓位限制: {symbol}")
            return False
        # 额外检查：总仓位不超过60%
        if (total_position_value + plan_amount) > total_assets * 0.6:
            logger.debug("保守型总仓位限制")
            return False
        return True