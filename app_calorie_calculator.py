import streamlit as st
import math
import os

# إعداد الصفحة
st.set_page_config(page_title="Diet Plus 🔥", layout="centered")

# ---------- CSS للتصميم ----------
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
            font-size: 18px;
            margin-bottom: 25px;
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
            background-color: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
        .tip-box {
            background-color: #ecfdf5;
            border-right: 6px solid #16a34a;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            direction: rtl;
            text-align: right;
        }
        .tip-box ul {
            list-style-type: "✅ ";
            padding-right: 25px;
            font-size: 17px;
            color: #333;
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

# ---------- رأس الصفحة ----------
st.image("logo deit_final-1.png", width=200)
st.markdown('<div class="main-title" id="home">Diet Plus 🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">حاسبة السعرات وكتلة الجسم بألوان الصحة والطاقة 🌿🍊</div>', unsafe_allow_html=True)

# ---------- الدوال ----------
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    return 10 * weight + 6.25 * height - 5 * age + (5 if gender == "ذكر" else -161)

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
    return round(calories), round(bmr), round(tdee)

def calculate_bmi(weight, height):
    h_m = height / 100
    return round(weight / (h_m ** 2), 1)

def calculate_ideal_weight(height, gender):
    if gender == "ذكر":
        return round(50 + 0.9 * (height - 152), 1)
    else:
        return round(45.5 + 0.9 * (height - 152), 1)

def macro_split(calories):
    protein = round((calories * 0.25) / 4)
    carbs = round((calories * 0.5) / 4)
    fat = round((calories * 0.25) / 9)
    return protein, carbs, fat

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

# ---------- الحساب ----------
if st.button("احسب السعرات 🔥"):
    calories, bmr, tdee = calculate_calories(weight, height, age, gender, activity, goal)
    bmi = calculate_bmi(weight, height)
    ideal_weight = calculate_ideal_weight(height, gender)
    ideal_calories = int(calculate_bmr(ideal_weight, height, age, gender) * get_activity_factor(activity))
    protein, carbs, fat = macro_split(calories)

    st.markdown("---")
    st.subheader("📊 النتائج المتكاملة")

    st.markdown(f"""
    ### 🔹 السعرات الحالية المطلوبة: **{calories:,} سعرة حرارية**
    ### 🔹 السعرات للوزن المثالي: **{ideal_calories:,} سعرة حرارية**
    ### 🧍‍♂️ مؤشر كتلة الجسم (BMI): **{bmi}**
    ### ⚖️ الوزن المثالي: **{ideal_weight} كجم**
    """)
    
    st.markdown("---")
    st.subheader("🍎 توزيع الماكروز (Macronutrients)")
    st.markdown(f"""
    - 🥩 **بروتين:** {protein} جم  
    - 🍚 **كربوهيدرات:** {carbs} جم  
    - 🧈 **دهون:** {fat} جم  
    """)

    st.markdown("---")
    st.markdown(
        "<div class='metric-container'><b>💡 نصيحة:</b> استخدم هذه القيم كمرجع وحدث بياناتك أسبوعيًا لمتابعة التقدم!</div>",
        unsafe_allow_html=True
    )

    # ---------- قسم النصائح ----------
    st.markdown("""
    <div class='tip-box'>
    <h3>📘 توصيات صحية مهمة</h3>
    <ul>
        <li>يتغير احتياجك من السعرات الحرارية بتغير نشاطك البدني أو بتغير وزنك.</li>
        <li>تناول أطعمة صحية قليلة الملح والسكر والدهون.</li>
        <li>مارس النشاط البدني 150 دقيقة أسبوعيًا من الأنشطة الهوائية معتدلة الشدة.</li>
        <li>أو 75 دقيقة من الأنشطة الهوائية عالية الشدة أسبوعيًا.</li>
        <li>لزيادة أو إنقاص نصف كجم بالأسبوع، أضف أو احذف 500 سعرة حرارية يوميًا.</li>
        <li>لزيادة أو إنقاص كيلوجرام واحد بالأسبوع، أضف أو احذف 1000 سعرة حرارية يوميًا.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------- زر تحميل PDF ----------
    if os.path.exists("SugarGuideMain.pdf"):
        with open("SugarGuideMain.pdf", "rb") as pdf_file:
            st.download_button(
                label="📥 تحميل دليل السعرات الحرارية (PDF)",
                data=pdf_file,
                file_name="SugarGuideMain.pdf",
                mime="application/pdf"
            )
