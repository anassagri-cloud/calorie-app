# file: app_calorie_calculator.py
import os
import math
import streamlit as st
import matplotlib.pyplot as plt

with open("style_caloriesmebro.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Page ----------
st.set_page_config(page_title="حاسبة السعرات - تصميم حديث", layout="centered")

# ---------- Theme / Palette ----------
GREEN = "#16a34a"      # Health
ORANGE = "#f97316"     # Energy
GRAY_BG = "#f1f5f9"    # Soft gray
CARD_BG = "#ffffffcc"  # translucent white
YELLOW_BG = "#fefce8"
BORDER_SOFT = "0px 6px 16px rgba(0,0,0,0.08)"

# ---------- Global CSS (RTL + Animations) ----------
st.markdown(f"""
<style>
  :root {{
    --green: {GREEN};
    --orange: {ORANGE};
    --graybg: {GRAY_BG};
    --cardbg: {CARD_BG};
  }}
  body {{
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 50%, #fff7ed 100%);
    background-attachment: fixed;
    direction: rtl !important;
  }}
  div[data-testid="stAppViewContainer"] {{
    direction: rtl !important;
    text-align: right !important;
  }}
  input, select, textarea, label {{
    direction: rtl !important;
    text-align: right !important;
  }}
  .title {{
    text-align:center; color:#065f46; font-weight:800; font-size:38px; margin-top:12px;
    animation: fadeIn .8s ease both;
  }}
  .subtitle {{
    text-align:center; color:#475569; font-size:17px; margin:-4px 0 22px; animation: fadeIn .9s both;
  }}
  .card {{
    background:{CARD_BG}; border-right:6px solid var(--green); border-radius:14px; padding:18px 18px 6px;
    margin:12px 0; box-shadow:{BORDER_SOFT}; animation: slideUp .5s ease both;
  }}
  .macro-card {{
    background:{YELLOW_BG}; border-right:6px solid #f59e0b; border-radius:14px; padding:18px;
    margin:12px 0; box-shadow:{BORDER_SOFT}; animation: slideUp .6s ease both;
  }}
  .tips {{
    background:#ecfdf5; border-right:6px solid var(--green); border-radius:12px; padding:18px; margin-top:14px;
    animation: fadeIn 1s both;
  }}
  .tips ul {{
    list-style-type:"✅ "; padding-right:22px; line-height:1.9; color:#334155; margin:0;
  }}
  .progress-wrap {{ margin:12px 0 6px; }}
  .progress-track {{
    width:100%; height:26px; border-radius:10px; background:#e5e7eb; overflow:hidden;
    box-shadow: inset 0 0 0 1px #e2e8f0;
  }}
  .progress-bar {{
    height:100%; width:0%;
    background: linear-gradient(90deg, var(--green), var(--orange));
    transition: width 1200ms ease;  /* animate width after mount */
  }}
  .row-3 {{
    display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:12px; align-items:stretch;
  }}
  .metric-box {{
    background:white; border-radius:12px; padding:14px; box-shadow:{BORDER_SOFT};
    display:flex; flex-direction:column; gap:6px; animation: fadeIn .8s both;
  }}
  .metric-label {{ color:#64748b; font-weight:600; font-size:14px; }}
  .metric-value {{ color:#0f172a; font-weight:800; font-size:22px; }}

  .stButton>button {{
    background: var(--orange); color:white; font-weight:700; border:none;
    border-radius:12px; height:50px; width:100%;
  }}
  .stButton>button:hover {{ background:#fb923c; }}

  @keyframes fadeIn {{
    from {{ opacity:0; transform: translateY(4px); }}
    to   {{ opacity:1; transform: translateY(0);  }}
  }}
  @keyframes slideUp {{
    from {{ opacity:0; transform: translateY(12px); }}
    to   {{ opacity:1; transform: translateY(0);  }}
  }}
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    return 10 * weight + 6.25 * height - 5 * age + (5 if gender == "ذكر" else -161)

def get_activity_factor(level: str) -> float:
    return {
        "خامل (بدون نشاط)": 1.2,
        "نشاط خفيف (1-3 أيام/أسبوع)": 1.375,
        "نشاط متوسط (3-5 أيام/أسبوع)": 1.55,
        "نشاط عالي (6-7 أيام/أسبوع)": 1.725,
        "نشاط شديد جدًا": 1.9
    }.get(level, 1.2)

def calculate_all(weight, height, age, gender, activity, goal):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * get_activity_factor(activity)
    if goal == "خسارة الوزن":
        calories = tdee - 500
    elif goal == "زيادة الوزن":
        calories = tdee + 500
    else:
        calories = tdee
    return round(calories), round(bmr), round(tdee)

def bmi_value(weight, height_cm):
    h_m = height_cm / 100
    return round(weight / (h_m ** 2), 1)

def ideal_weight(height_cm, gender):
    return round((50 + 0.9 * (height_cm - 152)) if gender == "ذكر" else (45.5 + 0.9 * (height_cm - 152)), 1)

def macro_split(cal):
    p = round((cal * 0.25) / 4)   # g
    c = round((cal * 0.50) / 4)   # g
    f = round((cal * 0.25) / 9)   # g
    return p, c, f

def meal_suggestion(calories, goal):
    if calories <= 1400: base = 3
    elif calories <= 2000: base = 4
    elif calories <= 2600: base = 5
    else: base = 6
    tips = ["أدرج بروتينًا وخضارًا بكل وجبة.", "قسّم السعرات على اليوم لتجنب الجوع."]
    if goal == "زيادة الوزن":
        base = min(base + 1, 6)
        msg = "وجبات صغيرة ومتكررة مع سناكات عالية البروتين والسعرات."
        tips.append("استخدم مكسرات/ألبان كاملة الدسم كسناك غذائي.")
    elif goal == "خسارة الوزن":
        msg = "جدول وجبات منتظم لتثبيت الجوع والطاقة."
        tips.append("اختر سناك غني بالألياف قبل الجوع الشديد.")
    else:
        msg = "وجبات متوازنة مع سناك خفيف عند الحاجة."
        tips.append("وازن بين بروتين وكربوهيدرات معقدة ودهون صحية.")
    return base, msg, tips

# ---------- Header ----------
st.markdown('<div class="title">🔥 حاسبة السعرات الحرارية</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">تصميم عربي متحرك مستوحى من واجهات التغذية الحديثة</div>', unsafe_allow_html=True)

# ---------- Form ----------
st.subheader("📋 أدخل بياناتك", divider="orange")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    weight = st.number_input("الوزن (كجم)", 40, 250, 70, step=1)
    height = st.number_input("الطول (سم)", 120, 230, 170, step=1)
with col2:
    age = st.number_input("العمر", 10, 90, 25, step=1)
    activity = st.selectbox(
        "مستوى النشاط البدني",
        ["خامل (بدون نشاط)", "نشاط خفيف (1-3 أيام/أسبوع)", "نشاط متوسط (3-5 أيام/أسبوع)",
         "نشاط عالي (6-7 أيام/أسبوع)", "نشاط شديد جدًا"]
    )
    goal = st.radio("الهدف", ["خسارة الوزن", "ثبات الوزن", "زيادة الوزن"], horizontal=True)

# ---------- Compute & Show ----------
if st.button("احسب السعرات 🔥"):
    calories, bmr, tdee = calculate_all(weight, height, age, gender, activity, goal)
    bmi = bmi_value(weight, height)
    iw = ideal_weight(height, gender)
    iw_cal = int(calculate_bmr(iw, height, age, gender) * get_activity_factor(activity))
    p, c, f = macro_split(calories)
    meals, meals_msg, meals_tips = meal_suggestion(calories, goal)

    # Metrics row (animated feel by layout & CSS)
    st.markdown('<div class="row-3">', unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-label">السعرات الحالية</div>
        <div class="metric-value">{calories:,} سعرة</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-label">BMR</div>
        <div class="metric-value">{bmr:,}</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-label">TDEE</div>
        <div class="metric-value">{tdee:,}</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Results Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"""
      <h4 style="margin:0 0 10px 0;">📊 النتائج المتقدمة</h4>
      🔹 <b>مؤشر كتلة الجسم (BMI):</b> {bmi}<br>
      🔹 <b>الوزن المثالي:</b> {iw} كجم<br>
      🔹 <b>السعرات المقترحة للوزن المثالي:</b> {iw_cal:,} سعرة<br>
      🔹 <b>عدد الوجبات المقترحة:</b> {meals} / اليوم
    """, unsafe_allow_html=True)

    # Progress bar toward ideal weight
    progress_ratio = max(0.0, min(1.0, iw / weight)) if weight > 0 else 0.0
    percent = int(progress_ratio * 100)
    color = "var(--green)" if percent >= 95 else ("#f59e0b" if percent >= 80 else "#ef4444")
    st.markdown('<div class="progress-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
      <div class="progress-track">
        <div class="progress-bar" style="width:{percent}%; background:{color};"></div>
      </div>
      <p style="margin:.4rem 0 0; color:#334155;">📈 مدى الاقتراب من الوزن المثالي: {percent}%</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # end .card

    # Macro card
    st.markdown('<div class="macro-card">', unsafe_allow_html=True)
    st.markdown("### 🥦 توزيع الماكروز اليومية", unsafe_allow_html=True)
    st.markdown(f"🥩 <b>بروتين:</b> {p} جم<br>🍚 <b>كربوهيدرات:</b> {c} جم<br>🧈 <b>دهون:</b> {f} جم", unsafe_allow_html=True)

    # Macro pie (matplotlib only)
    fig, ax = plt.subplots()
    labels = ["Protein (g)", "Carbs (g)", "Fat (g)"]
    values = [p, c, f]
    ax.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Meal guidance
    st.markdown('<div class="macro-card">', unsafe_allow_html=True)
    st.markdown("### 🍽️ توجيهات الوجبات", unsafe_allow_html=True)
    st.write(meals_msg)
    st.markdown("<ul>" + "".join([f"<li>{t}</li>" for t in meals_tips]) + "</ul>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips (health)
    st.markdown("""
      <div class="tips">
        <h4 style="margin:0 0 8px 0;">📘 توصيات صحية</h4>
        <ul>
          <li>احتياجك يتغير بتغير النشاط والوزن.</li>
          <li>قلّل الملح والسكر والدهون، واختر أطعمة كاملة.</li>
          <li>150 دقيقة/أسبوع نشاط معتدل أو 75 دقيقة عالي الشدة (أو مزيج).</li>
          <li>±0.5 كجم/أسبوع ≈ ±500 سعرة يوميًا، ±1 كجم/أسبوع ≈ ±1000 سعرة يوميًا.</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)

    # Guide PDF
    if os.path.exists("SugarGuideMain.pdf"):
        with open("SugarGuideMain.pdf", "rb") as fh:
            st.download_button(
                label="📥 تنزيل دليل السعرات (PDF)",
                data=fh,
                file_name="SugarGuideMain.pdf",
                mime="application/pdf",
                help="تحميل الدليل الكامل لخفض الوزن"
            )
    else:
        st.caption("ℹ️ ارفع الملف SugarGuideMain.pdf بجوار هذا السكربت لإظهار زر التحميل.")

