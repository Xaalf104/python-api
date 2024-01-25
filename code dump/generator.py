import pandas as pd
import numpy as np

# random seed
np.random.seed(42)

# no of samples
num_samples = 50

# Sample data for each feature (crop_yield, net_yield, and withered crops in this case)
farm_ids = np.arange(1, num_samples + 1)
initially_planted = np.random.randint(1, 30, size=num_samples)
yieldable = np.random.choice([1, 0], size=num_samples)

# For yieldable type (where planted crop could produce more than 1)
harvested_crops_yieldable = np.where(
    yieldable == 1,
    np.random.randint(2, 31, size=num_samples),
    np.random.randint(1, 30, size=num_samples),
)

# Generate perfect records
perfect_records_mask = (harvested_crops_yieldable / initially_planted >= 6) & (
    harvested_crops_yieldable - 0 >= 9
)

# Apply conditions
withered_crops = np.random.randint(0, 20, size=num_samples)
withered_crops[perfect_records_mask] = 0

crop_yield = harvested_crops_yieldable / initially_planted
net_yield = harvested_crops_yieldable - withered_crops

# Update values for perfect records
crop_yield[perfect_records_mask] = np.random.uniform(
    6, 7, size=np.sum(perfect_records_mask)
)
net_yield[perfect_records_mask] = harvested_crops_yieldable[perfect_records_mask] - 0

# DataFrame
df_perfect_records = pd.DataFrame(
    {
        "farmid": farm_ids,
        "planted_qty": initially_planted,
        "withered_crops": withered_crops,
        "harvested_qty": harvested_crops_yieldable,
        "crop_yield": crop_yield,
        "net_yield": net_yield,
        "type": yieldable,
    }
)

# Format crop yield to have only one decimal place
df_perfect_records["crop_yield"] = df_perfect_records["crop_yield"].round(1)

# Display the generated DataFrame with perfect records
print(df_perfect_records)

# Save dataset to a CSV file
df_perfect_records.to_csv("testset.csv", index=False)
