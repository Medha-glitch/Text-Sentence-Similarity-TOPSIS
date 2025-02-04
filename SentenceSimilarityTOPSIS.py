# -*- coding: utf-8 -*-
"""Text_sentence_similarity_TOPSIS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UPiVmgTY1G9zZW0s9sqK3HLVCUPXSgvu

##Using models: BERT, RoBERTa, DistilBERT, USE, Sentence-BERT##

##Criteria: Accuracy, Speed, Memory Usage, Ease of Use##
"""

import os
import pandas as pd

# Create synthetic data
data = {
    "Model": ["BERT", "RoBERTa", "DistilBERT", "USE", "Sentence-BERT"],
    "Accuracy": [0.92, 0.91, 0.89, 0.90, 0.93],
    "Speed": [0.5, 0.6, 0.4, 0.3, 0.7],
    "Memory Usage": [400, 450, 350, 300, 500],
    "Ease of Use": [8, 7, 9, 9, 8]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create the 'data' directory to save the data
if not os.path.exists("data"):
    os.makedirs("data")

# Save synthetic data to a CSV file
df.to_csv("data/synthetic_data.csv", index=False)
print("Synthetic data saved to 'data/synthetic_data.csv'")

"""##Normalizing the Dataset##"""

##Using euclidean normalization
#Extracting the numerical data, excluding 'Model' column
numerical_data = df.iloc[:, 1:].values

#Normalize the data:
normalized_data = numerical_data / np.sqrt((numerical_data ** 2).sum(axis=0))

#Convert back to a Dataframe
normalized_df = pd.DataFrame(normalized_data, columns=df.columns[1:])
normalized_df.insert(0, "Model", df["Model"])
print("\nNormalized Dataset:")
print(normalized_df)

"""##Assigning weights to Criteria##"""

##Weights for each criterion
weights = np.array([0.4, 0.3, 0.2, 0.1])

##multiply normalized data y the weights
weighted_normalized_data = normalized_data * weights

#Convert back to dataframe:
weighted_df = pd.DataFrame(weighted_normalized_data, columns=df.columns[1:])
weighted_df.insert(0, "Model", df["Model"])
print("\nWeighted Normalized Dataset:")
print(weighted_df)

"""##Determining Ideal and Negative-ideal Solutions##"""

##Determining ideal best and ideal worst
# Accuracy, Ease of Use
ideal_best = np.max(weighted_normalized_data[:, [0, 3]], axis=0)

# Speed, Memory Usage
ideal_best = np.append(ideal_best, np.min(weighted_normalized_data[:, [1, 2]], axis=0))

# Accuracy, Ease of Use
ideal_worst = np.min(weighted_normalized_data[:, [0, 3]], axis=0)

# Speed, Memory Usage
ideal_worst = np.append(ideal_worst, np.max(weighted_normalized_data[:, [1, 2]], axis=0))

print("\nIdeal Best:", ideal_best)
print("Ideal Worst:", ideal_worst)

"""##Calculating Separation Measures##"""

# Calculate separation measures
S_best = np.sqrt(((weighted_normalized_data - ideal_best) ** 2).sum(axis=1))
S_worst = np.sqrt(((weighted_normalized_data - ideal_worst) ** 2).sum(axis=1))

# Add to DataFrame
df["S_best"] = S_best
df["S_worst"] = S_worst
print("\nSeparation Measures:")
print(df[["Model", "S_best", "S_worst"]])

"""##Calculating Relative Closeness and Rank Models##"""

# Calculate relative closeness
df["Relative Closeness"] = df["S_worst"] / (df["S_best"] + df["S_worst"])

# Rank models
df["Rank"] = df["Relative Closeness"].rank(ascending=False)

# Sort by rank
df = df.sort_values(by="Rank")
print("\nFinal Ranking:")
print(df[["Model", "Relative Closeness", "Rank"]])

"""##Creating directories to store final results and visuals##"""

# Create directories if they don't exist
for directory in ["data", "results", "visuals"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Save synthetic data to a CSV file
df.to_csv("data/synthetic_data.csv", index=False)

# Save results to a CSV file
df[["Model", "Relative Closeness", "Rank"]].to_csv("results/final_ranking.csv", index=False)

"""##Visualizing Results##"""

import matplotlib.pyplot as plt

# Bar plot for Relative Closeness
plt.figure(figsize=(10, 5))
plt.bar(df["Model"], df["Relative Closeness"], color="skyblue")
plt.xlabel("Model")
plt.ylabel("Relative Closeness")
plt.title("Relative Closeness to Ideal Solution")
plt.show()

