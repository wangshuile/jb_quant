# 📈 Python Quantitative Trading Strategy Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![JoinQuant Platform](https://img.shields.io/badge/Platform-JoinQuant-orange.svg)](https://www.joinquant.com/)
[![Quantitative Trading](https://img.shields.io/badge/Domain-Quant_Trading-purple.svg)](https://mp.weixin.qq.com/s/PmfgMf8AaauF2mKwT96VLA)

**Keywords**: Quantitative Trading, Stock Strategy, Python Quant, JoinQuant, Backtesting System, Risk Management, Algorithmic Trading, Stock Selection Strategy, Market Timing Strategy

# jb_quant Quantitative Trading Strategy Framework

A modular quantitative trading strategy framework based on the JoinQuant platform, utilizing object-oriented design and the strategy pattern to support flexible combination and extension of strategic components.

## 🎯 Core Features

- **🏗️ Modular Architecture**: Employs the strategy pattern, allowing independent development, testing, and replacement of components
- **📊 Diversified Strategies**: Supports momentum, mean reversion, volatility, and various other stock selection strategies
- **⏰ Intelligent Timing**: Integrates Moving Average, RSI, Momentum, and other market timing strategies
- **🛡️ Multi-Layered Risk Control**: Base/Conservative/Aggressive risk management modes, supports stop-loss and take-profit
- **💾 Data Management**: Supports fixed stock pools and index constituents, with built-in smart caching
- **⚡ High Performance**: Optimizes data access performance and supports multiple trade execution methods

## 📁 Project Structure

```
jb_quant/
├── main.py                    # Main strategy entry point
├── requirements.txt           # Dependency list
├── README.md                  # Project documentation
│
├── config/                    # Configuration directory
│   └── trading_config.py      # Trading configuration class
│
├── core/                      # Core directory
│   ├── base.py                # Base classes and interface definitions
│   └── context.py             # Strategy context object class
│
├── factor/                    # Multi-factor calculation directory
│
├── factory/                   # Strategy factory directory
│   └── strategy_factory.py    # Strategy factory class
│
├── strategies/                # Strategy implementations directory
│   ├── timing_strategies/     # Market timing strategies
│   │   ├── base_timing.py     # Base timing strategy
│   │   ├── ma_timing.py       # Moving Average timing
│   │   └── disabled_timing.py # Disabled timing strategy
│   │   └── mom_timing.py      # Momentum timing strategy
│   │   └── rsi_timing.py      # RSI timing strategy
│   │
│   ├── selection_strategies/ # Stock selection strategies
│   │   ├── base_selection.py            # Base stock selection
│   │   ├── mean_reversion_selection.py  # Mean reversion selection
│   │   ├── momentum_selection.py        # Momentum selection
│   │   └── volatility_selection.py      # Volatility selection
│   │
│   └── risk_managers/         # Risk managers
│       ├── base_risk.py       # Base risk manager
│       ├── conservative_risk.py # Conservative risk manager
│       └── aggressive_risk.py   # Aggressive risk manager
│
├── data/                      # Data management directory
│   ├── base_data_manager.py   # Base data manager
│   ├── fixed_data_manager.py  # Fixed data manager
│   └── index_data_manager.py  # Index constituent data manager
│
├── trading/                   # Trade execution directory
│   ├── base_executor.py       # Base trade executor
│   ├── vwap_executor.py       # VWAP trade executor
│   └── limit_executor.py      # Limit order executor
│
├── strategy/                  # Quantitative trading strategies directory
│   ├── base_strategy.py       # Base strategy class
│   └── quantitative_strategy.py # Main quantitative strategy class
│
└── utils/                     # Utilities directory
    ├── logger.py              # Logging configuration
    ├── cache_manager.py       # Cache manager
    ├── data_converter.py      # Data conversion tools
    └── performance_analyzer.py # Performance analyzer
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the project
git clone <repository-url>
cd jb_quant

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure JoinQuant Token

**Method 1: Modify Configuration File**
Set your JoinQuant token in `config/trading_config.py`:

```python
token: str = 'your_joinquant_token'
```

**Method 2: Set Environment Variable**
```bash
# Windows
set GM_TOKEN='your_joinquant_token'

# Linux/Mac
export GM_TOKEN='your_joinquant_token'
```

### 3. Run Backtest

```bash
# Basic backtest
python main.py

# Specify backtest parameters (via config file)
# Set in trading_config.py:
# - backtest_start: Backtest start time
# - backtest_end: Backtest end time
# - initial_cash: Initial capital
```

### 4. Configure Strategy Combination

Adjust the strategy combination in the `trading_config.py` configuration file:

```python
# Example: Create custom strategy configuration
data_manager_type="index",          # Use index constituents
timing_strategy_type="ma",          # Moving Average timing
stock_selection_type="momentum",    # Momentum stock selection
risk_manager_type="conservative",   # Conservative risk control
trade_executor_type="limit",        # Limit order trading
stock_pool_size=20,                 # Stock pool size
max_positions=5,                    # Maximum number of positions
timing_enabled=True                 # Enable market timing
```

## ⚙️ Configuration Details

### Core Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_manager_type` | str | `"index"` | Data manager type: `"fixed"` or `"index"` |
| `timing_strategy_type` | str | `"disabled"` | Timing strategy: `"disabled"`, `"ma"`, `"rsi"`, `"momentum"` |
| `stock_selection_type` | str | `"momentum"` | Stock selection: `"momentum"`, `"mean_reversion"`, `"volatility"` |
| `risk_manager_type` | str | `"base"` | Risk manager: `"base"`, `"conservative"`, `"aggressive"` |
| `trade_executor_type` | str | `"base"` | Trade executor: `"base"`, `"limit"`, `"vwap"` |

### Risk Control Parameters

```python
# Stop-loss and take-profit configuration
stop_loss_rate = -0.08      # Stop-loss ratio -8%
stop_profit_rate = 0.15     # Take-profit ratio 15%
trailing_stop_rate = 0.05   # Trailing stop ratio 5%
max_position_ratio = 0.3    # Max single stock position ratio 30%
total_position_ratio = 0.95 # Total position limit 95%
```

## 🔧 Extending the Framework

### Adding New Stock Selection Strategies

1. Inherit from `BaseStockSelectionStrategy` class
2. Implement `select_stocks` and `calculate_score` methods
3. Register the new strategy in `StrategyFactory`

```python
class NewSelectionStrategy(BaseStockSelectionStrategy):
    def select_stocks(self, context, data_manager) -> List[StockInfo]:
        # Implement stock selection logic
        pass
    
    def calculate_score(self, context, symbol, data_manager) -> float:
        # Calculate stock score
        pass

# Register in StrategyFactory
@staticmethod
def create_stock_selection_strategy(config, selection_type=None):
    if selection_type == "new_strategy":
        return NewSelectionStrategy(config)
```

### Adding New Data Sources

1. Inherit from `BaseDataManager` class
2. Implement `get_stock_pool` method
3. Register in `StrategyFactory`

```python
class CustomDataManager(BaseDataManager):
    def get_stock_pool(self, context, size: int) -> List[str]:
        # Implement custom stock pool retrieval logic
        pass

# Register in StrategyFactory
@staticmethod
def create_data_manager(config, selection_type=None):
    if selection_type == "new_data_manager":
        return CustomDataManager(config)
```

## 📈 Performance Monitoring

The framework includes a built-in performance analyzer supporting:

- **Trade Statistics**: Win rate, average return, max gain/loss
- **Risk Metrics**: Sharpe ratio, maximum drawdown
- **Equity Curve**: Visualization of capital changes (requires matplotlib)

```python
# Get performance report
analyzer = PerformanceAnalyzer()
summary = analyzer.get_summary()
print(f"Total Trades: {summary['total_trades']}")
print(f"Win Rate: {summary['win_rate']:.2%}")
print(f"Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
```

## 📞 Support & Contact

## 💬 Issue Reporting

For problems or suggestions, please contact via:
- **GitHub Issues**: [Submit Issue Report](issues)
- **Technical Discussion Group**: Scan QR code below to join
- **WeChat Official Account**: Follow for latest updates and tutorials

## 🌟 Support Us

If this project is helpful to you, welcome to support our development work:

### 1. ⭐ **Star the Project**
Click the Star button on the top right of the GitHub/Gitee page - this is our biggest encouragement!

### 2. 🐛 **Contribute**
- Submit bug reports
- Propose new features
- Participate in code development

### 3. 💰 **Donation Support**
Your support helps us maintain and improve the project:

|                                     WeChat Donation                                      |                               Alipay Support                               |
|:----------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|
| <img src="./images/weixin.jpg" alt="WeChat Donation Code" width="180" height="180"><br/> | <img src="./images/pay.jpg" alt="Alipay QR Code" width="180" height="180"> |

**Scan to Support Development** → Thank you for every bit of support!

## 📱 Follow Us

**WeChat Official Account** - Get latest tutorials, technical articles and project updates:
<div align="center">
<img src="./images/gong.jpg" alt="WeChat Official Account QR Code" width="200" height="200">
</div>

**Follow our account for**:
- 🔔 Project update notifications
- 📚 Quantitative trading tutorials
- 💡 Usage tips and tricks
- 🎯 Practical case studies


### Community Resources
- **Bilibili**: [Video Tutorials](https://space.bilibili.com/your-channel)

## 🛠️ Business Cooperation

For business cooperation requests, please email: **2027429742@qq.com**

Cooperation directions include:
- 📊 Enterprise-level custom development
- 🏢 Quantitative research system construction
- 🎓 Quantitative trading training cooperation
- 🔌 Third-party system integration

## ⚠️ Notice
- For urgent issues, please email with subject marked 【URGENT】
- Business cooperation emails should be marked 【BUSINESS COOPERATION】

---

**Thank you for supporting the jb_quant framework!** 🚀

Every star, every piece of feedback, and every bit of support drives our continuous improvement!

---

> **Disclaimer**: Quantitative trading involves risk, invest carefully. This framework is for learning and research purposes only, not investment advice. Please test thoroughly before live trading and implement proper risk controls.

**Related Tags**: Quantitative Trading, Python, Stock Strategy, Backtesting System, Algorithmic Trading, FinTech, Investment Strategy, Trading System, Risk Management, Data Mining