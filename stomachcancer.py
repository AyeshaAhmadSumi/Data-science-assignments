import streamlit as st
import numpy as np
import pickle
import pandas as pd

st.set_page_config(
    page_title="Stomach Cancer Risk Model",
    page_icon="🎗",
    layout="wide"
)

@st.cache_resource
def load_model():
    return pickle.load(open('logr_model.pkl', 'rb'))

@st.cache_resource
def load_preprocessor():
    return pickle.load(open('preprocessor.pkl', 'rb'))

model = load_model()
preprocessor = load_preprocessor()

def make_prediction(input_data):
    input_df = pd.DataFrame([input_data], columns=[
        'age', 'gender', 'ethnicity', 'geographical_location', 'family_history',
        'smoking_habits', 'alcohol_consumption', 'helicobacter_pylori_infection',
        'dietary_habits', 'existing_conditions', 'endoscopic_images', 'biopsy_results',
        'ct_scan', 'mature_mirna_acc', 'mature_mirna_id', 'target_symbol',
        'target_entrez', 'target_ensembl', 'diana_microt', 'elmmo', 'microcosm',
        'miranda', 'mirdb', 'pictar', 'pita', 'targetscan', 'predicted.sum', 'all.sum'
    ])

    

    st.write("### Debug: Input DataFrame")
    st.dataframe(input_df)
    st.write("### Debug: Data Types")
    st.write(input_df.dtypes)

    # Preprocess and predict
    preprocessed_data = preprocessor.transform(input_df)
    prediction = model.predict(preprocessed_data)

    return prediction[0]

# ---- UI Layout ----

st.title('Stomach Cancer Prediction 🎗')
st.image('Stomach.png', use_container_width=True)

st.markdown("""
Please fill in the information below, and we'll predict your risk of stomach cancer based on the data provided.
""")

# ---- Input Fields ----

age = st.number_input('Age', 1, 100, 50, step=1)

sex = st.selectbox('Sex', ['Male', 'Female'])
ethnicity = st.selectbox('Ethnicity', ['Ethnicity_A', 'Ethnicity_B', 'Ethnicity_C'])
geographical_location = st.selectbox('Geographical Location', ['California', 'Other'])

# Map Yes/No to 1/0
def yes_no_to_num(value):
    return 1 if value == 'Yes' else 0

family_history = yes_no_to_num(st.selectbox('Family History of Stomach Cancer', ['Yes', 'No']))
smoking_habits = yes_no_to_num(st.selectbox('Smoking Habits', ['Yes', 'No']))
alcohol_consumption = yes_no_to_num(st.selectbox('Alcohol Consumption', ['Yes', 'No']))
helicobacter_pylori_infection = yes_no_to_num(st.selectbox('H. Pylori Infection', ['Yes', 'No']))

dietary_habits = st.selectbox('Dietary Habits', ['Low_salt', 'High_salt'])
existing_conditions = st.selectbox('Existing Conditions', ['Chronic Gastritis', 'Diabetes'])


# Numeric inputs
endoscopic_images = st.number_input('Endoscopic Images (score)', 0, 10, 5)
biopsy_results = st.number_input('Biopsy Results (score)', 0, 10, 5)
ct_scan = st.number_input('CT Scan (score)', 0, 10, 5)
mature_mirna_acc = st.number_input('Mature miRNA ACC', 0, 10, 5)
mature_mirna_id = st.number_input('Mature miRNA ID', 0, 10, 5)
target_symbol = st.number_input('Target Symbol', 0, 10, 5)
target_entrez = st.number_input('Target Entrez', 0, 10, 5)
target_ensembl = st.number_input('Target Ensembl', 0, 10, 5)
diana_microt = st.number_input('Diana microT', 0, 10, 5)
elmmo = st.number_input('ELMMo', 0, 10, 5)
microcosm = st.number_input('MicroCosm', 0, 10, 5)
miranda = st.number_input('Miranda', 0, 10, 5)
mirdb = st.number_input('miRDB', 0, 10, 5)
pictar = st.number_input('PicTar', 0, 10, 5)
pita = st.number_input('PITA', 0, 10, 5)
targetscan = st.number_input('TargetScan', 0, 10, 5)
predicted_sum = st.number_input('Predicted Sum', 0, 10, 5)
all_sum = st.number_input('All Sum', 0, 10, 5)

# ---- Prepare Data for Prediction ----

input_data = [
    int(age),
    sex,
    ethnicity,
    geographical_location,
    family_history,
    smoking_habits,
    alcohol_consumption,
    helicobacter_pylori_infection,
    dietary_habits,
    existing_conditions,
    float(endoscopic_images),
    float(biopsy_results),
    float(ct_scan),
    float(mature_mirna_acc),
    float(mature_mirna_id),
    float(target_symbol),
    float(target_entrez),
    float(target_ensembl),
    float(diana_microt),
    float(elmmo),
    float(microcosm),
    float(miranda),
    float(mirdb),
    float(pictar),
    float(pita),
    float(targetscan),
    float(predicted_sum),
    float(all_sum)
]

# ---- Prediction ----

if st.button('Predict'):
    try:
        prediction = make_prediction(input_data)
        if prediction == 1 or prediction > 0.5:
            st.error("⚠️ The model predicts: **Cancer Risk**")
            st.info("Please consult a healthcare professional.")
        else:
            st.success("✅ The model predicts: **No Cancer Risk**")
            st.info("You appear to be at low risk based on the input.")
    except Exception as e:
        st.exception(e)
