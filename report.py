import csv
import os
import datetime
import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self, finance_manager):
        # שומר הפניה ל-FinanceManager
        self.fm = finance_manager

    # פונקציה פנימית שמחזירה את שם הקטגוריה כטקסט
    def _get_category_label(self, cat):
        if hasattr(cat, "value"):
            return cat.value
        return str(cat)

    # --------------------------------
    # יצוא כל העסקאות לקובץ CSV
    # --------------------------------
    def export_transactions_to_csv(self, filename=None):
        # בדיקה אם יש עסקאות למשתמש
        if not self.fm.user.transactions:
            print("אין עסקאות לייצוא.")
            return None

        # יצירת תיקיית reports אם לא קיימת
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)

        # שם משתמש ללא רווחים
        username = self.fm.user.username.replace(" ", "_")

        # אם לא הועבר שם קובץ – בונים שם עם תאריך ושעה
        if filename is None:
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            base_filename = f"transactions_{username}_{now}"
        else:
            base_filename = os.path.splitext(filename)[0]

        # לוודא שהקובץ יהיה ייחודי (להוסיף מונה אם כבר קיים)
        counter = 1
        final_filename = os.path.join(reports_dir, f"{base_filename}.csv")
        while os.path.exists(final_filename):
            final_filename = os.path.join(reports_dir, f"{base_filename}_{counter:03}.csv")
            counter += 1

        # כתיבת הנתונים לקובץ CSV
        with open(final_filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Type", "Category", "Amount"])
            writer.writeheader()
            for t in self.fm.user.transactions:
                writer.writerow({
                    "Date": t["date"],
                    "Type": t["type"],
                    "Category": self._get_category_label(t["category"]),
                    "Amount": t["amount"]
                })

        print(f"✅ קובץ CSV נשמר: {os.path.abspath(final_filename)}")
        return final_filename   # מחזיר את הנתיב לקובץ CSV כדי להשתמש ביצירת הגרפים

    # --------------------------------
    # יצוא גרף של הכנסות לפי קטגוריה
    # --------------------------------
    def plot_incomes_by_category(self, csv_filename):
        # חישוב סכום לכל קטגוריה
        category_totals = {}
        for t in self.fm.user.transactions:
            if t["type"] == "income":
                category = self._get_category_label(t["category"])
                category_totals[category] = category_totals.get(category, 0) + t["amount"]

        # אם אין הכנסות – לא ליצור גרף
        if not category_totals:
            print("אין הכנסות להצגה.")
            return

        labels = list(category_totals.keys())
        amounts = list(category_totals.values())

        # יצירת גרף עמודות
        plt.figure(figsize=(8, 5))
        plt.bar(labels, amounts, color="green")
        plt.title(f"Incomes by Category - {self.fm.user.username}")
        plt.ylabel("Amount (₪)")

        # שמירת הגרף כקובץ PNG עם אותו שם כמו ה-CSV
        img_filename = os.path.splitext(csv_filename)[0] + "_incomes.png"
        plt.savefig(img_filename, bbox_inches="tight")
        plt.close()
        print(f"✅ גרף הכנסות נשמר: {os.path.abspath(img_filename)}")

    # --------------------------------
    # יצוא גרף של הוצאות לפי קטגוריה
    # --------------------------------
    def plot_expenses_by_category(self, csv_filename):
        # חישוב סכום לכל קטגוריה
        category_totals = {}
        for t in self.fm.user.transactions:
            if t["type"] == "expense":
                category = self._get_category_label(t["category"])
                category_totals[category] = category_totals.get(category, 0) + t["amount"]

        # אם אין הוצאות – לא ליצור גרף
        if not category_totals:
            print("אין הוצאות להצגה.")
            return

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())

        # יצירת גרף עוגה
        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f"Expenses by Category - {self.fm.user.username}")

        # שמירת הגרף כקובץ PNG עם אותו שם כמו ה-CSV
        img_filename = os.path.splitext(csv_filename)[0] + "_expenses.png"
        plt.savefig(img_filename, bbox_inches="tight")
        plt.close()
        print(f"✅ גרף הוצאות נשמר: {os.path.abspath(img_filename)}")

    # --------------------------------
    # יצוא גרף מסכם: הכנסות מול הוצאות
    # --------------------------------
    def plot_income_vs_expense(self, csv_filename):
        # חישוב סכום כולל הכנסות והוצאות
        total_expenses = sum(t["amount"] for t in self.fm.user.transactions if t["type"] == "expense")
        total_incomes = sum(t["amount"] for t in self.fm.user.transactions if t["type"] == "income")

        # יצירת גרף עמודות
        plt.figure(figsize=(5, 5))
        plt.bar(["Incomes", "Expenses"], [total_incomes, total_expenses], color=["green", "red"])
        plt.title(f"Incomes vs Expenses - {self.fm.user.username}")
        plt.ylabel("Amount (₪)")

        # שמירת הגרף כקובץ PNG עם אותו שם כמו ה-CSV
        img_filename = os.path.splitext(csv_filename)[0] + "_summary.png"
        plt.savefig(img_filename, bbox_inches="tight")
        plt.close()
        print(f"✅ גרף סיכום נשמר: {os.path.abspath(img_filename)}")
