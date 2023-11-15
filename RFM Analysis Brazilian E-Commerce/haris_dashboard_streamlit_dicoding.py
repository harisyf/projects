import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
sns.set(style='dark')


def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
    "order_approved_at": "max", # latest order date
    "order_id": "nunique", # order count
    "payment_value": "sum" # total revenue sum
    })
    rfm_df.columns = ["customer_id", "max_order_approved_at", "frequency", "monetary"]

    # determine when customer last order date in days
    rfm_df["max_order_approved_at"] = rfm_df["max_order_approved_at"].dt.date
    recent_date = df["order_approved_at"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_approved_at"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_approved_at", axis=1, inplace=True)

    return rfm_df

# Load cleaned data
os.chdir('D:\Documents\Graduate\Projects\Dicoding\Analisis Data dengan Python\E-Commerce Public Dataset')
main_df = pd.read_csv("main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at","order_delivered_carrier_date","order_delivered_customer_date"]
main_df.sort_values(by="order_approved_at", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d %H:%M:%S')
    main_df[column] = main_df[column].dt.date
    main_df[column] = pd.to_datetime(main_df[column], format='%Y-%m-%d')


# Filter data
min_date = main_df["order_approved_at"].min()
max_date = main_df["order_approved_at"].max()

with st.sidebar:
    # Take the start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_df[(main_df["order_approved_at"] >= str(start_date)) &
                (main_df["order_approved_at"] <= str(end_date))]

# Creating RFM dataframe
rfm_df = create_rfm_df(main_df)

# RFM Analysis on Brazilian E-Commerce
st.header('RFM Analysis on Brazilian E-Commerce Dashboard')

# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")


tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with tab1:
    avg_recency = round(rfm_df["recency"].mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

    fig1, ax1 = plt.subplots(figsize=(40, 25))
    sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), orient='h')
    ax1.set_xlabel('Days')
    ax1.set_ylabel("customer_id", fontsize=30)
    ax1.bar_label(ax1.containers[0], rotation=0, fontsize=30)
    ax1.set_title("By Recency (days)", loc="center", fontsize=50)
    ax1.tick_params(axis='y', labelsize=30)
    ax1.tick_params(axis='x', labelsize=30)
    
    st.pyplot(fig1)
 
with tab2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

    fig2, ax2 = plt.subplots(figsize=(40, 25))

    sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), orient='h')
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel("customer_id", fontsize=30)
    ax2.bar_label(ax2.containers[0], rotation=0, fontsize=30)
    ax2.set_title("By Frequency", loc="center", fontsize=50)
    ax2.tick_params(axis='y', labelsize=30)
    ax2.tick_params(axis='x', labelsize=30)
    
    st.pyplot(fig2)
 
with tab3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), 'BRL', locale='pt_BR')
    st.metric("Average Monetary", value=avg_monetary)

    fig3, ax3 = plt.subplots(figsize=(40, 25))

    sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), orient='h')
    ax3.set_xlabel('Transaction Value')
    ax3.set_ylabel("customer_id", fontsize=30)
    ax3.bar_label(ax3.containers[0], rotation=0, fontsize=30)
    ax3.set_title("By Monetary", loc="center", fontsize=50)
    ax3.tick_params(axis='y', labelsize=30)
    ax3.tick_params(axis='x', labelsize=30)
    
    st.pyplot(fig3)

# col1, col2, col3 = st.columns(3)

# with col1:
#     avg_recency = round(rfm_df["recency"].mean(), 1)
#     st.metric("Average Recency (days)", value=avg_recency)

# with col2:
#     avg_frequency = round(rfm_df.frequency.mean(), 2)
#     st.metric("Average Frequency", value=avg_frequency)

# with col3:
#     avg_monetary = format_currency(rfm_df.monetary.mean(), 'BRL', locale='pt_BR')
#     st.metric("Average Monetary", value=avg_monetary)

# fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(50, 15))

# sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), ax=ax[0], orient='h')
# ax[0].set_xlabel('Days')
# ax[0].set_ylabel("customer_id", fontsize=30)
# ax[0].bar_label(ax[0].containers[0], rotation=0, fontsize=30)
# ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=30)
# ax[0].tick_params(axis='x', labelsize=30)

# sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), ax=ax[1], orient='h')
# ax[1].set_xlabel('Frequency')
# ax[1].set_ylabel("customer_id", fontsize=30)
# ax[1].bar_label(ax[1].containers[0], rotation=0, fontsize=30)
# ax[1].set_title("By Frequency", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=30)
# ax[1].tick_params(axis='x', labelsize=30)

# sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), ax=ax[2], orient='h')
# ax[2].set_xlabel('Transaction Value')
# ax[2].set_ylabel("customer_id", fontsize=30)
# ax[2].bar_label(ax[2].containers[0], rotation=0, fontsize=30)
# ax[2].set_title("By Monetary", loc="center", fontsize=50)
# ax[2].tick_params(axis='y', labelsize=30)
# ax[2].tick_params(axis='x', labelsize=30)

# st.pyplot(fig)

st.caption('Copyright © Haris Yafie 2023')

