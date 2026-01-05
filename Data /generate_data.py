import json
import numpy as np
import csv
import uuid
import random
from faker import Faker
from datetime import date, datetime


#generate 1000 fake users with uuid, name, credit_score, and account_created
def generate_users():
   faker = Faker()
   data = []


   for _ in range(1000):
       entry = {
           "id": str(uuid.uuid4()),
           "name": faker.name(),
           "credit_score": np.random.randint(300, 850),
           "account_created": faker.date_between(start_date='-10y', end_date='today').isoformat()
       }
       data.append(entry)


   #save all users to json file
   with open('users.json', 'w') as f:
       json.dump(data, f, indent=4)


#generate 250 merchants with uuid, name, category, and risk_score(based on category)
def generate_merchants():
   faker = Faker()
   data = []
   risk_map = {'Travel': (0.5, 0.8), "Online/Retail": (0.5, 0.9), "Entertainment": (0.2, 0.5), "Health/Fitness":(0.2, 0.5), "Food/Dining": (0.1, 0.2), "Gas/Transport": (0.1, 0.2), "Grocery": (0.01, 0.15), "Home/Utilities": (0.01, 0.1)}
  
   for _ in range(250):
       id = str(uuid.uuid4())
       name = faker.unique.company()
       category = faker.random_element(elements=("Travel", "Online/Retail", "Entertainment", "Health/Fitness", "Food/Dining", "Gas/Transport", "Grocery", "Home/Utilities"))
       risk_range = risk_map.get(category)
       risk_score = random.uniform(*risk_range)
       entry = {
           'id': id,
           'name': name,
           'category': category,
           'risk_score': risk_score
       }
       data.append(entry)
  
   #save all merchants to csv
   fieldNamesMerchant = ['id', 'name', 'category', 'risk_score']
   with open('merchants.csv', 'w', newline='') as f:
       writer = csv.DictWriter(f, fieldnames=fieldNamesMerchant)
       writer.writeheader()
       writer.writerows(data)


   #generate 50,000 fake transactions with transaction_id(uuid4), user_id(must exist in users.json),
   # merchant_id(must exist in merchants.csv), amount($), timestamp(date/time str within last year))
   #is_fraud(0/1). This data will be fed into ML model
def generate_transactions():
   faker = Faker()
   data = []


   #returns dictionary with key -> user_id and value -> user_account_created
   def get_user_ids():
       try:
           with open('users.json', 'r') as file:
               users = json.load(file)
          
           if not isinstance(users, list):
               print(f"Error: data from users.json not list or DNE")
               return None
      
           user_ids = {user['id']: user['account_created'] for user in users if 'id' in user}
           if not user_ids:
               print("Error: No values found for user_ids")
               return None
          
       except FileNotFoundError:
           print("Error: File not found")
           return None
       except json.JSONDecodeError:
           print("Error: JSONDecodeError")
           return None
      
       return user_ids
  
   #returns dictionary with key -> merchant_id and value -> merchant_risk_score
   def get_merchant_ids():
       merchants = {}
       try:
           with open('merchants.csv', 'r') as file:
               merchants_data = csv.DictReader(file)
               for merchant in merchants_data:
                   merchants[merchant['id']] = merchant['risk_score']
          
       except FileNotFoundError:
           print("Error: File not found")
           return None
      
       return merchants
      
   #call helper functions and sort data before generating trasactions
   users = get_user_ids()
   merchants = get_merchant_ids()
   user_ids = list(users.keys())
   merchant_ids = list(merchants.keys())


   #generate transactions
   for _ in range(50000):
       transaction_id = str(uuid.uuid4())
       rand_user_id = random.choice(user_ids)
       rand_merchant_id = random.choice(merchant_ids)
       amount = round(random.uniform(0.01, 1000), 2)
       timestamp = faker.date_between(start_date=datetime.strptime(users[rand_user_id], '%Y-%m-%d'), end_date='today').isoformat()
       fraud_check = random.random() #generate number form 0.0 - 1.0
       fraud = -1
       if fraud_check < float(merchants[rand_merchant_id]) * 0.05: #multiply by 0.05 for more reasonable fraud logic
           fraud = 1
       else:
           fraud = 0


       entry = {
           'transaction_id':transaction_id,
           'user_id':rand_user_id,
           'merchant_id':rand_merchant_id,
           'amount':amount,
           'timestamp':timestamp,
           'is_fraud':fraud
       }
       data.append(entry)


   fieldNamesTransactions = ['transaction_id', 'user_id', 'merchant_id', 'amount', 'timestamp', 'is_fraud']
   with open('transactions.csv', 'w', newline='') as file:
       writer = csv.DictWriter(file, fieldnames=fieldNamesTransactions)
       writer.writeheader()
       writer.writerows(data)


if __name__ == "__main__":
   generate_users()
   generate_merchants()
   generate_transactions()
