#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:41:56 2023

@author: sohrab-salehin
"""

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

# Dom. Hotel
# df_4 should be replaced with new files up to date
# in this sample the report is until jun 23


# Importing files:

df_1= pd.read_csv("hotel_jan21_sep22.csv", parse_dates= ["Registered Date"], dtype= {"User Unique Identifier" : str})
df_1= df_1.dropna().reset_index(drop= True)
df_2= pd.read_csv("hotel_jan20_dec20.csv", parse_dates= ["Registered Date"], dtype= {"User Unique Identifier" : str})
df_2= df_2.dropna().reset_index(drop= True)
df_3= pd.read_csv("hote_before_jan20.csv", parse_dates= ["Registered Date"], dtype= {"User Unique Identifier" : str})
df_3= df_3.dropna().reset_index(drop= True)
df_4= pd.read_csv("hotel_jun22_jun23.csv", usecols= ['Registered Date', 'User Unique Identifier'] ,parse_dates= ["Registered Date"], dtype= {"User Unique Identifier" : str})
df_4= df_4.dropna().reset_index(drop= True)
df= pd.concat([df_1,df_2,df_3, df_4]).sort_values(by= "Registered Date")



# If you want to change customer window
customer_window = 10 #months


current_window_first_date= datetime.strptime('2023-02-01', '%Y-%m-%d')
current_window_last_date= datetime.strptime('2023-05-31', '%Y-%m-%d')

start_customer_period= current_window_first_date - relativedelta(months= customer_window) # period of total customers at start of the period
end_customer_period= current_window_last_date - relativedelta(months= customer_window) # period of total customers at end of the period

customers_at_start_of_period = df[
    (df["Registered Date"] < current_window_first_date)
    & (df["Registered Date"] >= start_customer_period)
]["User Unique Identifier"]


customers_at_end_of_period = df[
    (df["Registered Date"] >= end_customer_period)
    & (df["Registered Date"] <= current_window_last_date)
]["User Unique Identifier"]


customers_in_period = df[
    (df["Registered Date"] <= current_window_last_date)
    & (df["Registered Date"] >= current_window_first_date)
]["User Unique Identifier"]


customers_before_period = df[df["Registered Date"] < current_window_first_date][
    "User Unique Identifier"
]

dff = pd.merge(
    left=customers_in_period, right=customers_before_period, how="outer", indicator=True
)
new_users = dff[dff["_merge"] == "left_only"]["User Unique Identifier"]

start_customer_period_str = start_customer_period.strftime("%Y-%m-%d")
end_customer_period_str = end_customer_period.strftime("%Y-%m-%d")

print(
    f"Retention rate for {current_window_first_date} to {current_window_last_date} = {(customers_at_end_of_period.nunique() - new_users.nunique())/customers_at_start_of_period.nunique()}"
)
print(
    f"# total customers from {end_customer_period_str} to {current_window_last_date}: {customers_at_end_of_period.nunique()}"
)
print(
    f"# new customers in {current_window_first_date} to {current_window_last_date}: {new_users.nunique()}"
)
print(
    f"# total customers from {start_customer_period_str} to {current_window_first_date}: {customers_at_start_of_period.nunique()}"
)