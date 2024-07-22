import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# Read the CSV file
df = pd.read_csv('Commission1.csv')

# Ensure Date Drawn column is parsed as datetime
df['Date Drawn'] = pd.to_datetime(df['Date Drawn'])

# Assuming the column names are 'TakerVolume', 'MakerVolume', 'Date Drawn', 'Fee Profit', 'Commissions', 'Trading Pairs', 'VIP Level', and 'Source Type'
df["Total_volume"] = df["TakerVolume"] + df["MakerVolume"]

# 1. Total Volume Traded Over Time
df_v_total_volume = df[['Date Drawn', 'Total_volume']]
total_volume_by_date = df_v_total_volume.groupby('Date Drawn').sum().reset_index()
total_volume_by_date.columns = ['Date Drawn', 'Total Volume']

# 2. Daily Fee Profit
df_v_fee_profit = df[['Date Drawn', 'Fee Profit']]
daily_fee_profit = df_v_fee_profit.groupby('Date Drawn').sum().reset_index()
daily_fee_profit.columns = ['Date Drawn', 'Fee Profit']

# 3. Daily Commissions
df_v_commissions = df[['Date Drawn', 'Commissions']]
daily_commissions = df_v_commissions.groupby('Date Drawn').sum().reset_index()
daily_commissions.columns = ['Date Drawn', 'Commissions']

# 4. Trading Volume by Trading Pair
volume_by_pair = df.groupby('Trading Pairs')[['TakerVolume', 'MakerVolume']].sum()
volume_by_pair['Total Volume'] = volume_by_pair['TakerVolume'] + volume_by_pair['MakerVolume']

# 5. Average Commission per VIP Level
average_commission_by_vip = df.groupby('VIP Level')['Commissions'].mean().reset_index()
average_commission_by_vip.columns = ['VIP Level', 'Average Commission']

# 6. Volume by Source Type
volume_by_source_type = df.groupby('Source Type')[['TakerVolume', 'MakerVolume']].sum()
volume_by_source_type['Total Volume'] = volume_by_source_type['TakerVolume'] + volume_by_source_type['MakerVolume']

# 7. Top 5 Trading Pairs
top_5_pairs = volume_by_pair.nlargest(5, 'Total Volume').reset_index()

# 8. Monthly Fee Profit
monthly_fee_profit = df.set_index('Date Drawn')['Fee Profit'].resample('M').sum()

# Function to create and display plots
def plot_kpi(data, title, x_label, y_label, kind='line', rotation=0):
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind=kind, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.grid(True)
    st.pyplot(fig)

st.title('Trading Data Analysis')

# 1. Total Volume Traded Over Time
st.header('1. Total Volume Traded Over Time')
plot_kpi(total_volume_by_date.set_index('Date Drawn')['Total Volume'], 'Total Volume Traded Over Time', 'Date', 'Total Volume')

# 2. Daily Fee Profit
st.header('2. Daily Fee Profit')
plot_kpi(daily_fee_profit.set_index('Date Drawn')['Fee Profit'], 'Daily Fee Profit', 'Date', 'Fee Profit')

# 3. Daily Commissions
st.header('3. Daily Commissions')
plot_kpi(daily_commissions.set_index('Date Drawn')['Commissions'], 'Daily Commissions', 'Date', 'Commissions')

# 4. Trading Volume by Trading Pair
st.header('4. Trading Volume by Trading Pair')
plot_kpi(volume_by_pair['Total Volume'], 'Trading Volume by Trading Pair', 'Trading Pair', 'Total Volume', kind='bar', rotation=90)

# 5. Average Commission per VIP Level
st.header('5. Average Commission per VIP Level')
plot_kpi(average_commission_by_vip.set_index('VIP Level')['Average Commission'], 'Average Commission per VIP Level', 'VIP Level', 'Average Commission', kind='bar')

# 6. Volume by Source Type
st.header('6. Volume by Source Type')
plot_kpi(volume_by_source_type['Total Volume'], 'Volume by Source Type', 'Source Type', 'Total Volume', kind='bar')

# 7. Top 5 Trading Pairs
st.header('7. Top 5 Trading Pairs')
plot_kpi(top_5_pairs.set_index('Trading Pairs')['Total Volume'], 'Top 5 Trading Pairs by Volume', 'Trading Pair', 'Total Volume', kind='bar')

# 8. Monthly Trends in Fee Profit
st.header('8. Monthly Trends in Fee Profit')
plot_kpi(monthly_fee_profit, 'Monthly Trends in Fee Profit', 'Month', 'Fee Profit', kind='bar', rotation=45)
