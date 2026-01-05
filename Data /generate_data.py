import json
import numpy as np
import csv
import uuid
import random
from faker import Faker

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
    
    fieldNamesMerchant = ['id', 'name', 'category', 'risk_score']
    with open('merchants.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNamesMerchant)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    generate_users()
    generate_merchants()
        


    
