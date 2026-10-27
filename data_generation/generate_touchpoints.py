
import random
from datetime import timedelta
from pathlib import Path
import pandas as pd

# Reproducible random data
random.seed(44)

NUM_TOUCHPOINTS = 1_000_000
DATA_DIR = Path("data")

# Load existing datasets
customers = pd.read_csv(
    DATA_DIR / "customers.csv",
    parse_dates=["signup_date"]
)

campaigns = pd.read_csv(
    DATA_DIR / "campaigns.csv",
    parse_dates=["start_date", "end_date"]
)


# Generate event types based on marketing channel
def get_event_type(channel):
    if channel == "Email":
        return random.choices(
            ["impression", "click", "email_open"],
            weights=[0.15, 0.25, 0.60],
            k=1
        )[0]

    return random.choices(
        ["impression", "click"],
        weights=[0.80, 0.20],
        k=1
    )[0]


# Create customer ID -> signup date lookup
customer_signup = dict(
    zip(
        customers["customer_id"],
        customers["signup_date"]
    )
)

campaign_records = campaigns.to_dict("records")
customer_ids = customers["customer_id"].tolist()

touchpoints = []
i = 1

# Generate exactly 1 million valid touchpoints
while len(touchpoints) < NUM_TOUCHPOINTS:

    campaign = random.choice(campaign_records)

    # 5% of interactions are anonymous
    if random.random() < 0.05:
        customer_id = None
        earliest_date = campaign["start_date"]
    else:
        customer_id = random.choice(customer_ids)

        earliest_date = max(
            campaign["start_date"],
            customer_signup[customer_id]
        )

    latest_date = campaign["end_date"]

    # Skip combinations where the customer
    # signed up after the campaign ended
    if earliest_date > latest_date:
        continue

    # Generate a random timestamp within valid dates
    seconds_range = int(
        (latest_date - earliest_date).total_seconds()
    )

    event_time = earliest_date + timedelta(
        seconds=random.randint(0, seconds_range)
    )

    # Add the new touchpoint
    touchpoints.append({
        "touchpoint_id": i,
        "customer_id": customer_id,
        "campaign_id": campaign["campaign_id"],
        "event_type": get_event_type(campaign["channel"]),
        "event_time": event_time,
        "device_type": random.choices(
            ["mobile", "desktop", "tablet"],
            weights=[0.65, 0.30, 0.05],
            k=1
        )[0]
    })

    # Increment ID after successful insertion
    i += 1


# Convert to DataFrame
df = pd.DataFrame(touchpoints)

# Preserve integer IDs and allow missing customers
df["customer_id"] = df["customer_id"].astype("Int64")

# Validate generated records
assert len(df) == NUM_TOUCHPOINTS
assert df["touchpoint_id"].is_unique
assert df["campaign_id"].notna().all()
assert df["event_time"].notna().all()

# Save to CSV
output_path = DATA_DIR / "touchpoints.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

# Display summary
print(f"\nGenerated {len(df):,} touchpoints")

print("\nFirst 5 records:")
print(df.head())

print("\nEvent distribution:")
print(df["event_type"].value_counts())

print("\nAnonymous touchpoints:")
print(df["customer_id"].isna().sum())

print("\nUnique customers:")
print(df["customer_id"].nunique())

print("\nUnique campaigns:")
print(df["campaign_id"].nunique())

print(f"\nSaved to: {output_path.resolve()}")
