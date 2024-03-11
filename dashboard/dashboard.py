import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# create_monthly_users_df
def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "instant": "nunique",
        "cnt_x": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%Y-%m')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "instant": "index",
        "cnt_x": "totality"
    }, inplace=True)
    monthly_users_df['dteday'] = monthly_users_df.index
    return monthly_users_df

# create_byseason_df()
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").instant.sum().reset_index()
    byseason_df.rename(columns={
        "instant": "total_users"
    }, inplace=True)
    byseason_df['season'] = pd.Categorical(byseason_df['season'], ["spring", "summer", "fall", "winter"])
    
    return byseason_df

#create_byholiday_df()
def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").instant.sum().reset_index()
    byholiday_df.rename(columns={
        "instant": "total_users"
    }, inplace=True)
    
    return byholiday_df
    
all_df = pd.read_csv("dashboard/all_data.csv")

datetime_column = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_column:
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

monthly_users_df = create_monthly_users_df(main_df)
byseason_df = create_byseason_df(main_df)
byholiday_df = create_byholiday_df(main_df)

st.header('Dicoding Bike Dashboard :sparkles:')


st.subheader('Monthly Users')
 
col1, col2 = st.columns(2)

with col1:
    total_users = monthly_users_df['totality'].sum()
    st.metric("Total Users", value=total_users)
 
with col2:
    total_revenue = format_currency(monthly_users_df['totality'].sum(), "AUD", locale='es_CO') 
    st.metric("Totality", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_users_df["dteday"],
    monthly_users_df["totality"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader("Users Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="total_users", 
        x="season",
        data=byseason_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Users by Season", loc="center", fontsize=50)
    ax.set_ylabel('Total Users', fontsize=15)
    ax.set_xlabel('Season', fontsize=15)
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="total_users", 
        x="holiday",
        data=byholiday_df.sort_values(by="holiday", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Users by Holiday", loc="center", fontsize=50)
    ax.set_ylabel('Total Users', fontsize=15)
    ax.set_xlabel('Holiday', fontsize=15)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
