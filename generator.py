import pandas as pd
import numpy as np

# random seed
np.random.seed(42)

# no of samples
num_samples = 500

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

withered_crops = np.random.randint(0, 20, size=num_samples)
crop_yield = harvested_crops_yieldable / initially_planted
net_yield = harvested_crops_yieldable - withered_crops

# DataFrame
df = pd.DataFrame(
    {
        "farmid": farm_ids,
        "planted_qty": initially_planted,
        "withered_crops": withered_crops,
        "harvested_qty": harvested_crops_yieldable,
        "crop_yield": crop_yield,
        "net-yield": net_yield,
        "type": yieldable,
    }
)

# Display the first few rows of the generated DataFrame
print(df.head())

# Save synthetic dataset to a CSV file
df.to_csv("trainingset.csv", index=False)

# Save the DataFrame to an Excel file
df.to_excel("trainingset.xlsx", index=False)
