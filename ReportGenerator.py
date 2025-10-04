import csv

class ReportGenerator:
    def __init__(self, finance_manager):
        self.fm = finance_manager

    def _get_category_label(self, cat):
        if hasattr(cat, "value"):
            return cat.value
        return str(cat)

    def export_transactions_to_csv(self, filename="transactions.csv"):
        if not self.fm.user.transactions:
            print("אין פעולות לייצוא.")
            return
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["תאריך", "סכום", "קטגוריה", "תיאור", "סוג פעולה"])
            for t in self.fm.user.transactions:
                category_label = self._get_category_label(t["category"])
                writer.writerow([t["date"], t["amount"], category_label, t["description"], t["type"]])
        print(f"✅ הדוח נשמר בהצלחה כ־CSV בשם '{filename}'")
