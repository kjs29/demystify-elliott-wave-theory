import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from elliott_wave_theory import block_sampling, run
from scipy.stats import t

def extract_sample_data(filepath):
    df = pd.read_csv(filepath)
    differences = df['wave3_max - wave1_max'].tolist()
    differences = list(map(lambda x: round(float(x), 4), differences))
    wave3_max = df['wave3_max'].tolist()
    wave1_max = df['wave1_max'].tolist()
    return differences, wave1_max, wave3_max

def analyze_samples(samples):
    sample_n = len(samples)
    sample_std_dev = np.std(samples, ddof=1)  # ddof=1 for sample standard deviation
    sample_std_err = sample_std_dev / np.sqrt(sample_n)
    sample_mean = np.mean(samples)
    degrees_of_freedom = sample_n - 1
    t_statistic = sample_mean / sample_std_err
    p_value = t.sf(t_statistic, df=degrees_of_freedom)  # one-tailed test
    
    analysis_results = {
        "Sample Numbers": sample_n,
        "Sample Standard Deviation": sample_std_dev,
        "Sample Standard Error": sample_std_err,
        "Sample Mean": sample_mean,
        "Degrees of Freedom": degrees_of_freedom,
        "t-statistic": t_statistic,
        "p-value": p_value
    }
    
    return analysis_results

def save_histogram(samples, filename, bins=50, title='Mean of Differences (max(wave3) - max(wave1))', xlabel='Differences (max(wave3) - max(wave1))', ylabel='Frequency', grid=True, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    plt.hist(samples, bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    plt.show()
    plt.savefig(filename)

def save_boxplot(data, filename, labels=['Wave1 Max', 'Wave3 Max'], title='Box Plot of Wave1 Max and Wave3 Max', ylabel='Values', figsize=(10, 6)):
    plt.figure(figsize=figsize)
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()
    plt.savefig(filename)

def process_data(filename, conduct_block_sampling=False, number_of_splits=30, retracement_ratio=0.618, reset_threshold=100000, output_folder="hypothesis_test"):
    os.makedirs(output_folder, exist_ok=True)
    base_name = filename.split('.')[0]
    
    if conduct_block_sampling:
        file_numbers = block_sampling(filename, number_of_splits)
        print(f"Samples to run: {file_numbers}")

        combined_diff = []
        combined_wave1_max = []
        combined_wave3_max = []

        for n in file_numbers:
            splitted_filename = f"{base_name}_{n}_splitted.csv"
            run(splitted_filename, retracement_ratio, reset_threshold, folder=output_folder)
            sample_filepath = f"{output_folder}/{base_name}_{n}_splitted_result.csv"
            diff, wave1_max, wave3_max = extract_sample_data(sample_filepath)
            combined_diff.extend(diff)
            combined_wave1_max.extend(wave1_max)
            combined_wave3_max.extend(wave3_max)

        diff_analysis = analyze_samples(combined_diff)
        print_analysis_results(diff_analysis)
        
        save_histogram(combined_diff, os.path.join(output_folder, 'Mean_of_Differences_Histogram.jpg'))
        save_boxplot([combined_wave1_max, combined_wave3_max], os.path.join(output_folder, 'Wave1_Max_and_Wave3_Max_Boxplot.jpg'))
    else:
        run(filename, retracement_ratio, reset_threshold, folder=output_folder)
        sample_filepath = f"{output_folder}/{base_name}_result.csv"
        diff, wave1_max, wave3_max = extract_sample_data(sample_filepath)
        
        diff_analysis = analyze_samples(diff)
        print_analysis_results(diff_analysis)
        
        save_histogram(diff, os.path.join(output_folder, 'Mean_of_Differences_Histogram.jpg'))
        save_boxplot([wave1_max, wave3_max], os.path.join(output_folder, 'Wave1_Max_and_Wave3_Max_Boxplot.jpg'))

def print_analysis_results(results):
    for key, value in results.items():
        print(f"{key}: {value}")
    p_value = results["p-value"]
    if p_value < 0.05:
        print(f"p-value of {p_value} is less than the standard significance level of 0.05, so it rejects the null hypothesis.")
    else:
        print(f"p-value of {p_value} is greater than the standard significance level of 0.05, so it fails to reject the null hypothesis.")


filename = "btc_historical.csv"
process_data(
    filename, 
    conduct_block_sampling=True, 
    number_of_splits=16,
    retracement_ratio=0.618,
    reset_threshold=100000,
    output_folder="hypothesis_test"
)