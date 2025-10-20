import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="🔥 حاسبة السعرات الحرارية", layout="centered")

# ---------- واجهة الرأس ----------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            color: #ff5733;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            color: #555;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #ff5733;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            height: 50px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #ff784e;
            color: white;
        }
        .metric-container {
            background-color: #fff5f0;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔥 حاسبة السعرات الحرارية اليومية</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">احسب احتياجك اليومي من السعرات بناءً على وزنك، طولك، عمرك، ونشاطك.</div>', unsafe_allow_html=True)

# ---------- دوال الحساب ----------
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    if gender == "ذكر":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "أنثى":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return 0

def get_activity_factor(level: str) -> float:
    levels = {
        "خامل (بدون نشاط)": 1.2,
        "نشاط خفيف (1-3 أيام/أسبوع)": 1.375,
        "نشاط متوسط (3-5 أيام/أسبوع)": 1.55,
        "نشاط عالي (6-7 أيام/أسبوع)": 1.725,
        "نشاط شديد جدًا": 1.9
    }
    return levels.get(level, 1.2)

def calculate_calories(weight, height, age, gender, activity, goal):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * get_activity_factor(activity)
    if goal == "خسارة الوزن":
        calories = tdee - 500
    elif goal == "زيادة الوزن":
        calories = tdee + 500
    else:
        calories = tdee
    return round(calories, 2), round(bmr, 2), round(tdee, 2)

# ---------- واجهة الإدخال ----------
with st.container():
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

# ---------- حساب وإظهار النتائج ----------
if st.button("احسب السعرات 🔥"):
    calories, bmr, tdee = calculate_calories(weight, height, age, gender, activity, goal)

    st.markdown("---")
    st.subheader("📊 النتائج")

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="BMR", value=f"{bmr} 🔥")
        with col2:
            st.metric(label="TDEE", value=f"{tdee} 🔥")
        with col3:
            st.metric(label="السعرات المطلوبة", value=f"{calories} 🔥")

    st.markdown("---")
    st.markdown(
        "<div class='metric-container'><b>💡 نصيحة:</b> يمكنك تعديل هدفك أو مستوى النشاط للحصول على نتائج مختلفة.</div>",
        unsafe_allow_html=True
    )
