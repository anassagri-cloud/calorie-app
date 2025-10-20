import streamlit as st
import pandas as pd
import random
import os

# إعداد الصفحة
st.set_page_config(page_title="خطة الوجبات - DietPlus", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
body {direction: rtl !important; text-align: right !important; background: #f9fafb;}
.card-meal {
  background: #ffffffcc; border-right: 6px solid #16a34a; border-radius: 14px;
  padding: 16px; margin-bottom: 14px; box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
  animation: fadeIn .5s ease both;
}
.meal-title { color: #065f46; font-weight: 700; font-size: 20px; margin-bottom: 6px; }
.meal-item { font-size: 17px; color: #333; line-height: 1.8; }
.subtitle { text-align: center; color: #475569; font-size: 18px; margin-bottom: 25px; }
@keyframes fadeIn {from {opacity:0; transform:translateY(8px);} to {opacity:1; transform:translateY(0);}}
</style>
""", unsafe_allow_html=True)

# ---------- العنوان ----------
st.markdown("<h1 style='text-align:center;color:#065f46;'>🍽️ خطة الوجبات اليومية</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>وجبات مقترحة تناسب هدفك الغذائي</p>", unsafe_allow_html=True)

# ---------- تحميل بيانات الوجبات ----------
file_path = "pice_menu_DIETPLUS_simple.xlsx"
if not os.path.exists(file_path):
    st.error("⚠️ لم يتم العثور على ملف الوجبات 'pice_menu_DIETPLUS_simple.xlsx'. الرجاء رفعه في نفس مجلد التطبيق.")
else:
    df = pd.read_excel(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    if "name" not in df.columns or "calories" not in df.columns:
        st.error("ملف الوجبات يجب أن يحتوي على عمودين: name و calories.")
    else:
        # ---------- إدخال السعرات ----------
        total_calories = st.number_input("🎯 السعرات اليومية المستهدفة:", min_value=1000, max_value=4000, value=2000, step=50)
        meal_count = st.radio("🍱 عدد الوجبات في اليوم:", [3, 4], horizontal=True)

        # ---------- توزيع السعرات ----------
        split_ratios = [0.3, 0.4, 0.3] if meal_count == 3 else [0.25, 0.35, 0.25, 0.15]
        meal_names = ["الإفطار", "الغداء", "العشاء"] if meal_count == 3 else ["الإفطار", "الغداء", "العشاء", "سناك"]
        
        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- عرض الوجبات ----------
        for name, ratio in zip(meal_names, split_ratios):
            target_cals = total_calories * ratio
            selected = []
            current_sum = 0

            # اختيار عشوائي حتى نصل للسعرات المستهدفة ±10%
            for _, row in df.sample(frac=1).iterrows():
                if abs(current_sum - target_cals) < 100:
                    break
                if current_sum + row["calories"] <= target_cals + 80:
                    selected.append(row)
                    current_sum += row["calories"]

            st.markdown(f"<div class='card-meal'><div class='meal-title'>{name} 🍴</div>", unsafe_allow_html=True)
            for item in selected:
                st.markdown(f"<div class='meal-item'>• {item['name']} — {int(item['calories'])} سعرة حرارية</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top:6px;font-weight:600;'>إجمالي السعرات: {int(current_sum)} سعرة حرارية</p></div>", unsafe_allow_html=True)
