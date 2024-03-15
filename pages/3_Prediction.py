import pickle
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import streamlit as st

st.set_page_config(
    page_title = "Heart Attack Dashboard",
    page_icon="🧊",
    layout = "wide"
)

# Import model & scaler
jantung_model = pickle.load(open('jantung.sav', 'rb'))
scaler = joblib.load('scaler.save') 

# Judul
st.title('Heart Attack Prediction')
with st.container(border=True):

    input = [0 for x in range(0, 29)]

    # Tinggi
    tinggi = st.number_input('Tinggi badan (m)', value=1.7, placeholder="Type a number...")
    st.caption('Use . instead of ,')
    input[0] = tinggi

    # Berat
    berat = st.number_input('Berat badan (kg)', value=60, placeholder="Type a number...")
    st.caption('Use . instead of ,')
    input[1] = berat

    # BMI
    bmi = round(berat/(tinggi*tinggi), 2)
    if st.button('BMI'):
        st.write('BMI: ', bmi)
        input[2] = bmi

    col1, col2 = st.columns(2)

    # Age
    with col1:
        age = st.number_input('Usia', value=30, placeholder="Type a number...")

    if age <= 24:
        input[4] = 1
    elif 25 <= age <= 29:
        input[5] = 1
    elif 30 <= age <= 34:
        input[6] = 1
    elif 35 <= age <= 39:
        input[7] = 1
    elif 40 <= age <= 44:
        input[8] = 1
    elif 45 <= age <= 49:
        input[9] = 1
    elif 50 <= age <= 54:
        input[10] = 1
    elif 55 <= age <= 59:
        input[11] = 1
    elif 60 <= age <= 64:
        input[12] = 1
    elif 65 <= age <= 69:
        input[13] = 1
    elif 70 <= age <= 74:
        input[14] = 1 
    elif 75 <= age <= 79:
        input[15] = 1
    elif 80 <= age:
        input[16] = 1

    # Smoke status
    with col2:
        smoke = st.selectbox("Smoke status", ['Current smoker - every day', 
                                        'Current smoker - some days', 
                                        'Former smoker', 'Never smoked'])

    if smoke == 'Current smoker - every day':
        input[17] = 1
    elif smoke == 'Current smoker - some days':
        input[18] = 1
    elif smoke == 'Former smoker':
        input[19] = 1
    elif smoke == 'Never smoked':
        input[20] = 1

    # E cigarette
    with col1:
        ecigar = st.selectbox("ECigarette Usage", ['Never use', 
                                            'Not at all (right now)', 
                                            'Everyday', 'Somedays'])

    if ecigar == 'Everyday':
        input[21] = 1
    elif ecigar == 'Never use':
        input[22] = 1
    elif ecigar == 'Not at all (right now)':
        input[23] = 1
    elif ecigar == 'Somedays':
        input[24] = 1

    # Alcohol
    with col2:
        alcohol = st.selectbox("Alcohol", ["Yes", "No"])

    if alcohol == 'No':
        input[25] = 1
    elif alcohol == 'Yes':
        input[26] = 1

    # Physical Active
    with col1:
        physic = st.selectbox("Physically active", ["Yes", "No"])

    if physic == 'No':
        input[27] = 1
    elif physic == 'Yes':
        input[28] = 1

    # Sleep Hour
    with col2:
        sleep = st.slider('Sleep hour per day', 3.0, 11.0, 8.0)
        input[3] = sleep

heart_attack_diag = ''
if st.button('Predict'):
    input = tuple(input)
    as_array = np.array(input)
    reshape = as_array.reshape(1, -1)
    std_data = scaler.transform(reshape)
    heart_attack_pred = jantung_model.predict(std_data)

    if (heart_attack_pred[0]==0):
        heart_attack_diag = 'Tidak berpotensi menderita penyakit jantung'
    else:
        heart_attack_diag = 'Berpotensi menderita penyakit jantung'
    
    st.success(heart_attack_diag)