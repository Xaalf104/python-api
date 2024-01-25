import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report,
)
from joblib import load

# Load the trained model and MultiLabelBinarizer
rf_classifier = load("trained_model.joblib")
mlb = load("mlb_model.joblib")

# Load the dataset for evaluation (you can replace this with your dataset)
eval_data = pd.read_csv("new_samples_with_tags.csv")

# Clean up class names by stripping leading and trailing spaces
eval_data["tags"] = eval_data["tags"].apply(
    lambda x: [tag.strip() for tag in x.split(",")]
)

# Assume you want to predict the tags based on the features in your evaluation dataset
eval_features = eval_data[
    [
        "withered_crops",
        "crop_yield",
        "net_yield",
        "type",
    ]
]

# MultiLabelBinarizer to convert the comma-separated tags into binary labels
eval_tags_binary = mlb.transform(eval_data["tags"])

# Make predictions on the evaluation dataset
eval_predictions = rf_classifier.predict(eval_features)

# Inverse transform predictions to get human-readable tags
predicted_tags = mlb.inverse_transform(eval_predictions)

# Add predicted tags to the dataframe
eval_data["predicted_tags"] = [list(tags) for tags in predicted_tags]

# Display the dataframe with predicted tags
print(eval_data)

# Evaluate the model
accuracy = accuracy_score(eval_tags_binary, eval_predictions)
precision = precision_score(
    eval_tags_binary, eval_predictions, average="samples", zero_division=1
)
recall = recall_score(
    eval_tags_binary, eval_predictions, average="samples", zero_division=1
)
classification_rep = classification_report(
    eval_tags_binary,
    eval_predictions,
    target_names=mlb.classes_,
    output_dict=True,
    zero_division=1,
)

# Print evaluation metrics
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

# Plot precision and recall for each class
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
ax1.bar(
    mlb.classes_,
    classification_rep["precision"]["micro"],
    color="blue",
    alpha=0.7,
    label="Precision",
)
ax1.set_title("Micro Precision")
ax1.set_ylabel("Precision Score")
ax1.legend()

ax2.bar(
    mlb.classes_,
    classification_rep["recall"]["micro"],
    color="green",
    alpha=0.7,
    label="Recall",
)
ax2.set_title("Micro Recall")
ax2.set_ylabel("Recall Score")
ax2.legend()

plt.xlabel("Classes")
plt.show()
