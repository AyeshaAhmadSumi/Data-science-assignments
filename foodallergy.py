import streamlit as st
import pandas as pd

# Load the dataset (ensure 'FoodData.csv' is in your working directory)
@st.cache_data
def load_dataset():
    return pd.read_csv("FoodData.csv")

def main():
    st.set_page_config(page_title="Food Allergy Symptom Checker", layout="centered")
    st.title("🥗 Food Allergy Symptom Checker")

    st.write("### Step 1: Select a food item to see if it's associated with any known allergies.")
    data = load_dataset()

    # Dropdown for selecting food
    food_list = sorted(data["Food"].dropna().unique())
    selected_food = st.selectbox("Select a food item:", food_list)

    # Show allergy info for selected food
    food_info = data[data["Food"] == selected_food]
    if not food_info.empty:
        allergy = food_info["Allergy"].values[0]
        group = food_info["Group"].values[0]
        origin = food_info["Class"].values[0]

        st.write(f"**Food Group**: {group}")
        st.write(f"**Origin**: {origin}")
        if pd.notna(allergy):
            st.error(f"⚠️ Allergy associated with {selected_food}: **{allergy}**")
        else:
            st.success(f"No specific allergy associated with {selected_food} in the dataset.")

    st.markdown("---")
    st.write("### Step 2: Answer the following to assess your general food allergy risk.")

    hives = st.radio("1. Do you experience hives after eating certain foods?", ("Yes", "No"))
    itching = st.radio("2. Does your mouth or areas around it itch after eating certain foods?", ("Yes", "No"))
    nausea = st.radio("3. Do you feel nauseous or vomit after eating certain foods?", ("Yes", "No"))
    swelling = st.radio("4. Do you experience swelling in the face, mouth, or other areas after eating?", ("Yes", "No"))
    breathing = st.radio("5. Do you have difficulty breathing after eating certain foods?", ("Yes", "No"))

    risk_score = sum(symptom == "Yes" for symptom in [hives, itching, nausea, swelling, breathing])

    st.markdown("### Risk Assessment")
    if risk_score >= 4:
        st.warning("🚨 High risk for food allergies. Please consult a healthcare professional.")
    elif risk_score == 3:
        st.info("⚠️ Moderate risk. It’s advisable to talk to a healthcare provider.")
    else:
        st.success("✅ Low risk based on responses. Still, consult a doctor if you’re concerned.")

    st.caption("📝 This tool is for informational purposes only and not a substitute for medical advice.")

if __name__ == "__main__":
    main()
