# Tags Predictor for Crop Performance for AgriHub

This project aims to predict tags or labels related to agricultural practices based on various features using machine learning techniques. The trained model can help in categorizing agricultural data and providing insights into different agricultural practices.

## Overview

This project utilizes a RandomForestClassifier model and a Multi Label Binarizer to handle multi-label classifiication trained on a dataset containing features such as planted quantity, harvested quantity, crop yield, net yield, withered crops, and type of plant(single harvest crops or multiple harvest crops/yields multiple ). 
The model predicts tags or labels associated with each data entry, providing valuable information for analysis and decision-making in agriculture.

## Features

- Predicts tags related to agricultural practices based on input features.
- Utilizes RandomForestClassifier for accurate prediction.
- Provides insights into different agricultural practices based on data analysis.
- Export outputs to CSV

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:
 - ```git clone https://github.com/Xaalf104/python-api.git```

3. Install the required dependencies:
 - ```pip install flask numpy pandas```
 - ```pip install -U scikit-learn```
