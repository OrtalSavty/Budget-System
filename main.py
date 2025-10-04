from user import UserManager
from finance import FinanceManager, Expense, Income
from categories import ExpenseCategory, IncomeCategory
from report import ReportGenerator

def main():
    user_manager = UserManager()
    user = None

    print("----- מערכת ניהול תקציב -----")

    # לולאה עד חיבור מוצלח
    while user is None:
        print("בחר: 1. הרשמה | 2. התחברות")
        choice = input("בחר: ").strip()
        # אם נבחר "1" יתבצע תהליך יצירת משתמש חדש
        if choice == "1":
            username = input("שם משתמש חדש: ").strip()
            password = input("סיסמה: ").strip()
            try:
                user_manager.register(username, password)
                print("✅ נרשמת בהצלחה! עכשיו תוכלי להתחבר עם המשתמש שיצרת.")
                # לא יוצאים — חוזרים לתפריט כדי לאפשר התחברות
            except Exception as e:
                print("שגיאה בהרשמה:", e)
                # חוזרים ללולאה לנסות שוב

        # אם נבחר "2" יתבצע תהליך התחברות למשתמש קיים
        elif choice == "2":
            username = input("שם משתמש: ").strip()
            password = input("סיסמה: ").strip()
            try:
                user = user_manager.login(username, password)
                print(f"ברוך/ה הבא/ה {username}!")
            except Exception as e:
                print("שגיאה בהתחברות:", e)
                # חוזרים ללולאה לנסות שנית

        # אם נבחר כל מספר אחר תקפוץ הותדעת שגיאה ויהיה ניתן לנסות שוב
        else:
            print("בחירה לא חוקית — הזן/י 1 או 2 וננסה שוב.")

    # לאחר התחברות מוצלחת ממשיכים לתפריט הראשי
    fm = FinanceManager(user)
    rg = ReportGenerator(fm)

    # בחירת םעולה רצויה מתפריט קיים
    while True:
        print("\n--- תפריט ראשי ---")
        print("1. הוספת הוצאה")
        print("2. הוספת הכנסה")
        print("3. הצגת כל הפעולות")
        print("4. סיכום כללי")
        print("5. הוצאות לפי קטגוריה")
        print("6. הכנסות לפי קטגוריה")
        print("0. יציאה")
        choice = input("בחר פעולה: ").strip()

        # אם נבחר "1" תיהיה אופציה להוספת הוצאה
        if choice == "1":
            try:
                amount = float(input("סכום הוצאה: ").strip())
                print("קטגוריות הוצאה:", [c.get_label() for c in ExpenseCategory])
                category_input = input("בחר קטגוריה: ").strip()
                category = None
                for c in ExpenseCategory:
                    if c.get_label() == category_input:
                        category = c
                        break

                if category is None:
                    print("קטגוריה לא חוקית — נסי שוב.")
                    continue

                description = input("תיאור: ").strip()
                expense = Expense(amount, category, description)
                fm.add_expense(expense)
                user_manager.save_users()
                print("✅ הוצאה נוספה")
            except ValueError:
                print("סכום לא תקין — הזן/ה סכום מספרי.")
            except Exception as e:
                print("שגיאה:", e)

        # אם נבחר "2" תיהיה אופציה להוספת הכנסה
        elif choice == "2":
            try:
                amount = float(input("סכום הכנסה: ").strip())
                print("קטגוריות הכנסה:", [c.get_label() for c in IncomeCategory])
                category_input = input("בחר קטגוריה: ").strip()

                category = None
                for c in IncomeCategory:
                    if c.get_label() == category_input:
                        category = c
                        break

                if category is None:
                    print("קטגוריה לא חוקית — נסה שוב.")
                    continue

                description = input("תיאור: ").strip()
                income = Income(amount, category, description)
                fm.add_income(income)
                user_manager.save_users()
                print("✅ הכנסה נוספה")

            except ValueError:
                print("סכום לא תקין — הזן/י סכום מספרי.")
            except Exception as e:
                print("שגיאה:", e)

        # אם נבחר "3" יופיע הדוח בשלם כולל תאריכים
        elif choice == "3":
            rg.export_transactions_to_csv("דוח_פעולות.csv")

        # אם נבחר "4" יופיע סיכום כללי של הכנסות הוצאות ומאזן
        elif choice == "4":
            rg.print_summary()

        # אם נבחר "5" יופיע כל ההוצאות שהתבצעו
        elif choice == "5":
            rg.print_expenses_by_category()

        # אם נבחר "6" יופיע כל ההכנסות שהתקבלו
        elif choice == "6":
            rg.print_incomes_by_category()

        # אם נבחר "0" נצא מהתוכנית
        elif choice == "0":
            print("להתראות 👋")
            break

    # כל בחירת מספר אחר תוביל לניסיון חוזר כי הבחירה אינה חוקית
        else:
            print("בחירה לא חוקית, נסה שוב.")

if __name__ == "__main__":
    main()