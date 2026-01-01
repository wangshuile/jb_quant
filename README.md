# 📈 Python量化交易策略框架

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![掘金量化](https://img.shields.io/badge/平台-掘金量化-orange.svg)](https://www.myquant.cn/)
[![量化投资](https://img.shields.io/badge/领域-量化投资-purple.svg)](https://mp.weixin.qq.com/s/PmfgMf8AaauF2mKwT96VLA)

**关键词**：量化交易、股票策略、Python量化、掘金量化、回测系统、风险管理、算法交易、选股策略、择时策略

# jb_quant量化交易策略框架

一个基于掘金量化平台的模块化量化交易策略框架，采用面向对象设计和策略模式，支持灵活的策略组件组合和扩展。

## 🎯 核心特性

- **🏗️ 模块化架构**：采用策略模式，各个组件可独立开发、测试和替换
- **📊 多样化策略**：支持动量、均值回归、波动率等多种选股策略
- **⏰ 智能择时**：集成移动平均线、RSI、动量等多种择时策略
- **🛡️ 多层风控**：基础/保守/激进三种风险管理模式，支持止盈止损
- **💾 数据管理**：支持固定股票池和指数成分股，内置智能缓存
- **⚡ 高性能**：优化数据访问性能，支持多种交易执行方式

## 📁 项目结构

```
jb_quant/
├── main.py                    # 主策略入口文件
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目说明文档
│
├── config/                    # 配置文件目录
│   └── trading_config.py      # 交易配置类
│
├── core/                      # 配置文件目录
│   ├── base.py                # 基础类，包含实体对象定义与接口定义
│   └── context.py             # 策略上下文对象类
│
├── factor/                      # 多因子文件目录【计算多因子信息】
│
├── factory/                   # 策略工厂文件目录
│   └── strategy_factory.py    # 策略工厂类
│
├── strategies/                  # 策略实现目录
│   ├── timing_strategies/       # 择时策略
│   │   ├── base_timing.py       # 基础择时策略
│   │   ├── ma_timing.py         # 移动平均线择时
│   │   └── disabled_timing.py   # 禁用择时策略
│   │   └── mom_timing.py        # 动量择时策略
│   │   └── rsi_timing.py        # RSI择时策略
│   │
│   ├── selection_strategies/ # 选股策略
│   │   ├── base_selection.py            # 基础选股
│   │   ├── mean_reversion_selection.py  # 均值回归选股
│   │   ├── momentum_selection.py        # 动量选股
│   │   └── volatility_selection.py      # 波动率选股
│   │
│   └── risk_managers/       # 风险管理器
│       ├── base_risk.py     # 基础风控
│       ├── conservative_risk.py  # 保守风控
│       └── aggressive_risk.py    # 激进风控
│
├── data/                            # 数据管理目录
│   ├── base_data_manager.py         # 数据管理器基类
│   ├── fixed_data_manager.py        # 固定数据管理器基类
│   └── index_data_manager.py        # 指数成分股数据管理器基类
│
├── trading/                  # 交易执行目录
│   ├── base_executor.py      # 交易执行器基类
│   ├── vmap_executor.py      # VWAP交易执行器
│   └── limit_executor.py     # 限价执行器、
│
├── strategy/                       # 量化交易策略目录
│   ├── base_strategy.py            # 策略基类
│   └── quantitative_strategy.py    # 量化交易策略主类
│
└── utils/                   # 工具类目录
    ├── logger.py            # 日志配置
    ├── cache_manager.py     # 缓存管理器
    ├── data_converter.py    # 数据转换工具
    └── performance_analyzer.py # 性能分析器

```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd jb_quant

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置掘金Token

**方法一：修改配置文件**
在 `config/trading_config.py` 中设置你的掘金token:

```python
token: str = '你的掘金token'
```

**方法二：设置环境变量**
```bash
# Windows
set GM_TOKEN='你的掘金token'
```

### 3. 运行回测

```bash
# 基础回测
python main.py

# 指定回测参数（通过修改配置文件）
# 在 trading_config.py 中设置：
# - backtest_start: 回测开始时间
# - backtest_end: 回测结束时间
# - initial_cash: 初始资金
```

### 4. 配置策略组合

在 `trading_config.py` 配置文件中调整策略组合：

```python
# 示例：创建自定义策略配置
data_manager_type="index",          # 使用指数成分股
timing_strategy_type="ma",          # 移动平均线择时
stock_selection_type="momentum",    # 动量选股
risk_manager_type="conservative",   # 保守风控
trade_executor_type="limit",        # 限价交易
stock_pool_size=20,                 # 股票池大小
max_positions=5,                    # 最大持仓数
timing_enabled=True                  # 启用择时
```

## ⚙️ 配置说明

### 核心配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data_manager_type` | str | `"index"` | 数据管理器类型：`"fixed"`或`"index"` |
| `timing_strategy_type` | str | `"disabled"` | 择时策略：`"disabled"`、`"ma"`、`"rsi"`、`"momentum"` |
| `stock_selection_type` | str | `"momentum"` | 选股策略：`"momentum"`、`"mean_reversion"`、`"volatility"` |
| `risk_manager_type` | str | `"base"` | 风控类型：`"base"`、`"conservative"`、`"aggressive"` |
| `trade_executor_type` | str | `"base"` | 交易执行：`"base"`、`"limit"`、`"vwap"` |

### 风险控制参数

```python
# 止损止盈配置
stop_loss_rate = -0.08      # 止损比例 -8%
stop_profit_rate = 0.15     # 止盈比例 15%
trailing_stop_rate = 0.05   # 移动止盈比例 5%
max_position_ratio = 0.3    # 单只股票最大仓位 30%
total_position_ratio = 0.95 # 总仓位限制 95%
```

## 🔧 扩展开发

### 添加新的选股策略

1. 继承 `BaseStockSelectionStrategy` 类
2. 实现 `select_stocks` 和 `calculate_score` 方法
3. 在 `StrategyFactory` 中注册新策略

```python
class NewSelectionStrategy(BaseStockSelectionStrategy):
    def select_stocks(self, context, data_manager) -> List[StockInfo]:
        # 实现选股逻辑
        pass
    
    def calculate_score(self, context, symbol, data_manager) -> float:
        # 计算股票得分
        pass

# 在 StrategyFactory 中注册
@staticmethod
def create_stock_selection_strategy(config, selection_type=None):
    if selection_type == "new_strategy":
        return NewSelectionStrategy(config)
```

### 添加新的数据源

1. 继承 `BaseDataManager` 类
2. 实现 `get_stock_pool` 方法
3. 在 `StrategyFactory` 中注册

```python
class CustomDataManager(BaseDataManager):
    def get_stock_pool(self, context, size: int) -> List[str]:
        # 实现自定义股票池获取逻辑
        pass

# 在 StrategyFactory 中注册
@staticmethod
def create_data_manager(config, selection_type=None):
    if selection_type == "new_data_manager":
        return CustomDataManager(config)
```

## 📈 性能监控

框架内置性能分析器，支持：

- **交易统计**：胜率、平均收益、最大收益/亏损
- **风险指标**：夏普比率、最大回撤
- **资金曲线**：权益变化可视化（需安装matplotlib）

```python
# 获取性能报告
analyzer = PerformanceAnalyzer()
summary = analyzer.get_summary()
print(f"总交易次数: {summary['total_trades']}")
print(f"胜率: {summary['win_rate']:.2%}")
print(f"夏普比率: {summary['sharpe_ratio']:.2f}")
```
# 📞 支持与联系

## 💬 问题反馈

如有问题或建议，请通过以下方式联系：
- **GitHub Issues**: [提交问题报告](issues)
- **技术交流群**: 扫描下方二维码加入
- **微信公众号**: 关注获取最新更新和教程

## 🌟 支持我们

如果这个项目对您有帮助，欢迎支持我们的开发工作：

### 1. ⭐ **Star 项目**
在 GitHub/Gitee 页面右上角点击 Star，这是对我们最大的支持！

### 2. 🐛 **参与贡献**
- 提交 Bug 报告
- 提出新功能建议
- 参与代码开发

### 3. 💰 **赞赏支持**
您的支持将帮助我们持续维护和改进项目：

|                                   微信赞赏                                    |                               支付宝支持                                |
|:-------------------------------------------------------------------------:|:------------------------------------------------------------------:|
| <img src="./images/weixin.jpg" alt="微信赞赏码" width="200" height="200"><br/> | <img src="./images/pay.jpg" alt="支付宝收款码" width="200" height="200"> |

**扫码支持开发工作** → 感谢您的每一份支持！

## 📱 关注我们

**微信公众号** - 获取最新教程、技术文章和项目更新：
<div align="center">
<img src="./images/gong.jpg" alt="微信公众号二维码" width="200" height="200">
</div>

**关注公众号获取**：
- 🔔 项目更新通知
- 📚 量化交易教程
- 💡 使用技巧分享
- 🎯 实战案例解析


### 社区资源
- **Bilibili**: [视频教程](https://space.bilibili.com/your-channel)

## 🛠️ 商务合作

如有商业合作需求，请邮件联系：**2027429742@qq.com**

合作方向包括：
- 📊 企业级定制开发
- 🏢 量化投研系统搭建
- 🎓 量化交易培训合作
- 🔌 第三方系统集成

## ⚠️ 注意
- 紧急问题可邮件联系，标题注明【紧急】
- 商务合作邮件请注明【商务合作】

---

**感谢您对 jb_quant 框架的支持！** 🚀

您的每一次 Star、每一次反馈、每一次支持，都是我们持续改进的动力！

---

> **温馨提示**: 量化交易有风险，投资需谨慎。本框架仅供学习和研究使用，不构成投资建议。实盘交易前请充分测试，并注意风险控制。

**相关标签**：量化交易 Python 股票策略 回测系统 算法交易 金融科技 投资策略 交易系统 风险管理 数据挖掘