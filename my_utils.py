# my_utils.py
# -*- coding: utf-8 -*-
"""
توابع کمکی مشترک پروژه
شامل یکدست‌سازی متن، تبدیل اعداد، تبدیل مبلغ و استانداردسازی دوره
"""

import re
import pandas as pd

# بخش یک: کاراکترهای عددی

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS  = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"

# بخش دو: یکدست‌سازی متن فارسی و عربی

def norm_text(text):
    """
    کاراکترهای عربی را به فارسی تبدیل می‌کند، نیم‌فاصله را به فاصله
    تبدیل می‌کند، فاصله‌های اضافی را حذف می‌کند و متن را trim می‌کند.
    """
    if not isinstance(text, str):
        return text
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = text.replace("\u200c", " ")
    text = text.replace("\u200f", "").replace("\u200e", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

# بخش سه: تبدیل اعداد فارسی و عربی به انگلیسی

def to_english_digits(text):
    """
    هر رقم فارسی یا عربی داخل متن را به رقم انگلیسی تبدیل می‌کند.
    """
    if not isinstance(text, str):
        return text
    for p, e in zip(PERSIAN_DIGITS, ENGLISH_DIGITS):
        text = text.replace(p, e)
    for a, e in zip(ARABIC_DIGITS, ENGLISH_DIGITS):
        text = text.replace(a, e)
    return text

# بخش چهار: تبدیل مبلغ به عدد

def clean_amount(value):
    """
    مبلغ را به عدد تبدیل می‌کند. کاما، واحد ریال و تومان و فاصله را
    حذف می‌کند. اگر مقدار قابل تبدیل نبود، None برمی‌گرداند.
    """
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    s = to_english_digits(str(value))
    s = s.replace(",", "").replace("،", "")
    s = s.replace("ریال", "").replace("ريال", "")
    s = s.replace("تومان", "").replace(" ", "").strip()

    if s == "" or s.lower() in ("nan", "none", "null"):
        return None

    try:
        return float(s)
    except ValueError:
        return None

# بخش پنج: استانداردسازی دوره

def norm_period(value):
    """
    دوره را به قالب 1405/03 یا 1405/04 تبدیل می‌کند.
    اگر مقدار قابل تشخیص نبود، همان متن اصلی را برمی‌گرداند.
    """
    if pd.isna(value):
        return None
    s = to_english_digits(str(value))
    s = s.replace("-", "/").replace(".", "/")
    m = re.search(r"(1[34]\d{2})\D+(\d{1,2})", s)
    if m:
        year = m.group(1)
        month = m.group(2).zfill(2)
        return f"{year}/{month}"
    return s

# بخش شش: تشخیص دسته و ماه از روی نام فایل

def detect_category_period(file_key):
    """
    از روی نام فایل، دسته و ماه را تشخیص می‌دهد.
    خروجی یک تاپل است: (دسته، ماه)
    """
    category = "نامشخص"
    if "خدمات_فناوری" in file_key:
        category = "خدمات_فناوری"
    elif "پشتیبانی" in file_key:
        category = "پشتیبانی"
    elif "تعداد_نفرات" in file_key:
        category = "تعداد_نفرات"

    period = None
    if "خرداد" in file_key:
        period = "1405/03"
    elif "تیر" in file_key:
        period = "1405/04"

    return category, period

# بخش هفت: علامت‌گذاری مشکلات ردیف

def flag_row(row):
    """
    برای هر ردیف، سه علامت می‌گذارد:
    - مبلغ گمشده
    - مبلغ منفی
    - نام شرکت ناشناخته
    """
    amount = row.get("amount")
    row["amount_missing"]  = pd.isna(amount)
    row["amount_negative"] = (not pd.isna(amount)) and (amount < 0)
    row["company_unknown"] = pd.isna(row.get("company_name"))
    return row

# بخش هشت: تست سریع توابع

if __name__ == "__main__":
    print(norm_text("شركت آلفا"))              # شرکت آلفا
    print(to_english_digits("۱۴۰۵/۰۳"))         # 1405/03
    print(clean_amount("۲۴۵,۰۰۰,۰۰۰ ریال"))     # 245000000.0
    print(clean_amount("عدد ثبت نشده"))          # None
    print(norm_period("1405-3"))                # 1405/03
    print(norm_period("خرداد 1405"))            # 1405/03
    print(detect_category_period("پشتیبانی_خرداد"))  # ('پشتیبانی', '1405/03')