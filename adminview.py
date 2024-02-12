from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the data
excel_file_path = "Sample data.xlsx"
df = pd.read_excel(excel_file_path)


def generate_report(dataframe, filters):
    report = []

    for filter_set in filters:
        farm_names = filter_set.get("farm_names")
        condition = filter_set.get("condition")

        # Filter farms based on farm_names
        if farm_names:
            filtered_df = dataframe[dataframe["farm_name"].isin(farm_names)]
        else:
            filtered_df = dataframe.copy()

        # Additional conditions
        if condition == "yieldable":
            filtered_df = filtered_df[filtered_df["type"] == 1]
            filtered_df["yield_condition"] = filtered_df["crop_yield"].apply(
                lambda x: "Good" if x > 1 else "Bad"
            )

        elif condition == "net_yield":
            filtered_df["net_yield_condition"] = filtered_df.apply(
                lambda row: "Good" if row["net_yield"] > row["planted_qty"] else "Bad",
                axis=1,
            )

        # Generate report for the filtered dataframe
        report_text = generate_individual_report(filtered_df)
        report.append(report_text)

    return report


def generate_individual_report(dataframe):
    report_text = ""

    # Group farms based on crop yield
    commendable_performers = dataframe[(dataframe["crop_yield"] >= 6)]
    least_performers = dataframe[dataframe["crop_yield"] < 3]

    # Group farms based on net yield
    bad_netyield = dataframe[(dataframe["net_yield"] <= dataframe["planted_qty"])]
    good_netyield = dataframe[(dataframe["net_yield"] > dataframe["planted_qty"])]

    # Group farms based on withered_crops severity
    severe_withered_crops = dataframe[dataframe["withered_crops"] >= 5]
    bad_withered_crops = dataframe[
        (dataframe["withered_crops"] >= 3) & (dataframe["withered_crops"] < 5)
    ]
    mild_withered_crops = dataframe[
        (dataframe["withered_crops"] >= 1) & (dataframe["withered_crops"] < 3)
    ]

    # Generate report for farms with commendable yields
    if not commendable_performers.empty:
        commendable_yield_report = generate_commendable_yield_report(
            "Farms with Commendable Yield", commendable_performers
        )
        report_text += commendable_yield_report
    else:
        report_text += "Despite diverse locations and farming practices, no farms exhibit an exceptionally commendable yield. The overall performance of the farms contributes to the adaptability and resilience of urban agriculture.\n\n"

    # Generate report for farms with commendable net_yield
    if not good_netyield.empty:
        good_netyield_report = generate_good_net_yield_report(
            "Farms with Good net_yield", good_netyield
        )
        report_text += good_netyield_report

    # Generate report for farms with bad net_yield and suggestions
    if not bad_netyield.empty:
        bad_netyield_report = generate_bad_net_yield_report(
            "Farms with Bad net_yield", bad_netyield
        )
        report_text += bad_netyield_report

    # Generate report for farms with withered_crops severity
    if not severe_withered_crops.empty:
        severe_withered_crops_report = generate_withered_crops_report(
            "Farms with Severe Withered Crops", severe_withered_crops
        )
        report_text += severe_withered_crops_report

    if not mild_withered_crops.empty:
        mild_withered_crops_report = generate_withered_crops_report(
            "Farms with Mild Withered Crops", mild_withered_crops
        )
        report_text += mild_withered_crops_report

    if not bad_withered_crops.empty:
        bad_withered_crops_report = generate_withered_crops_report(
            "Farms with Bad Withered Crops", bad_withered_crops
        )
        report_text += bad_withered_crops_report

    return report_text


def generate_commendable_yield_report(category, farms):
    category_report = f"{category}:\n"

    if len(farms) > 1:
        farm_names = ", ".join(farms["farm_name"])
        min_yield = farms["crop_yield"].min()
        max_yield = farms["crop_yield"].max()

        plant_types = ", ".join(farms["plant"].unique())
        category_report += f"Farms such as {farm_names}, exhibit a commendable yield ranging from {min_yield} to {max_yield} {plant_types} per plant, underscoring efficient cultivation practices.\n\n"
    elif len(farms) == 1:
        farm_name = farms["farm_name"].iloc[0]
        yield_per_plant = farms["crop_yield"].iloc[0]
        plant_type = farms["plant"].iloc[0]

        category_report += f"{farm_name} exhibits a commendable yield of {yield_per_plant} {plant_type}s per plant, underscoring efficient cultivation practices.\n\n"

    return category_report


def generate_good_net_yield_report(category, farms):
    category_report = f"{category}:\n"

    if len(farms) > 1:
        farm_names = ", ".join(farms["farm_name"])
        min_netyield = farms["net_yield"].min()
        max_netyield = farms["net_yield"].max()

        category_report += f"Farms such as {farm_names}, exhibit a net yield ranging from {min_netyield} to {max_netyield}, indicating good results as net yield is greater than planted quantity.\n\n"
    elif len(farms) == 1:
        farm_name = farms["farm_name"].iloc[0]
        netyield = farms["net_yield"].iloc[0]

        category_report += f"{farm_name} exhibits a net yield of {netyield}, indicating good results as net yield is greater than planted quantity.\n\n"

    return category_report


def generate_bad_net_yield_report(category, farms):
    category_report = f"{category}:\n"

    if len(farms) > 1:
        farm_names = ", ".join(farms["farm_name"])
        min_netyield = farms["net_yield"].min()
        max_netyield = farms["net_yield"].max()

        category_report += f"Farms such as {farm_names}, exhibit a net yield ranging from {min_netyield} to {max_netyield}, indicating bad results as net yield is less than or equal to planted quantity.\n\n"
    elif len(farms) == 1:
        farm_name = farms["farm_name"].iloc[0]
        netyield = farms["net_yield"].iloc[0]

        category_report += f"{farm_name} exhibits a net yield of {netyield}, indicating bad results as net yield is less than or equal to planted quantity.\n\n"

    return category_report


def generate_withered_crops_report(category, farms):
    category_report = f"{category}:\n"

    if not farms.empty:
        for farm_name, withered_crops in farms[
            ["farm_name", "withered_crops"]
        ].itertuples(index=False, name=None):
            category_report += f"{farm_name} has {withered_crops} withered crops.\n"

        # Calculate the average number of withered crops across all farms
        average_withered_crops = round(farms["withered_crops"].mean(), 1)

        # Generate severity level description
        severity_level = get_severity_level(average_withered_crops)
        category_report += f"\nThe severity level is {severity_level}.\n"

        # Generate sentence recommendation based on severity
        recommendation_sentence = get_recommendation_sentence(
            severity_level, average_withered_crops
        )
        category_report += recommendation_sentence + "\n"

    return category_report


def get_severity_level(num_withered_crops):
    if num_withered_crops > 5:
        return "Severe"
    elif num_withered_crops >= 3:
        return "Bad"
    else:
        return "Mild"


def get_recommendation_sentence(severity_level, num_withered_crops):
    if severity_level == "Severe":
        return f"The presence of {num_withered_crops} withered crops is severe, suggesting a challenging environment that may be infested with pests. We recommend exploring methods outlined in our recommended materials."
    elif severity_level == "Mild":
        return f"The occurrence of {num_withered_crops} withered crops indicates a mild level of severity. To address this, consider reviewing our recommended materials for insights."
    elif severity_level == "Bad":
        return f"With {num_withered_crops} withered crops, the severity level is considered bad. This may be indicative of unfavorable conditions. Explore our recommended materials for potential solutions."


@app.route("/generate_report", methods=["POST"])
def generate_report_api():
    request_data = request.json
    filters = request_data.get("filters", [])
    report = generate_report(df, filters)
    return jsonify({"report": report})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
