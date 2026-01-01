# coding=utf-8
import os
import sys
from typing import Optional, Dict, Any
from datetime import datetime
try:
    from gm.api import *
    from config.trading_config import TradingConfig
    from strategy.base_strategy import BaseStrategy
    from strategy.quantitative_strategy import QuantitativeTradingStrategy
    from factory.strategy_factory import StrategyFactory
    from utils.logger import default_logger as logger
except ImportError as e:
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)
    from gm.api import *
    from config.trading_config import TradingConfig
    from strategy.base_strategy import BaseStrategy
    from strategy.quantitative_strategy import QuantitativeTradingStrategy
    from factory.strategy_factory import StrategyFactory
    from utils.logger import default_logger as logger
    logger.debug(f"通过路径修正完成导入: {e}")

# 全局策略实例
strategy: Optional[BaseStrategy] = None


class OrderStatusParser:
    """订单状态解析器，封装订单相关逻辑"""

    @staticmethod
    def get_position_effect_text(effect: int, side: int) -> str:
        """获取开平仓类型文本"""
        position_map = {
            (1, 1): '开多仓',
            (1, 2): '开空仓',
            (2, 1): '平空仓',
            (2, 2): '平多仓'
        }
        return position_map.get((effect, side), '未知操作')

    @staticmethod
    def get_order_type_text(order_type: int) -> str:
        """获取委托类型文本"""
        return '限价' if order_type == 1 else '市价'

    @staticmethod
    def format_datetime(dt) -> str:
        """格式化时间"""
        if hasattr(dt, 'strftime'):
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return str(dt)


def on_backtest_finished(context, indicator: Dict[str, Any]) -> None:
    """回测结束回调函数"""
    try:
        logger.info("=" * 60)
        logger.info("回测完成，汇总结果如下：")
        if indicator:
            # 主要业绩指标
            pnl_ratio = indicator.get('pnl_ratio', 0)
            pnl_ratio_annual = indicator.get('pnl_ratio_annual', 0)
            sharpe = indicator.get('sharpe', 0)
            max_drawdown = indicator.get('max_drawdown', 0)
            logger.info(f"【业绩指标】")
            logger.info(f"  累计收益率: {pnl_ratio:>10.2%}")
            logger.info(f"  年化收益率: {pnl_ratio_annual:>10.2%}")
            logger.info(f"  夏普比率: {sharpe:>13.2f}")
            logger.info(f"  最大回撤: {max_drawdown:>10.2%}")
            # 风险指标
            if 'volatility' in indicator:
                logger.info(f"  波动率: {indicator['volatility']:>13.2%}")
            if 'win_rate' in indicator:
                logger.info(f"  胜率: {indicator['win_rate']:>14.2%}")
            if 'profit_loss_ratio' in indicator:
                logger.info(f"  盈亏比: {indicator['profit_loss_ratio']:>13.2f}")
        # 获取账户信息
        try:
            account = context.account()
            cash = account.cash
            positions = account.positions()
            # 计算持仓价值
            total_position_value = sum(pos['volume'] * pos['price'] for pos in positions)
            total_value = cash.available + total_position_value
            logger.info(f"【账户信息】")
            logger.info(f"  最终总资产: ¥{total_value:>12,.2f}")
            logger.info(f"  可用现金: ¥{cash.available:>13,.2f}")
            logger.info(f"  持仓市值: ¥{total_position_value:>12,.2f}")
            # 持仓统计
            active_positions = [p for p in positions if p['volume'] > 0]
            logger.info(f"  持仓数量: {len(active_positions):>13}")
            if active_positions:
                logger.info(f"  详细持仓:")
                for pos in sorted(active_positions, key=lambda x: x['volume'] * x['price'], reverse=True)[
                           :5]:  # 显示前5大持仓
                    pos_value = pos['volume'] * pos['price']
                    logger.info(f"    - {pos.get('symbol', '未知')}: {pos['volume']}股, 市值: ¥{pos_value:,.2f}")
        except Exception as e:
            logger.warning(f"获取账户详细信息失败: {e}")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"处理回测完成回调时发生错误: {e}")


def on_error(context, code: int, info: str) -> None:
    """错误处理基础回调"""
    logger.error(f"程序异常，需要手动重启，异常代码: {code}, 异常信息: {info}")


def on_order_status(context, order: Dict[str, Any]) -> None:
    """订单状态基础回调"""
    try:
        symbol = order.get('symbol', '未知')
        price = order.get('price', 0)
        volume = order.get('volume', 0)
        value = order.get('value', 0)
        percent = order.get('percent', 0)
        target_percent = order.get('target_percent', 0)
        target_volume = order.get('target_volume', 0)
        target_value = order.get('target_value', 0)
        filled_volume = order.get('filled_volume', 0)
        filled_vwap = order.get('filled_vwap', 0)
        filled_amount = order.get('filled_amount', 0)
        filled_commission = order.get('filled_commission', 0)
        status = order.get('status', -1)
        side = order.get('side', 0)
        effect = order.get('position_effect', 0)
        order_type = order.get('order_type', 0)
        created_at = OrderStatusParser.format_datetime(order.get('created_at'))
        updated_at = OrderStatusParser.format_datetime(order.get('updated_at'))
        ord_rej_reason_detail = order.get("ord_rej_reason_detail", "")
        # 获取操作类型文本
        side_effect = OrderStatusParser.get_position_effect_text(effect, side)
        order_type_word = OrderStatusParser.get_order_type_text(order_type)
        # 构造状态信息
        status_msg = f"委托状态:{status}, 委托时间:{created_at}, 成交时间:{updated_at}"
        # 构造详细信息
        detail_msg = (
            f"操作: 以{order_type_word}方式{side_effect}, "
            f"委托价格: ¥{price:.2f}, 委托数量: {volume:.0f}, 委托金额: ¥{value:.2f}, "
            f"委托仓位: {percent:.2%}, 目标仓位: {target_percent:.2%}, "
            f"目标数量: {target_volume:.0f}, 目标金额: ¥{target_value:.2f}, "
            f"已成交: {filled_volume:.0f}股, 成交金额: ¥{filled_amount:.2f}, "
            f"成交均价: ¥{filled_vwap:.2f}, 手续费: ¥{filled_commission:.2f}, "
            f"状态详情: {ord_rej_reason_detail}"
        )
        # 获取股票名称（如果有）
        stock_name = ""
        if hasattr(context, 'stock_name_list') and symbol in context.stock_name_list:
            stock_name = context.stock_name_list[symbol]
        # 完整消息
        full_msg = f"{status_msg}, 标的: {stock_name or symbol}, {detail_msg}"
        # 更新持仓信息
        strategy.context.risk_manager.update_position_all(context=context)
        # 根据状态选择日志级别
        if status == 3:  # 委托全部成交
            logger.info(full_msg)
        else:
            logger.warning(full_msg)
    except Exception as e:
        logger.error(f"处理订单状态时发生错误: {e}, 订单数据: {order}")


def init(context) -> None:
    """策略初始化函数"""
    global strategy

    try:
        logger.info("🚀 开始初始化策略")
        logger.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # 创建配置
        config = TradingConfig()
        logger.debug(f"配置加载成功，策略ID: {config.strategy_id}")
        # 创建策略工厂
        factory = StrategyFactory()
        # 创建策略实例
        strategy = QuantitativeTradingStrategy(config, factory)
        # 初始化策略
        strategy.init_strategy(context)
        logger.info("✅ 策略初始化完成")
        logger.info(f"策略模式: {config.mode}")
        if config.mode == 'BACKTEST':
            logger.info(f"回测期间: {config.backtest_start} 至 {config.backtest_end}")
            logger.info(f"初始资金: ¥{config.initial_cash:,.2f}")
            logger.info(f"手续费率: {config.commission_ratio:.4%}")
            logger.info(f"滑点率: {config.slippage_ratio:.4%}")
    except Exception as e:
        logger.error(f"❌ 策略初始化失败: {e}")
        logger.exception("初始化详细错误信息:")
        raise


def main() -> None:
    """主函数"""
    try:
        # 创建配置
        config = TradingConfig()
        logger.info("🎯 启动量化交易策略")
        logger.info(f"策略名称: {config.strategy_name or '未命名策略'}")
        logger.info(f"运行模式: {config.mode}")
        if config.mode == 'BACKTEST':
            logger.info("📊 进入回测模式")
            # 验证回测参数
            if not config.backtest_start or not config.backtest_end:
                raise ValueError("回测开始时间或结束时间未设置")
            run_params = {
                'strategy_id': config.strategy_id,
                'filename':"main.py",
                'mode': MODE_BACKTEST,
                'token': config.token,
                'backtest_start_time': config.backtest_start,
                'backtest_end_time': config.backtest_end,
                'backtest_initial_cash': config.initial_cash,
                'backtest_commission_ratio': config.commission_ratio,
                'backtest_slippage_ratio': config.slippage_ratio
            }
            # 添加可选参数
            if hasattr(config, 'backtest_transaction_ratio'):
                run_params['backtest_transaction_ratio'] = config.backtest_transaction_ratio
            logger.info(f"回测参数: {run_params}")
            # 执行回测
            run(**run_params)
        else:
            logger.info("💰 进入实盘交易模式")
            logger.warning("注意：实盘交易有风险，请谨慎操作！")
            run(
                strategy_id=config.strategy_id,
                filename="main.py",
                mode=MODE_LIVE,
                token=config.token
            )
    except KeyboardInterrupt:
        logger.info("⏹️ 用户中断策略执行")
    except Exception as e:
        logger.error(f"❌ 策略运行失败: {e}")
        logger.error("详细错误信息:")
        sys.exit(1)


if __name__ == '__main__':
    main()