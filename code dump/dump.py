# Define conditions for assigning tags based on 'Crop Yield'
crop_yield_conditions = [
    (df["crop_yield"] >= 15),
    (df["crop_yield"] >= 8),
    (df["crop_yield"] > 5),
    (df["crop_yield"] > 2),
    (df["crop_yield"] < 2),
]

# Define corresponding tags for each 'Crop Yield' condition
crop_yield_tags = [
    ["commendable"],
    ["good"],
    ["average crop yield"],
    ["needs improvement"],
    ["terrible crop yield"],
]

# Loop through conditions and tags, updating the 'Tags' column
for condition, tag_list in zip(crop_yield_conditions, crop_yield_tags):
    df.loc[condition, "Tags"] = df.loc[condition, "Tags"].apply(
        lambda x: ",".join(np.append(x.split(","), tag_list))
        if x
        else ",".join(tag_list)
    )

# Define conditions for assigning tags based on 'Net Yield'
net_yield_conditions = [
    (df["net_yield"] >= 5),
    (df["net_yield"] >= 3) & (df["net_yield"] < 5),
    (df["net_yield"] < 3),
]

# Define corresponding tags for each 'Net Yield' condition
net_yield_tags = [
    ["pestcontrol", "naturalpestmanagement", "croprotation"],
    ["vermiculture", "soilmanagement", "irrigation"],
    ["companionplanting", "fertilization", "greenhousegrowing"],
]

# Loop through conditions and tags, updating the 'Tags' column
for condition, tag_list in zip(net_yield_conditions, net_yield_tags):
    df.loc[condition, "Tags"] = df.loc[condition, "Tags"].apply(
        lambda x: ",".join(np.append(x.split(","), tag_list))
        if x
        else ",".join(tag_list)
    )
