import os
import pandas as pd
import pickle


class MultiLabelBinarizerCustom:
    def __init__(self, classes=None):
        self.classes_ = classes

    def fit(self, y):
        self.classes_ = sorted(set(tag for tags in y for tag in tags))
        return self

    def transform(self, y):
        return [[1 if c in tags else 0 for c in self.classes_] for tags in y]

    def inverse_transform(self, y):
        return [self.classes_[idx] for idx, val in enumerate(y) if val == 1]


def load_model(
    model_file="trained_model.pkl",
    mlb_file="mlb_model.pkl",
    directory="models",
):
    model_path = os.path.join(directory, model_file)
    mlb_path = os.path.join(directory, mlb_file)
    with open(model_path, "rb") as model_fp:
        rf_classifier = pickle.load(model_fp)
    with open(mlb_path, "rb") as mlb_fp:
        mlb = pickle.load(mlb_fp)
    return rf_classifier, mlb


def predict_tags(new_features, rf_classifier, mlb):
    predicted_tags = mlb.inverse_transform(rf_classifier.predict(new_features))
    return predicted_tags


if __name__ == "__main__":
    # Load the trained model and MultiLabelBinarizer instance
    rf_classifier, mlb = load_model()

    # Define new features for prediction
    new_features = pd.DataFrame(
        {
            "withered_crops": [0],
            "crop_yield": [0.7],
            "net_yield": [8],
            "type": [0],
        }
    )

    # Use the loaded model to predict tags for new features
    predicted_tags = predict_tags(new_features, rf_classifier, mlb)
    print(f"Predicted Tags for New Features: {predicted_tags}")
