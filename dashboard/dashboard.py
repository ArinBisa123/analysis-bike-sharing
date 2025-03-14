import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set_theme(style='whitegrid')

csv_file_path = os.path.join(os.path.dirname(
    __file__), 'bike_sharing_merge_df.csv')

# load data
main_df = pd.read_csv(csv_file_path)
main_df['dteday'] = main_df['dteday'].apply(pd.to_datetime, format='%Y-%m-%d')
# main_df.info()


def create_weather_daily_df(df):
    weather_daily = df.groupby(['temp_daily', 'atemp_daily', 'hum_daily', 'windspeed_daily']).agg({
        'cnt_daily': 'sum',
    }).reset_index()
    weather_daily.rename(columns={
        'cnt_daily': 'total users',
    }, inplace=True)
    return weather_daily


def create_weather_hourly_df(df):
    weather_hourly = df.groupby(['temp_hourly', 'atemp_hourly', 'hum_hourly', 'windspeed_hourly']).agg({
        'cnt_hourly': 'sum',
    }).reset_index()
    weather_hourly.rename(columns={
        'cnt_hourly': 'total users',
    }, inplace=True)
    return weather_hourly


def create_users_hourly_df(df):
    user_by_hour_df = df.groupby(by='hr')['cnt_hourly'].sum().reset_index()
    user_by_hour_df.rename(columns={
        'cnt_hourly': 'total users',
        'hr': 'time'
    }, inplace=True)
    return user_by_hour_df


def categorize_weather(weather_code):
    if weather_code == 1:
        return 'Clear, Few clouds,'
    elif weather_code == 2:
        return 'Mist + Cloudy'
    elif weather_code == 3:
        return 'Light Snow, Light Rain, Thunderstorm'
    elif weather_code == 4:
        return ' Heavy Rain, Thunderstorm, Mist, Snow, Fog'


main_df['daily_weather_condition'] = main_df['weathersit_daily'].apply(
    categorize_weather)
main_df['hourly_weather_condition'] = main_df['weathersit_hourly'].apply(
    categorize_weather)


def create_categorize_users_daily_weather_df(df):
    users_group_by_daily_weather = df.groupby('daily_weather_condition')[
        'cnt_daily'].sum().reset_index()

    high_daily_user_threshold = users_group_by_daily_weather['cnt_daily'].median(
    )

    users_group_by_daily_weather['user_group'] = users_group_by_daily_weather['cnt_daily'].apply(
        lambda x: 'Pengguna Tinggi' if x > high_daily_user_threshold else 'Pengguna Rendah'
    )
    users_group_by_daily_weather.rename(columns={
        'daily_weather_condition': 'daily weathersit',
        'cnt_daily': 'users count',
        'user_group': 'category'
    }, inplace=True)
    return users_group_by_daily_weather


def create_categorize_users_hourly_weather_df(df):
    users_group_by_hourly_weather = df.groupby('hourly_weather_condition')[
        'cnt_hourly'].sum().reset_index()
    high_hourly_user_threshold = users_group_by_hourly_weather['cnt_hourly'].median(
    )
    users_group_by_hourly_weather['user_group'] = users_group_by_hourly_weather['cnt_hourly'].apply(
        lambda x: 'Pengguna Tinggi' if x > high_hourly_user_threshold else 'Pengguna Rendah'
    )
    users_group_by_hourly_weather.rename(columns={
        'hourly_weather_condition': 'hourly weathersit',
        'cnt_hourly': 'users count',
        'user_group': 'category'
    }, inplace=True)
    return users_group_by_hourly_weather


def create_users_by_daily_weather(df):
    users_by_daily_weather = df.groupby('daily_weather_condition')[
        'cnt_daily'].sum().reset_index()
    return users_by_daily_weather


def create_users_by_hourly_weather(df):
    users_by_hourly_weather = df.groupby('hourly_weather_condition')[
        'cnt_hourly'].sum().reset_index()
    return users_by_hourly_weather


weather_daily_df = create_weather_daily_df(main_df)
weather_hourly_df = create_weather_hourly_df(main_df)
users_hourly_df = create_users_hourly_df(main_df)
group_users_daily_weather_df = create_categorize_users_daily_weather_df(
    main_df)
group_users_hourly_weather_df = create_categorize_users_hourly_weather_df(
    main_df)
users_by_daily_weather_df = create_users_by_daily_weather(main_df)
users_by_hourly_weather_df = create_users_by_hourly_weather(main_df)

print(weather_daily_df.head())
print(weather_hourly_df.head())
print(users_hourly_df)
print(group_users_daily_weather_df)
print(group_users_hourly_weather_df)
print(users_by_daily_weather_df)
print(users_by_hourly_weather_df)

st.title(':bike: BIKE SHARING ANALYSIS :bar_chart:')
st.write('This dashboard presents analysis bike rentals contains the hourly and daily count of rental bikes between the years 2011 and 2012 in the Capital bike share system with the corresponding weather and seasonal information.')

tab1, tab2, tab3 = st.tabs(
    ["Weather VS Users", "Time VS Users", "Clustering Weathersit"])


with tab1:
    with st.container():
        st.header("Correlations Between Temperature (temp), Apparent Temperature (atemp), Humidity (hum), Windspeed, And Number of Users")

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
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
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
        st.header("Correlations Between Time (hr) and Number of Users")

        hour_range = st.slider("Select time range (hr)", 0, 23, (0, 23))
        filtered_hourly_df = users_hourly_df[(users_hourly_df['time'] >= hour_range[0]) & (
            users_hourly_df['time'] <= hour_range[1])]

        st.write(f"Showing data for hours: {hour_range}")

        st.subheader('Filtered Hourly Data')
        st.dataframe(filtered_hourly_df)

        fig2, ax3 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=filtered_hourly_df['time'], y=filtered_hourly_df['total users'],
                     marker='o', color='b', ax=ax3)
        ax3.set_title('Total Rentals Hourly')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Users')
        ax3.set_xticks(range(hour_range[0], hour_range[1] + 1))
        st.pyplot(fig2)

with tab3:
    with st.container():
        st.header("Weathersit Clustering Based on Number of Users")

        weather_condition = st.selectbox(
            "Select a weather condition type",
            ['daily weather condition', 'hourly weather condition']
        )
        if weather_condition == 'daily weather condition':
            st.dataframe(group_users_daily_weather_df)
        else:
            st.dataframe(group_users_hourly_weather_df)

        st.subheader(f"Categorized Users by {weather_condition}")

        fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(18, 10))
        if weather_condition == 'daily weather condition':
            ax4.bar(users_by_daily_weather_df['daily_weather_condition'],
                    users_by_daily_weather_df['cnt_daily'], color='#ffafcc')
            ax4.set_title('Daily Users Based on Weathersit')
            ax4.set_xlabel('Weathersit')
            ax4.set_ylabel('Daily Users')
            ax4.set_xticklabels(
                users_by_daily_weather_df['daily_weather_condition'], rotation=45, ha='right')
            ax4.set_ylim(
                0, max(users_by_daily_weather_df['cnt_daily']) * 1.1)
        elif weather_condition == 'hourly weather condition':
            ax5.bar(users_by_hourly_weather_df['hourly_weather_condition'],
                    users_by_hourly_weather_df['cnt_hourly'], color='skyblue')
            ax5.set_title('Hourly Users Based on Weathersit')
            ax5.set_xlabel('Weathersit')
            ax5.set_ylabel('Hourly Users')
            ax5.set_xticklabels(
                users_by_hourly_weather_df['hourly_weather_condition'], rotation=45, ha='right')
            ax5.set_ylim(
                0, max(users_by_hourly_weather_df['cnt_hourly']) * 1.1)
        st.pyplot(fig3)
