import pandas as pd

# lists to store messages for each plant
report_wc = []
report_cy = []
report_ny = []

# strings
terrible_wc = "Withered crops are too high"
bad_wc = "Withered crops are at a concerning level"
good_wc = "Withered crops are within acceptable limits"
mild_wc = "Withered crops are mild. Needs improvement."

excellent_cy = "Crop yield is commendable"
bad_cy = "Crop yield is low"
average_cy = "Crop yield is average"
terrible_cy = "Crop yield is terrible"

excellent_ny = "Net yield is commendable"
bad_ny = "Net yield is below expectations"
average_ny = "Net yield is average"


def generate_individual_reports(dataframe):
    for index, row in dataframe.iterrows():
        report = f"Report for {row['plant']} crop:\n"

        # Analyze withered crops
        if row["withered_crops"] > 5 and row["type"] == 1:
            report += f"Withered crops are too high, "
            report_wc.append((row["plant"] + ": " + terrible_wc))
        elif row["withered_crops"] >= 3 and row["type"] == 1:
            report += f"Withered crops are at a concerning level, "
            report_wc.append((row["plant"] + ": " + bad_wc))
        else:
            report += f"Withered crops are within acceptable limits, "
            report_wc.append((row["plant"] + ": " + good_wc))

        # Analyze crop yield
        if row["crop_yield"] >= 5 and row["type"] == 1:
            report += f"crop yield is average, "
            report_cy.append((row["plant"] + ": " + average_cy))
        elif row["crop_yield"] < 5 and row["type"] == 1:
            report += f"crop yield is low, "
            report_cy.append((row["plant"] + ": " + bad_cy))
        elif row["crop_yield"] < 0 and row["type"] == 1:
            report += f"crop yield is terrible, "
            report_cy.append((row["plant"] + ": " + terrible_cy))
        elif row["crop_yield"] >= 10 and row["type"] == 1:
            report += f"crop yield is commendable, "
            report_cy.append((row["plant"] + ": " + excellent_cy))

        # Analyze net yield
        if row["net_yield"] >= 12 and row["type"] == 1:
            report += f"net yield is commendable.\n"
            report_ny.append((row["plant"] + ": " + excellent_ny))
        elif row["net_yield"] >= 8 and row["type"] == 1:
            report += f"net yield is average. \n"
            report_ny.append((row["plant"] + ": " + average_ny))
        elif row["net_yield"] < 8 and row["type"] == 1:
            report += f"net yield is below expectations\n"
            report_ny.append((row["plant"] + ": " + bad_ny))

    return report_wc, report_cy, report_ny


if __name__ == "__main__":
    excel_file_path = "sample_data_individualcrop.xlsx"

    # Read Excel file
    df = pd.read_excel(excel_file_path)

    # generate reports
    reports_wc, reports_cy, reports_ny = generate_individual_reports(df)

    print(report_ny, "\n")
    print(report_cy, "\n")

    # Print the contents of lists
    # print("\nContents of report_wc list:")
    # for item in reports_wc:
    #     print(f"{item[0]} {item[1]}")

    # print("\nContents of report_cy list:")
    # for item in reports_cy:
    #     print(f"{item[0]} {item[1]}")

    # print("\nContents of report_ny list:")
    # for item in reports_ny:
    #     print(f"{item[0]} {item[1]}")
