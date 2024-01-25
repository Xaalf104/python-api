import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import hamming_loss, jaccard_score, classification_report
from joblib import dump, load

# Load the existing model
existing_model = load("trained_model.joblib")

# Load the MultiLabelBinarizer instance
mlb = load("mlb_model.joblib")

# Load the existing dataset
existing_data = pd.read_csv("modified_trainingsetthousand.csv")

# Load the new dataset with only the "withered_crops" feature
new_data = pd.read_csv("modified_trainingset.csv")

# Combine the existing and new datasets
combined_data = pd.concat([existing_data, new_data], ignore_index=True)

# Assume you want to predict the tags based on the "withered_crops" feature only
features = combined_data[["withered_crops"]]

# MultiLabelBinarizer to convert the comma-separated tags into binary labels
tags_binary = mlb.transform(combined_data["tags"].apply(lambda x: x.split(",")))

# Train the model on the combined dataset
existing_model.fit(features, tags_binary)

# Save the updated model
dump(existing_model, "updated_model.joblib")

# Make predictions on the entire dataset
predictions = existing_model.predict(features)

# Evaluate the updated model
hamming_loss_value = hamming_loss(tags_binary, predictions)
jaccard_score_value = jaccard_score(tags_binary, predictions, average="samples")

print(f"Updated Model Metrics:")
print(f"Hamming Loss: {hamming_loss_value:.2f}")
print(f"Jaccard Score: {jaccard_score_value:.2f}")

# Print updated classification report
updated_report = classification_report(
    tags_binary, predictions, target_names=mlb.classes_
)
print(updated_report)

# Now, let's use the updated model to predict tags for a new set of features
new_features = pd.DataFrame(
    {"withered_crops": [15]}
)  # Example value for the new feature
new_predictions = existing_model.predict(new_features)

# Inverse transform to get human-readable tags
predicted_tags = mlb.inverse_transform(new_predictions)
print(f"Predicted Tags for New Features: {predicted_tags}")
