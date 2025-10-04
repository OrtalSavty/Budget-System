# קטגוריות לבחירה להוצאות והכנסות
from enum import Enum

class ExpenseCategory(Enum):
    FOOD = "אוכל"
    TRANSPORT = "תחבורה"
    ENTERTAINMENT = "בידור"
    BILLS = "חשבונות"
    CLOTHING = "ביגוד"
    HEALTH = "בריאות"
    EDUCATION = "חינוך"
    HOUSEHOLD = "משק בית"
    PERSONAL_CARE = "טיפוח אישי"
    GIFTS = "מתנות"
    SAVINGS = "חיסכון"
    OTHER = "אחר"

    def get_label(self):
        return self.value


class IncomeCategory(Enum):
    SALARY = "משכורת"
    GIFT = "מתנה"
    INVESTMENT = "השקעה"
    RENTAL_INCOME = "הכנסה משכירות"
    REFUND = "החזר כספי"
    SIDE_INCOME = "הכנסה נוספת"
    PENSION = "פנסיה/קצבה"
    OTHER = "אחר"

    def get_label(self):
        return self.value

