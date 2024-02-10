import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from joblib import load

# Load the trained model
rf_classifier = load("./models/trained_model.joblib")

# Load the MultiLabelBinarizer instance
mlb = load("./models/mlb_model.joblib")

# Load new samples without tags
new_samples = pd.read_csv("testset.csv")

# Preprocess the new samples (similar to training data preprocessing)
new_samples_features = new_samples[
    [
        "withered_crops",
        "crop_yield",
        "net_yield",
        "type",
    ]
]

# Make predictions
new_samples_predictions = rf_classifier.predict(new_samples_features)

# Inverse transform predictions
predicted_tags_new_samples = mlb.inverse_transform(new_samples_predictions)

# Convert the list of tuples into a list of lists with removed spaces
suggested_tags = [[tag.strip() for tag in tags] for tags in predicted_tags_new_samples]

# Define the tags to check for in the suggested tags
tags_to_check = [
    "commendable crop yield",
    "good crop yield",
    "average crop yield",
    "needs improvement",
    "terrible crop yield",
    "average crop yield",
    "commendable crop yield",
    "needs crop improvement",
    "terrible crop yield",
    "excellent net yield",
    "good net yield",
    "bad net yield",
    "good net yield",
    "excellent net yield",
    "bad net yield",
]

# Iterate over each row in the DataFrame
for i, row in new_samples.iterrows():
    desc_tags = []
    for tag in tags_to_check:
        if tag in suggested_tags[i]:
            desc_tags.append(tag)
            suggested_tags[i].remove(tag)
    new_samples.at[i, "tags"] = ", ".join(suggested_tags[i])
    new_samples.at[i, "desc"] = ", ".join(desc_tags)

# Save the DataFrame with the new "tags" and "desc" columns to a new CSV file
new_samples.to_csv("testsetoutput.csv", index=False)
