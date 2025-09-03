# tests/test_bank_unittest.py
from bank import Account, transfer, OverdraftError
import unittest


class TestAccount(unittest.TestCase):
    # 1.4 正常系要件: deposit
    def test_deposit_normal(self):
        ### ここに記述
        a.deposit(300)
        self.assertEqual(a.balance, 1300)
        
    # 1.5 異常系要件: deposit (amountがint以外)
    def test_deposit_type_error(self):
        a = Account('Alice', 1000)
        with self.assertRaises(### ここに記述):
            a.deposit(3.14)
            
    # 1.5 異常系要件: deposit (amount <= 0)
    def test_deposit_non_positive(self):
        a = Account("Alice", 1000)
        with self.assertRaises(ValueError):
            ### ここに記述
        with self.assertRaises(ValueError):
            a.deposit(-1)
            
    # 1.4 正常系要件: withdraw
    def test_withdraw_normal(self):
        a = Account("Alice", 1000)
        a.withdraw(400)
        ### ここに記述
        
    # 1.5 異常系要件: withdraw (amountがint以外)
    def test_withdraw_type_error(self):
        ### ここに記述
        with self.assertRaises(TypeError):
            a.withdraw("100")
    
    # 1.5 異常系要件: withdraw (amount <= 0)
    def test_withdraw_non_positive(self):
        a = Account("Alice", 1000)
        ### ここに記述
            a.withdraw(0)
        with self.assertRaises(ValueError):
            a.withdraw(-10)
            
    # 1.5 異常系要件: withdraw (amount > balance)
    def test_withdraw_overdraft(self):
        a = Account("Alice", 200)
        with self.assertRaises(OverdraftError):
            a.withdraw(300)
        ### ここに記述


class TestTransfer(unittest.TestCase):
    # 1.4 正常系要件: transfer
    def test_transfer_normal(self):
        a = Account("Alice", 1000)
        b = Account("Bob", 200)
        transfer(a, b, 300)
        self.assertEqual((a.balance, b.balance), (700, 500))
        ### ここに記述

    # 1.5 異常系要件: transfer (amount <= 0)
    def test_transfer_invalid_amount(self):
        ### ここに記述
        b = Account("Bob", 200)
        with self.assertRaises(ValueError):
            transfer(a, b, 0)
        with self.assertRaises(ValueError):
            transfer(a, b, -1)

    # 1.5 異常系要件: transfer (amountがint以外)
    def test_transfer_type_error(self):
        a = Account("Alice", 1000)
        b = Account("Bob", 200)
        with self.assertRaises(TypeError):
            ### ここに記述
            
    # 1.5 異常系要件: transfer (src is dst)
    def test_transfer_same_account(self):
        ### ここに記述
        with self.assertRaises(ValueError):
            transfer(a,a,100)
            
    # 1.5 異常系要件: transfer (src残高不足)
    def test_transfer_overdraft_atomic(self):
        a = Account("Alice", 100)
        b = Account("Bob", 200)
        with self.assertRaises(OverdraftError):
            transfer(a, b, 300)
        ### ここに記述


if __name__ == '__main__':
    unittest.main()
