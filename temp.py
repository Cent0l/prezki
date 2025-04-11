from enum import Enum
from datetime import datetime, timedelta


class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
    CLOSED = "CLOSED"


class SavingsAccount:
    def __init__(self):
        self.balance = 0.0  # saldo (PDF: balance)
        self.accountStatus = Status.INACTIVE  # domyślnie NIEAKTYWNE (PDF: accountStatus)
        self.lastOperationDate = datetime.now()  # (PDF: lastOperationDate)
        self.failedWithdrawalCount = 0  # (PDF: failedWithdrawalCount)

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("Invalid deposit amount format")
        if amount <= 0:
            raise ValueError("Invalid deposit amount")

        if self.accountStatus == Status.CLOSED or self.accountStatus == Status.LOCKED:
            raise ValueError("Operation not allowed for current account status")

        self.balance += amount
        self.lastOperationDate = datetime.now()

        if self.accountStatus == Status.INACTIVE:
            self.accountStatus = Status.ACTIVE  # (PDF: INACTIVE + deposit → ACTIVE)

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("Invalid withdrawal amount format")
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")

        if self.accountStatus != Status.ACTIVE:
            raise ValueError("Operation not allowed for current account status")

        if amount > self.balance:
            self.failedWithdrawalCount += 1
            if self.failedWithdrawalCount >= 3:
                self.accountStatus = Status.LOCKED  # (PDF: 3 nieudane wypłaty → LOCKED)
            raise ValueError("Insufficient funds")

        self.balance -= amount
        self.lastOperationDate = datetime.now()
        self.failedWithdrawalCount = 0  # (PDF: poprawna wypłata → reset licznik)

    def calculateInterest(self, days):
        if not isinstance(days, int):
            raise ValueError("Invalid days format")
        if days <= 0:
            raise ValueError("Invalid number of days")

        if self.balance <= 1000:
            rate = 0.01
        elif self.balance <= 10000:
            rate = 0.02
        else:
            rate = 0.03

        return round(self.balance * rate * (days / 365), 2)

    def closeAccount(self):
        if self.accountStatus == Status.CLOSED:
            raise ValueError("Account is already closed")
        if self.balance != 0:
            raise ValueError("Cannot close account with non-zero balance")
        self.accountStatus = Status.CLOSED  # (PDF: saldo = 0 → CLOSED)

    def activateAccount(self):
        if self.accountStatus == Status.LOCKED:
            raise ValueError("Cannot activate locked account. Use unblockAccount() first")
        if self.accountStatus == Status.CLOSED:
            raise ValueError("Cannot activate closed account")
        self.accountStatus = Status.ACTIVE  # (PDF: activateAccount())

    def unblockAccount(self):
        if self.accountStatus != Status.LOCKED:
            raise ValueError("Account is not blocked")
        self.accountStatus = Status.ACTIVE
        self.failedWithdrawalCount = 0  # (PDF: unblockAccount())

    def checkActivity(self):
        if self.accountStatus != Status.ACTIVE:
            return  # (PDF: INACTIVE, LOCKED, CLOSED → brak zmian)

        if datetime.now() - self.lastOperationDate > timedelta(days=365):
            self.accountStatus = Status.INACTIVE  # (PDF: brak operacji 12m → INACTIVE)

    def resetFailedWithdrawalCount(self):
        self.failedWithdrawalCount = 0  # (PDF: resetFailedWithdrawalCount())

    def changeStatus(self, newStatus):
        if not isinstance(newStatus, Status):
            raise ValueError("Invalid account status")

        if self.accountStatus == Status.CLOSED:
            raise ValueError("Cannot change status of closed account")

        if newStatus == Status.CLOSED and self.balance != 0:
            raise ValueError("Cannot close account with non-zero balance")

        self.accountStatus = newStatus  # (PDF: changeStatus())
