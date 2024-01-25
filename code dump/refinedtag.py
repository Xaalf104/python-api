import pandas as pd
import numpy as np


# Load your dataset
df = pd.read_csv("final.csv")

# define propper tags for eac hcasse
# Define conditions for assigning tags
conditions = [
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 8)
    & (df["net_yield"] >= 10)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 5)
    & (df["net_yield"] <= 9)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 2)
    & (df["net_yield"] <= 9)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 2)
    & (df["net_yield"] <= 9)
    & (df["type"] == 1),
    # high net yield but low crop yield
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 5)
    & (df["net_yield"] >= 10)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 2)
    & (df["net_yield"] >= 10)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 2)
    & (df["net_yield"] >= 10)
    & (df["type"] == 1),
]

# Define corresponding tags for each condition
tags = [
    [
        "composting",
        "sustainablepractices",
        "raisedbeds",
        "mulching",
        "waterconservation",
    ],  # 1
    [
        "vermiculture",
        "soilmanagement",
        "irrigation",
        "fertilization",
        "organicfarming",
        "pollinatorfriendly",
    ],  # 3
    [
        "pestcontrol",
        "companionplanting",
        "sustainableagriculture",
        "precisionfarming",
        "covercrops",
        "greenhousegrowing",
        "naturalpestmanagement",
        "croprotation",
    ],  # 5
    [
        "precisionfarming",
        "permaculture",
        "covercrops",
        "greenhousegrowing",
        "sustainableagriculture",
    ],  # 26
    [
        "vermiculture",
        "soilmanagement",
        "irrigation",
        "fertilization",
        "organicfarming",
        "pollinatorfriendly",
    ],  # 3
    [
        "pestcontrol",
        "companionplanting",
        "sustainableagriculture",
        "precisionfarming",
        "covercrops",
        "greenhousegrowing",
        "naturalpestmanagement",
        "croprotation",
    ],  # 5
    [
        "precisionfarming",
        "permaculture",
        "covercrops",
        "greenhousegrowing",
        "sustainableagriculture",
    ],  # 26
]

# Loop through conditions and tags, updating the 'Tags' column for urban farming
for condition, tag_list in zip(conditions, tags):
    df.loc[condition, "tags"] = df.loc[condition, "tags"].apply(
        lambda x: ",".join(
            np.append(
                x.split(", "),
                np.random.choice(
                    tag_list, min(np.random.randint(2, 4), len(tag_list)), replace=False
                ),
            )
        )
        if x
        else ",".join(
            np.random.choice(
                tag_list, min(np.random.randint(2, 4), len(tag_list)), replace=False
            )
        )
    )

conditions = [
    # low net yield and low crop yield
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 1)
    & (df["net_yield"] >= 8)
    & (df["type"] == 0),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 0)
    & (df["net_yield"] >= 8)
    & (df["type"] == 0),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 1)
    & (df["net_yield"] < 8)
    & (df["type"] == 0),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] < 0)
    & (df["net_yield"] < 8)
    & (df["type"] == 0),
]

# Define corresponding tags for each condition
tags = [
    [
        "composting",
        "sustainablepractices",
        "raisedbeds",
        "mulching",
        "waterconservation",
    ],  # 1
    [
        "vermiculture",
        "soilmanagement",
        "irrigation",
        "fertilization",
        "organicfarming",
        "pollinatorfriendly",
    ],  # 3
    [
        "pestcontrol",
        "companionplanting",
        "sustainableagriculture",
        "precisionfarming",
        "covercrops",
        "greenhousegrowing",
        "naturalpestmanagement",
        "croprotation",
    ],  # 5
    [
        "precisionfarming",
        "permaculture",
        "covercrops",
        "greenhousegrowing",
        "sustainableagriculture",
    ],  # 26
]

# Loop through conditions and tags, updating the 'Tags' column for urban farming
for condition, tag_list in zip(conditions, tags):
    df.loc[condition, "tags"] = df.loc[condition, "tags"].apply(
        lambda x: ",".join(
            np.append(
                x.split(", "),
                np.random.choice(
                    tag_list, min(np.random.randint(2, 4), len(tag_list)), replace=False
                ),
            )
        )
        if x
        else ",".join(
            np.random.choice(
                tag_list, min(np.random.randint(2, 4), len(tag_list)), replace=False
            )
        )
    )

# Add a space after the comma in the 'tags' column
df["tags"] = df["tags"].apply(lambda x: x.replace(",", ", ") if x else x)

# Display the modified DataFrame
print(df)

# Save the modified DataFrame to a new CSV file
df.to_csv("adjusted.csv", index=False)
