import pandas as pd


def generate_individual_reports(dataframe):
    individual_reports = []

    report = f"Report for Crops:\n"
    for index, row in dataframe.iterrows():
        report += "\n"
        # Analyze withered crops
        if row["withered_crops"] > 5:
            report += f"For {row['plant']} crop, withered crops are too high,"
        elif row["withered_crops"] >= 3:
            report += (
                f"For {row['plant']} crop, withered crops are at a concerning level,"
            )
        else:
            report += (
                f"For {row['plant']} crop, withered crops are within acceptable limits,"
            )

        # Analyze crop yield
        if row["crop_yield"] >= 6:
            report += f"crop yield is commendable, "
        elif row["crop_yield"] < 3:
            report += f"crop yield is low, "
        else:
            report += f"crop yield is average, "

        # Analyze net yield
        if row["net_yield"] >= 10:
            report += f"net yield is commendable.\n"
        elif row["net_yield"] <= 8:
            report += f"net yield is below expectations. "
        else:
            report += f"net yield is average.\n"

        # apped reports
        report += "\nTags: \n\n"
        individual_reports.append(report)

    return individual_reports


if __name__ == "__main__":
    excel_file_path = "sample_data_individualcrop.xlsx"

    # Read Excel file
    df = pd.read_excel(excel_file_path)

    # Generate individual reports for each row
    reports = generate_individual_reports(df)

    # Print individual reports for each crop rport
    for report in reports:
        print(report)
