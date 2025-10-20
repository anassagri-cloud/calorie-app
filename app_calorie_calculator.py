import streamlit as st

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
            border-left: 6px solid #16a34a;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
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
st.markdown('<div class="sub-title">حاسبة السعرات الحرارية اليومية بألوان الصحة والطاقة 🌿🍊</div>', unsafe_allow_html=True)

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

    st.markdown(
        "<div class='metric-container'><b>💡 نصيحة:</b> حافظ على طاقتك وتوازن صحتك بالأكل المتنوع والنشاط المستمر 🌿🍊</div>",
        unsafe_allow_html=True
    )

    # ---------- قسم النصائح الصحية ----------
    st.markdown("""
    <div class='tip-box'>
    <h3>📘 توصيات صحية مهمة</h3>
    <ul>
        <li>يتغير احتياجك من السعرات الحرارية بتغير نشاطك البدني أو بتغير وزنك.</li>
        <li>تناول أطعمة صحية قليلة الملح والسكر والدهون.</li>
        <li>مارس النشاط البدني 150 دقيقة أسبوعيًا من الأنشطة الهوائية معتدلة الشدة (مثل المشي السريع، الدراجة، السباحة).</li>
        <li>أو 75 دقيقة من الأنشطة الهوائية عالية الشدة أسبوعيًا (مثل الجري أو كرة القدم).</li>
        <li>يمكن الدمج بين النشاط المعتدل والعالي لتحقيق التوازن.</li>
        <li>لزيادة أو إنقاص نصف كجم بالأسبوع، أضف أو احذف 500 سعرة حرارية يوميًا.</li>
        <li>لزيادة أو إنقاص كيلوجرام واحد بالأسبوع، أضف أو احذف 1000 سعرة حرارية يوميًا.</li>
    </ul>
    <p><b>📎 للحصول على دليل السعرات الحرارية لخفض الوزن:</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- زر تحميل PDF ----------
    with open("SugarGuideMain.pdf", "rb") as pdf_file:
        st.download_button(
            label="📥 تحميل دليل السعرات الحرارية (PDF)",
            data=pdf_file,
            file_name="SugarGuideMain.pdf",
            mime="application/pdf",
            help="اضغط هنا لتحميل الدليل الكامل لخفض الوزن"
        )
