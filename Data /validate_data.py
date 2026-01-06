import pandas as pd
import numpy as np


class DataAudit:

    #open up data files from generate_data.py as pandas dataframe objects
    def __init__(self, data_path ="Data /"):
        self.merchants_df = pd.read_csv(f'{data_path}merchants.csv')
        self.transactions_df = pd.read_csv(f'{data_path}transactions.csv')
        self.users_df = pd.read_json(f'{data_path}users.json')
        self.master_df = pd.DataFrame()
    # print(merchants_df) to see dataframe object


    # 1. Confirm that every transaction from transactions.csv has a real user in users.json
    def validate_users(self):
        users_exist_series = self.transactions_df['user_id'].isin(self.users_df['id']) #series that saves true/false based on if the user_id from transactions is in users
        users_exist = users_exist_series.all() #do all the users exist or no? checking for false in the series

        if users_exist == True:
            print(f"All users in transactions exist in users: {users_exist}")
        else: #print user_ids from transactions that dont exist in users
            false_users = self.transactions_df[~users_exist_series] #false users is a filtered df
            false_user_ids = false_users['user_id'].unique()
            print(f"There are {len(false_user_ids)} false users. The missing ids are: {false_user_ids}.")

    
    #Similar to validate_users method except for merchants
    def validate_merchants(self):
        merchants_exist_series = self.transactions_df["merchant_id"].isin(self.merchants_df['id'])
        merchants_exist = merchants_exist_series.all()

        if merchants_exist == True:
            print(f"All merchants in transactions exist: {merchants_exist}")
        else:
            false_merchants = self.transactions_df[~merchants_exist_series] #filtered df
            false_merchant_ids = false_merchants['merchant_id'].unique()
            print(f"There are {len(false_merchant_ids)} false merchants. The missing ids are {false_merchant_ids}.")


    #print out summary of our data with key metrics
    def summarize_transaction_data(self):
        print(self.transactions_df.info())
        print(self.transactions_df.isnull().sum())
        print(self.transactions_df.describe())

    
    #merge transactions df with users and merchants df to create "master" df
    def merge_dataframes(self):
        #do first merge transactions_df with merchants_df
        temp_df = self.transactions_df.merge(self.merchants_df, left_on='merchant_id', right_on='id')
        #do second merge the first merge merged with users_df
        self.master_df = temp_df.merge(self.users_df, left_on = 'user_id', right_on='id')
        #drop excess id_columns to save space
        self.master_df = self.master_df.drop(['id_x', 'id_y'], axis=1)
        print(self.master_df)




if __name__ == "__main__":
    audit = DataAudit()
    audit.validate_users()
    audit.validate_merchants()
    audit.merge_dataframes()
    
    # Let's peek at the result of your merge
    print("\n--- Master DataFrame Preview ---")
    print(audit.master_df.head())
    print(f"Master DF Shape: {audit.master_df.shape}")