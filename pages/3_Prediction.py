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
with st.container():
    # Tinggi
    tinggi = st.number_input('Tinggi badan (m)', value=1.7, placeholder="Type a number...")
    st.caption('Use . instead of ,')

    # Berat
    berat = st.number_input('Berat badan (kg)', value=60, placeholder="Type a number...")
    st.caption('Use . instead of ,')

    # BMI
    bmi = round(berat/(tinggi*tinggi), 2)
    if st.button('BMI'):
        st.write('BMI: ', bmi)

    # Age
    age = st.selectbox("Age Category", ['Age 18 to 24', 'Age 25 to 29', 'Age 30 to 34', 
                            'Age 35 to 39', 'Age 40 to 44', 'Age 45 to 49', 
                            'Age 50 to 54', 'Age 55 to 59', 'Age 60 to 64', 
                            'Age 65 to 69', 'Age 70 to 74', 'Age 75 to 79', 
                            'Age 80 or older',])

    if age == 'Age 18 to 24':
        age = 0
    elif age == 'Age 25 to 29':
        age = 1
    elif age == 'Age 30 to 34':
        age = 2
    elif age == 'Age 35 to 39':
        age = 3
    elif age == 'Age 40 to 44':
        age = 4
    elif age == 'Age 45 to 49':
        age = 5
    elif age == 'Age 50 to 54':
        age = 6
    elif age == 'Age 55 to 59':
        age = 7
    elif age == 'Age 60 to 64':
        age = 8
    elif age == 'Age 65 to 69':
        age = 9
    elif age == 'Age 70 to 74':
        age = 10
    elif age == 'Age 75 to 79':
        age = 11
    elif age == 'Age 80 or older':
        age = 12

    # Smoke status
    smoke = st.selectbox("Smoke status", ['Current smoker - every day', 
                                        'Current smoker - some days', 
                                        'Former smoker', 'Never smoked'])

    if smoke == 'Current smoker - every day':
        smoke = 0
    elif smoke == 'Current smoker - some days':
        smoke = 1
    elif smoke == 'Former smoker':
        smoke = 2
    elif smoke == 'Never smoked':
        smoke = 3

    # E cigarette
    ecigar = st.selectbox("ECigarette Usage", ['Never use', 
                                            'Not at all (right now)', 
                                            'Everyday', 'Somedays'])

    if ecigar == 'Never use':
        ecigar = 0
    elif ecigar == 'Not at all (right now)':
        ecigar = 1
    elif ecigar == 'Everyday':
        ecigar = 2
    elif ecigar == 'Somedays':
        ecigar = 3

    # Alcohol
    alcohol = st.selectbox("Alcohol", ["Yes", "No"])

    if alcohol == 'Yes':
        alcohol = 1
    elif alcohol == 'No':
        alcohol = 0

    # Physical Active
    physic = st.selectbox("Physically active", ["Yes", "No"])

    if physic == 'Yes':
        physic = 1
    elif physic == 'No':
        physic = 0

    # Sleep Hour
    sleep = st.slider('Sleep hour per day', 3.0, 11.0, 8.0)


heart_attack_diag = ''
print(tinggi, berat, bmi, age, smoke, ecigar, alcohol, physic, sleep)
if st.button('Predict'):
    input = (tinggi, berat, bmi, age, smoke, ecigar, alcohol, physic,sleep)
    as_array = np.array(input)
    reshape = as_array.reshape(1, -1)
    std_data = scaler.transform(reshape)
    print(std_data)
    heart_attack_pred = jantung_model.predict(std_data)

    if (heart_attack_pred[0]==0):
        heart_attack_diag = 'Tidak berpotensi menderita penyakit jantung'
    else:
        heart_attack_diag = 'Berpotensi menderita penyakit jantung'
    
    st.success(heart_attack_diag)