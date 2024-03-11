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
data = pd.read_parquet('bf.parquet', engine='pyarrow')
data = data.drop(data.columns[0], axis=1)
bf = data.sample(frac =.25) 

# Select box 1
with st.container():
    behaviour = st.selectbox("Behaviour", ['SmokerStatus', 'ECigaretteUsage', 'AlcoholDrinkers', 'PhysicalActivities'])

# Bar chart 1
def color_sort(behaviour):
    if behaviour == 'AlcoholDrinkers' or behaviour == 'PhysicalActivities':
        return "ascending"
    elif behaviour == 'ECigaretteUsage':
        return ['Never', 'Not at all', 'Somedays', 'Everyday']
    else: 
        return "descending"
    
def label_sort(behaviour):
    if behaviour == 'ECigaretteUsage':
        return ['Everyday', 'Somedays', 'Not at all', 'Never']
    else:
        return "ascending"
        
with st.container():
    print(color_sort)
    title = alt.TitleParams('Behaviour Correlations Among Different Age Groups', anchor='middle')
    bar_chart1 = alt.Chart(bf, title=title).mark_bar().encode(
        column=alt.Column('AgeCategory', header=alt.Header(orient='bottom')),
        y=alt.Y('count({behaviour}):Q', title="Individuals"),
        # x='SmokerStatus:N',
        x=alt.X(behaviour,
                sort=label_sort(behaviour),
                axis=alt.Axis(labels=False), 
                title=None),
        color=alt.Color(behaviour, sort=color_sort(behaviour)).scale(scheme="lightgreyred")
    ).properties(
        width=75
    ).configure_title(fontSize=20)
    st.altair_chart(bar_chart1)

# Text
colc1, colc2, colc3 = st.columns([1,2,1])
with colc2:
    with st.container(border=True):
        if behaviour == 'SmokerStatus':
            st.markdown(
            """
            Berdasarkan kelompok umur, tidak sedikit orang yang masih berusia remaja memiliki kebiasaan merokok setiap hari dan akan  bertambah jumlahnya hingga umur sekitar 60 
            kemudian menurun. Salah satu faktor yang mendorong hal tersebut adalah yaitu persepsi bahwa merokok menghilangkan stress atau hanya ingin terlihat gaul/dewasa.
            \nSeiring dengan itu, jumlah orang yang berhenti merokok atau Former smoker akan bertambah setelah umur 60. Hal tersebut disebabkan oleh kondisi tubuh yang sudah 
            tidak lagi sehat dan lebih rentan terkena penyakit.

            """)
        elif behaviour == 'ECigaretteUsage':
            st.markdown(
            """
            Pengguna e-cigarette atau rokok elektrik banyak dialami oleh kelompok usia muda yaitu 18-24. Rokok elektrik menjadi tren di kalangan pelajar atau mahasiswa, 
            karena mudah didapatkan dan dianggap menarik. Penyebab lain yaitu ajakan perokok kepada non-perokok karena terdapat berbagai rasa yang menarik pada rokok elektrik 
            sehingga dapat mempengaruhi orang yang tidak merokok untuk mencoba. 
            \nPerlu diingat bahwa penggunaan rokok elektrik pada remaja dapat menyebabkan gangguan perkembangan otak dan kerusakan fungsi paru-paru. Selain itu, risiko kesehatan 
            yang terkait dengan rokok elektrik masih menjadi penelitian untuk memahami efek jangka panjangnya.
            """)
        elif behaviour == 'AlcoholDrinkers':
            st.markdown(
            """
            Kebiasaan meminum alcohol banyak dilakukan oleh kelompok usia dewasa hingga umur 70. Amerika adalah negara sub-tropis sehingga banyak penduduknya yang meminum alcohol 
            untuk menghangatkan tubuh dan membuat peminumnya merasa lebih relax. 
            \nMeminum alcohol memiliki dampak yang mirip dengan merokok yaitu kecanduan sehingga tidak dapat membatasi jumlah alcohol yang dikonsumsi. Hal tersebut dapat 
            berdampak pada kesehatan seperti gangguan otak dan saraf, masalah pencernaan serta penyakit jantung.
            """)
        elif behaviour == 'PhysicalActivities':
            st.markdown(
            """
            Grafik menunjukkan bahwa jumlah orang yang beraktivitas fisik meningkat hingga kelompok usia 65-69. Hal tersebut disebabkan oleh tuntutan pekerjaan yang mengharuskan 
            mereka beraktivitas fisik setiap hari. Beraktivitas fisik memiliki dampak bagus bagi tubuh namun juga harus diimbangi dengan istirahat yang cukup. Jika tidak 
            maka tubuh akan merasa kelelahan.
            \nKelelahan sangat berpengaruh terhadap kondisi psikis seseorang, sehingga dapat mengakibatkan penyumbatan pembuluh darah yang mengarah ke jantung. Jika ini 
            terjadi, maka besar potensi seseorang mengalami serangan jantung dengan risiko kematian yang tinggi.
            """)

# Column Initiation
col21, col22= st.columns(2)
st.write('***')
# col31, col32, col33 = st.columns(3, gap='small')
col221, col222= st.columns(2)

# Bar chart 2
bf['BMI'] = pd.cut(bf['BMI'], bins=[0, 18.5, 24.9, 29.9, 1000], include_lowest=True, labels=['Underweight', 'Healthy', 'Overweight', 'Obesity'])
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
    with st.container(border=True):
        st.markdown(
            """
            Grafik diatas merupakan BMI para penderita serangan jantung. Dari grafik tersebut, dapat disimpulkan bahwa banyak penderita penyakit jantung 
            memiliki BMI diatas batas normal yaitu 18-25. Nilai BMI dengan jumlah terbanyak  yaitu sekitar 26 dan 27, dan meningkat di nilai 32. Hal tersebut 
            menunjukkan banyak penderita penyakit jantung yang obesitas atau memiliki pola hidup yang kurang sehat.
            """)

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
    with st.container(border=True):
        st.markdown("""
        Grafik menunjukkan bahwa orang yang dulunya merokok sering kali terkena serangan jantung. Selain itu, orang yang tidak pernah merokok 
        juga tidak sedikit yang mengalami penyakit jantung. Jumlah penderita penyakit jantung banyak yang tidak menggunakan rokok elektrik dan 
        tidak mengonsumsi alkohol. Sehingga dapat disimpulkan bahwa satu faktor tidak cukup untuk menunjukkan bahwa 
        seseorang dapat terkena penyakit jantung. Orang yang memiliki beberapa kebiasaan buruk akan lebih rentan terkena penyakit jantung.
        """)

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

# Bar chart 4
with col221:
    bar_chart5 = alt.Chart(SleepHoursData, title='Distribution of Sleep Hours').mark_bar().encode(
        y=alt.Y('count({SleepHoursData}):Q', title="Frequency"),
        x='SleepHours:N',
        color=alt.Color('count({SleepHoursData}):Q', title='Frequency').scale(scheme="lightgreyred")
    ).properties(
    # width=400,
    )
    st.altair_chart(bar_chart5, use_container_width=True)
    with st.container(border=True):
        st.markdown(
            """
            Grafik diatas merupakan distribusi jam tidur para penderita serangan jantung. Berdasarkan grafik tersebut, para penderita penyakit jantung memiliki jam tidur yang relatif 
            normal yaitu sekitar 6 sampai 8 jam sehari. Tetapi, terdapat juga yang memiliki jam tidur dibawah 6 jam dan diatas 8 jam sehari. Dalam jangka panjang, kebiasaan jam tidur
            tidak normal dapat memicu penyakit kronis seperti gangguan jantung dan diabetes.
            """)

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
with col222:
    st.write(fig)
    with st.container(border=True):
        st.markdown(
            """
            Faktor utama seseorang menderita penyakit jantung dari grafik diatas yaitu merokok dengan persentase 40.2%. Diikuti dengan faktor kelelahan sebesar 22.8%, 
            alkohol sebesar 20.2%, dan rokok elektrik sebesar 16.8%. 
            """)

st.write('***')

colk1, colk2, colk3 = st.columns([1, 3, 1])
with colk2:
    with st.container(border=True):
        st.subheader('Kesimpulan')
        st.markdown("""
            Semakin tua usia seseorang, maka semakin rentan menderita penyakit jantung. Hal
            tersebut disebabkan oleh faktor kebiasaan yang kurang sehat seperti merokok dan mengonsumsi alkohol. 
            Jumlah perokok aktif meningkat semakin bertambahnya umur hingga usia 65 tahun. Sedangkan orang dengan
            usia lebih muda cenderung memilih rokok elektrik. Kebiasaan tidak sehat lain yaitu
            meminum alkohol juga semakin meningkat hingga umur 70. Selain itu, orang dengan usia
            tersebut juga banyak yang melakukan aktivitas fisik sehingga dapat menimbulkan kelelahan.
            Body Mass Index (BMI) yang dimiliki oleh penderita penyakit jantung cenderung tidak
            normal yaitu berkisar antara 25-30 yang berarti overweight dan tidak sedikit pula yang
            melebihi 30 atau obesitas. Terlepas dari hal tersebut, kebanyakan penderita penyakit
            jantung memiliki jam tidur normal sekitar 6 hingga 8 jam.
            Faktor utama yang membuat seseorang menderita penyakit jantung yaitu
            merokok. Selain itu, kelelahan dan meminum alkohol juga dapat membuat seseorang terkena penyakit jantung.
            """)
        st.subheader('Rekomendasi')
        st.markdown("""
            Secara keseluruhan, serangan jantung dapat dicegah. Dengan mengubah perilaku kita, kita dapat mengurangi risiko secara signifikan. 
            Beberapa cara yang dapat dilakukan antara lain:
            - Mengurangi kebiasaan merokok karena rokok dapat membuat kondisi jantung dan
            paru-paru menjadi tidak sehat, bahkan ketika seseorang berhenti merokok.
            - Beraktivitas fisik dengan porsi secukupnya untuk menghindari kelelahan yang 
            dapat menyebabkan tekanan ekstra pada jantung. 
            - Mengurangi konsumsi alkohol yang dapat meningkatkan tekanan darah sehingga
            meningkatkan risiko gagal jantung atau stroke.
            """)