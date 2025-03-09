import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='whitegrid')

# load data
main_df = pd.read_csv("bike_sharing_merge_df.csv")
main_df['dteday'] = main_df['dteday'].apply(pd.to_datetime, format='%Y-%m-%d')
# main_df.info()


def create_weather_daily_df(df):
    weather_daily = df.groupby(['temp_daily', 'atemp_daily', 'hum_daily', 'windspeed_daily']).agg({
        'cnt_daily': 'sum',
    }).reset_index()
    weather_daily.rename(columns={
        'cnt_daily': 'total_rentals',
    }, inplace=True)
    return weather_daily


def create_weather_hourly_df(df):
    weather_hourly = df.groupby(['temp_hourly', 'atemp_hourly', 'hum_hourly', 'windspeed_hourly']).agg({
        'cnt_hourly': 'sum',
    }).reset_index()
    weather_hourly.rename(columns={
        'cnt_hourly': 'total_rentals',
    }, inplace=True)
    return weather_hourly


def create_users_hourly_df(df):
    user_by_hour_df = df.groupby(by='hr')['cnt_hourly'].sum().reset_index()
    user_by_hour_df.rename(columns={
        'cnt_hourly': 'total_rentals',
        'hr': 'time'
    }, inplace=True)
    return user_by_hour_df


def create_rfm_df(df):

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df['season_name'] = df['season_daily'].map(
        season_map)
    reference_date = df['dteday'].max()

    season_rfm = []

    for season_name, season_df in df.groupby(by='season_name'):
        current_date = season_df['dteday'].max()

        recency = (reference_date - current_date).days
        frequency = season_df['dteday'].nunique()
        monetary = season_df['cnt_daily'].sum()

        season_rfm.append({
            'season': season_name,
            'recency': recency,
            'frequency': frequency,
            'monetary': monetary,
        })

    season_rfm_df = pd.DataFrame(season_rfm)

    season_rfm_df['r_score'] = pd.qcut(season_rfm_df['recency'], 5, labels=[
                                       5, 4, 3, 2, 1], duplicates='drop')
    season_rfm_df['f_score'] = pd.qcut(season_rfm_df['frequency'], 5, labels=[
                                       1, 2, 3, 4, 5], duplicates='drop')
    season_rfm_df['m_score'] = pd.qcut(season_rfm_df['monetary'], 5, labels=[
                                       1, 2, 3, 4, 5], duplicates='drop')

    return season_rfm_df


weather_daily_df = create_weather_daily_df(main_df)
weather_hourly_df = create_weather_hourly_df(main_df)
users_hourly_df = create_users_hourly_df(main_df)
rfm_season_df = create_rfm_df(main_df)

print(weather_daily_df.head())
print(weather_hourly_df.head())
print(users_hourly_df)
print(rfm_season_df)

st.title(':bike: BIKE SHARING ANALYSIS :bar_chart:')
st.write('This dashboard presents analysis bike rentals contains the hourly and daily count of rental bikes between the years 2011 and 2012 in the Capital bike share system with the corresponding weather and seasonal information.')

tab1, tab2, tab3 = st.tabs(
    ["Weather VS Users", "Time VS Users", "Season VS Users"])


with tab1:
    with st.container():
        st.header("Hubungan berbagai metrik cuaca (Suhu (temp), Suhu yang Dirasakan (atemp), Kelembaban (hum), Kecepatan Angin (windspeed)) terhadap jumlah pengguna bike sharing")

        weather_metric_choice = st.selectbox(
            "Choose a Weather Metric",
            ['temp', 'atemp', 'hum', 'windspeed']
        )
        st.write(f"Selected weather metric: {weather_metric_choice}")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Raw Daily Weather Metrics')
            st.dataframe(weather_daily_df)

        with col2:
            st.subheader('Raw Hourly Weather Metrics')
            st.dataframe(weather_hourly_df)
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 16))
        if weather_metric_choice == 'temp':
            ax1.scatter(main_df['temp_daily'],
                        main_df['cnt_daily'], alpha=0.5)
            ax1.set_xlabel('Daily Temperature')
            ax1.set_ylabel('Daily Users')
            ax1.set_title('Temperature VS Users')
            ax2.scatter(main_df['temp_hourly'],
                        main_df['cnt_hourly'], alpha=0.5, color='green')
            ax2.set_xlabel('Hourly Temperature')
            ax2.set_ylabel('Hourly Users')
            ax2.set_title('Temperature VS Users')
            st.pyplot(fig1)
        elif weather_metric_choice == 'atemp':
            ax1.scatter(main_df['atemp_daily'],
                        main_df['cnt_daily'], alpha=0.5)
            ax1.set_xlabel('Daily Apparent Temperature')
            ax1.set_ylabel('Daily Users')
            ax1.set_title('Apparent Temperature VS Users')
            ax2.scatter(main_df['atemp_hourly'],
                        main_df['cnt_hourly'], alpha=0.5, color='green')
            ax2.set_xlabel('Hourly Apparent Temperature')
            ax2.set_ylabel('Hourly Users')
            ax2.set_title('Apparent Temperature VS Users')
            st.pyplot(fig1)
        elif weather_metric_choice == 'hum':
            ax1.scatter(main_df['hum_daily'],
                        main_df['cnt_daily'], alpha=0.5)
            ax1.set_xlabel('Daily Humidity')
            ax1.set_ylabel('Daily Users')
            ax1.set_title('Humidity VS Users')
            ax2.scatter(main_df['hum_hourly'],
                        main_df['cnt_hourly'], alpha=0.5, color='green')
            ax2.set_xlabel('Hourly Humidity')
            ax2.set_ylabel('Hourly Users')
            ax2.set_title('Humidity VS Users')
            st.pyplot(fig1)

        elif weather_metric_choice == 'windspeed':
            ax1.scatter(main_df['atemp_daily'],
                        main_df['cnt_daily'], alpha=0.5)
            ax1.set_xlabel('Daily Windspeed')
            ax1.set_ylabel('Daily Users')
            ax1.set_title('Windspeed VS Users')
            ax2.scatter(main_df['atemp_hourly'],
                        main_df['cnt_hourly'], alpha=0.5, color='green')
            ax2.set_xlabel('Hourly Windspeed')
            ax2.set_ylabel('Hourly Users')
            ax2.set_title('Windspeed VS Users')
            st.pyplot(fig1)


with tab2:
    with st.container():
        st.header("Hubungan waktu (hr) terhadap jumlah pengguna bike sharing")
        st.subheader('Raw Hourly Users Metrics')
        st.dataframe(users_hourly_df)

    fig2, ax3 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=main_df['hr'], y=main_df['cnt_hourly'],
                 marker='o', color='b', ax=ax3)
    ax3.set_title('Jumlah Penyewaan Berdasarkan Waktu')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Users')
    ax3.set_xticks(range(0, 24))

    st.pyplot(fig2)

with tab3:
    with st.container():
        st.header("Analisis RFM berdasarkan musim (season)")
        st.dataframe(rfm_season_df)

        col3, col4, col5 = st.columns(3)
        fig3, (ax4, ax5, ax6) = plt.subplots(1, 3, figsize=(18, 10))

        with col3:
            st.subheader("Recency By Season")
            sns.barplot(x='season', y='recency', data=rfm_season_df,
                        palette='coolwarm', ax=ax4)
            ax4.set_title('Recency by Season')
            ax4.set_xlabel('Season')
            ax4.set_ylabel('Recency (Days)')

        with col4:
            st.subheader("Frequency By Season")
            sns.barplot(x='season', y='frequency',
                        data=rfm_season_df, palette='coolwarm', ax=ax5)
            ax5.set_title('Frequency by Season')
            ax5.set_xlabel('Season')
            ax5.set_ylabel('Frequency (Number of Days)')

        with col5:
            st.subheader("Monetary By Season")
            sns.barplot(x='season', y='monetary',
                        data=rfm_season_df, palette='magma', ax=ax6)
            ax6.set_title('Monetary by Season')
            ax6.set_xlabel('Season')
            ax6.set_ylabel('Monetary (Total Rental Count)')
        st.pyplot(fig3)
