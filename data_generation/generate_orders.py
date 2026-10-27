
import random
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from bisect import bisect_left, bisect_right
from itertools import accumulate

import pandas as pd

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

random.seed(45)

NUM_ORDERS = 200_000
DATA_DIR = Path("data")

ANALYSIS_END = pd.Timestamp("2025-12-31 23:59:59")
ATTRIBUTION_WINDOW = timedelta(days=30)

# Target: 70% of orders with a recent touchpoint
TARGET_INFLUENCED_SHARE = 0.70

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

print("Loading customer and touchpoint data...", flush=True)

customers = pd.read_csv(
    DATA_DIR / "customers.csv",
    parse_dates=["signup_date"]
)

touchpoints = pd.read_csv(
    DATA_DIR / "touchpoints.csv",
    parse_dates=["event_time"]
)

# --------------------------------------------------
# 3. CREATE LOOKUP STRUCTURES
# --------------------------------------------------

signup_dates = dict(zip(
    customers["customer_id"],
    customers["signup_date"]
))

customer_touchpoints = defaultdict(list)

identified = touchpoints.dropna(
    subset=["customer_id"]
)

for row in identified.itertuples(index=False):
    customer_touchpoints[int(row.customer_id)].append(
        row.event_time
    )

# Sort customer events once
for events in customer_touchpoints.values():
    events.sort()

customer_ids = customers["customer_id"].tolist()

print(
    f"Loaded {len(customers):,} customers and "
    f"{len(touchpoints):,} touchpoints.",
    flush=True
)

# --------------------------------------------------
# 4. FAST WEIGHTED CUSTOMER SELECTION
# --------------------------------------------------

# Customers have different purchasing propensities
purchase_weights = [
    random.lognormvariate(0, 1)
    for _ in customer_ids
]

cumulative_weights = list(
    accumulate(purchase_weights)
)

total_weight = cumulative_weights[-1]


def select_customer():
    """Select a customer using binary search."""

    position = random.random() * total_weight

    index = bisect_left(
        cumulative_weights,
        position
    )

    return customer_ids[index]


# --------------------------------------------------
# 5. FAST ATTRIBUTION WINDOW CHECK
# --------------------------------------------------

def has_recent_touchpoint(events, order_date):
    """
    Return True if the customer has a touchpoint
    in the 30 days before the order.
    """

    if not events:
        return False

    window_start = order_date - ATTRIBUTION_WINDOW

    index = bisect_left(
        events,
        window_start
    )

    return (
        index < len(events)
        and events[index] <= order_date
    )


# --------------------------------------------------
# 6. GENERATE ORDERS
# --------------------------------------------------

orders = []

influenced_count = 0
organic_count = 0

MAX_ATTEMPTS = NUM_ORDERS * 50
attempts = 0

print("Generating orders...", flush=True)

while len(orders) < NUM_ORDERS:

    attempts += 1

    if attempts > MAX_ATTEMPTS:
        raise RuntimeError(
            "Maximum attempts exceeded. "
            "Check customer and touchpoint data."
        )

    customer_id = select_customer()

    signup_date = signup_dates[customer_id]

    events = customer_touchpoints.get(
        customer_id, []
    )

    # Choose the desired attribution category
    marketing_influenced = (
        random.random() < TARGET_INFLUENCED_SHARE
    )

    # ----------------------------------------------
    # Marketing-influenced orders
    # ----------------------------------------------

    if marketing_influenced:

        if not events:
            continue

        # Select an eligible marketing event
        last_eligible = bisect_right(
            events,
            ANALYSIS_END - timedelta(hours=1)
        )

        if last_eligible == 0:
            continue

        event_time = events[
            random.randrange(last_eligible)
        ]

        # Purchase within 30 days of touchpoint
        order_date = event_time + timedelta(
            days=random.randint(0, 29),
            hours=random.randint(1, 23)
        )

    # ----------------------------------------------
    # Orders without recent marketing touchpoints
    # ----------------------------------------------

    else:

        earliest = signup_date

        if earliest > ANALYSIS_END:
            continue

        seconds_available = int(
            (ANALYSIS_END - earliest).total_seconds()
        )

        order_date = earliest + timedelta(
            seconds=random.randint(
                0,
                seconds_available
            )
        )

    # ----------------------------------------------
    # Validate order dates
    # ----------------------------------------------

    if order_date > ANALYSIS_END:
        continue

    if order_date < signup_date:
        continue

    # Fast check using binary search
    recent_touchpoint = has_recent_touchpoint(
        events,
        order_date
    )

    # Enforce the target attribution category
    if marketing_influenced != recent_touchpoint:
        continue

    # ----------------------------------------------
    # Generate order attributes
    # ----------------------------------------------

    order_status = random.choices(
        ["completed", "cancelled", "pending"],
        weights=[0.88, 0.07, 0.05],
        k=1
    )[0]

    order_amount = round(
        max(
            5,
            min(
                random.lognormvariate(4.5, 0.8),
                2000
            )
        ),
        2
    )

    payment_method = random.choices(
        [
            "credit_card",
            "debit_card",
            "paypal",
            "apple_pay"
        ],
        weights=[0.50, 0.20, 0.20, 0.10],
        k=1
    )[0]

    orders.append({
        "order_id": len(orders) + 1,
        "customer_id": customer_id,
        "order_date": order_date,
        "order_amount": order_amount,
        "order_status": order_status,
        "payment_method": payment_method
    })

    if recent_touchpoint:
        influenced_count += 1
    else:
        organic_count += 1

    # Progress update
    if len(orders) % 25_000 == 0:
        print(
            f"Generated {len(orders):,} / "
            f"{NUM_ORDERS:,} orders "
            f"({attempts:,} attempts)",
            flush=True
        )


# --------------------------------------------------
# 7. CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(orders)

# --------------------------------------------------
# 8. VALIDATION
# --------------------------------------------------

assert len(df) == NUM_ORDERS

assert df["order_id"].is_unique

assert df["customer_id"].isin(
    customer_ids
).all()

assert df["order_amount"].gt(0).all()

assert df["order_date"].le(
    ANALYSIS_END
).all()

assert (
    influenced_count + organic_count
    == NUM_ORDERS
)

# --------------------------------------------------
# 9. SAVE DATA
# --------------------------------------------------

output_path = DATA_DIR / "orders.csv"

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)

# --------------------------------------------------
# 10. SUMMARY
# --------------------------------------------------

print("\n" + "=" * 50)
print("ORDER GENERATION COMPLETED")
print("=" * 50)

print(f"\nGenerated {len(df):,} orders")

print("\nFirst 5 orders:")
print(df.head())

print("\nOrder status distribution:")
print(df["order_status"].value_counts())

print("\nMarketing touchpoint within 30 days:")
print(f"Yes: {influenced_count:,}")
print(f"No:  {organic_count:,}")

print("\nMarketing-influenced percentage:")
print(
    f"{100 * influenced_count / NUM_ORDERS:.2f}%"
)

print("\nUnique purchasing customers:")
print(df["customer_id"].nunique())

completed_revenue = df.loc[
    df["order_status"] == "completed",
    "order_amount"
].sum()

print("\nTotal completed order revenue:")
print(f"${completed_revenue:,.2f}")

print(f"\nTotal generation attempts: {attempts:,}")

print(f"\nSaved to: {output_path.resolve()}")
