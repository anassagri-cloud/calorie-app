import streamlit as st
import math
import os

# إعداد الصفحة
st.set_page_config(page_title="حاسبة السعرات - Diet Plus", layout="centered")

# ---------- CSS ----------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 50%, #fff7ed 100%);
            background-attachment: fixed;
            direction: rtl !important;
        }
        div[data-testid="stAppViewContainer"] {
            direction: rtl !important;
            text-align: right !important;
        }
        div[data-testid="stVerticalBlock"] {
            direction: rtl !important;
        }
        .main-title {
            text-align: center;
            font-size: 38px;
            color: #065f46;
            font-weight: bold;
            margin-top: 90px;
            direction: rtl;
        }
        .sub-title {
            text-align: center;
            color: #444;
            font-size: 18px;
            margin-bottom: 25px;
            direction: rtl;
        }
        .card {
            background-color: #ffffffcc;
            border-right: 6px solid #16a34a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            direction: rtl;
            text-align: right;
            font-size: 18px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        }
        .macro-card {
            background-color: #fefce8;
            border-right: 6px solid #f59e0b;
            border-radius: 12px;
            padding: 20px;
            direction: rtl;
            text-align: right;
            font-size: 18px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
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
        input, select, textarea, label {
            direction: rtl !important;
            text-align: right !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- العنوان ----------
st.markdown('<div class="main-title">🔥 حاسبة السعرات الحرارية</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نتائجك الصحية بشكل منظم وواضح 🌿🍊</div>', unsafe_allow_html=True)

# ---------- الدوال ----------
def calculate_bmr(weight, height, age, gender):
    return 10 * weight + 6.25 * height - 5 * age + (5 if gender == "ذكر" else -161)

def get_activity_factor(level):
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
st.subheader("📋 أدخل بياناتك", divider="orange")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    weight = st.number_input("الوزن (كجم)", 40, 200, 70)
    height = st.number_input("الطول (سم)", 120, 220, 170)
with col2:
    age = st.number_input("العمر", 10, 80, 25)
    activity = st.selectbox(
        "مستوى النشاط البدني",
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

    # نسبة التقدم نحو الوزن المثالي
    progress = min(1.0, max(0.0, ideal_weight / weight))
    percent = int(progress * 100)
    color = "green" if percent >= 95 else ("orange" if percent >= 80 else "red")

    # ---------- النتائج ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <h3>📊 النتائج:</h3>
    🔹 <b>السعرات الحرارية الحالية:</b> {calories:,} سعرة حرارية<br>
    🔹 <b>معدل الأيض الأساسي (BMR):</b> {bmr:,} سعرة حرارية<br>
    🔹 <b>مؤشر كتلة الجسم (BMI):</b> {bmi}<br>
    🔹 <b>الوزن المثالي:</b> {ideal_weight} كجم<br>
    🔹 <b>السعرات المقترحة للوزن المثالي:</b> {ideal_calories:,} سعرة حرارية
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- شريط التقدم ----------
    st.markdown("<h4>📈 مدى اقترابك من الوزن المثالي:</h4>", unsafe_allow_html=True)
    progress_html = f"""
    <div style='width:100%;background:#e5e7eb;border-radius:10px;height:25px;'>
        <div style='width:{percent}%;background:{color};height:25px;border-radius:10px;'></div>
    </div>
    <p style='text-align:right;'>النسبة الحالية: {percent}%</p>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

    # ---------- الماكروز ----------
    st.markdown("<div class='macro-card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <h4>🥦 توزيع الماكروز اليومية:</h4>
    🥩 <b>بروتين:</b> {protein} جم<br>
    🍚 <b>كربوهيدرات:</b> {carbs} جم<br>
    🧈 <b>دهون:</b> {fat} جم
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- التوصيات ----------
    st.markdown("""
    <div class='tip-box'>
    <h3>📘 توصيات صحية مهمة</h3>
    <ul>
        <li>يتغير احتياجك من السعرات بتغير وزنك أو نشاطك البدني.</li>
        <li>تناول أطعمة صحية قليلة الملح والسكر والدهون.</li>
        <li>مارس النشاط البدني 150 دقيقة أسبوعيًا من الأنشطة المعتدلة.</li>
        <li>يمكن الدمج بين النشاط المعتدل والعالي لتحقيق التوازن.</li>
        <li>لزيادة أو إنقاص نصف كجم بالأسبوع، أضف أو احذف 500 سعرة حرارية يوميًا.</li>
        <li>لزيادة أو إنقاص كيلوجرام بالأسبوع، أضف أو احذف 1000 سعرة حرارية يوميًا.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------- تحميل PDF ----------
    if os.path.exists("SugarGuideMain.pdf"):
        with open("SugarGuideMain.pdf", "rb") as pdf_file:
            st.download_button(
                label="📥 تحميل دليل السعرات الحرارية (PDF)",
                data=pdf_file,
                file_name="SugarGuideMain.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ لم يتم العثور على ملف الدليل 'SugarGuideMain.pdf'. يرجى رفعه في نفس مجلد التطبيق.")
