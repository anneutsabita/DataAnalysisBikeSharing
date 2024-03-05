import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_correlation_df(df):
    # Menghitung korelasi
    correlation = df[['temp', 'hum', 'windspeed', 'cnt']].corr()

    # Heatmap korelasi
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.show()

def create_fluctuation_monthly_df(df):
    # Agregasi data per bulan
    hour_df_monthly = df.groupby("mnth").agg({"cnt": "sum"})

    # Visualisasi fluktuasi musiman
    sns.lineplot(x="mnth", y="cnt", data=df)
    plt.title("Fluktuasi Musiman Peminjaman Sepeda")
    plt.show()

def create_fluctuation_hourly_df(df):
    # Agregasi data per jam
    hour_df_hourly = df.groupby("hr").agg({"cnt": "sum"})

    # Visualisasi fluktuasi harian
    sns.lineplot(x="hr", y="cnt", data=df)
    plt.title("Fluktuasi Harian Peminjaman Sepeda")
    plt.show()

def create_trend_visual_df(df):
    # Visualisasi tren
    sns.lineplot(x="yr", y="cnt", data=df)
    plt.title("Tren Peminjaman Sepeda")
    plt.show()
    

all_df = pd.read_csv("https://raw.githubusercontent.com/anneutsabita/Bike-sharing-dataset/main/hour.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

correlation_df = create_correlation_df(main_df)
fluctuation_monthly_df = create_fluctuation_monthly_df(main_df)
fluctuation_hourly_df =create_fluctuation_hourly_df(main_df)
trend_visual = create_trend_visual_df(main_df)

st.header('Data Analysis Dashboard :sparkles:')

st.subheader('Bike Sharing Dataset')
 
st.title("Correlation Heatmap")
st.write("This heatmap shows the correlation between temperature, humidity, wind speed, and bike rental count.")
correlation = all_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title('Correlation Heatmap')
st.pyplot(fig)

st.title("Correlation Scatter Plot")
st.write("This plot shows that weather factors, especially temperature, play an important role in determining bicycle borrowing patterns, while humidity and wind speed also have an influence, although to a lesser extent compared to temperature.")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="temp", y="cnt", data=all_df, ax=ax, label='Temperature')
sns.scatterplot(x="hum", y="cnt", data=all_df, ax=ax, label='Humidity')
sns.scatterplot(x="windspeed", y="cnt", data=all_df, ax=ax, label='Windspeed')
ax.set_xlabel('Value')
ax.set_ylabel('Count')
ax.set_title('Scatter Plot of Temperature, Humidity, and Windspeed vs Count')
st.pyplot(fig)

st.title("Seasonal fluctuations in bicycle lending")
st.write("This plot shows that weather factors, especially temperature, play an important role in determining bicycle borrowing patterns, while humidity and wind speed also have an influence, although to a lesser extent compared to temperature.")
# Membuat objek gambar dan sumbu untuk dua kolom
fig1, ax1 = plt.subplots(figsize=(8, 6))
fig2, ax2 = plt.subplots(figsize=(8, 6))

# Agregasi data per bulan
hour_df_monthly = all_df.groupby("mnth").agg({"cnt": "sum"})

# Visualisasi fluktuasi musiman
sns.lineplot(x="mnth", y="cnt", data=all_df, ax=ax1)
ax1.set_title("Fluktuasi Musiman Peminjaman Sepeda")

# Agregasi data per jam
hour_df_hourly = all_df.groupby("hr").agg({"cnt": "sum"})

# Visualisasi fluktuasi harian
sns.lineplot(x="hr", y="cnt", data=all_df, ax=ax2)
ax2.set_title("Fluktuasi Harian Peminjaman Sepeda")

# Menampilkan plot di Streamlit dalam dua kolom
col1, col2 = st.columns(2)
col1.pyplot(fig1)
col2.pyplot(fig2)