import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import hamming_loss, jaccard_score, classification_report
from joblib import dump, load

# Load the generated dataset with tags
df = pd.read_csv("final_dataset.csv")

# Assume you want to predict the tags based on other features
# For simplicity, let's use 'Initially Planted', 'Withered Crops', and 'Net Yield'
features = df[
    [
        "withered_crops",
        "crop_yield",
        "net_yield",
        "type",
    ]
]

# MultiLabelBinarizer to convert the comma-separated tags into binary labels
mlb = MultiLabelBinarizer()
tags_binary = mlb.fit_transform(df["tags"].apply(lambda x: x.split(",")))

# Create and train the RandomForestClassifier on the entire dataset
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(features, tags_binary)

# Save the trained model
dump(rf_classifier, "trained_model.joblib")

# Save the MultiLabelBinarizer instance
dump(mlb, "mlb_model.joblib")

# Make predictions on the entire dataset
predictions = rf_classifier.predict(features)

# Evaluate the model
hamming_loss_value = hamming_loss(tags_binary, predictions)
jaccard_score_value = jaccard_score(tags_binary, predictions, average="samples")

print(f"Hamming Loss: {hamming_loss_value:.2f}")
print(f"Jaccard Score: {jaccard_score_value:.2f}")

# Print classification report
report = classification_report(tags_binary, predictions, target_names=mlb.classes_)
print(report)

# Now, let's use the trained model to predict tags for a new set of features
new_features = pd.DataFrame(
    {
        "withered_crops": [0],
        "crop_yield": [0.7],
        "net_yield": [8],
        "type": [0],
    }
)
new_predictions = rf_classifier.predict(new_features)

# Inverse transform to get human-readable tags
predicted_tags = mlb.inverse_transform(new_predictions)
print(f"Predicted Tags for New Features: {predicted_tags}")
