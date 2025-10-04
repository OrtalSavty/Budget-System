from datetime import date
from categories import ExpenseCategory, IncomeCategory


class Transaction:
    """מחלקת בסיס לכל פעולה כספית (abstract-like)"""
    def __init__(self, amount, category, description, transaction_date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = transaction_date if transaction_date else date.today().isoformat()

    def __str__(self):
        return f"{self.date} | {self.amount}₪ | {self.category.name} ({self.category.get_label()}) | {self.description}"


class Expense(Transaction):
    """מחלקת הוצאה"""
    def __init__(self, amount, category: ExpenseCategory, description, transaction_date=None):
        super().__init__(amount, category, description, transaction_date)


class Income(Transaction):
    """מחלקת הכנסה"""
    def __init__(self, amount, category: IncomeCategory, description, transaction_date=None):
        super().__init__(amount, category, description, transaction_date)


class FinanceManager:
    """מנהל את כל הפעולות של המשתמש"""
    def __init__(self, user):
        self.user = user   # כאן user מגיע מ-UserManager
        # כל הפעולות נשמרות בתוך האובייקט של המשתמש
        if not hasattr(self.user, "transactions"):
            self.user.transactions = []

    def add_expense(self, expense: Expense):
        self.user.transactions.append({
            "type": "expense",
            "amount": expense.amount,
            "category": expense.category.name,
            "description": expense.description,
            "date": expense.date
        })

    def add_income(self, income: Income):
        self.user.transactions.append({
            "type": "income",
            "amount": income.amount,
            "category": income.category.name,
            "description": income.description,
            "date": income.date
        })

    def show_all_transactions(self):
        if not self.user.transactions:
            print("אין פעולות להצגה.")
            return
        print("\n--- כל הפעולות ---")
        for t in self.user.transactions:
            print(f"{t['date']} | {t['amount']}₪ | {t['category']} | {t['description']} ({t['type']})")
