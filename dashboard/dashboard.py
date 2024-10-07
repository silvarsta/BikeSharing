import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

sns.set(style='dark')

# Load the data
data = pd.read_csv("dashboard/data_all.csv")

# Convert 'dteday' to datetime format
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar for filtering data by date range
min_date = data['dteday'].min()
max_date = data['dteday'].max()

with st.sidebar:
    st.image("https://png.pngtree.com/template/20200713/ourmid/pngtree-bicycle-logo-design-image_390987.jpg")

    # Input date range
    start_date = st.date_input(
        label='Tanggal Awal',
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

    end_date = st.date_input(
        label='Tanggal Akhir',
        value=max_date,
        min_value=start_date,  # Ensure end date cannot be before start date
        max_value=max_date
    )

# Ensure that the dates are correctly converted to datetime format
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Check if both start and end dates are selected
if start_date is not None and end_date is not None:
    if start_date >= end_date:
        st.warning(
            "Silakan pilih tanggal akhir yang lebih besar dari tanggal awal.")
    else:
        # Filter the data based on selected date range
        filtered_data = data[(data['dteday'] >= start_date)
                             & (data['dteday'] <= end_date)]
else:
    st.warning("Silakan pilih tanggal awal dan tanggal akhir untuk melihat data.")

# Filter the data based on selected date range
filtered_data = data[(data['dteday'] >= start_date)
                     & (data['dteday'] <= end_date)]


st.header('Bike Sharing Dashboard')
st.subheader('Visualisasi Data Penyewaan Sepeda')

# 1. Visualisasi Jumlah Penyewaan Berdasarkan Musim
season_counts = filtered_data.groupby('weathersit')['cnt'].sum()

color_season = sns.color_palette("coolwarm", len(season_counts))

st.subheader("Pola Penyewaan Berdasarkan Musim")
st.markdown("Grafik ini menunjukkan jumlah penyewaan sepeda yang terjadi di setiap musim. "
            "Dapat dilihat bagaimana pengaruh perubahan musim terhadap popularitas penyewaan sepeda.")

rentals_by_season = filtered_data.groupby(
    'season_label')['cnt'].sum().reset_index()
season_order = ["Spring", "Summer", "Fall", "Winter"]
rentals_by_season['season_label'] = pd.Categorical(
    rentals_by_season['season_label'], categories=season_order, ordered=True)
rentals_by_season = rentals_by_season.sort_values('season_label')

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(rentals_by_season['season_label'],
        rentals_by_season['cnt'], color=color_season)
ax1.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim", fontsize=20)
ax1.set_xlabel("Musim", fontsize=14)
ax1.set_ylabel("Jumlah Penyewaan", fontsize=14)
st.pyplot(fig1)

# 2. Visualisasi Proporsi Penyewaan oleh Pengguna Terdaftar dan Kasual
st.subheader("Proporsi Penyewaan oleh Pengguna Terdaftar dan Kasual")
st.markdown("Bagan pai ini menampilkan proporsi penyewaan yang dilakukan oleh pengguna terdaftar (registered) "
            "dan pengguna kasual (casual). Proporsi ini bisa memberikan wawasan mengenai jenis pelanggan yang lebih dominan.")

user_counts = filtered_data[['casual', 'registered']].sum()

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.pie(user_counts, labels=['Casual', 'Registered'],
        autopct='%1.1f%%', startangle=90, colors=['#FFB6C1', '#FF69B4'])
ax2.set_title('Proporsi Penyewaan oleh Pengguna Terdaftar dan Kasual')
st.pyplot(fig2)

# 3. Visualisasi Pengaruh Jenis Cuaca terhadap Jumlah Penyewaan
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
st.markdown("Grafik ini menggambarkan bagaimana kondisi cuaca mempengaruhi jumlah penyewaan sepeda. "
            "Jenis cuaca yang lebih cerah cenderung meningkatkan penyewaan, sementara hujan lebat menurunkan minat.")

weather_counts = filtered_data.groupby('weathersit')['cnt'].sum()

colors = sns.color_palette("YlGnBu", len(weather_counts))

fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.bar(weather_counts.index, weather_counts, color=colors)
ax3.set_title(
    'Pengaruh Jenis Cuaca terhadap Jumlah Penyewaan Sepeda', fontsize=20)
ax3.set_xlabel('Jenis Cuaca', fontsize=14)
ax3.set_ylabel('Jumlah Penyewaan', fontsize=14)
ax3.set_xticks(ticks=np.arange(len(weather_counts)))
ax3.set_xticklabels(['Clear', 'Mist', 'Light Rain', 'Heavy Rain'], rotation=0)
st.pyplot(fig3)

# Menampilkan data yang sudah difilter
st.subheader("Data Penyewaan Sepeda yang Difilter")
st.dataframe(filtered_data)

# Menampilkan statistik deskriptif
st.subheader("Statistik Deskriptif")
st.write(filtered_data.describe())