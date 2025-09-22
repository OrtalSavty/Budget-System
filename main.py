from enum import Enum


class FinanceException(Exception):
    pass


class ExpenseCategory(Enum):
    FOOD = "אוכל"
    TRANSPORT = "תחבורה"
    ENTERTAINMENT = "בידור"
    OTHER = "אחר"

    def get_label(self):
        return self.value


class IncomeCategory(Enum):
    SALARY = "משכורת"
    GIFT = "מתנה"
    INVESTMENT = "השקעה"
    OTHER = "אחר"

    def get_label(self):
        return self.value


class Transaction:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.amount}₪ - {self.category.get_label()} - {self.description}"


class Expense(Transaction):
    pass


class Income(Transaction):
    pass


class FinanceManager:
    def __init__(self, user_name):
        if not user_name:
            raise FinanceException("שם משתמש לא יכול להיות ריק")
        self.user_name = user_name
        self.transactions = []

    def add_expense(self, expense: Expense):
        self.transactions.append(expense)

    def add_income(self, income: Income):
        self.transactions.append(income)

    def show_all_transactions(self):
        if not self.transactions:
            print("אין פעולות להצגה")
        for t in self.transactions:
            print(t)


class ReportGenerator:
    def __init__(self, fm: FinanceManager):
        self.fm = fm

    def print_summary(self):
        expenses = sum(t.amount for t in self.fm.transactions if isinstance(t, Expense))
        incomes = sum(t.amount for t in self.fm.transactions if isinstance(t, Income))
        print(f"סיכום חודשי: הכנסות {incomes}₪, הוצאות {expenses}₪, מאזן {incomes - expenses}₪")

    def print_expenses_by_category(self):
        category_totals = {}
        for t in self.fm.transactions:
            if isinstance(t, Expense):
                category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
        print("הוצאות לפי קטגוריות:")
        for cat, total in category_totals.items():
            print(f"{cat.get_label()}: {total}₪")


def add_expense(fm: FinanceManager):
    try:
        amount = float(input("סכום: "))
        print("קטגוריות הוצאה זמינות:")
        for c in ExpenseCategory:
            print(f"{c.name} - {c.get_label()}")
        cat_str = input("בחר קטגוריית הוצאה: ").upper()
        category = ExpenseCategory[cat_str]
        description = input("תיאור: ")
        fm.add_expense(Expense(amount, category, description))
        print("הוצאה נוספה בהצלחה!")
    except Exception as e:
        print(f"שגיאה בהוספת הוצאה: {e}")


def add_income(fm: FinanceManager):
    try:
        amount = float(input("סכום: "))
        print("קטגוריות הכנסה זמינות:")
        for c in IncomeCategory:
            print(f"{c.name} - {c.get_label()}")
        cat_str = input("בחר קטגוריית הכנסה: ").upper()
        category = IncomeCategory[cat_str]
        description = input("תיאור: ")
        fm.add_income(Income(amount, category, description))
        print("הכנסה נוספה בהצלחה!")
    except Exception as e:
        print(f"שגיאה בהוספת הכנסה: {e}")


def main():
    user_name = input("הכנס את שמך: ").strip()
    try:
        fm = FinanceManager(user_name)
        rg = ReportGenerator(fm)
        print(f"ברוך הבא {user_name}!")
    except FinanceException as e:
        print(f"שגיאה ביצירת המערכת: {e}")
        return

    while True:
        print("\n----- תפריט ניהול כספים -----")
        print("1. הוספת הוצאה")
        print("2. הוספת הכנסה")
        print("3. הצגת דוח חודשי")
        print("4. הצגת כל הפעולות")
        print("5. יציאה")
        choice = input("בחר אופציה: ")

        if choice == "1":
            add_expense(fm)
        elif choice == "2":
            add_income(fm)
        elif choice == "3":
            rg.print_summary()
            rg.print_expenses_by_category()
        elif choice == "4":
            fm.show_all_transactions()
        elif choice == "5":
            print(f"להתראות {user_name}!")
            break
        else:
            print("בחירה לא חוקית")


if __name__ == "__main__":
    main()
