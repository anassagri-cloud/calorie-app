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

def suggest_meal_count(calories, goal):
    if calories < 1600:
        base_meals = 3
    elif calories < 2200:
        base_meals = 4
    else:
        base_meals = 5

    if goal == "زيادة الوزن":
        base_meals += 1
        note = "قسّم السعرات على وجبات أكثر صغيرة لدعم زيادة الوزن الصحية."
    elif goal == "خسارة الوزن":
        note = "حافظ على وجبات منتظمة مع وجبة خفيفة صحية بين الوجبات الرئيسية."
    else:
        note = "وزع السعرات على وجبات رئيسية متوازنة مع وجبات خفيفة عند الحاجة."

    base_meals = min(max(base_meals, 3), 6)
    return base_meals, note

# ---------- إدخال البيانات ----------
st.subheader("🧮 أدخل بياناتك", divider="orange")

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
    meal_count, meal_note = suggest_meal_count(calories, goal)

    st.markdown("---")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <h3>📊 النتائج:</h3>
    🔹 <b>السعرات الحرارية الحالية:</b> {calories:,} سعرة حرارية<br>
    🔹 <b>معدل الأيض الأساسي (BMR):</b> {bmr:,} سعرة حرارية<br>
    🔹 <b>مؤشر كتلة الجسم (BMI):</b> {bmi}<br>
    🔹 <b>الوزن المثالي:</b> {ideal_weight} كجم<br>
    🔹 <b>السعرات المقترحة للوزن المثالي:</b> {ideal_calories:,} سعرة حرارية
    🔹 <b>السعرات المقترحة للوزن المثالي:</b> {ideal_calories:,} سعرة حرارية<br>
    🔹 <b>عدد الوجبات المقترحة:</b> {meal_count} وجبات يوميًا
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='macro-card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <h4>🥦 توزيع الماكروز اليومية:</h4>
    🥩 <b>بروتين:</b> {protein} جم<br>
    🍚 <b>كربوهيدرات:</b> {carbs} جم<br>
    🧈 <b>دهون:</b> {fat} جم
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- قسم التوصيات ----------
    st.markdown("""
    <div class='tip-box'>
    <h3>📘 توصيات صحية مهمة</h3>
    <ul>
        <li>يتغير احتياجك من السعرات بتغير وزنك أو نشاطك البدني.</li>
        <li>تناول أطعمة صحية قليلة الملح والسكر والدهون.</li>
        <li>مارس النشاط البدني 150 دقيقة أسبوعيًا من الأنشطة المعتدلة (مثل المشي أو السباحة).</li>
        <li>يمكن الدمج بين النشاط المعتدل والعالي لتحقيق التوازن.</li>
        <li>لزيادة أو إنقاص نصف كجم بالأسبوع، أضف أو احذف 500 سعرة حرارية يوميًا.</li>
        <li>لزيادة أو إنقاص كيلوجرام بالأسبوع، أضف أو احذف 1000 سعرة حرارية يوميًا.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.info(f"🍽️ نصيحة الوجبات: {meal_note}")

    # ---------- زر تحميل PDF ----------
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
