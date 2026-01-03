# 📈 Python量化交易策略框架

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![掘金量化](https://img.shields.io/badge/平台-掘金量化-orange.svg)](https://www.myquant.cn/)
[![量化投資](https://img.shields.io/badge/領域-量化投資-purple.svg)](https://mp.weixin.qq.com/s/PmfgMf8AaauF2mKwT96VLA)

**關鍵字**：量化交易、股票策略、Python量化、掘金量化、回測系統、風險管理、算法交易、選股策略、擇時策略

# jb_quant量化交易策略框架

一個基於掘金量化平台的模組化量化交易策略框架，採用物件導向設計和策略模式，支援靈活的策略組件組合和擴展。

## 🎯 核心特性

- **🏗️ 模組化架構**：採用策略模式，各個組件可獨立開發、測試和替換
- **📊 多樣化策略**：支援動量、均值回歸、波動率等多種選股策略
- **⏰ 智慧擇時**：整合移動平均線、RSI、動量等多種擇時策略
- **🛡️ 多層風控**：基礎/保守/激進三種風險管理模式，支援止盈止損
- **💾 資料管理**：支援固定股票池和指數成分股，內建智慧快取
- **⚡ 高效能**：最佳化資料存取效能，支援多種交易執行方式

## 📁 專案結構

```
jb_quant/
├── main.py                    # 主策略入口檔案
├── requirements.txt           # 相依套件列表
├── README.md                  # 專案說明文件
│
├── config/                    # 設定檔目錄
│   └── trading_config.py      # 交易設定類別
│
├── core/                      # 核心類別目錄
│   ├── base.py                # 基礎類別，包含實體物件定義與介面定義
│   └── context.py             # 策略上下文物件類別
│
├── factor/                    # 多因子檔案目錄【計算多因子資訊】
│
├── factory/                   # 策略工廠檔案目錄
│   └── strategy_factory.py    # 策略工廠類別
│
├── strategies/                # 策略實作目錄
│   ├── timing_strategies/     # 擇時策略
│   │   ├── base_timing.py     # 基礎擇時策略
│   │   ├── ma_timing.py       # 移動平均線擇時
│   │   └── disabled_timing.py # 停用擇時策略
│   │   └── mom_timing.py      # 動量擇時策略
│   │   └── rsi_timing.py      # RSI擇時策略
│   │
│   ├── selection_strategies/  # 選股策略
│   │   ├── base_selection.py            # 基礎選股
│   │   ├── mean_reversion_selection.py  # 均值回歸選股
│   │   ├── momentum_selection.py        # 動量選股
│   │   └── volatility_selection.py      # 波動率選股
│   │
│   └── risk_managers/         # 風險管理器
│       ├── base_risk.py       # 基礎風控
│       ├── conservative_risk.py  # 保守風控
│       └── aggressive_risk.py    # 激進風控
│
├── data/                      # 資料管理目錄
│   ├── base_data_manager.py   # 資料管理器基類
│   ├── fixed_data_manager.py  # 固定資料管理器基類
│   └── index_data_manager.py  # 指數成分股資料管理器基類
│
├── trading/                   # 交易執行目錄
│   ├── base_executor.py       # 交易執行器基類
│   ├── vmap_executor.py       # VWAP交易執行器
│   └── limit_executor.py      # 限價執行器
│
├── strategy/                  # 量化交易策略目錄
│   ├── base_strategy.py       # 策略基類
│   └── quantitative_strategy.py # 量化交易策略主類別
│
└── utils/                     # 工具類目錄
    ├── logger.py              # 日誌配置
    ├── cache_manager.py       # 快取管理器
    ├── data_converter.py      # 資料轉換工具
    └── performance_analyzer.py # 效能分析器

```

## 🚀 快速開始

### 1. 環境準備

```bash
# 複製專案
git clone <repository-url>
cd jb_quant

# 安裝相依套件
pip install -r requirements.txt
```

### 2. 配置掘金Token

**方法一：修改設定檔**
在 `config/trading_config.py` 中設定你的掘金token:

```python
token: str = '你的掘金token'
```

**方法二：設定環境變數**
```bash
# Windows
set GM_TOKEN='你的掘金token'
```

### 3. 執行回測

```bash
# 基礎回測
python main.py

# 指定回測參數（透過修改設定檔）
# 在 trading_config.py 中設定：
# - backtest_start: 回測開始時間
# - backtest_end: 回測結束時間
# - initial_cash: 初始資金
```

### 4. 配置策略組合

在 `trading_config.py` 設定檔中調整策略組合：

```python
# 範例：建立自訂策略配置
data_manager_type="index",          # 使用指數成分股
timing_strategy_type="ma",          # 移動平均線擇時
stock_selection_type="momentum",    # 動量選股
risk_manager_type="conservative",   # 保守風控
trade_executor_type="limit",        # 限價交易
stock_pool_size=20,                 # 股票池大小
max_positions=5,                    # 最大持倉數
timing_enabled=True                 # 啟用擇時
```

## ⚙️ 配置說明

### 核心配置參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `data_manager_type` | str | `"index"` | 資料管理器類型：`"fixed"`或`"index"` |
| `timing_strategy_type` | str | `"disabled"` | 擇時策略：`"disabled"`、`"ma"`、`"rsi"`、`"momentum"` |
| `stock_selection_type` | str | `"momentum"` | 選股策略：`"momentum"`、`"mean_reversion"`、`"volatility"` |
| `risk_manager_type` | str | `"base"` | 風控類型：`"base"`、`"conservative"`、`"aggressive"` |
| `trade_executor_type` | str | `"base"` | 交易執行：`"base"`、`"limit"`、`"vwap"` |

### 風險控制參數

```python
# 止損止盈配置
stop_loss_rate = -0.08      # 止損比例 -8%
stop_profit_rate = 0.15     # 止盈比例 15%
trailing_stop_rate = 0.05   # 移動止盈比例 5%
max_position_ratio = 0.3    # 單檔股票最大倉位 30%
total_position_ratio = 0.95 # 總倉位限制 95%
```

## 🔧 擴展開發

### 加入新的選股策略

1. 繼承 `BaseStockSelectionStrategy` 類別
2. 實作 `select_stocks` 和 `calculate_score` 方法
3. 在 `StrategyFactory` 中註冊新策略

```python
class NewSelectionStrategy(BaseStockSelectionStrategy):
    def select_stocks(self, context, data_manager) -> List[StockInfo]:
        # 實作選股邏輯
        pass
    
    def calculate_score(self, context, symbol, data_manager) -> float:
        # 計算股票得分
        pass

# 在 StrategyFactory 中註冊
@staticmethod
def create_stock_selection_strategy(config, selection_type=None):
    if selection_type == "new_strategy":
        return NewSelectionStrategy(config)
```

### 加入新的資料來源

1. 繼承 `BaseDataManager` 類別
2. 實作 `get_stock_pool` 方法
3. 在 `StrategyFactory` 中註冊

```python
class CustomDataManager(BaseDataManager):
    def get_stock_pool(self, context, size: int) -> List[str]:
        # 實作自訂股票池取得邏輯
        pass

# 在 StrategyFactory 中註冊
@staticmethod
def create_data_manager(config, selection_type=None):
    if selection_type == "new_data_manager":
        return CustomDataManager(config)
```

## 📈 效能監控

框架內建效能分析器，支援：

- **交易統計**：勝率、平均收益、最大收益/虧損
- **風險指標**：夏普比率、最大回撤
- **資金曲線**：權益變化視覺化（需安裝matplotlib）

```python
# 取得效能報告
analyzer = PerformanceAnalyzer()
summary = analyzer.get_summary()
print(f"總交易次數: {summary['total_trades']}")
print(f"勝率: {summary['win_rate']:.2%}")
print(f"夏普比率: {summary['sharpe_ratio']:.2f}")
```

# 📞 支援與聯絡

## 💬 問題回饋

如有問題或建議，請透過以下方式聯絡：
- **GitHub Issues**: [提交問題報告](issues)
- **技術交流群**: 掃描下方二維碼加入
- **微信公眾號**: 關注取得最新更新和教學

## 🌟 支援我們

如果這個專案對您有幫助，歡迎支援我們的開發工作：

### 1. ⭐ **Star 專案**
在 GitHub/Gitee 頁面右上角點擊 Star，這是對我們最大的支援！

### 2. 🐛 **參與貢獻**
- 提交 Bug 報告
- 提出新功能建議
- 參與程式碼開發

### 3. 💰 **讚賞支援**
您的支援將幫助我們持續維護和改進專案：

|                                   微信讚賞                                    |                               支付寶支援                                |
|:-------------------------------------------------------------------------:|:------------------------------------------------------------------:|
| <img src="./images/weixin.jpg" alt="微信讚賞碼" width="180" height="180"><br/> | <img src="./images/pay.jpg" alt="支付寶收款碼" width="180" height="180"> |

**掃碼支援開發工作** → 感謝您的每一份支援！

## 📱 關注我們

**微信公眾號** - 取得最新教學、技術文章和專案更新：
<div align="center">
<img src="./images/gong.jpg" alt="微信公眾號二維碼" width="200" height="200">
</div>

**關注公眾號取得**：
- 🔔 專案更新通知
- 📚 量化交易教學
- 💡 使用技巧分享
- 🎯 實戰案例解析


### 社群資源
- **Bilibili**: [影片教學](https://space.bilibili.com/524125327)

## 🛠️ 商務合作

如有商業合作需求，請郵件聯絡：**2027429742@qq.com**

合作方向包括：
- 📊 企業級客製化開發
- 🏢 量化投研系統搭建
- 🎓 量化交易培訓合作
- 🔌 第三方系統整合

## ⚠️ 注意
- 緊急問題可郵件聯絡，標題註明【緊急】
- 商務合作郵件請註明【商務合作】

---

**感謝您對 jb_quant 框架的支援！** 🚀

您的每一次 Star、每一次回饋、每一次支援，都是我們持續改進的動力！

---

> **溫馨提示**: 量化交易有風險，投資需謹慎。本框架僅供學習和研究使用，不構成投資建議。實盤交易前請充分測試，並注意風險控制。

**相關標籤**：量化交易 Python 股票策略 回測系統 算法交易 金融科技 投資策略 交易系統 風險管理 資料探勘