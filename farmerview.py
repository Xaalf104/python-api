import pandas as pd

# lists to store messages for each plant
report_wc = []
report_cy = []
report_ny = []

# strings aka messages for each level
terrible_wc = "The withered crops have significantly impacted yield. Immediate action is neededwithered crops have significantly impacted yield. Immediate action is needed"
bad_wc = "The number of withered crops is concerning and impacting yield"
good_wc = "The withered crops count is zero, indicating excellent crop health and minimal losses during cultivation. This suggests effective pest control, optimal water management, and overall favorable growing conditions. Keep up the good work!"
mild_wc = "There are some losses due to withered crops, but they're manageable"

excellent_cy = "Crop yield is exceptional!"
bad_cy = "Crop yield is below expectations"
average_cy = "crop yield is satisfactory"
terrible_cy = "Crop yield is disastrously low"

excellent_ny = "Net yield exceeds expectations"
bad_ny = "Net yield is lower than anticipated"
average_ny = "Net yield is performing average"
terrible_ny = "Net yield is negative, indicating significant losses"


def generate_individual_reports(dataframe):
    for index, row in dataframe.iterrows():
        report = f"Report for {row['plant']} crop:\n"

        # Analyze withered crops
        if row["withered_crops"] >= 5 and row["type"] == 1:
            report += f"Withered crops have significantly impacted yield. Immediate action is needed. "
            report_wc.append((row["plant"] + ": " + terrible_wc))
        elif (
            row["withered_crops"] >= 0
            and row["withered_crops"] < 5
            and row["type"] == 1
        ):
            report += f"The number of withered crops is concerning and impacting yield "
            report_wc.append((row["plant"] + ": " + bad_wc))
        elif row["withered_crops"] == 0 and row["type"] == 1:
            report += f"The withered crops count is zero, indicating excellent crop health and minimal losses during cultivation. This suggests effective pest control, optimal water management, and overall favorable growing conditions. Keep up the good work! "
            report_wc.append((row["plant"] + ": " + good_wc))

        # Analyze crop yield
        if row["crop_yield"] >= 5 and row["type"] == 1:
            report += f"  "
            report_cy.append((row["plant"] + ": " + average_cy))
        elif row["crop_yield"] < 5 and row["type"] == 1:
            report += f"crop yield is below expectations "
            report_cy.append((row["plant"] + ": " + bad_cy))
        elif row["crop_yield"] < 0 and row["type"] == 1:
            report += f"crop yield is disastrously low "
            report_cy.append((row["plant"] + ": " + terrible_cy))
        elif row["crop_yield"] >= 10 and row["type"] == 1:
            report += f"Crop yield is exceptional! "
            report_cy.append((row["plant"] + ": " + excellent_cy))

        # Analyze net yield
        if row["net_yield"] >= 12 and row["type"] == 1:
            report += f"net yield exceeds expectations.\n"
            report_ny.append((row["plant"] + ": " + excellent_ny))
        elif row["net_yield"] >= 8 and row["type"] == 1:
            report += f"net yield is performing average. \n"
            report_ny.append((row["plant"] + ": " + average_ny))
        elif row["net_yield"] < 8 and row["type"] == 1:
            report += f"net yield is below expectations\n"
            report_ny.append((row["plant"] + ": " + bad_ny))
        elif row["net_yield"] < 0 and row["type"] == 1:
            report += f"net yield is negative, indicating significant losses\n"
            report_ny.append((row["plant"] + ": " + terrible_ny))

        # for tangingang ano type 0 == individual crop / non yieldable plant
        # withered crops
        if row["withered_crops"] > 5 and row["type"] == 0:
            report += f"Withered crops have significantly impacted yield. Immediate action is needed. "
            report_wc.append((row["plant"] + ": " + terrible_wc))
        elif row["withered_crops"] >= 3 and row["type"] == 0:
            report += f"The number of withered crops is concerning and impacting yield "
            report_wc.append((row["plant"] + ": " + bad_wc))
        elif (
            row["withered_crops"] >= 1
            and row["withered_crops"] < 3
            and row["type"] == 0
        ):
            report += (
                f"There are some losses due to withered crops, but they're manageable "
            )
            report_wc.append(row["plant"] + ": " + mild_wc)
        else:
            report_wc.append(row["plant"] + ": " + good_wc)

        #  crop yield
        if row["crop_yield"] == 1 and row["type"] == 0:
            report += f"crop yield is satisfactory "
            report_cy.append(row["plant"] + ": " + average_cy)
        elif row["crop_yield"] < 1 and row["crop_yield"] > 0 and row["type"] == 0:
            report += f"Crop yield is below expectations, "
            report_cy.append(row["plant"] + ": " + bad_cy)
        elif row["crop_yield"] < 0 and row["type"] == 0:
            report += f"Crop yield is disastrously low, "
            report_cy.append(row["plant"] + ": " + terrible_cy)
        elif row["crop_yield"] > 1 and row["type"] == 0:
            report += f"Crop yield is exceptional! "
            report_cy.append(row["plant"] + ": " + excellent_cy)

        # net yield
        if row["net_yield"] == row["planted_qty"] and row["type"] == 0:
            report += f"net yield is performing average. \n"
            report_ny.append(average_ny)
        elif row["net_yield"] > row["planted_qty"] and row["type"] == 0:
            report += f"net yield exceeds expectationsyield is commendable. \n"
            report_ny.append(excellent_ny)
        elif row["net_yield"] < row["planted_qty"] and row["type"] == 0:
            report += f"net yield is lower than anticipated\n"
            report_ny.append(bad_ny)
        elif row["net_yield"] < 0 and row["type"] == 0:
            report += f"net yield is negative, indicating significant losses\n"
            report_ny.append(terrible_ny)

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
