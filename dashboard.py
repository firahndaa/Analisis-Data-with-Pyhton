import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    
    data['dteday'] = pd.to_datetime(data['dteday'])
    
    data['season'] = data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    data['weekday'] = data['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
    data['mnth'] = data['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    
    data['weathersit'] = data['weathersit'].map({
        1: 'Clear/Partly Cloudy',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    })
    
    data['yr'] = data['yr'].replace({0: 2011, 1: 2012})
    
    return data

def main():
    st.title('Bike Rental Analysis Dashboard')

    data = load_and_preprocess_data('day.csv')

    st.sidebar.title('Navigation')
    analysis = st.sidebar.radio('Select Analysis', 
                                ['Weather Effect', 'Yearly Comparison', 'Working Days vs Holidays', 'Seasonal Analysis'])

    if analysis == 'Weather Effect':
        st.header('Effect of Weather on Bike Rentals')
        
        monthly_weather = data.groupby(['mnth', 'weathersit'])['cnt'].sum().reset_index()
        
        weather_colors = {
            'Clear/Partly Cloudy': 'red',
            'Light Snow/Rain': 'green',
            'Misty/Cloudy': 'yellow',
            'Severe Weather': 'blue'  
        }
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='mnth', y='cnt', hue='weathersit', data=monthly_weather, palette=weather_colors, ax=ax)
        plt.title('Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda per Bulan')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Peminjaman')
        plt.legend(title='Kondisi Cuaca')
        st.pyplot(fig)

    elif analysis == 'Yearly Comparison':
        st.header('Comparison of Bike Rentals: 2011 vs 2012')
        
        monthly_comparison = data.groupby(['mnth', 'yr'])['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=monthly_comparison, x='mnth', y='cnt', hue='yr', marker='o', ax=ax)
        plt.title('Bike Rental Comparison: 2011 vs 2012')
        plt.xlabel('Month')
        plt.ylabel('Number of Rentals')
        st.pyplot(fig)

    elif analysis == 'Working Days vs Holidays':
        st.header('Bike Rentals: Working Days vs Non-Working Days')
        
        working_day_avg = data[data['workingday'] == 1]['cnt'].mean()
        non_working_day_avg = data[data['workingday'] == 0]['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 8))
        sizes = [working_day_avg, non_working_day_avg]
        labels = ['Working Days', 'Non-Working Days']
        colors = ['#1f77b4', '#ff7f0e']
        explode = (0.1, 0)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Average Bike Rentals: Working Days vs Non-Working Days')
        st.pyplot(fig)
        
        st.write(f"Average bike rentals on working days: {working_day_avg:.2f}")
        st.write(f"Average bike rentals on non-working days: {non_working_day_avg:.2f}")

    elif analysis == 'Seasonal Analysis':
        st.header('Bike Rental Analysis by Season')
        
        season_usage = data.groupby('season')['cnt'].sum()
        season_percentage = (season_usage / season_usage.sum()) * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=season_percentage.index, y=season_percentage.values, palette='Blues', ax=ax)
        plt.title('Percentage of Bike Usage by Season')
        plt.xlabel('Season')
        plt.ylabel('Percentage of Bike Usage')
        
        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width() / 2.0, height + 1, f'{height:.1f}%', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        season_average = data.groupby('season')['cnt'].mean()
        st.write("Average Bike Rentals by Season:")
        st.write(season_average)

if __name__ == '__main__':
    main()