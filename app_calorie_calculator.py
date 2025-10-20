import streamlit as st

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

    protein = (calories * 0.3) / 4
    carbs = (calories * 0.4) / 4
    fats = (calories * 0.3) / 9

    return {
        "BMR": round(bmr, 2),
        "TDEE": round(tdee, 2),
        "Calories": round(calories, 2),
        "Protein (g)": round(protein, 1),
        "Carbs (g)": round(carbs, 1),
        "Fats (g)": round(fats, 1)
    }

st.set_page_config(page_title="🔥 حاسبة السعرات الحرارية", layout="centered")
st.title("🔥 حاسبة السعرات الحرارية اليومية")
st.markdown("احسب احتياجك اليومي من السعرات بناءً على وزنك، طولك، عمرك، ونشاطك.")

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

if st.button("احسب السعرات 🔥"):
    result = calculate_calories(weight, height, age, gender, activity, goal)

    st.subheader("🔹 النتائج:")
    st.write(f"**معدل الأيض الأساسي (BMR):** {result['BMR']} سعرة")
    st.write(f"**السعرات اليومية (TDEE):** {result['TDEE']} سعرة")
    st.write(f"**السعرات المطلوبة لهدفك:** {result['Calories']} سعرة")

    st.markdown("---")
    st.subheader("🍽️ توزيع الماكروز:")
    col1, col2, col3 = st.columns(3)
    col1.metric("بروتين (غرام)", result["Protein (g)"])
    col2.metric("كربوهيدرات (غرام)", result["Carbs (g)"])
    col3.metric("دهون (غرام)", result["Fats (g)"])

    st.markdown("---")
    st.info("💡 نصيحة: يمكنك تعديل الأهداف أسبوعيًا حسب تطور وزنك.")
