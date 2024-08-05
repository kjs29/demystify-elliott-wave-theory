import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from elliott_wave_theory import block_sampling, run
from scipy.stats import t

def extract_sample_data(filepath):
    # Extracts sample data from a CSV file.
    df = pd.read_csv(filepath)
    differences = df['wave3_max - wave1_max'].tolist()
    differences = list(map(lambda x: round(float(x), 4), differences))
    wave3_max = df['high2'].tolist()
    wave1_max = df['high1'].tolist()

    return differences, wave1_max, wave3_max

def analyze_samples(samples):
    # Analyzes the samples and computes statistical metrics.
    sample_n = len(samples)
    sample_std_dev = np.std(samples, ddof=1)  # ddof=1 for sample standard deviation
    sample_std_err = sample_std_dev / np.sqrt(sample_n)
    sample_mean = np.mean(samples)
    degrees_of_freedom = sample_n - 1
    t_statistic = sample_mean / sample_std_err
    p_value = t.sf(t_statistic, df=degrees_of_freedom)  # one-tailed test
    
    analysis_results = {
        "Number of Samples": sample_n,
        "Sample Standard Deviation": sample_std_dev,
        "Sample Standard Error": sample_std_err,
        "Sample Mean": sample_mean,
        "Degrees of Freedom": degrees_of_freedom,
        "t-statistic": t_statistic,
        "p-value": p_value
    }

    return analysis_results

def print_analysis_results(results):
    # Prints the analysis results.
    for key, value in results.items():
        print(f"{key}: {value}")
    p_value = results["p-value"]
    if p_value < 0.05:
        print(f"p-value of {p_value} is less than the standard significance level of 0.05, so it rejects the null hypothesis.")
    else:
        print(f"p-value of {p_value} is greater than the standard significance level of 0.05, so it fails to reject the null hypothesis.")

def save_histogram(samples, filename, bins=50, title='Mean of Differences (max(wave3) - max(wave1))', xlabel='Differences (max(wave3) - max(wave1))', ylabel='Frequency', grid=True, figsize=(10, 6)):
    # Create a histogram and save it
    plt.figure(figsize=figsize)
    plt.hist(samples, bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    # plt.show()
    plt.savefig(filename)

def save_boxplot(data, filename, labels=['Wave1 Max', 'Wave3 Max'], title='Box Plot of Wave1 Max and Wave3 Max', ylabel='Values', figsize=(10, 6)):
    # Create a box plot graph of the provided data
    plt.figure(figsize=figsize)
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)
    # plt.show()
    plt.savefig(filename)

def test_strategy_1(filepath):
    # Success: Selling at wave3's Fibonacci retracement level after high2 exceeds high1
    # Failure: Selling at low1 if high2 is less than or equal to high1.
    # Returns a tuple containing success and failure values.
    df = pd.read_csv(filepath)
    success_value, failure_value = [], []
    for i, row in df.iterrows():
        low1 = row['low1']
        high1 = row['high1']
        high2 = row['high2']
        profit = row['s1_profit']
        loss = row['s1_loss']
        if high2 > high1:
            success_value.append(profit)
        else:
            failure_value.append(loss)
    return success_value, failure_value

def print_strategy_1_result(success_value, failure_value):
    # Print strategy 1's result
    average_success_value = np.mean(success_value)
    average_failure_value = np.mean(failure_value)
    probability_success = len(success_value) / (len(success_value) + len(failure_value))
    expected_value = probability_success * average_success_value + (1 - probability_success) * average_failure_value
    print(f"\nTest Strategy 1 Result:\n")
    print(f"Total Success #: {len(success_value)} / Total Failure $: {len(failure_value)}")
    print(f"P(Success): {probability_success} / Average Success profit: {average_success_value}")
    print(f"P(Failure): {1 - probability_success} / Average Failure loss: {average_failure_value}")
    print(f"Overall Expected Value: {expected_value}\n")

def process_data(filename, 
                 conduct_block_sampling=False, 
                 number_of_splits=30, 
                 retracement_ratio=0.618,
                 high2_retracement_ratio=0.382, 
                 reset_threshold=100000, 
                 output_folder="hypothesis_test"):
    # Processes the data by conducting block sampling and analyzing the results.
    os.makedirs(output_folder, exist_ok=True)
    base_name = filename.split('.')[0]
    total_success_waves = 0
    total_failure_waves = 0

    # Block sampling
    if conduct_block_sampling:
        
        # Hypothesis testing
        file_numbers = block_sampling(filename, number_of_splits)
        print(f"Sample Blocks to Run: {file_numbers}")
        combined_diff = []
        combined_wave1_max = []
        combined_wave3_max = []
        
        # Strategy 1
        combined_success_value = []
        combined_failure_value = []

        for n in file_numbers:
            splitted_filename = f"{base_name}_{n}_splitted.csv"
            success_waves, failure_waves = run(splitted_filename, retracement_ratio, high2_retracement_ratio, reset_threshold, folder=output_folder)
            sample_filepath = f"{output_folder}/{base_name}_{n}_splitted_result.csv"
            diff, wave1_max, wave3_max = extract_sample_data(sample_filepath)
            combined_diff.extend(diff)
            combined_wave1_max.extend(wave1_max)
            combined_wave3_max.extend(wave3_max)
            total_success_waves += len(success_waves)
            total_failure_waves += len(failure_waves)

            # Aggregate individual data from each sample for strategy 1 test
            success_value, failure_value = test_strategy_1(sample_filepath)
            combined_success_value.extend(success_value)
            combined_failure_value.extend(failure_value)

        diff_analysis = analyze_samples(combined_diff)
        diff_analysis['Success Ratio'] = total_success_waves / (total_success_waves + total_failure_waves) if (total_success_waves + total_failure_waves) > 0 else 0
        print_analysis_results(diff_analysis)
        save_histogram(combined_diff, os.path.join(output_folder, 'Mean_of_Differences_Histogram.jpg'))
        save_boxplot([combined_wave1_max, combined_wave3_max], os.path.join(output_folder, 'Wave1_Max_and_Wave3_Max_Boxplot.jpg'))
        
        # Strategy 1
        print_strategy_1_result(combined_success_value, combined_failure_value)
    else:
        # Hypothesis testing
        success_waves, failure_waves = run(filename, retracement_ratio, high2_retracement_ratio, reset_threshold, folder=output_folder)
        sample_filepath = f"{output_folder}/{base_name}_result.csv"
        diff, wave1_max, wave3_max = extract_sample_data(sample_filepath)
        diff_analysis = analyze_samples(diff)
        diff_analysis['Success Ratio'] = len(success_waves) / (len(success_waves) + len(failure_waves)) if (len(success_waves) + len(failure_waves)) > 0 else 0
        print_analysis_results(diff_analysis)
        save_histogram(diff, os.path.join(output_folder, 'Mean_of_Differences_Histogram.jpg'))
        save_boxplot([wave1_max, wave3_max], os.path.join(output_folder, 'Wave1_Max_and_Wave3_Max_Boxplot.jpg'))
        
        # Strategy 1
        success_value, failure_value = test_strategy_1(sample_filepath)
        print_strategy_1_result(success_value, failure_value)

filename = "btc_historical.csv"
process_data(
    filename,
    conduct_block_sampling=True,
    number_of_splits=40,
    retracement_ratio=0.618,
    high2_retracement_ratio=0.382,
    reset_threshold=1000000,
    output_folder="hypothesis_test"
)