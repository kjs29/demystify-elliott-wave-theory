import pandas as pd
import matplotlib.pyplot as plt
import random
from scipy.signal import find_peaks


def load_file(filename):
    df = pd.read_csv(filename)
    
    return df

def save_to_csv(df, new_filename, include_index=True):
    # index included to make it easier to verify and compare local lows later
    df.to_csv(new_filename, index=include_index, index_label='index_column')


def add_columns(df, arr, column_name, default_value=0, active_value=1):
    df[column_name] = default_value
    df.loc[arr, column_name] = active_value

    return df

def convert_UNIX_to_datetime(df):

    if 'date' in df.columns:
        df.drop(columns=['date'], inplace=True)
    if 'unix' in df.columns or 'time' in df.columns:
        # Convert the Unix timestamp to a readable date
        time_column = 'unix' if 'unix' in df.columns else 'time'
        
        df['date'] = pd.to_datetime(df[time_column], unit='s')
        df.drop(columns=[time_column], inplace=True)

        # Insert the 'date' column as the first column
        df.insert(0, 'date', df.pop('date'))

    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

def extract_local_lows_highs(row, low_only=False, high_only=False, index=False):
    # Extract local lows and local highs to number types
    if low_only:
        local_lows = row['local_lows'].split(';')
        if index:
            return [int(low.split(',')[0]) for low in local_lows]
        else:
            return [float(low.split(',')[1]) for low in local_lows]

    # Extract local highs
    if high_only:
        local_highs = row['local_highs'].split(';')
        if index:
            return [int(high.split(',')[0]) for high in local_highs]
        else:
            return [float(high.split(',')[1]) for high in local_highs]

    # Extract both local lows and local highs
    local_lows = row['local_lows'].split(';')
    local_highs = row['local_highs'].split(';')
    if index:
        local_lows = [int(low.split(',')[0]) for low in local_lows]
        local_highs = [int(high.split(',')[0]) for high in local_highs]
    else:
        local_lows = [float(low.split(',')[1]) for low in local_lows]
        local_highs = [float(high.split(',')[1]) for high in local_highs]

    return local_lows, local_highs

def add_green_red(df):
    green_red = []
    for i,row in df.iterrows():
        close = row['close']
        open = row['open']
        if close > open:
            green_red.append("green")
        elif close < open:
            green_red.append("red")
        else:
            green_red.append("doji")
    df['green_red'] = green_red

    return df

def add_tail_range(df):
    tail_range = []
    for i,row in df.iterrows():
        green_red = row['green_red']
        if green_red == "red":
            tail_range.append(f"{row['low']}, {row['close']}")
        else:
            tail_range.append(f"{row['low']}, {row['open']}")
    df['tail_range'] = tail_range

    return df

def find_local_minima(df, distance=1):
    # Find local minima
    low = df['low'].values
    lows_arr, _ = find_peaks(-low, distance=distance)

    return lows_arr

def add_local_lows(df, reset_threshold=3):
    # If a new lower minima is found, pop any existing higher lows and add the new low. 
    # If the new low is lower than 'reset_threshold' number of previous lows, local_lows is cleared.
    local_lows = []
    local_lows_column = [] # A list to store the cumulative local lows for each row.
    for i, row in df.iterrows():
        local_minima = row['local_minima']
        low = row['low']
        if local_minima == 1:
            if not local_lows:
                local_lows.append(f"{i}, {low}")
            else:
                last_local_low = float(local_lows[-1].split(',')[1])
                if low > last_local_low:
                    local_lows.append(f"{i}, {low}")
                elif low < last_local_low:
                    tmp = local_lows.copy()
                    count_lower_low = 0
                    for j in range(len(local_lows)-1, -1, -1):
                        index, existing_low = tmp[j].split(',')
                        existing_low = float(existing_low)
                        if existing_low > low:
                            tmp.pop()
                            count_lower_low += 1
                        else:
                            break
                    if count_lower_low >= reset_threshold:
                        tmp.clear()
                    local_lows = tmp
                    local_lows.append(f"{i}, {low}")
        local_lows_column.append(';'.join(local_lows))
    df['local_lows'] = local_lows_column
    
    return df

def convert_local_lows_to_dates(df):
    # Convert local_lows to dates
    converted_dates = [None] * len(df)
    for i, row in df.iterrows():
        local_lows = row['local_lows']
        if local_lows:
            local_lows_index = extract_local_lows_highs(row, True, False, True)
            dates = []
            for each_index in local_lows_index:
                dates.append(str(df.loc[each_index, 'date']))
            converted_dates[i] = '; '.join(dates)
    df['local_lows_converted'] = converted_dates
    
    return df

def detect_waves(df):
    # Detect waves
    # A wave is detected if there are at least two local lows that increase in value in chronological order
    df['wave_detected'] = 0
    for i, row in df.iterrows():
        local_lows = row['local_lows'].split(';')
        if len(local_lows) > 1:
            df.at[i, 'wave_detected'] = 1
    
    return df

def add_local_highs(df):
    # Find local highs between two local lows
    local_highs = [None] * len(df)
    for i, row in df.iterrows():
        wave_detected = row['wave_detected']
        if wave_detected == 1: # local_lows at least have two lows
            local_lows = row['local_lows'].split(';')
            high_values = []
            for j in range(1, len(local_lows)):
                prev_index, prev_price = local_lows[j-1].split(',')
                cur_index, cur_price = local_lows[j].split(',')
                
                # find highest high 
                highest_high_index = df.loc[int(prev_index)+1:int(cur_index)-1, 'high'].idxmax()
                highest_high_price = df.loc[int(prev_index)+1:int(cur_index)-1, 'high'].max()
                high_values.append(f"{highest_high_index}, {highest_high_price}")
            local_highs[i] = '; '.join(high_values)
    df['local_highs'] = local_highs

    return df

def add_fib_levels(df, retracement_ratio=0.618):
    # Add Fibonacci retracement level between two local lows
    fib_levels = [None] * len(df)
    for i, row in df.iterrows():
        detected = row['wave_detected']
        if detected == 1:   # requires at least two local lows
            local_lows, local_highs = extract_local_lows_highs(row)
            fib_level_values = []
            for j in range(len(local_highs)):
                wave1_max = local_highs[j]
                wave1_start = local_lows[j]
                wave3_start  = local_lows[j+1]
                fib_level = wave1_max - (wave1_max - wave1_start) * retracement_ratio
                fib_level_values.append(f"{fib_level:.4f}")
            fib_levels[i] = '; '.join(map(str, fib_level_values))
    
    df[f'fib_levels_{1 - retracement_ratio}'] = fib_levels
    
    return df

def check_second_wave_end_within_fib_range(df, retracement_ratio=0.618):
    # Check if the second wave ends within the Fibonacci retracement levels of the first wave
    # False: out of range, True: within the range
    check_fib = [None] * len(df)
    for i, row in df.iterrows():
        detected = row['wave_detected']
        if detected == 1:   # requires at least two local lows
            local_lows = extract_local_lows_highs(row, True)
            if len(local_lows) > 2:
                fib_levels = row[f'fib_levels_{1 - retracement_ratio}'].split(';') # ['6835.201435', '7238.915215']
                fib_levels = list(map(float, fib_levels))
                check_fib_values = []
                for j in range(1, len(local_lows)):
                    first_wave_start = local_lows[j - 1]
                    second_wave_end = local_lows[j]
                    fib_level = fib_levels[j - 1]
                    if first_wave_start < second_wave_end <= fib_level:
                        check_fib_values.append(True)
                    else:
                        check_fib_values.append(False)
                check_fib[i] = '; '.join(map(str, check_fib_values))
    
    df[f'second_wave_end_within_fib_range_{1 - retracement_ratio}'] = check_fib
    
    return df

def save_unique_waves_df(df, filename, retracement_ratio=0.618):
    # Save unique wave data to a CSV file.
    unique_lows = {}
    wave12345_detected = [] # [date = str(df.iloc[local_lows_index[j]]['date']) + '; ' + str(df.iloc[local_lows_index[j+1]]['date']) + '; ' + str(df.iloc[local_lows_index[j+2]]['date'])]
    for i, row in df.iterrows():
        detected = row['wave_detected']
        if detected == 1:   # requires at least two local lows
            local_lows = row['local_lows'].split(';')   # ['11, 6522.48', '13, 6850.5425', '18, 7156.88']
            if len(local_lows) > 2:
                
                local_lows_index = extract_local_lows_highs(row, True, False, True)
                local_lows_price = extract_local_lows_highs(row, True, False, False)
                local_highs = extract_local_lows_highs(row, False, True)
                within_fib_range = row[f'second_wave_end_within_fib_range_{1 -  retracement_ratio}'].split(';')
                within_fib_range = list(map(lambda x: x.strip().lower() == 'true', within_fib_range))    # Convert string 'True' to boolean True

                for j in range(len(within_fib_range) - 2):
                    each_fib_range = within_fib_range[j]
                    if each_fib_range:
                        each_lows = str(local_lows_price[j]) + "; " + str(local_lows_price[j+1]) + "; " + str(local_lows_price[j+2])
                        if each_lows not in unique_lows:
                            date = str(df.iloc[local_lows_index[j]]['date']) + '; ' + str(df.iloc[local_lows_index[j+1]]['date']) + '; ' + str(df.iloc[local_lows_index[j+2]]['date'])
                            wave1_max = local_highs[j]
                            wave3_max = local_highs[j+1]
                            diff = float(wave3_max - wave1_max)
                            unique_lows[each_lows] = [date, wave1_max, wave3_max, diff]

    # Convert the dictionary to a DataFrame
    result_df = pd.DataFrame.from_dict(unique_lows, orient='index', columns=['dates', 'wave1_max', 'wave3_max', 'wave3_max - wave1_max'])
    
    save_to_csv(result_df, filename, False)

def save_stock_chart(df, filename):
    plt.figure(figsize=(14, 9))
    plt.plot(df['date'], df['high'], label='High', color='green')
    plt.plot(df['date'], df['close'], label='Close', color='blue')
    plt.plot(df['date'], df['low'], label='Low', color='red')

    # Highlight local lows
    local_low_indices = []
    local_low_values = []
    for lows in df['local_lows']:
        for low in lows.split(';'):
            if low:
                index, value = low.split(',')
                local_low_indices.append(int(index))
                local_low_values.append(float(value))

    plt.scatter(df['date'].iloc[local_low_indices], local_low_values, color='orange', label='Local Lows')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices: High, Close, Low')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(filename)
    plt.close()

def block_sampling(filename, number_of_splits=10):
    # Block Sampling

    def split_dataframe(df, number_of_splits):
        # Split a DataFrame into arbitrary number of DataFrames
        num_rows = len(df)
        rows_per_split = num_rows // number_of_splits
        df_list = []
        for i in range(number_of_splits):
            start_row = i * rows_per_split
            # If it's the last split, include all remaining rows
            if i == number_of_splits - 1:
                end_row = num_rows
            else:
                end_row = (i + 1) * rows_per_split
            split_df = df.iloc[start_row:end_row]
            df_list.append(split_df)
        
        return df_list
    
    def count_green_ratio(df):
        # Determine the ratio of green rows out of total rows
        green = (df['green_red'] == 'green').sum()
        total = len(df)
        
        return green / total
    
    df = load_file(filename)
    new_dfs = split_dataframe(df, number_of_splits) # List of DataFrame
    green_ratios = {}
    for i in range(1, number_of_splits + 1):
        new_df = new_dfs[i-1]
        new_df = add_green_red(new_df)
        new_df_green_ratio = count_green_ratio(new_df)
        green_ratios[i] = [i, round(new_df_green_ratio, 4)]
        splitted_filename = f"{filename.split('.')[0]}_{i}_splitted.csv"
        save_to_csv(new_dfs[i-1], splitted_filename, False)
    
    green_ratios = sorted(green_ratios.values(), key=lambda x:x[1])
    
    # Stratified Sampling
    red = green_ratios[:2]
    green = random.sample(green_ratios[-3:], 2)
    sideways = random.sample(green_ratios[3:-3], 5)

    print("Sampling is finished, process these samples.")
    print(f"Red: {red}")
    print(f"Green: {green}")
    print(f"Sideways: {sideways}")
    filenumbers = [x for x, y in red] + [x for x, y in green] + [x for x, y in sideways]
    
    return filenumbers

def run(filename, folder='hypothesis_test'):
    # Run a file, and save the results at folder/ location.
    df = load_file(filename)
    df = convert_UNIX_to_datetime(df)
    df = add_green_red(df)
    df = add_tail_range(df)
    local_low = find_local_minima(df)
    add_columns(df, local_low, "local_minima", 0, 1)
    df = add_local_lows(df, reset_threshold=5)
    df = convert_local_lows_to_dates(df)
    df = detect_waves(df)
    df = add_local_highs(df)
    df = add_fib_levels(df, 0.618)
    df = check_second_wave_end_within_fib_range(df, 0.618)
    base_name = filename.split(".")[0]
    save_unique_waves_df(df, f"{folder}/{base_name}_result.csv", retracement_ratio=0.618)
    save_to_csv(df, f"{folder}/{base_name}_processed.csv", True)
    save_stock_chart(df,f"{folder}/{base_name}_chart.jpg")


filename = "btc_historical.csv"
folder = "hypothesis_test"

if __name__ == "__main__": 
    # run(filename, folder)
    pass