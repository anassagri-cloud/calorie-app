import streamlit as st
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Diet Plus 🔥", layout="centered")

# ---------- CSS ----------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f1f5f9 0%, #ffffff 40%, #fff7ed 100%);
            background-attachment: fixed;
        }
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #16a34a;
            color: white;
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 12px;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            z-index: 999;
        }
        .navbar a {
            text-decoration: none;
            color: white;
            transition: 0.3s;
        }
        .navbar a:hover {
            color: #f97316;
        }
        .main-title {
            text-align: center;
            font-size: 42px;
            color: #065f46;
            font-weight: bold;
            margin-top: 90px;
        }
        .sub-title {
            text-align: center;
            color: #444;
            font-size: 20px;
            margin-bottom: 25px;
            font-weight: 600;
        }
        .stButton>button {
            background-color: #f97316;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            height: 50px;
            width: 100%;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #fb923c;
        }
        .metric-container {
            background-color: rgba(255,255,255,0.85);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
        }
        .block-container {
            background: transparent !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- شريط التنقل ----------
st.markdown("""
<div class="navbar">
    <a href="#home">🏠 الصفحة الرئيسية</a>
    <a href="#meals">🍱 خطة الوجبات</a>
    <a href="#tracking">📈 متابعة الوزن</a>
</div>
""", unsafe_allow_html=True)

# ---------- العنوان ----------
st.markdown('<div class="main-title" id="home">Diet Plus 🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">حاسبة السعرات الحرارية</div>', unsafe_allow_html=True)

# ---------- دوال الحساب ----------
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    if gender == "ذكر":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "أنثى":
        return 10 * weight + 6.25 * height - 5 * age - 161
    return 0

def get_activity_factor(level: str) -> float:
    factors = {
        "خامل (بدون نشاط)": 1.2,
        "نشاط خفيف (1-3 أيام/أسبوع)": 1.375,
        "نشاط متوسط (3-5 أيام/أسبوع)": 1.55,
        "نشاط عالي (6-7 أيام/أسبوع)": 1.725,
        "نشاط شديد جدًا": 1.9
    }
    return factors.get(level, 1.2)

def calculate_calories(weight, height, age, gender, activity, goal):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * get_activity_factor(activity)
    if goal == "خسارة الوزن":
        calories = tdee - 500
    elif goal == "زيادة الوزن":
        calories = tdee + 500
    else:
        calories = tdee

    # حساب الماكروز
    protein = (calories * 0.3) / 4
    carbs = (calories * 0.4) / 4
    fats = (calories * 0.3) / 9

    return round(calories, 2), round(bmr, 2), round(tdee, 2), round(protein, 1), round(carbs, 1), round(fats, 1)

# ---------- إدخال البيانات ----------
st.subheader("🧮 أدخل بياناتك")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    weight = st.number_input("الوزن (كجم)", 40, 200, 70)
    height = st.number_input("الطول (سم)", 120, 220, 170)
with col2:
    age = st.number_input("العمر", 10, 80, 25)
    activity = st.selectbox(
        "مستوى النشاط",
        ["خامل (بدون نشاط)", "نشاط خفيف (1-3 أيام/أسبوع)", "نشاط متوسط (3-5 أيام/أسبوع)",
         "نشاط عالي (6-7 أيام/أسبوع)", "نشاط شديد جدًا"]
    )
    goal = st.radio("الهدف", ["خسارة الوزن", "ثبات الوزن", "زيادة الوزن"])

# ---------- الحساب والنتائج ----------
if st.button("احسب السعرات 🔥"):
    calories, bmr, tdee, protein, carbs, fats = calculate_calories(weight, height, age, gender, activity, goal)

    st.markdown("---")
    st.subheader("📊 النتائج")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="BMR", value=f"{bmr}")
    with col2:
        st.metric(label="TDEE", value=f"{tdee}")
    with col3:
        st.metric(label="السعرات المطلوبة", value=f"{calories}")

    st.markdown("---")
    st.subheader("🍽️ توزيع الماكروز اليومية")
    col1, col2, col3 = st.columns(3)
    col1.metric("🥩 بروتين (غ)", f"{protein}")
    col2.metric("🍚 كربوهيدرات (غ)", f"{carbs}")
    col3.metric("🧈 دهون (غ)", f"{fats}")

    # ---------- الرسم البياني ----------
    st.markdown("### 🎨 توزيع الماكروز (شكل دائري)")
    fig, ax = plt.subplots()
    labels = ["بروتين", "كربوهيدرات", "دهون"]
    values = [protein * 4, carbs * 4, fats * 9]  # نعيد التحويل إلى سعرات
    colors = ["#16a34a", "#f97316", "#d1d5db"]

    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("---")
    st.markdown(
        "<div class='metric-container'><b>💡 نصيحة:</b> وزّع وجباتك بحيث تحتوي على جميع المكونات الغذائية للحصول على طاقة وصحة مثالية 🌿🍊</div>",
        unsafe_allow_html=True
    )

# ---------- أقسام إضافية ----------
st.markdown('<div id="meals"></div>', unsafe_allow_html=True)
st.header("🍱 خطة الوجبات")
st.info("قريبًا: سيتم ربط هذا القسم بملف DIETPLUS Excel لاقتراح وجبات مناسبة للسعرات.")

st.markdown('<div id="tracking"></div>', unsafe_allow_html=True)
st.header("📈 متابعة الوزن")
st.info("قريبًا: قسم لتسجيل الوزن الأسبوعي وعرضه في رسم بياني تفاعلي.")
