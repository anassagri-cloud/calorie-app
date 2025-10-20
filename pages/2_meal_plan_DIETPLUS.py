import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Meal Plan DIETPLUS")

st.title("🍱 Meal Plan from DIETPLUS Menu")
st.markdown("Select your daily calorie target and get random meal suggestions from the DIETPLUS menu.")

@st.cache_data
def load_menu():
    file_path = "pice_menu_DIETPLUS_simple.xlsx"
    df = pd.read_excel(file_path)
    df = df.dropna(subset=['name arabic', 'Calorie'])
    return df

try:
    menu = load_menu()
except Exception as e:
    st.error("❌ File 'pice_menu_DIETPLUS_simple.xlsx' not found. Please upload it to the same folder.")
    st.stop()

calories_target = st.number_input("Enter your daily calorie target:", 1200, 4000, 2200)

if st.button("Generate Plan 🍴"):
    st.subheader(f"🔹 Daily Meal Plan ({calories_target} Calories):")

    meal_distribution = {
        "Breakfast": 0.3,
        "Lunch": 0.4,
        "Dinner": 0.2,
        "Snack": 0.1
    }

    for meal, ratio in meal_distribution.items():
        target_cal = calories_target * ratio
        subset = menu.sample(5)
        subset["diff"] = abs(subset["Calorie"] - target_cal / len(subset))
        chosen = subset.sort_values("diff").head(1).iloc[0]

        st.write(f"### {meal}")
        st.write(f"**{chosen['name arabic']}**")
        st.write(f"🔹 Calories: {chosen['Calorie']} kcal")
        st.markdown("---")

    st.success("✅ This is an approximate meal plan based on DIETPLUS data.")
