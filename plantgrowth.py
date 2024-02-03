from flask import Flask, request, jsonify

app = Flask(__name__)


# calculate ng percentage increase
# abs - absolute value, tanggalin mo na lang kung gusto mo ipakita if negative (eg. -51%, -32%) ipapakita m
def calculate_percentage_increase(average_growth, recent_growth):
    if average_growth == 0:
        return "No significant increase in growth rate."

    percentage_increase = ((recent_growth - average_growth) / abs(average_growth)) * 100
    return percentage_increase


# messasges pati conditions
def compare_growth(average_growth, recent_growth):
    if recent_growth > average_growth:
        percentage_increase = calculate_percentage_increase(
            average_growth, recent_growth
        )
        return f"You're doing well! Recent plant growth is higher than average growth by {percentage_increase:.2f}%."
    elif recent_growth < average_growth:
        return f"Your plant has a lower growth rate that is lower than your usual {average_growth:.2f}%."
    else:
        return "No significant increase in growth rate."


# ikaw na magpalit ng route :d
@app.route("/", methods=["POST"])
def compare_growth():
    try:
        data = request.get_json()
        average_growth = data.get("average_growth")
        recent_growth = data.get("recent_growth")

        if average_growth is None or recent_growth is None:
            return jsonify({"error": "Missing data"}), 400

        # values
        result = compare_growth(average_growth, recent_growth)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
