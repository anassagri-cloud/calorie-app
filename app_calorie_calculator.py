import os
import math
import streamlit as st
import matplotlib.pyplot as plt

# ---------- Page ----------
st.set_page_config(page_title="CaloriesMe — حاسبة السعرات", layout="wide")

# ---------- Theme / Palette ----------
GREEN = "#16a34a"      # Health
ORANGE = "#f97316"     # Energy
GRAY_BG = "#eef2f6"    # Soft gray
CARD_BG = "rgba(255,255,255,0.7)"  # glassy
BORDER_SOFT = "0px 10px 30px rgba(2,8,23,0.08)"

# ---------- Assets (Banner) ----------
# يمكنك تغيير الرابط لصور أخرى من Unsplash/Pexels
BANNER_URL = "https://images.unsplash.com/photo-1579758629934-095eddd2d6f4?q=80&w=1600&auto=format&fit=crop"   # وجبة صحية متوازنة
ATHLETE_URL = "https://images.unsplash.com/photo-1599058917212-d750089bc07c?q=80&w=1600&auto=format&fit=crop"  # شخص يمارس الجري في الخارج


# ---------- Global CSS (RTL + Glass + Banner) ----------
st.markdown(f"""
<style>
  :root {{
    --green: {GREEN};
    --orange: {ORANGE};
    --graybg: {GRAY_BG};
  }}
  body {{
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 40%, #fff7ed 100%);
    background-attachment: fixed;
    direction: rtl !important;
  }}
  div[data-testid="stAppViewContainer"] {{
    direction: rtl !important;
    text-align: right !important;
  }}
  input, select, textarea, label {{ direction: rtl !important; text-align: right !important; }}

  /* Top bar */
  .topbar {{
    position: sticky; top: 0; z-index: 10;
    background: rgba(255,255,255,0.6); backdrop-filter: saturate(180%) blur(14px);
    border-bottom: 1px solid rgba(15,23,42,.06);
    display:flex; align-items:center; justify-content:space-between;
    padding: 10px 18px; margin: -16px -16px 12px -16px;
  }}
  .brand {{
    display:flex; gap:10px; align-items:center; font-weight:800; color:#0f172a;
  }}
  .bolt {{
    width:28px; height:28px; border-radius:8px; display:grid; place-items:center;
    background: linear-gradient(135deg, var(--orange), var(--green)); color:white; font-weight:900;
    box-shadow: 0 6px 18px rgba(249,115,22,.25);
  }}
  .top-links a {{
    color:#334155; text-decoration:none; font-weight:600; margin-left:12px;
  }}

  /* Banner */
  .banner {{
    position: relative; border-radius:20px; overflow:hidden; height: 280px;
    box-shadow:{BORDER_SOFT}; margin: 4px 0 16px;
    background: #000;
  }}
  .banner .layer {{
    position:absolute; inset:0; display:grid; grid-template-columns: 2fr 1fr;
  }}
  .banner .left {{
    background-image: url('{BANNER_URL}');
    background-size: cover; background-position:center;
  }}
  .banner .right {{
    background-image: url('{ATHLETE_URL}');
    background-size: cover; background-position:center;
  }}
  .banner::after {{
    content:""; position:absolute; inset:0;
    background: linear-gradient(90deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,.15) 45%, rgba(0,0,0,.45) 100%),
                radial-gradient(1200px 280px at 10% 50%, rgba(22,163,74,.25), transparent 60%);
  }}
  .banner .headline {{
    position:absolute; inset:0; display:flex; flex-direction:column; justify-content:center; padding: 0 28px;
    color:white; text-shadow: 0 2px 10px rgba(0,0,0,.35);
  }}
  .headline h1 {{ margin:0 0 6px; font-size:36px; font-weight:900; }}
  .headline p {{ margin:0; font-size:16px; opacity:.95; }}

  /* Titles */
  .section-title {{
    color:#065f46; font-weight:900; font-size:22px; margin: 6px 0 12px;
  }}
  .subtitle {{
    color:#475569; font-size:15px; margin:-6px 0 18px;
  }}

  /* Cards (glass) */
  .card {{
    background:{CARD_BG}; backdrop-filter: blur(10px);
    border: 1px solid rgba(148,163,184,.25);
    border-right: 6px solid var(--green);
    border-radius:16px; padding:18px; margin:12px 0;
    box-shadow:{BORDER_SOFT};
    animation: rise .5s ease both;
  }}

  /* Metrics grid */
  .row-3 {{
    display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:12px; align-items:stretch;
  }}
  .metric-box {{
    background: rgba(255,255,255,.8); border:1px solid rgba(148,163,184,.25);
    border-radius:14px; padding:14px; box-shadow:{BORDER_SOFT}; display:flex; gap:10px;
    align-items:center;
  }}
  .metric-ico {{
    width:42px; height:42px; border-radius:10px; display:grid; place-items:center;
    background: linear-gradient(135deg, var(--green), var(--orange)); color:white; font-weight:900;
    box-shadow: 0 8px 18px rgba(16,185,129,.25);
  }}
  .metric-label {{ color:#64748b; font-weight:700; font-size:13px; }}
  .metric-value {{ color:#0f172a; font-weight:900; font-size:20px; }}

  /* Buttons */
  .stButton>button {{
    background: var(--orange); color:white; font-weight:800; border:none;
    border-radius:12px; height:50px; width:100%;
  }}
  .stButton>button:hover {{ background:#fb923c; }}

  /* Progress */
  .progress-wrap {{ margin:12px 0 6px; }}
  .progress-track {{
    width:100%; height:26px; border-radius:10px; background:#e5e7eb; overflow:hidden;
    box-shadow: inset 0 0 0 1px #e2e8f0;
  }}
  .progress-bar {{
    height:100%; width:0%; background: linear-gradient(90deg, var(--green), var(--orange));
    transition: width 1200ms ease;
  }}

  @keyframes rise {{
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

# ---------- Top bar ----------
st.markdown("""
<div class="topbar">
  <div class="brand">
    <div class="bolt">⚡</div>
    <div>CaloriesMe — حاسبة السعرات</div>
  </div>
  <div class="top-links">
    <a href="#form">الحاسبة</a>
    <a href="#results">النتائج</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Banner ----------
st.markdown("""
<div class="banner">
  <div class="layer">
    <div class="left"></div>
    <div class="right"></div>
  </div>
  <div class="headline">
    <h1>ابدأ رحلتك الصحية اليوم 💚</h1>
    <p>مزيج متوازن من التغذية والنشاط — احسب سعراتك خلال ثوانٍ، واحصل على توزيع ماكروز ووجبات مقترحة.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Form ----------
st.markdown('<div id="form"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 أدخل بياناتك</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">لنحتاج فقط إلى بعض المعلومات الأساسية لحساب احتياجك اليومي بدقة.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    age = st.number_input("العمر", 10, 90, 25, step=1)
with col2:
    weight = st.number_input("الوزن (كجم)", 40, 250, 70, step=1)
    height = st.number_input("الطول (سم)", 120, 230, 170, step=1)
with col3:
    activity = st.selectbox(
        "مستوى النشاط البدني",
        ["خامل (بدون نشاط)", "نشاط خفيف (1-3 أيام/أسبوع)", "نشاط متوسط (3-5 أيام/أسبوع)",
         "نشاط عالي (6-7 أيام/أسبوع)", "نشاط شديد جدًا"]
    )
    goal = st.radio("الهدف", ["خسارة الوزن", "ثبات الوزن", "زيادة الوزن"], horizontal=True)

calc = st.button("احسب السعرات 🔥")

# ---------- Compute & Show ----------
if calc:
    calories, bmr, tdee = calculate_all(weight, height, age, gender, activity, goal)
    bmi = bmi_value(weight, height)
    iw = ideal_weight(height, gender)
    iw_cal = int(calculate_bmr(iw, height, age, gender) * get_activity_factor(activity))
    p, c, f = macro_split(calories)
    meals, meals_msg, meals_tips = meal_suggestion(calories, goal)

    # Metrics
    st.markdown('<div id="results"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 لمحة سريعة</div>', unsafe_allow_html=True)

    st.markdown('<div class="row-3">', unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-ico">🔥</div>
        <div>
          <div class="metric-label">السعرات الحالية</div>
          <div class="metric-value">{calories:,} سعرة</div>
        </div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-ico">⚙️</div>
        <div>
          <div class="metric-label">BMR</div>
          <div class="metric-value">{bmr:,}</div>
        </div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="metric-box">
        <div class="metric-ico">🏃</div>
        <div>
          <div class="metric-label">TDEE</div>
          <div class="metric-value">{tdee:,}</div>
        </div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Details Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### النتائج المتقدمة", unsafe_allow_html=True)
    st.markdown(f"""
      🔹 **مؤشر كتلة الجسم (BMI):** {bmi}<br>
      🔹 **الوزن المثالي:** {iw} كجم<br>
      🔹 **السعرات المقترحة للوزن المثالي:** {iw_cal:,} سعرة<br>
      🔹 **عدد الوجبات المقترحة:** {meals} / اليوم
    """, unsafe_allow_html=True)

    # Progress toward ideal weight
    progress_ratio = max(0.0, min(1.0, iw / weight)) if weight > 0 else 0.0
    percent = int(progress_ratio * 100)
    color = "var(--green)" if percent >= 95 else ("#f59e0b" if percent >= 80 else "#ef4444")
    st.markdown(f"""
      <div class="progress-wrap">
        <div class="progress-track">
          <div class="progress-bar" style="width:{percent}%; background:{color};"></div>
        </div>
        <p style="margin:.4rem 0 0; color:#334155;">📈 مدى الاقتراب من الوزن المثالي: {percent}%</p>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Macros
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🥦 توزيع الماكروز اليومية", unsafe_allow_html=True)
    st.markdown(f"🥩 **بروتين:** {p} جم&nbsp;&nbsp;|&nbsp;&nbsp;🍚 **كربوهيدرات:** {c} جم&nbsp;&nbsp;|&nbsp;&nbsp;🧈 **دهون:** {f} جم", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    labels = ["Protein (g)", "Carbs (g)", "Fat (g)"]
    values = [p, c, f]
    ax.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Meal guidance
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🍽️ توجيهات الوجبات", unsafe_allow_html=True)
    st.write(meals_msg)
    st.markdown("<ul>" + "".join([f"<li>{t}</li>" for t in meals_tips]) + "</ul>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips (health)
    st.markdown("""
      <div class="card">
        <h4 style="margin:0 0 8px 0;">📘 توصيات صحية</h4>
        <ul style="line-height:1.9; color:#334155;">
          <li>احتياجك يتغير بتغير النشاط والوزن.</li>
          <li>قلّل الملح والسكر والدهون، واختر أطعمة كاملة.</li>
          <li>150 دقيقة/أسبوع نشاط معتدل أو 75 دقيقة عالي الشدة (أو مزيج).</li>
          <li>±0.5 كجم/أسبوع ≈ ±500 سعرة يوميًا، ±1 كجم/أسبوع ≈ ±1000 سعرة يوميًا.</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)

    # Guide PDF (optional)
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

else:
    st.info("أدخل بياناتك ثم اضغط **احسب السعرات 🔥** لعرض النتائج والماكروز والاقتراحات.")
