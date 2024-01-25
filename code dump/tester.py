import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from joblib import load

# Load the trained model
rf_classifier = load("trained_model.joblib")

# Load the MultiLabelBinarizer instance
mlb = load("mlb_model.joblib")

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

# Add a new column "tags" to the DataFrame and assign the predicted tags
new_samples["tags"] = [", ".join(tags) for tags in predicted_tags_new_samples]

# Save the DataFrame with the new "tags" column to a new CSV file
new_samples.to_csv("testsetoutput.csv", index=False)
