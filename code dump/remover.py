import pandas as pd

# Load your dataset
df = pd.read_csv("final_dataset.csv")

# Words to remove
words_to_remove = [
    "nan",
]

# Convert the list of words to a pattern for matching
pattern = "|".join(words_to_remove)

# Remove the words and their commas (with optional space) from the 'tags' column
df["tags"] = df["tags"].str.replace(f"({pattern})(,\\s*)?", "", regex=True)

# Save the modified DataFrame to a new CSV file
df.to_csv("final.csv", index=False)

# Display the modified DataFrame
print(df)
