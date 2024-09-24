import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

def do_calculations(df, working_days, selected_feature, selected_age, selected_gender):
    df['Много болничных'] = df['Количество больничных дней'] > working_days
    df['Группы работников'] = df['Много болничных'].replace({True: f"Большe {working_days} больничниых", False: f"Меньше {working_days} больничниых"})
    p = len(df[df['Много болничных']]) / len(df)
    n = len(df)

    se = np.sqrt(p*(1-p) / n)
    if selected_feature == "Возраст":
        po = len(df[df['Возраст'] >= selected_age][df['Много болничных']]) / len(df[df['Возраст'] >= selected_age])
        py = len(df[df['Возраст'] < selected_age][df['Много болничных']]) / len(df[df['Возраст'] < selected_age])
        st.write(f"Средний процент людей с большим количеством болничных {p*100:.2f}%")
        st.write(f"Средний процент людей с большим количеством болничных среди людей старше {selected_age} {po*100:.2f}%")
        st.write(f"Средний процент людей с большим количеством болничных среди моложе {selected_age} {py*100:.2f}%")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,7))
        ax1.set_title(f"Поцентное распределение групп работников среди людей >={selected_age}")
        sns.histplot(ax=ax1, data=df[df['Возраст'] >= selected_age],  x="Группы работников", multiple="stack", stat = "probability",  shrink=.8)
        ax2.set_title(f"Поцентное распределение групп работников среди людей <{selected_age}")
        sns.histplot(ax=ax2, data=df[df['Возраст'] < selected_age],  x="Группы работников", multiple="stack", stat = "probability", shrink=.8)
        st.pyplot(fig)

        if po < py:
            st.write(f"Видно что люди моложе {selected_age} пропускают в течении года более {working_days} дней чаще чем люди более старшего возраста \n. Будем проверять обраную Гипотезу")
        st.write(f"Нулевая гипотеза H0: люди моложе {selected_age} и люди страше пропускают в течении года более {working_days} дней с равной частотой")
        if po < py:
            st.write(f"Альтернативная гипотеза H1: люди моложе {selected_age} чаще пропускают по болезни более {working_days} дней в течении года чаще своих старших коллег")
            z = (py - po) / se
        else:
            st.write(f"Альтернативная гипотеза H1: люди старше {selected_age} чаще пропускают по болезни более {working_days} дней в течении года чаще своих молодых коллег")
            z = (po - py) / se

        p_value = 1 - norm.cdf(z)
        alpha = 0.05
        st.write(f"Для проверки используем пороговое значение alpha: {alpha} (шанс случайного отклонения должен быть меньше {alpha*100}%)")
        st.text(f"Z-статистика: {z:.4f}")
        st.text(f"P-значение: {p_value:.4f}")
        if p_value < alpha:
            if po < py:
                st.write(f"Отвергаем нулевую гипотезу: люди моложе {selected_age} чаще пропускают по болезни более {working_days} дней в течении года чем их старшие коллеги")
            else:
                st.write(f"Отвергаем нулевую гипотезу: люди старше {selected_age} чаще пропускают по болезни более {working_days} дней в течении года чем более молодые коллеги")
        else:
            st.write(f"Не хватает данных для отклонения нулевой гипотезы. Люди моложе {selected_age} и люди страше пропускают в течении года более {working_days} дней с равной частотой")

    if selected_feature == "Пол":
        pm = len(df[df['Пол'] == 'М'][df['Много болничных']]) / len(df[df['Пол'] == 'М'])
        pw = len(df[df['Пол'] == 'Ж'][df['Много болничных']]) / len(df[df['Пол'] == 'Ж'])
        st.write(f"Средний процент людей с большим количеством болничных {p*100:.2f}%")
        st.write(f"Средний процент людей с большим количеством болничных среди мужчин {pm*100:.2f}%")
        st.write(f"Средний процент людей с большим количеством болничных среди женщин {pw*100:.2f}%")


        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,7))
        ax1.set_title("Общий состав Работников")
        sns.histplot(ax=ax1, data=df,  x="Пол", hue='Группы работников', multiple="dodge", stat = "count", shrink=.8)
        ax2.set_title("Группы работников среди Мужчин")
        sns.histplot(ax=ax2, data=df[df['Пол'] == 'М'],  x="Группы работников", multiple="stack", stat = "probability",  shrink=.8)
        ax3.set_title("Группы работников среди Женщин")
        sns.histplot(ax=ax3, data=df[df['Пол'] == 'Ж'],  x="Группы работников", multiple="stack", stat = "probability", shrink=.8)
        st.pyplot(fig)

        if selected_gender == "М":
            po = pw
            py = pm
        else:
            po = pm
            py = pw
        unselected_gender = 'Ж' if  selected_gender == 'М' else 'М'
        if po < py:
            st.write(f"Видно что {selected_gender} пропускают в течении года более {working_days} дней чаще чем {unselected_gender} \n. Будем проверять обраную Гипотезу")
        st.write(f"Нулевая гипотеза H0: {selected_gender} и {unselected_gender} пропускают в течении года более {working_days} дней с равной частотой")
        if po < py:
            st.write(f"Альтернативная гипотеза H1: {selected_gender} чаще пропускают по болезни более {working_days} дней в течении года чаще {unselected_gender}")
            z = (py - po) / se
        else:
            st.write(f"Альтернативная гипотеза H1: {unselected_gender} чаще пропускают по болезни более {working_days} дней в течении года чаще {selected_gender}")
            z = (po - py) / se

        p_value = 1 - norm.cdf(z)
        alpha = 0.05
        st.text(f"Z-статистика: {z:.4f}")
        st.text(f"P-значение: {p_value:.4f}")
        st.write(f"Для проверки используем пороговое значение alpha: {alpha} (шанс случайного отклонения должен быть меньше {alpha*100}%)")
        if p_value < alpha:
            if po < py:
                st.write(f"Отвергаем нулевую гипотезу: {selected_gender} чаще пропускают по болезни более {working_days} дней в течении года чем {unselected_gender}")
            else:
                st.write(f"Отвергаем нулевую гипотезу: {unselected_gender} чаще пропускают по болезни более {working_days} дней в течении года чем {selected_gender}")
        else:
            st.write(f"Не хватает данных для отклонения нулевой гипотезы. {selected_gender} и {unselected_gender} пропускают в течении года более {working_days} дней с равной частотой")

def main():
    st.set_page_config(
        page_title="Анализ данных о больничных днях",
        page_icon=":rat:",
        layout="wide",
    )
    st.title("Анализ данных о больничных днях")

    st.sidebar.header("Загрузите CSV файл")
    uploaded_file = st.sidebar.file_uploader("Выберите файл", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='windows-1251')
        
        expected_columns = ["Количество больничных дней", "Возраст", "Пол"]
        if all(column in df.columns for column in expected_columns):
            st.sidebar.success("Файл успешно загружен и проверен.")
            min_working_days = int(df["Количество больничных дней"].min())
            max_working_days = int(df["Количество больничных дней"].max())
            min_age = int(df["Возраст"].min())
            max_age = int(df["Возраст"].max())

            unique_genders = df["Пол"].unique()
            st.header("Укажите параметры проверяемой гипотезы")
            st.text("Какое количество рабочих дней в году, пропускаемое людьми, вас интересует?")
            working_days = st.slider("working_days", min_value=min_working_days, max_value=max_working_days - 1, value=2)

            
            selected_feature = st.selectbox("Признак", options=["Возраст", "Пол"])
            selected_gender = 'М'
            selected_age = 0

            if selected_feature == "Возраст":
                selected_age = st.slider("age", min_value=min_age+1, max_value=max_age, value=min_age+1)
            if selected_feature == "Пол":
                selected_gender = st.selectbox("gender", options=unique_genders)

            st.header("Выбраная гипотеза:")
            if selected_feature == "Возраст":
                st.write(f"Работники старше {selected_age} лет (age) пропускают в течении года более {working_days} рабочих дней по болезни значительно чаще своих коллег")
            if selected_feature == "Пол":
                st.write(f"{selected_gender} пропускают в течение года более {working_days} рабочих дней (work_days) по болезни значимо чаще {'Ж' if  selected_gender == 'М' else 'М'}.")
            
            do_calculations(df, working_days, selected_feature, selected_age, selected_gender)
        else:
            st.sidebar.error("Ошибка: В файле отсутствуют необходимые колонки. Файл должен содержать колонки Количество больничных дней, Возраст, Пол")
    
if __name__ == "__main__":
    main()