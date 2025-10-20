 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app_calorie_calculator.py b/app_calorie_calculator.py
index a263f573793734702611aa8ffb4cb65ff7ea62d2..fc77d67601ba6a3fbaa70bab86e4921a1976abf7 100644
--- a/app_calorie_calculator.py
+++ b/app_calorie_calculator.py
@@ -1,27 +1,26 @@
 import streamlit as st
-import math
 import os
 
 # إعداد الصفحة
 st.set_page_config(page_title="حاسبة السعرات - Diet Plus", layout="centered")
 
 # ---------- CSS ----------
 st.markdown("""
     <style>
         body {
             background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 50%, #fff7ed 100%);
             background-attachment: fixed;
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
@@ -102,97 +101,143 @@ def calculate_calories(weight, height, age, gender, activity, goal):
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
 
+def suggest_meal_plan(calories, goal):
+    """اقترح عدد وجبات مناسب مع نصائح داعمة لكل هدف."""
+    if calories <= 1400:
+        base_meals = 3
+    elif calories <= 2000:
+        base_meals = 4
+    elif calories <= 2600:
+        base_meals = 5
+    else:
+        base_meals = 6
+
+    tips = [
+        "احرص على تضمين مصدر بروتين وخضروات في كل وجبة رئيسية.",
+        "قسّم مجموع السعرات بالتساوي على مدار اليوم لتجنب الجوع الحاد.",
+    ]
+
+    if goal == "زيادة الوزن":
+        base_meals = min(base_meals + 1, 6)
+        guidance = "اختر وجبات صغيرة ومتكررة مع إضافة سناكات غنية بالبروتين والسعرات."  # noqa: E501
+        tips.append("استخدم سناك غني بالسعرات بين الوجبات مثل المكسرات أو الزبادي الكامل.")
+    elif goal == "خسارة الوزن":
+        guidance = "التزم بوجبات منتظمة وثابتة لتثبيت مستوى الجوع والطاقة."  # noqa: E501
+        tips.append("اختر سناك خفيف غني بالألياف قبل الشعور بالجوع الشديد.")
+    else:
+        guidance = "حافظ على وجبات متوازنة مع سناك خفيف عند الحاجة لدعم الثبات."  # noqa: E501
+        tips.append("قسّم وجباتك بين بروتين، كربوهيدرات معقدة، ودهون صحية.")
+
+    return {
+        "count": base_meals,
+        "guidance": guidance,
+        "tips": tips,
+    }
+
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
+    meal_plan = suggest_meal_plan(calories, goal)
 
     st.markdown("---")
     st.markdown("<div class='card'>", unsafe_allow_html=True)
     st.markdown(f"""
     <h3>📊 النتائج:</h3>
     🔹 <b>السعرات الحرارية الحالية:</b> {calories:,} سعرة حرارية<br>
     🔹 <b>معدل الأيض الأساسي (BMR):</b> {bmr:,} سعرة حرارية<br>
     🔹 <b>مؤشر كتلة الجسم (BMI):</b> {bmi}<br>
     🔹 <b>الوزن المثالي:</b> {ideal_weight} كجم<br>
-    🔹 <b>السعرات المقترحة للوزن المثالي:</b> {ideal_calories:,} سعرة حرارية
+    🔹 <b>السعرات المقترحة للوزن المثالي:</b> {ideal_calories:,} سعرة حرارية<br>
+    🔹 <b>عدد الوجبات المقترحة:</b> {meal_plan["count"]} وجبات يوميًا
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
 
+    meal_guidance_html = [
+        "<div class='macro-card'>",
+        "<h4>🍽️ توجيهات الوجبات اليومية:</h4>",
+        f"<p>{meal_plan['guidance']}</p>",
+        "<ul>",
+        *[f"<li>{tip}</li>" for tip in meal_plan["tips"]],
+        "</ul>",
+        "</div>",
+    ]
+    st.markdown("".join(meal_guidance_html), unsafe_allow_html=True)
+
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
EOF
)
