import requests
import random
from faker import Faker

BASE_URL = 'http://127.0.0.1:8000'

fake = Faker()

# Function to create a new Medicine
def create_medicine():
    url = f"{BASE_URL}/medicines/"
    data = {
        "manufacturer": fake.company(),
        "name": fake.word(),
        "indications": fake.sentence(),
        "contraindications": fake.sentence(),
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to create a new Availability
def create_availability():
    url = f"{BASE_URL}/availabilities/"
    data = {
        "price": round(random.uniform(1, 100), 2),
        "count": random.randint(1, 100),
        "expiration_date": fake.future_datetime().isoformat(),  # Convert to ISO format string
        "pharmacy_name": fake.company(),
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to create a new Pharmacy
def create_pharmacy():
    url = f"{BASE_URL}/pharmacies/"
    data = {
        "telephone": fake.phone_number(),
        "address": fake.address(),
        "pharmacy_name": fake.company(),
        "specialization": fake.word(),
        "working_time": fake.time(),
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Error:", err)

    return None


for _ in range(100):
    create_medicine()

for _ in range(100):
    create_availability()

for _ in range(100):
    create_pharmacy()

