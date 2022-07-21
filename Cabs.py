import pandas as pd
import xlrd
from datetime import datetime

# loading the data
cab = pd.read_csv('Cab_data.csv')
city = pd.read_csv('City.csv')
customers = pd.read_csv('Customer_ID.csv')
transactions = pd.read_csv('Transaction_ID.csv')

# forming a master file
master1 = pd.merge(cab, transactions, on='Transaction ID', how='outer')
master2 = pd.merge(master1, customers, on='Customer ID', how='left')

# removing rows with missing values
master2.dropna(inplace=True)

# converting date data to normal date format
for i in range(0, len(master2['Date of Travel'])):
    master2['Date of Travel'][i] = xlrd.xldate.xldate_as_datetime(master2['Date of Travel'][i], 0)

master2['Date of Travel'] = pd.to_datetime(master2['Date of Travel'])

# sorting the data by date of travel
master2.sort_values(by='Date of Travel')

# cost of trip per KM travelled and profit calculations
master2['Cost/KM'] = master2['Cost of Trip']/master2['KM Travelled']
master2['Profit'] = master2['Price Charged'] - master2['Cost of Trip']
master2['% profit'] = master2['Profit']*100/master2['Cost of Trip']
master2['Profit/KM'] = master2['Profit']/master2['KM Travelled']

# checking the output dataframe
print(master2.describe())
print(master2.info())
months = master2["Date of Travel"].dt.month

print(master2['Date of Travel'].dt.month.value_counts())

pink_or_yellow = master2.groupby('Company')

pink = pink_or_yellow.get_group('Pink Cab', master2)
yellow = pink_or_yellow.get_group('Yellow Cab', master2)

print(pink['Date of Travel'].dt.month.value_counts())
print(yellow['Date of Travel'].dt.month.value_counts())

# division by mode of payment for each of the companies
print('Card to Cash payment mode comparison:')
print(pink.groupby('Payment_Mode').count())
print(yellow.groupby('Payment_Mode').count())
print('\n')


# division by male/female riders
print('Male-to-female riders comparison:')
print(pink.groupby('Gender').count())
print(yellow.groupby('Gender').count())
print('\n')

# users by cities
print('riders by cities:')


# average monthly income of a rider
print('avg monthly income of a rider:')
print(pink['Income (USD/Month)'].mean())
print(yellow['Income (USD/Month)'].mean())
print('\n')


# average age of a rider
print('avg rider age:')
print(pink['Age'].mean())
print(pink['Age'].describe())
print(yellow['Age'].mean())
print(yellow['Age'].describe())
print('\n')


# revenue and profit per customer calculations
print('total revenue:')
print(pink['Price Charged'].sum())
print(yellow['Price Charged'].sum())
print('\n')

# total profit
print('total profit:')
print(pink['Profit'].sum())
print(yellow['Profit'].sum())
print('\n')

# revenue per rider
print('revenue per rider:')
print(pink['Price Charged'].sum()/len(pink))
print(yellow['Price Charged'].sum()/len(yellow))
print('\n')

# profit per rider
print('profit per rider:')
print(pink['Profit'].sum()/len(pink))
print(yellow['Profit'].sum()/len(yellow))
print('\n')

# profit per KM
print('profit per KM:')
print(pink['Profit/KM'].mean())
print(yellow['Profit/KM'].mean())
print('\n')

# % profit
print('avg % profit:')
print(pink['% profit'].mean())
print(yellow['% profit'].mean())
print('\n')


# year-on-year stats
print('year-on-year rides:')
print(pink['Date of Travel'].dt.year.value_counts())
print(yellow['Date of Travel'].dt.year.value_counts())
print('\n')





