import pandas as pd

# report lists
report_wc = []
report_cy = []
report_ny = []

individual_reports = []

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
            report_wc.append(terrible_wc)
        elif row["withered_crops"] >= 3 and row["type"] == 1:
            report += f"Withered crops are at a concerning level, "
            report_wc.append(bad_wc)
        else:
            report += f"Withered crops are within acceptable limits, "
            report_wc.append(good_wc)

        # Analyze crop yield
        if row["crop_yield"] >= 5 and row["type"] == 1:
            report += f"crop yield is average, "
            report_cy.append(average_cy)
        elif row["crop_yield"] < 5 and row["type"] == 1:
            report += f"crop yield is low, "
            report_cy.append(bad_cy)
        elif row["crop_yield"] < 0 and row["type"] == 1:
            report += f"crop yield is terrible, "
            report_cy.append(terrible_cy)
        elif row["crop_yield"] >= 10 and row["type"] == 1:
            report += f"crop yield is commendable, "
            report_cy.append(excellent_cy)

        # Analyze net yield
        if row["net_yield"] >= 12 and row["type"] == 1:
            report += f"net yield is commendable.\n"
            report_ny.append(excellent_ny)
        elif row["net_yield"] >= 8 and row["type"] == 1:
            report += f"net yield is average. \n"
            report_ny.append(average_ny)
        elif row["net_yield"] < 8 and row["type"] == 1:
            report += f"net yield is below expectations\n"
            report_ny.append(bad_ny)

        # for tangingang ano type 0 == individual crop / non yieldable plant
        # withered crops
        if row["withered_crops"] > 5 and row["type"] == 0:
            report += f"Withered crops are too high, "
            report_wc.append(terrible_wc)
        elif row["withered_crops"] >= 3 and row["type"] == 0:
            report += f"Withered crops are at a concerning level, "
            report_wc.append(bad_wc)
        elif (
            row["withered_crops"] >= 1
            and row["withered_crops"] < 3
            and row["type"] == 0
        ):
            report += f"Withered crops are mild. Needs improvement. "
            report_wc.append(mild_wc)
        else:
            report_wc.append(good_wc)

        #  crop yield
        if row["crop_yield"] == 1 and row["type"] == 0:
            report += f"crop yield is average, "
            report_cy.append(average_cy)
        elif 0 < row["crop_yield"] < 1 and row["type"] == 0:
            report += f"crop yield is low, "
            report_cy.append(bad_cy)
        elif row["crop_yield"] < 0 and row["type"] == 0:
            report += f"crop yield is terrible, "
            report_cy.append(terrible_cy)
        elif row["crop_yield"] >= 1 and row["type"] == 0:
            report += f"crop yield is commendable, "
            report_cy.append(excellent_cy)

        # net yield
        if row["net_yield"] == row["planted_qty"] and row["type"] == 0:
            report += f"net yield is average. \n"
            report_ny.append(average_ny)
        elif row["net_yield"] > row["planted_qty"] and row["type"] == 0:
            report += f"net yield is commendable. \n"
            report_ny.append(excellent_ny)
        elif row["net_yield"] < row["planted_qty"] and row["type"] == 0:
            report += f"net yield is below expectations\n"
            report_ny.append(bad_ny)

        individual_reports.append(report)

    return report_wc, report_cy, report_ny, individual_reports


if __name__ == "__main__":
    excel_file_path = "sample_data_individualcrop.xlsx"

    # Read Excel file
    df = pd.read_excel(excel_file_path)

    # generate reports
    reports_wc, reports_cy, reports_ny, reports = generate_individual_reports(df)

    for report in reports:
        print(report)

    print("Reports for Withered Crops:")
    for report in reports_wc:
        print(report)

    print("\nReports for Crop Yield:")
    for report in reports_cy:
        print(report)

    print("\nReports for Net Yield:")
    for report in reports_ny:
        print(report)
