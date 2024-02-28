# Import library
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

# Config page
st.set_page_config(
    page_title = "Heart Attack Dashboard",
    page_icon="🧊",
    layout = "wide"
)

# Title
st.title('Analisis Faktor Risiko dan Perilaku Kesehatan Terhadap Serangan Jantung')

# Load dataframe
bf = pd.read_parquet('bf.parquet', engine='pyarrow')
bf = bf.drop(bf.columns[0], axis=1)

# Select box 1
with st.container():
    behaviour = st.selectbox("Behaviour", ['SmokerStatus', 'ECigaretteUsage', 'AlcoholDrinkers', 'PhysicalActivities'])

# Bar chart 1
with st.container():
    title = alt.TitleParams('Behaviour Correlations Among Different Age Groups', anchor='middle')
    bar_chart1 = alt.Chart(bf, title=title).mark_bar().encode(
        column=alt.Column('AgeCategory', header=alt.Header(orient='bottom')),
        y=alt.Y('count({behaviour}):Q', title="Individuals"),
        # x='SmokerStatus:N',
        x=alt.X(behaviour, axis=alt.Axis(labels=False), title=None),
        color=alt.Color(behaviour).scale(scheme="lightgreyred")
    ).properties(
        width=75
    ).configure_title(fontSize=20)
    st.altair_chart(bar_chart1)

# Column Initiation
col21, col22= st.columns(2)
col31, col32, col33 = st.columns(3, gap='small')

# Bar chart 2
with col21:
    BMIData = bf[bf['HadHeartAttack'] == 'Yes']
    bar_chart2 = alt.Chart(BMIData, title='BMI Prevalence').mark_bar().encode(
    # column=alt.Column('BMI', header=alt.Header(orient='bottom')),
    y=alt.Y('count(BMI):Q', title="Individuals"),
    x=alt.X('BMI'),
    # , axis=alt.Axis(labels=False), title=None
    # color=alt.Color('SmokerStatus').scale(scheme="lightgreyred")
    color=alt.Color('count(BMI):Q', title='Individuals').scale(scheme="lightgreyred")
    ).properties(
        height=450
    ).configure_title(fontSize=20)
    st.altair_chart(bar_chart2, use_container_width=True)

# Bar chart 3
with col22:
    bar_chart3 = alt.Chart(bf, title='Different diseases and Behavioral Factors correlation with heart attack').mark_bar().encode(
        column=alt.Column(behaviour, header=alt.Header(orient='bottom')),
        y=alt.Y('count({behaviour}):Q', title="Individuals"),
        x=alt.X('HadHeartAttack', axis=alt.Axis(labels=False), title=None),
        color=alt.Color('HadHeartAttack').scale(scheme="lightgreyred")
    ).properties(
        # height=450,
        width=100
    ).configure_title(fontSize=20)
    st.altair_chart(bar_chart3)

# Data prevalence
SmokerData = bf[(bf['SmokerStatus'] == 'Current smoker (Everyday)') | (bf['SmokerStatus'] == 'Current smoker (Somedays)')]
ECigaretteData = bf[(bf['ECigaretteUsage'] == 'Everyday') | (bf['ECigaretteUsage'] == 'Somedays')]
AlcoholDrinkersData = bf[(bf['AlcoholDrinkers'] == 'Yes')]
PhysicallyActiveData = bf[(bf['PhysicalActivities'] == 'Yes')]
SleepHoursData = bf[bf['HadHeartAttack'] == 'Yes']

Smoker_heart_attack_percentage = (SmokerData['HadHeartAttack'].value_counts(normalize=True) * 100).to_dict()
ECigarette_heart_attack_percentage = (ECigaretteData['HadHeartAttack'].value_counts(normalize=True) * 100).to_dict()
Alcohol_heart_attack_percentage = (AlcoholDrinkersData['HadHeartAttack'].value_counts(normalize=True) * 100).to_dict()
PhysicalActivities_heart_attack_percentage = (PhysicallyActiveData['HadHeartAttack'].value_counts(normalize=True) * 100).to_dict()

behavior_percentages = {
    'Smoking': Smoker_heart_attack_percentage.get('Yes'),
    'E-Cigarette Use': ECigarette_heart_attack_percentage.get('Yes'),
    'Alcohol Consumption': Alcohol_heart_attack_percentage.get('Yes'),
    'Physically Active': PhysicalActivities_heart_attack_percentage.get('Yes')
}

# Bar chart 4 with diff data
if behaviour == 'SmokerStatus':
    behavior_data = SmokerData
elif behaviour == 'ECigaretteUsage':
    behavior_data = ECigaretteData
elif behaviour == 'AlcoholDrinkers':
    behavior_data = AlcoholDrinkersData
elif behaviour == 'PhysicalActivities':
    behavior_data = PhysicallyActiveData

with col31:
    bar_chart4 = alt.Chart(behavior_data, title='Correlation with Heart Attack Risk').mark_bar().encode(
        y=alt.Y('count({behaviour}):Q', title="Individuals"),
        x='HadHeartAttack:N',
        color=alt.Color('count({behaviour}):Q', title='Individuals').scale(scheme="lightgreyred")
    ).properties(
        # width=300
    ).configure_mark(
        color='#E15917'
    )
    st.altair_chart(bar_chart4, use_container_width=True)

# Bar chart 5
with col32:
    bar_chart5 = alt.Chart(SleepHoursData, title='Distribution of Sleep Hours').mark_bar().encode(
        y=alt.Y('count({SleepHoursData}):Q', title="Frequency"),
        x='SleepHours:N',
        color=alt.Color('count({SleepHoursData}):Q', title='Frequency').scale(scheme="lightgreyred")
    ).properties(
    # width=400,
)
    st.altair_chart(bar_chart5)

# Pie chart
fig = px.pie(
    values=behavior_percentages.values(),
    names=behavior_percentages.keys(),
    color_discrete_sequence=px.colors.sequential.RdBu,
    title='Prevalence of Health Behaviors among Heart Patients'
)
fig.update_layout(
    margin=dict(l=10, r=10, t=21, b=10),
    width=400,
    height=300,
#     # paper_bgcolor="LightSteelBlue",
)
with col33:
    st.write(fig)



