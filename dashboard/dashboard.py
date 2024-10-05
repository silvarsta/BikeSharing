import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


def create_rentals_by_season_df(df):
    rentals_by_season_df = df.groupby("season_label")[
        "cnt"].sum().reset_index()
    rentals_by_season_df.rename(
        columns={"cnt": "total_rentals"}, inplace=True)
    return rentals_by_season_df


def create_rentals_by_user_type_df(df):
    rentals_by_user_type_df = df[["casual", "registered"]].sum().reset_index()
    rentals_by_user_type_df.columns = ["user_type", "total_rentals"]
    return rentals_by_user_type_df


def create_rentals_by_weathersit_df(df):
    rentals_by_weathersit_df = df.groupby(
        "weathersit")["cnt"].mean().reset_index()
    rentals_by_weathersit_df.rename(
        columns={"cnt": "avg_rentals"}, inplace=True)
    return rentals_by_weathersit_df


data = pd.read_csv("dashboard/data_all.csv")

data['dteday'] = pd.to_datetime(data['dteday'])

data['season_label'] = data['season'].astype('category').cat.codes + 1

min_date = data["dteday"].min()
max_date = data["dteday"].max()

with st.sidebar:
    st.image("https://png.pngtree.com/template/20200713/ourmid/pngtree-bicycle-logo-design-image_390987.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (
    data['dteday'] <= pd.to_datetime(end_date))]

main_df = data[(data["dteday"] >= str(start_date))
               & (data["dteday"] <= str(end_date))]

rentals_by_season_df = create_rentals_by_season_df(main_df)
rentals_by_user_type_df = create_rentals_by_user_type_df(main_df)
rentals_by_weathersit_df = create_rentals_by_weathersit_df(main_df)

st.header('Bike Sharing Dashboard')
st.subheader('Visualisasi Data Penyewaan Sepeda')

# Plot 1: Total Rentals by Season
st.subheader("Pola Penyewaan Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_label', y='total_rentals',
            data=rentals_by_season_df, ax=ax1, palette='coolwarm')
ax1.set_title("Total Penyewaan Berdasarkan Musim", fontsize=20)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
ax1.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig1)

# Plot 2: Rentals by User Type (Casual vs Registered)
st.subheader(
    "Frekuensi Penyewaan Pengguna Terdaftar Dibandingkan Pengguna Kasual")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='user_type', y='total_rentals',
            data=rentals_by_user_type_df, ax=ax2, palette='Purples')
ax2.set_title("Total Penyewaan Berdasarkan Jenis Pengguna", fontsize=20)
ax2.set_xlabel("Jenis Pengguna")
ax2.set_ylabel("Total Penyewaan")
ax2.set_xticklabels(["Casual", "Registered"])
st.pyplot(fig2)

# Plot 3: Average Rentals by Weather Situation
st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='avg_rentals', y='weathersit', data=rentals_by_weathersit_df.sort_values(
    by='avg_rentals', ascending=False), ax=ax3, palette='Blues')
ax3.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", fontsize=20)
ax3.set_xlabel("Rata-rata Penyewaan")
ax3.set_ylabel("Kondisi Cuaca")
ax3.set_yticklabels(["Clear", "Cloudy", "Light Rain", "Heavy Rain"])
st.pyplot(fig3)

st.subheader("Data Penyewaan Sepeda yang Difilter")
st.dataframe(filtered_data)

st.subheader("Statistik Deskriptif")
st.write(filtered_data.describe())
