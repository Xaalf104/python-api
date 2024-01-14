import pandas as pd

# Tags for each severity level
severe_tags = ["pestmanagement", "environmentalconditions", "crophealth"]
mild_tags = ["cropmaintenance", "environmentaladjustment", "crophealth", "fertilizer"]
bad_tags = [
    "cropcare",
    "environmentalmanagement",
    "pestcontrol",
    "soilmaintenance",
]


def read_excel_and_generate_report(excel_file_path, farm_ids=None):
    # Read Excel file
    df = pd.read_excel(excel_file_path)

    report = generate_report(df, farm_ids)

    print(report)


def generate_report(dataframe, farm_ids=None):
    report_text = "In this report, we explore the crop yields, withered crops, and harvested crops for urban farms, shedding light on the efficacy of urban agriculture.\n\n"

    # Filter farms based on farm_ids
    if farm_ids is not None:
        dataframe = dataframe[dataframe["Farm ID"].isin(farm_ids)]

    # Group farms based on crop yield
    commendable_performers = dataframe[(dataframe["Crop Yield"] >= 6)]
    least_performers = dataframe[dataframe["Crop Yield"] < 3]

    # Group farms based on net yield
    bad_netyield = dataframe[(dataframe["Net Yield"] <= 8)]
    good_netyield = dataframe[(dataframe["Net Yield"] >= 10)]

    # Group farms based on withered crops severity
    severe_withered_crops = dataframe[dataframe["Withered Crops"] >= 5]
    bad_withered_crops = dataframe[
        (dataframe["Withered Crops"] >= 3) & (dataframe["Withered Crops"] < 5)
    ]
    mild_withered_crops = dataframe[
        (dataframe["Withered Crops"] >= 1) & (dataframe["Withered Crops"] < 3)
    ]

    # Generate report for farms with commendable yields
    if not commendable_performers.empty:
        commendable_yield_report = generate_commendable_yield_report(
            "Farms with Commendable Yield", commendable_performers
        )
        report_text += commendable_yield_report
    else:
        report_text += "Despite diverse locations and farming practices, no farms exhibit an exceptionally commendable yield. The overall performance of the farms contributes to the adaptability and resilience of urban agriculture.\n\n"

    # Generate report for farms with commendable net yield
    if not good_netyield.empty:
        good_netyield_report = generate_commendable_yield_report(
            "Farms with Commendable Net Yield", good_netyield
        )
        report_text += good_netyield_report

    # Generate report for farms with bad net yield and suggestions
    if not bad_netyield.empty:
        bad_netyield_report = generate_bad_net_yield_report(
            "Farms with Bad Net Yield", bad_netyield
        )
        report_text += bad_netyield_report

    # Generate report for farms with withered crops severity
    if not severe_withered_crops.empty:
        severe_withered_crops_report = generate_withered_crops_report(
            "Farms with Severe Withered Crops", severe_withered_crops, severe_tags
        )
        report_text += severe_withered_crops_report

    if not mild_withered_crops.empty:
        mild_withered_crops_report = generate_withered_crops_report(
            "Farms with Mild Withered Crops", mild_withered_crops, mild_tags
        )
        report_text += mild_withered_crops_report

    if not bad_withered_crops.empty:
        bad_withered_crops_report = generate_withered_crops_report(
            "Farms with Bad Withered Crops", bad_withered_crops, bad_tags
        )
        report_text += bad_withered_crops_report

    # List of farms and the amount of withered crops they have
    farms_with_withered_crops_report = generate_farms_with_withered_crops_report(
        dataframe
    )
    report_text += farms_with_withered_crops_report

    # least performers
    report_text += "Least Performers:\n"
    for farm_name, yield_per_plant in least_performers[
        ["Farm", "Crop Yield"]
    ].itertuples(index=False, name=None):
        report_text += f"{farm_name} - With a yield of {yield_per_plant}\n"

    # Least performers and suggestions
    if not least_performers.empty:
        report_text += "\nFarms such as "
        least_farms_list = ", ".join(least_performers["Farm"])
        report_text += f"{least_farms_list}, are currently facing challenges in achieving optimal yields. To improve crop yields, consider exploring methods outlined in our recommended article on enhancing agricultural productivity.\n\n"
    else:
        report_text += "None\n\n"

    report_text += "Notably, these farms collectively contribute to the adaptability and resilience of urban agriculture. Challenges, as seen in some locations, highlight opportunities for improvement and continued advancements in urban farming practices. Overall, this report underscores the multifaceted nature of urban farming, emphasizing both successful strategies and areas for growth in the pursuit of sustainable and productive agriculture within city limits."

    return report_text


def generate_commendable_yield_report(category, farms):
    category_report = f"{category}:\n"

    if len(farms) > 1:
        farm_names = ", ".join(farms["Farm"])
        min_yield = farms["Crop Yield"].min()
        max_yield = farms["Crop Yield"].max()

        plant_types = ", ".join(farms["Plant"].unique())
        category_report += f"Farms such as {farm_names}, exhibit a commendable yield ranging from {min_yield} to {max_yield} {plant_types} per plant, underscoring efficient cultivation practices.\n\n"
    elif len(farms) == 1:
        farm_name = farms["Farm"].iloc[0]
        yield_per_plant = farms["Crop Yield"].iloc[0]
        plant_type = farms["Plant"].iloc[0]

        category_report += f"{farm_name} exhibits a commendable yield of {yield_per_plant} {plant_type}s per plant, underscoring efficient cultivation practices.\n\n"

    return category_report


def generate_bad_net_yield_report(category, farms):
    category_report = f"{category}:\n"

    if len(farms) > 1:
        farm_names = ", ".join(farms["Farm"])
        min_netyield = farms["Net Yield"].min()
        max_netyield = farms["Net Yield"].max()

        category_report += f"Farms such as {farm_names}, exhibit a net yield ranging from {min_netyield} to {max_netyield}, indicating challenges in achieving optimal yields. Consider exploring methods outlined in our recommended article on enhancing agricultural productivity.\n\n"
    elif len(farms) == 1:
        farm_name = farms["Farm"].iloc[0]
        netyield = farms["Net Yield"].iloc[0]

        category_report += f"{farm_name} exhibits a net yield of {netyield}, indicating challenges in achieving optimal yields. Consider exploring methods outlined in our recommended article on enhancing agricultural productivity.\n\n"

    return category_report


def generate_withered_crops_report(category, farms, tags):
    category_report = f"{category}:\n"

    if not farms.empty:
        for farm_name, withered_crops in farms[["Farm", "Withered Crops"]].itertuples(
            index=False, name=None
        ):
            category_report += f"{farm_name} has {withered_crops} withered crops.\n"

        # Calculate the average number of withered crops across all farms
        average_withered_crops = round(farms["Withered Crops"].mean(), 1)

        # Generate severity level description
        severity_level = get_severity_level(average_withered_crops)
        category_report += f"\nThe severity level is {severity_level}.\n"

        # Generate sentence recommendation based on severity
        recommendation_sentence = get_recommendation_sentence(
            severity_level, average_withered_crops
        )
        category_report += recommendation_sentence + "\n"

        # Add tags based on severity
        if severity_level == "Severe":
            category_report += f"Tags: {', '.join(severe_tags)}\n\n"
        elif severity_level == "Mild":
            category_report += f"Tags: {', '.join(mild_tags)}\n\n"
        elif severity_level == "Bad":
            category_report += f"Tags: {', '.join(bad_tags)}\n"

    return category_report


def generate_average_withered_crops_report(dataframe, farm_ids):
    # If farm_ids is None, include all farms
    if farm_ids is None:
        selected_farms = dataframe
    else:
        # Filter farms based on farm_ids
        selected_farms = dataframe[dataframe["Farm ID"].isin(farm_ids)]

    if selected_farms.empty:
        return "No data available for the selected farms."

    # round up average of selected farms viaz
    average_withered_crops = round(selected_farms["Withered Crops"].mean(), 1)

    # Generate severity level description
    severity_level = get_severity_level(average_withered_crops)

    # Generate sentence recommendation based on severity
    recommendation_sentence = get_recommendation_sentence(
        severity_level, average_withered_crops
    )

    # Define dictionary to map severity levels to tags
    severity_tags_mapping = {
        "Severe": severe_tags,
        "Mild": mild_tags,
        "Bad": bad_tags,
    }

    # Retrieve tags based on severity
    tags = severity_tags_mapping.get(severity_level, [])

    report_text = (
        f"Average Withered Crops of Selected Farms:\n"
        f"The average withered crops across selected farms is {average_withered_crops}.\n\n"
        f"The severity level is {severity_level}.\n"
        f"{recommendation_sentence}\n"
        f"Tags: {', '.join(tags)}\n"
    )

    return report_text


def generate_farms_with_withered_crops_report(dataframe):
    report = "\nList of Farms and the Amount of Withered Crops:\n"

    for farm_name, withered_crops in dataframe[["Farm", "Withered Crops"]].itertuples(
        index=False, name=None
    ):
        report += f"{farm_name}: {withered_crops} withered crops\n"

    report += "\n"

    return report


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


if __name__ == "__main__":
    excel_file_path = "Sample data.xlsx"
    farm_ids_to_process = (
        None  # Replace with your selected farm IDs or set to None to process all farms
    )

    df = pd.read_excel(excel_file_path)

    # Generate the main report for all farms
    print("Main Report (All Farms):\n")
    main_report = generate_report(df)
    print(main_report)

    # Generate the additional report for selected farm IDs
    print("\nAdditional Report (Selected Farm IDs):\n")
    additional_report = generate_average_withered_crops_report(df, farm_ids_to_process)
    print(additional_report)
