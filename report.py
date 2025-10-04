import csv
class ReportGenerator:
    # מחלקה להפקת דוחות כספיים עבור משתמש
    def __init__(self, finance_manager):
        self.fm = finance_manager

    def _get_category_label(self, cat):
        # מחזירה שם קטגוריה בעברית גם אם זה Enum וגם אם זה str ישן
        if hasattr(cat, "value"):  # אם זה Enum
            return cat.value
        return str(cat)  # אם זה str ישן

    def print_summary(self):
        # מדפיס סיכום כללי של הכנסות, הוצאות ומאזן
        # בחירה '4' באופציות
        expenses = sum(t["amount"] for t in self.fm.user.transactions if t["type"] == "expense")
        incomes = sum(t["amount"] for t in self.fm.user.transactions if t["type"] == "income")
        balance = incomes - expenses
        print("\n--- סיכום כללי ---")
        print(f"הכנסות: {incomes}₪")
        print(f"הוצאות: {expenses}₪")
        print(f"מאזן: {balance}₪")

    def print_expenses_by_category(self):
        # מדפיס סיכום הוצאות לפי קטגוריה
        # בחירה '5' באופציות
        category_totals = {}
        for t in self.fm.user.transactions:
            if t["type"] == "expense":
                category = t["category"]
                category_totals[category] = category_totals.get(category, 0) + t["amount"]

        print("\n--- הוצאות לפי קטגוריה ---")
        if not category_totals:
            print("אין הוצאות להצגה.")
        for cat, total in category_totals.items():
            print(f"{self._get_category_label(cat)}: {total}₪")

    def print_incomes_by_category(self):
        # מדפיס סיכום הכנסות לפי קטגוריה
        # בחירה '6' באופציות
        category_totals = {}
        for t in self.fm.user.transactions:
            if t["type"] == "income":
                category = t["category"]
                category_totals[category] = category_totals.get(category, 0) + t["amount"]

        print("\n--- הכנסות לפי קטגוריה ---")
        if not category_totals:
            print("אין הכנסות להצגה.")
        for cat, total in category_totals.items():
            print(f"{self._get_category_label(cat)}: {total}₪")

    def export_transactions_to_csv(self, filename="transactions.csv"):
        if not self.fm.user.transactions:
            print("אין פעולות לייצוא.")
            return
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["תאריך", "סכום", "קטגוריה", "תיאור", "סוג פעולה"])
           # פעולות עבור המשתמש
            for t in self.fm.user.transactions:
                category_label = self._get_category_label(t["category"])
                writer.writerow([t["date"], t["amount"], category_label, t["description"], t["type"]])
        print(f"✅ הדוח נשמר בהצלחה כ־CSV בשם '{filename}'")

