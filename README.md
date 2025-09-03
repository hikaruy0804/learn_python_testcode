# Pythonテスト駆動開発 学習リポジトリ

## 1. プロジェクト概要

### 目的

Pythonコードで、**仕様書からテストコードの実装**を行います。
また、同じ内容について、Python標準ライブラリ`unittest`と、テストフレームワーク`pytest`の２つを記述します。

### 学習の進め方

`src/bank`に実装された銀行口座の仕様（本READMEのセクション5）を読み解き、`tests`ディレクトリにあなた自身のテストコードを記述します。
演習は、まず`unittest`で実装し、次に`pytest`で書き直す（リファクタリングする）ことで、両者の違いと`pytest`の利便性を体感できるように構成されています。

行き詰まった場合は、`tests_answer`ディレクトリに解答例が用意されていますので、参考にしてください。

## 2. 環境構築

本プロジェクトは、高速なPythonパッケージインストーラである`uv`を使用します。

1.  **`uv`のインストール**
    `uv`が未インストールの場合、公式の指示に従いインストールしてください。
    (例: `pip install uv` または `pipx install uv`)

2.  **リポジトリのクローンと移動**
    ```bash
    git clone <リポジトリのURL>
    cd <リポジトリ名>
    ```

3.  **仮想環境の作成**
    ```bash
    uv venv
    ```
    プロジェクトルートに`.venv`という仮想環境が作成されます。

4.  **依存パッケージのインストール**
    ```bash
    uv sync
    ```
    `pyproject.toml`と`uv.lock`を基に必要なライブラリ（`pytest`など）が仮想環境にインストールされます。

## 3. テストコードの記述（演習ステップ）

この演習は2つのステップで進め、`unittest`と`pytest`の違いを体感することを目指します。

### ステップ1: `unittest`で記述する

まずは、Pythonの標準ライブラリである`unittest`を使い、仕様を満たすテストを`tests/test_bank_unittest.py`に記述してみましょう。

**`unittest`の基本:**
- `unittest.TestCase`を継承したクラスを作成
- `test_`で始まるメソッドを定義
- `self.assertEqual()`などでアサーション
- `with self.assertRaises()`で例外を検証

### unittest

**テストの実行:**
```bash
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

**実行結果の確認:**
実行後、コンソールの最終行に`OK`と表示されれば、すべてのテストが正常に完了しています。

### ステップ2: `pytest`で記述

`tests/test_bank_pytest.py`に`pytest`を使って同じテストを記述してみましょう。

**`pytest`の実行:**
```bash
uv run pytest -v
```

**実行結果の確認:**
実行後、`... passed in ...`のような緑色のメッセージが表示されれば成功です。

**`pytest`の利点:**
- **記述量の削減**: クラス定義が不要になり、コードが簡潔になります。
- **`assert`文**: Python標準の`assert`だけで、より詳細な失敗レポートが得られます。
- **Fixture**: `@pytest.fixture`を使うことで、テストの準備・後片付け処理を柔軟に共通化できます。
- **Parametrize**: `@pytest.mark.parametrize`を使うと、複数の入力パターンを持つテストを簡単に自動生成できます。

---

## 4. 機能仕様（Bankミニドメイン）

### 4.1 概要

-   単純な銀行口座ドメインを実装する。入出金・振替を提供。
-   金額は整数（最小単位：円）で扱い、小数は不可。
-   例外と境界条件を明確に定義する（テストしやすい仕様）。

### 4.2 ユースケース

-   ユーザーは口座を作成し、入金・出金できる。
-   2つの口座間で振替できる。
-   口座残高は常に 0 以上でなければならない。

### 4.3 API（外部公開）

-   **クラス:**
    -   `Account(owner: str, balance: int = 0)`
        -   `deposit(amount: int) -> None`
        -   `withdraw(amount: int) -> None`
-   **関数:**
    -   `transfer(src: Account, dst: Account, amount: int) -> None`
-   **例外:**
    -   `OverdraftError`: 残高不足
    -   `ValueError`: 不正金額・同一口座振替などの仕様違反
    -   `TypeError`: 引数の型が不正

### 4.4 正常系要件

-   `deposit`: 金額 `amount` は `int` かつ `> 0`。`balance` に加算。
-   `withdraw`: 金額 `amount` は `int` かつ `> 0`。残高が足りるときのみ減算。
-   `transfer`:
    -   `amount` は `int` かつ `> 0`
    -   `src is not dst`
    -   `src.withdraw(amount)` が成功した場合のみ `dst.deposit(amount)` を行う（部分更新なし）。

### 4.5 異常系要件

-   `deposit`:
    -   `amount <= 0` → `ValueError`
    -   `amount` が `int` 以外 → `TypeError`
-   `withdraw`:
    -   `amount <= 0` → `ValueError`
    -   `amount` が `int` 以外 → `TypeError`
    -   `amount > balance` → `OverdraftError`
-   `transfer`:
    -   `amount <= 0` → `ValueError`
    -   `amount` が `int` 以外 → `TypeError`
    -   `src is dst` → `ValueError`
    -   `src` 残高不足 → `OverdraftError`（この場合 `dst` は未更新）

### 4.6 非機能要件（最小）

-   Python 3.10+ / 外部依存なし
-   スレッドセーフ要件は持たない（学習用途のため単一スレッド想定）
-   例外メッセージは簡潔で一貫
