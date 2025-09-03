from dataclasses import dataclass, field
from .errors import OverdraftError

@dataclass
class Account:
    """
    単純な銀行口座。
    - balance は常に 0 以上
    - 金額は int（円）で扱う
    """
    owner: str
    balance: int = field(default=0)

    def deposit(self, amount: int) -> None:
        """amount>0 のとき残高に加算。型不正・非正値は例外。"""
        if not isinstance(amount, int):
            raise TypeError("amount must be int")
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        """amount>0 かつ 残高>=amount のとき残高から減算。違反時は例外。"""
        if not isinstance(amount, int):
            raise TypeError("amount must be int")
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if amount > self.balance:
            raise OverdraftError("insufficient funds")
        self.balance -= amount


def transfer(src: Account, dst: Account, amount: int) -> None:
    """
    src から dst へ振替。
    - amount>0 の int
    - src と dst は別の口座
    - withdraw 成功後に deposit を行う（部分更新なし）
    """
    if not isinstance(amount, int):
        raise TypeError("amount must be int")
    if amount <= 0:
        raise ValueError("amount must be > 0")
    if src is dst:
        raise ValueError("src and dst must be different accounts")

    # ここで例外が出た場合は deposit が呼ばれない（整合性保持）
    src.withdraw(amount)
    dst.deposit(amount)
