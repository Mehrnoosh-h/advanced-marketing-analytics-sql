
from faker import Faker
import pandas as pd
import random
from datetime import date, timedelta
from pathlib import Path

# Reproducible random data
fake = Faker("en_US")
Faker.seed(42)
random.seed(42)

NUM_CUSTOMERS = 100_000

# Marketing acquisition channels
channels = ["Google", "Meta", "TikTok", "Organic", "Email"]
weights = [0.30, 0.25, 0.15, 0.20, 0.10]

states = ["CA", "NY", "TX", "FL", "IL", "WA", "MA", "CO"]

start_date = date(2024, 1, 1)
end_date = date(2025, 12, 31)
date_range = (end_date - start_date).days

customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    first_name = fake.first_name()
    last_name = fake.last_name()

    signup_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )

    channel = random.choices(
        channels, weights=weights, k=1
    )[0]

    customers.append({
        "customer_id": i,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"customer{i}@example.com",
        "signup_date": signup_date,
        "state": random.choice(states),
        "acquisition_channel": channel
    })

df = pd.DataFrame(customers)

output_path = Path("data/customers.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print(f"Generated {len(df):,} customers")
print(df.head())
print("\nAcquisition channel distribution:")
print(df["acquisition_channel"].value_counts())
print(f"\nSaved to: {output_path.resolve()}")
