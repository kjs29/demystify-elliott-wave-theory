import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from elliott_wave_theory import filename, folder, block_sampling, run
from scipy.stats import t

def extract_sample_data(filename):
    df = pd.read_csv(filename)
    differences = df['wave3_max - wave1_max'].tolist()
    differences = list(map(lambda x: round(float(x), 4), differences))

    wave3_max = df['wave3_max'].tolist()
    wave1_max = df['wave1_max'].tolist()
    
    return differences, wave1_max, wave3_max

def analyze_samples(arr):
    # Analyze sample data
    sample_n = len(arr)
    sample_std_dev = np.std(arr, ddof=1) # ddof = 1 means calculate sample standard deviation
    sample_std_err = sample_std_dev / np.sqrt(sample_n)
    sample_mean = sum(arr) / sample_n
    degrees_of_freedom = sample_n - 1
    t_statistic = (sample_mean - 0) / sample_std_err
    p_value = t.sf(t_statistic, df=degrees_of_freedom) # one-tailed test
    print(f"sample_n : {sample_n} / sample_std_dev : {sample_std_dev} / sample_std_err : {sample_std_err} / sample_mean : {sample_mean} / df: {degrees_of_freedom}")
    return t_statistic, p_value

def save_histogram(arr, filename, bins=50, title='Mean of Differences (max(wave3) - max(wave1))', xlabel='Differences (max(wave3) - max(wave1))', ylabel='Frequency', grid=True, figsize=(10, 6)):
    # Plotting the histogram
    plt.figure(figsize=figsize)
    plt.hist(arr, bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    # plt.show()
    plt.savefig(filename)
    plt.close()

def save_boxplot(arr, filename, labels=['Wave1 Max', 'Wave3 Max'], title='Box Plot of Wave1 Max and Wave3 Max', ylabel='Values', figsize=(10, 6)):
    plt.figure(figsize=figsize)
    plt.boxplot(arr, labels=labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

# Get block samples
filenumbers = block_sampling(filename, 16)
print(f"Samples to run : {filenumbers}")

# Create folder for samples
os.makedirs(folder, exist_ok=True)  # hypothesis_test/

# Base name
base_name = filename.split('.')[0]

# Process data
for n in filenumbers:   # [1,3,5]
    # if filename is 'btc_historical.csv' and folder is 'hypothesis_test', 
    # it creates 'btc_historical_1_splitted_result.csv', 'btc_historical_3_splitted_result.csv', 'btc_historical_5_splitted_result.csv' at 'hypothesis_test'.
    run(f"{base_name}_{n}_splitted.csv", folder)

# Combine all the differences to compute the overall mean of differences, wave3_max, wave1_max from the sample data
combined_diff = []
combined_wave1_max = []
combined_wave3_max = []
for n in filenumbers:
    each_diff, each_wave1_max, each_wave3_max = extract_sample_data(f"{folder}/{base_name}_{n}_splitted_result.csv")
    combined_diff.extend(each_diff)
    combined_wave1_max.extend(each_wave1_max)
    combined_wave3_max.extend(each_wave3_max)


# Analyze samples
result = analyze_samples(combined_diff)
print(f"Hypothesis test result : t-statistics : {result[0]}, p-value : {result[1]}")

# Save histogram
save_histogram(combined_diff, 'Mean of Differences Histogram.jpg')

#Save botplot
boxplot_data = [combined_wave1_max, combined_wave3_max]
save_boxplot(boxplot_data, 'Wave1 Max & Wave3 Max Boxplot.jpg')

# Result
if result[1] < 0.05:
    print(f"p-value of {result[1]} is less than the standard significance level of 0.05, so it rejects the null hypothesis.")
else:
    print(f"p-value of {result[1]} is greater than the standard significance level of 0.05, so it fails to reject the null hypothesis.")