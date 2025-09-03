import pytest
from bank import Account, transfer, OverdraftError


@pytest.fixture
def accounts():
    return Account("Alice", 1000), Account("Bob", 200)

class TestAccount:
    # 1.4 正常系要件: deposit
    def test_deposit_normal(self):
        a = Account("Alice", 1000)
        a.deposit(300)
        assert a.balance == 1300
        
    # 1.5 異常系要件: deposit (amountがint以外)
    @pytest.mark.parametrize("bad", [3.14, "100", None])
    def test_deposit_type_error(self, bad):
        a = Account("Alice", 1000)
        with pytest.raises(TypeError):
            a.deposit(bad)
    
    # 1.5 異常系要件: deposit (amount <= 0)
    @pytest.mark.parametrize("bad", [0,-1, -100])
    def test_deposit_non_positive(self, bad):
        a = Account("Alice", 1000)
        with pytest.raises(ValueError):
            a.deposit(bad)
            
    # 1.4 正常系要件: withdraw
    def test_withdraw_normal(self):
        a = Account("Alice", 1000)
        a.withdraw(250)
        assert a.balance == 750
        
    # 1.5 異常系要件: withdraw (amountがint以外)
    @pytest.mark.parametrize("bad", ["100", 1.0, None])
    def test_withdraw_type_error(self, bad):
        a = Account("Alice", 1000)
        with pytest.raises(TypeError):
            a.withdraw(bad)
            
    # 1.5 異常系要件: withdraw (amount <= 0)
    @pytest.mark.parametrize("bad",[0, -5])
    def test_withdraw_non_positive(self, bad):
        a = Account("Alice", 1000)
        with pytest.raises(ValueError):
            a.withdraw(bad)
            
    # 1.5 異常系要件: withdraw (amount > balance)
    def test_withdraw_overdraft(self):
        a = Account("Alice", 200)
        with pytest.raises(OverdraftError):
            a.withdraw(500)
        assert a.balance == 200
        

class TestTransfer:
    # 1.4 正常系要件: transfer
    def test_transfer_normal(self, accounts):
        a, b = accounts
        transfer(a, b, 300)
        assert (a.balance, b.balance) == (700, 500)
        assert 1200 == a.balance + b.balance
        
    # 1.5 異常系要件: transfer (amount <= 0)
    @pytest.mark.parametrize("bad", [0, -1, -100])
    def test_transfer_invalid_amount(self, accounts, bad):
        a, b = accounts
        with pytest.raises(ValueError):
            transfer(a, b, bad)
            
    # 1.5 異常系要件: transfer (amountがint以外)
    def test_transfer_type_error(self, accounts):
        a, b = accounts
        with pytest.raises(TypeError):
            transfer(a, b, 100.0)
            
    # 1.5 異常系要件: transfer (src is dst)
    def test_transfer_same_account(self):
        a = Account("Alice", 1000)
        with pytest.raises(ValueError):
            transfer(a, a, 100)
            
    # 1.5 異常系要件: transfer (src残高不足)
    def test_transfer_overdraft_atomic(self, accounts):
        a, b = accounts
        with pytest.raises(OverdraftError):
            transfer(a, b, 5000)
        assert(a.balance, b.balance) == (1000, 200)
