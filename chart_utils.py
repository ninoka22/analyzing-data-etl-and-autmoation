# chart_utils.py
# -*- coding: utf-8 -*-
"""توابع کمکی برای نمایش درست متن فارسی در نمودارها"""

import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt

# تنظیم فونت فارسی
plt.rcParams["font.family"] = "Tahoma"
plt.rcParams["axes.unicode_minus"] = False

def fa(text):
    """
    متن فارسی را برای نمایش درست در نمودار آماده می‌کند.
    حروف را به هم می‌چسباند و ترتیب راست به چپ را اصلاح می‌کند.
    """
    if not isinstance(text, str):
        return text
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)