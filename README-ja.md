# 📈 Python量化取引戦略フレームワーク

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![掘金量化](https://img.shields.io/badge/プラットフォーム-掘金量化-orange.svg)](https://www.myquant.cn/)
[![量化投资](https://img.shields.io/badge/分野-量化投資-purple.svg)](https://mp.weixin.qq.com/s/PmfgMf8AaauF2mKwT96VLA)

**キーワード**：量化取引、株戦略、Python量化、掘金量化、バックテストシステム、リスク管理、アルゴリズム取引、銘柄選択戦略、タイミング戦略

# jb_quant量化取引戦略フレームワーク

掘金量化プラットフォームを基にしたモジュール化された量化取引戦略フレームワークです。オブジェクト指向設計とストラテジーパターンを採用し、柔軟な戦略コンポーネントの組み合わせと拡張をサポートします。

## 🎯 主な特徴

- **🏗️ モジュール化アーキテクチャ**：ストラテジーパターンを採用し、各コンポーネントを独立して開発、テスト、交換可能
- **📊 多様な戦略**：モメンタム、平均回帰、ボラティリティなど多様な銘柄選択戦略をサポート
- **⏰ インテリジェントなタイミング**：移動平均線、RSI、モメンタムなど多様なタイミング戦略を統合
- **🛡️ 多層リスク管理**：基本/保守的/積極的の3つのリスク管理モード、利食い・損切りをサポート
- **💾 データ管理**：固定銘柄プールと指数構成銘柄をサポート、内蔵インテリジェントキャッシュ
- **⚡ 高性能**：データアクセス性能を最適化、多様な取引実行方式をサポート

## 📁 プロジェクト構成

```
jb_quant/
├── main.py                    # メイン戦略エントリーファイル
├── requirements.txt           # 依存パッケージリスト
├── README.md                  # プロジェクト説明ドキュメント
│
├── config/                    # 設定ファイルディレクトリ
│   └── trading_config.py      # 取引設定クラス
│
├── core/                      # コアファイルディレクトリ
│   ├── base.py                # 基底クラス、エンティティオブジェクト定義とインターフェース定義を含む
│   └── context.py             # 戦略コンテキストオブジェクトクラス
│
├── factor/                    # マルチファクターファイルディレクトリ【マルチファクター情報計算】
│
├── factory/                   # 戦略ファクトリーファイルディレクトリ
│   └── strategy_factory.py    # 戦略ファクトリークラス
│
├── strategies/                # 戦略実装ディレクトリ
│   ├── timing_strategies/     # タイミング戦略
│   │   ├── base_timing.py     # 基本タイミング戦略
│   │   ├── ma_timing.py       # 移動平均線タイミング
│   │   └── disabled_timing.py # タイミング無効戦略
│   │   └── mom_timing.py      # モメンタムタイミング戦略
│   │   └── rsi_timing.py      # RSIタイミング戦略
│   │
│   ├── selection_strategies/  # 銘柄選択戦略
│   │   ├── base_selection.py            # 基本銘柄選択
│   │   ├── mean_reversion_selection.py  # 平均回帰銘柄選択
│   │   ├── momentum_selection.py        # モメンタム銘柄選択
│   │   └── volatility_selection.py      # ボラティリティ銘柄選択
│   │
│   └── risk_managers/         # リスクマネージャー
│       ├── base_risk.py       # 基本リスク管理
│       ├── conservative_risk.py # 保守的リスク管理
│       └── aggressive_risk.py   # 積極的リスク管理
│
├── data/                      # データ管理ディレクトリ
│   ├── base_data_manager.py   # データマネージャー基底クラス
│   ├── fixed_data_manager.py  # 固定データマネージャー基底クラス
│   └── index_data_manager.py  # 指数構成銘柄データマネージャー基底クラス
│
├── trading/                   # 取引実行ディレクトリ
│   ├── base_executor.py       # 取引実行器基底クラス
│   ├── vmap_executor.py       # VWAP取引実行器
│   └── limit_executor.py      # 指値実行器
│
├── strategy/                  # 量化取引戦略ディレクトリ
│   ├── base_strategy.py       # 戦略基底クラス
│   └── quantitative_strategy.py # 量化取引戦略メインクラス
│
└── utils/                     # ユーティリティクラスディレクトリ
    ├── logger.py              # ログ設定
    ├── cache_manager.py       # キャッシュマネージャー
    ├── data_converter.py      # データ変換ツール
    └── performance_analyzer.py # パフォーマンスアナライザー

```

## 🚀 クイックスタート

### 1. 環境準備

```bash
# プロジェクトをクローン
git clone <repository-url>
cd jb_quant

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. 掘金Tokenの設定

**方法1：設定ファイルを修正**
`config/trading_config.py` で掘金tokenを設定：

```python
token: str = 'あなたの掘金token'
```

**方法2：環境変数を設定**
```bash
# Windows
set GM_TOKEN='あなたの掘金token'

# Linux/Mac
export GM_TOKEN='あなたの掘金token'
```

### 3. バックテストの実行

```bash
# 基本バックテスト
python main.py

# バックテストパラメータを指定（設定ファイルを修正）
# trading_config.py で設定：
# - backtest_start: バックテスト開始時間
# - backtest_end: バックテスト終了時間
# - initial_cash: 初期資金
```

### 4. 戦略組み合わせの設定

`trading_config.py` 設定ファイルで戦略組み合わせを調整：

```python
# 例：カスタム戦略設定を作成
data_manager_type="index",          # 指数構成銘柄を使用
timing_strategy_type="ma",          # 移動平均線タイミング
stock_selection_type="momentum",    # モメンタム銘柄選択
risk_manager_type="conservative",   # 保守的リスク管理
trade_executor_type="limit",        # 指値取引
stock_pool_size=20,                 # 銘柄プールサイズ
max_positions=5,                    # 最大保有ポジション数
timing_enabled=True                  # タイミングを有効化
```

## ⚙️ 設定説明

### コア設定パラメータ

| パラメータ | タイプ | デフォルト値 | 説明 |
|------|------|--------|------|
| `data_manager_type` | str | `"index"` | データマネージャータイプ：`"fixed"` または `"index"` |
| `timing_strategy_type` | str | `"disabled"` | タイミング戦略：`"disabled"`、`"ma"`、`"rsi"`、`"momentum"` |
| `stock_selection_type` | str | `"momentum"` | 銘柄選択戦略：`"momentum"`、`"mean_reversion"`、`"volatility"` |
| `risk_manager_type` | str | `"base"` | リスク管理タイプ：`"base"`、`"conservative"`、`"aggressive"` |
| `trade_executor_type` | str | `"base"` | 取引実行：`"base"`、`"limit"`、`"vwap"` |

### リスク管理パラメータ

```python
# 損切り・利食い設定
stop_loss_rate = -0.08      # 損切り比率 -8%
stop_profit_rate = 0.15     # 利食い比率 15%
trailing_stop_rate = 0.05   # トレーリングストップ比率 5%
max_position_ratio = 0.3    # 単一銘柄最大ポジション比率 30%
total_position_ratio = 0.95 # 総ポジション制限 95%
```

## 🔧 拡張開発

### 新しい銘柄選択戦略を追加

1. `BaseStockSelectionStrategy` クラスを継承
2. `select_stocks` と `calculate_score` メソッドを実装
3. `StrategyFactory` で新戦略を登録

```python
class NewSelectionStrategy(BaseStockSelectionStrategy):
    def select_stocks(self, context, data_manager) -> List[StockInfo]:
        # 銘柄選択ロジックを実装
        pass
    
    def calculate_score(self, context, symbol, data_manager) -> float:
        # 銘柄スコアを計算
        pass

# StrategyFactory で登録
@staticmethod
def create_stock_selection_strategy(config, selection_type=None):
    if selection_type == "new_strategy":
        return NewSelectionStrategy(config)
```

### 新しいデータソースを追加

1. `BaseDataManager` クラスを継承
2. `get_stock_pool` メソッドを実装
3. `StrategyFactory` で登録

```python
class CustomDataManager(BaseDataManager):
    def get_stock_pool(self, context, size: int) -> List[str]:
        # カスタム銘柄プール取得ロジックを実装
        pass

# StrategyFactory で登録
@staticmethod
def create_data_manager(config, selection_type=None):
    if selection_type == "new_data_manager":
        return CustomDataManager(config)
```

## 📈 パフォーマンスモニタリング

フレームワーク内蔵パフォーマンスアナライザーで以下をサポート：

- **取引統計**：勝率、平均リターン、最大利益/損失
- **リスク指標**：シャープレシオ、最大ドローダウン
- **資金曲線**：エクイティ変化の可視化（matplotlibのインストールが必要）

```python
# パフォーマンスレポートを取得
analyzer = PerformanceAnalyzer()
summary = analyzer.get_summary()
print(f"総取引回数: {summary['total_trades']}")
print(f"勝率: {summary['win_rate']:.2%}")
print(f"シャープレシオ: {summary['sharpe_ratio']:.2f}")
```

# 📞 サポートと連絡

## 💬 問題報告

問題や提案がある場合は、以下の方法でご連絡ください：
- **GitHub Issues**: [問題報告を提出](issues)
- **技術交流グループ**: 下記QRコードをスキャンして参加
- **WeChat公式アカウント**: フォローして最新更新とチュートリアルを取得

## 🌟 サポートのお願い

このプロジェクトがお役に立った場合は、開発をサポートしていただけると幸いです：

### 1. ⭐ **プロジェクトをStar**
GitHub/Giteeページの右上でStarをクリック、これが最大のサポートです！

### 2. 🐛 **貢献に参加**
- バグ報告を提出
- 新機能を提案
- コード開発に参加

### 3. 💰 **寄付によるサポート**
ご支援いただくと、プロジェクトの継続的なメンテナンスと改善に役立ちます：

|                                    WeChat寄付                                     |                               Alipayサポート                                |
|:-------------------------------------------------------------------------------:|:-----------------------------------------------------------------------:|
| <img src="./images/weixin.jpg" alt="WeChat寄付コード" width="180" height="180"><br/> | <img src="./images/pay.jpg" alt="Alipay受取コード" width="180" height="180"> |

**スキャンして開発をサポート** → ご支援いただき誠にありがとうございます！

## 📱 フォロー

**WeChat公式アカウント** - 最新チュートリアル、技術記事、プロジェクト更新を取得：
<div align="center">
<img src="./images/gong.jpg" alt="WeChat公式アカウントQRコード" width="200" height="200">
</div>

**公式アカウントで取得できる内容**：
- 🔔 プロジェクト更新通知
- 📚 量化取引チュートリアル
- 💡 使用テクニック共有
- 🎯 実戦ケース解析


### コミュニティリソース
- **Bilibili**: [ビデオチュートリアル](https://space.bilibili.com/your-channel)

## 🛠️ ビジネス協力

ビジネス協力が必要な場合は、メールでご連絡ください：**2027429742@qq.com**

協力方向：
- 📊 企業向けカスタム開発
- 🏢 量化投研システム構築
- 🎓 量化取引トレーニング協力
- 🔌 サードパーティシステム統合

## ⚠️ 注意
- 緊急の場合はメールで連絡、件名に【緊急】と明記
- ビジネス協力のメールは件名に【ビジネス協力】と明記

---

**jb_quant フレームワークへのご支援ありがとうございます！** 🚀

皆様のStar、フィードバック、サポートの一つ一つが、私たちが継続的に改善する原動力です！

---

> **ご注意**: 量化取引にはリスクがあり、投資には注意が必要です。本フレームワークは学習と研究目的のみで使用され、投資アドバイスを構成するものではありません。実取引前に十分なテストを行い、リスク管理に注意してください。

**関連タグ**：量化取引 Python 株戦略 バックテストシステム アルゴリズム取引 FinTech 投資戦略 取引システム リスク管理 データマイニング