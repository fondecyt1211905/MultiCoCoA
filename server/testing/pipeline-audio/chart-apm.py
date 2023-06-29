import sys, os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--csv", type=argparse.FileType('rb'), required=True, help="filename .csv")
parser.add_argument("--feature", type=str, default="F0final_sma_amean", help="feature")
args = parser.parse_known_args()

if __name__ == '__main__':
    df = pd.read_csv(args[0].csv, sep=";").reset_index()
    print(df.info())
    plt.figure(figsize=(10,10))
    plt.title("Interventions...")
    sns.scatterplot(data = df,x = "index", y = args[0].feature, hue="active_voice", style="active_voice", palette=['green','orange','brown','dodgerblue','red','yellow'])
    plt.show()
