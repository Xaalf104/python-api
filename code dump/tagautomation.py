import pandas as pd
import numpy as np

# SAMA MO YUNG MGA PREDICTIONS NG TAGS SA CONDITIONS SA WITHERED, yung cropyielkd at net ytield


# Load your dataset
df = pd.read_csv("new_samples_with_tags.csv")

# Define conditions for assigning tags based on 'Crop Yield'
crop_yield_conditions = [
    (df["crop_yield"] >= 15),
    (df["crop_yield"] >= 8) & (df["crop_yield"] < 15) & (df["type"] == 1),
    (df["crop_yield"] >= 5) & (df["crop_yield"] < 8) & (df["type"] == 1),
    (df["crop_yield"] >= 2) & (df["crop_yield"] < 5) & (df["type"] == 1),
    (df["crop_yield"] < 2) & (df["type"] == 1),
    (df["crop_yield"] == 1) & (df["type"] == 0),
    (df["crop_yield"] >= 1) & (df["type"] == 0),
    (df["crop_yield"] < 1) & (df["type"] == 0),
    (df["crop_yield"] < 0) & (df["type"] == 0),
]

# Define corresponding tags for each 'Crop Yield' condition
crop_yield_tags = [
    ["commendable crop yield"],
    ["good crop yield"],
    ["average crop yield"],
    ["needs improvement"],
    ["terrible crop yield"],
    ["average crop yield"],
    ["commendable crop yield"],
    ["needs crop improvement"],
    ["terrible crop yield"],
]

df["tags"] = np.select(crop_yield_conditions, crop_yield_tags, default=df["tags"])

# Define conditions for assigning tags based on 'Net Yield'
net_yield_conditions = [
    (df["net_yield"] >= 16) & (df["type"] == 1),  # 1
    (df["net_yield"] > 8) & (df["net_yield"] < 16) & (df["type"] == 1),  # 2
    (df["net_yield"] <= 8) & (df["type"] == 1),  # 3
    (df["net_yield"] == df["planted_qty"]) & (df["type"] == 0),  # 4
    (df["net_yield"] > df["planted_qty"]) & (df["type"] == 0),  # 5
    (df["net_yield"] < df["planted_qty"]) & (df["type"] == 0),  # 6
]

# Define corresponding tags for each 'Net Yield' condition
net_yield_tags = [
    ["excellent net yield"],  # 1
    ["good net yield"],  # 2
    ["bad net yield"],  # 3
    ["good net yield"],  # 4
    ["excellent net yield"],  # 5
    ["bad net yield"],  # 6
]

# Loop through conditions and tags, updating the 'Tags' column
for condition, tag_list in zip(net_yield_conditions, net_yield_tags):
    df.loc[condition, "tags"] = df.loc[condition, "tags"].apply(
        lambda x: ",".join(np.append(x.split(","), tag_list))
        if x
        else ",".join(tag_list)
    )

# Define conditions for assigning tags
conditions = [
    (df["withered_crops"] >= 26),
    (df["withered_crops"] >= 20) & (df["withered_crops"] < 26),
    (df["withered_crops"] >= 18) & (df["withered_crops"] < 20),
    (df["withered_crops"] >= 14) & (df["withered_crops"] < 18),
    (df["withered_crops"] >= 11) & (df["withered_crops"] < 14),
    (df["withered_crops"] >= 5) & (df["withered_crops"] < 11),
    (df["withered_crops"] >= 1) & (df["withered_crops"] < 5),
    (df["withered_crops"] > 0) & (df["withered_crops"] < 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 5)
    & (df["net_yield"] >= 10)
    & (df["type"] == 1),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 1)
    & (df["net_yield"] >= df["planted_qty"])
    & (df["type"] == 0),
    (df["withered_crops"] == 0)
    & (df["crop_yield"] >= 1)
    & (df["net_yield"] <= df["planted_qty"])
    & (df["type"] == 0),
]

# Define corresponding tags for each condition
tags = [
    ["precisionfarming", "permaculture"],  # 26
    ["covercrops"],  # 20
    ["greenhousegrowing", "sustainableagriculture"],  # 18
    ["companionplanting", "regenerativeagriculture"],  # 14
    ["naturalpestmanagement", "croprotation", "pestcontrol"],  # 11
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
        "vermiculture",
        "soilmanagement",
        "irrigation",
        "fertilization",
        "organicfarming",
        "pollinatorfriendly",
    ],  # 3
    [
        "composting",
        "sustainablepractices",
        "raisedbeds",
        "mulching",
        "waterconservation",
    ],  # 1
    ["farmersmarket", "foodsecurity", "localfood", "farmtofork"],  # 0
    ["farmersmarket", "foodsecurity", "localfood", "farmtofork"],  # 0
    [
        "companionplanting",
        "regenerativeagriculture",
        "naturalpestmanagement",
        "croprotation",
        "pestcontrol",
    ],  # 14
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
df.to_csv("final.csv", index=False)
