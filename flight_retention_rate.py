#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:54:13 2023

@author: sohrab-salehin
"""

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

# Dom. Flight
# df_4 should be replaced with new files up to date
# in this sample the report is until jun 23


# Importing files:

df_1= pd.read_excel("flight_jan21_dec21.xlsx", parse_dates= ["Paid Date"], dtype= {"Mobile" : str}).drop_duplicates(subset= 'Mobile')
df_1= df_1.dropna().reset_index(drop= True)
df_2= pd.read_excel("flight_jan22_may22.xlsx", parse_dates= ["Paid Date"], dtype= {"Mobile" : str}).drop_duplicates(subset= 'Mobile')
df_2= df_2.dropna().reset_index(drop= True)
df_3= pd.read_excel("flight_oct18_dec20.xlsx", parse_dates= ["Paid Date"], dtype= {"Mobile" : str}).drop_duplicates(subset= 'Mobile')
df_3= df_3.dropna().reset_index(drop= True)
df_4= pd.read_csv("flight_jun22_jun23.csv", usecols= ['Paid Date', 'Mobile'] ,parse_dates= ["Paid Date"], dtype= {"Mobile" : str}).drop_duplicates(subset= 'Mobile')
df_4= df_4.dropna().reset_index(drop= True)
df= pd.concat([df_1,df_2,df_3, df_4]).sort_values(by= "Paid Date")

# If you want to change customer window
customer_window = 6 #months


current_window_first_date= datetime.strptime('2023-02-01', '%Y-%m-%d')
current_window_last_date= datetime.strptime('2023-05-31', '%Y-%m-%d')

start_customer_period= current_window_first_date - relativedelta(months= customer_window) # period of total customers at start of the period
end_customer_period= current_window_last_date - relativedelta(months= customer_window) # period of total customers at end of the period

customers_at_start_of_period = df[(df["Paid Date"] < current_window_first_date) & (df["Paid Date"] >= start_customer_period)]['Mobile']
customers_at_end_of_period = df[(df["Paid Date"] >= end_customer_period) & (df["Paid Date"] <= current_window_last_date)]['Mobile']
customers_in_period = df[(df["Paid Date"] <= current_window_last_date) & (df["Paid Date"] >= current_window_first_date)]['Mobile']
customers_before_period = df[df["Paid Date"] < current_window_first_date]['Mobile']

dff= pd.merge(left= customers_in_period, right= customers_before_period, how= 'outer', indicator= True)
new_users = dff[dff['_merge'] == 'left_only']['Mobile']

start_customer_period_str= start_customer_period.strftime('%Y-%m-%d')
end_customer_period_str= end_customer_period.strftime('%Y-%m-%d')

print(f"Retention rate for {current_window_first_date} to {current_window_last_date} = {(customers_at_end_of_period.nunique() - new_users.nunique())/customers_at_start_of_period.nunique()}")
print(f"# total customers from {end_customer_period_str} to {current_window_last_date}: {customers_at_end_of_period.nunique()}")
print(f"# new customers in {current_window_first_date} to {current_window_last_date}: {new_users.nunique()}")
print(f"# total customers from {start_customer_period_str} to {current_window_first_date}: {customers_at_start_of_period.nunique()}")