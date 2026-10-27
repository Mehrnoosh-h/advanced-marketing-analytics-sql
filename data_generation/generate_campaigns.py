
import random
from datetime import date, timedelta
from pathlib import Path
import pandas as pd

random.seed(43)

NUM_CAMPAIGNS = 500

channel_types = {
    "Google": ["Search", "Display", "Shopping"],
    "Meta": ["Retargeting", "Awareness", "Conversion"],
    "TikTok": ["Awareness", "Video", "Conversion"],
    "Organic": ["SEO", "Content"],
    "Email": ["Newsletter", "Promotion", "Retention"]
}

campaigns = []

for i in range(1, NUM_CAMPAIGNS + 1):
    channel = random.choice(list(channel_types.keys()))
    campaign_type = random.choice(channel_types[channel])

    start_date = date(2024, 1, 1) + timedelta(
        days=random.randint(0, 650)
    )

    duration = random.randint(14, 90)
    end_date = min(
        start_date + timedelta(days=duration),
        date(2025, 12, 31)
    )

    budget = round(random.uniform(1000, 100000), 2)

    campaigns.append({
        "campaign_id": i,
        "campaign_name": f"{channel}_{campaign_type}_{i}",
        "channel": channel,
        "campaign_type": campaign_type,
        "start_date": start_date,
        "end_date": end_date,
        "campaign_budget": budget,
        "campaign_status": "Completed"
    })

df = pd.DataFrame(campaigns)

output_path = Path("data/campaigns.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print(f"Generated {len(df):,} campaigns")
print(df.head())
print("\nCampaign distribution:")
print(df["channel"].value_counts())
print(f"\nSaved to: {output_path.resolve()}")
