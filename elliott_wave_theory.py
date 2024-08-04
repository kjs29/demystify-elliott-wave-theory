import random
import copy
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
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

def shift_column(df, column, number_of_shifts=1):
    df[column] = df[column].shift(number_of_shifts)
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

def extract_each_row_local_lows_highs(row, low_only=False, high_only=False, index=False):
    # Extract local lows from each row and local highs to number types
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

def extract_all_local_lows(df):
    # Extract all local lows from the DataFrame, return a list [[index, price], [index, price], ...]
    local_lows = []
    seen_indices = set()
    for i, row in df.iterrows():
        lows = row['local_lows']
        for low in lows.split(';'):
            if low:
                index, value = low.split(',')
                index = int(index)
                value = float(value)
                if index not in seen_indices:
                    local_lows.append([index, value])
                    seen_indices.add(index)
    return local_lows

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
            local_lows_index = extract_each_row_local_lows_highs(row, True, False, True)
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

def store_unique_pairs_local_lows(df):
    # Store unique pairs of local lows
    # Returns a dictionary: 
    #   key : unique local lows as keys
    #   value : [highest price's index for low1's index + 1 : low2's index - 1,
    #           highest price between low1's index + 1 : low2's index - 1]
    unique_pairs_local_lows = {}
    for i, row in df.iterrows():
        wave_detected = row['wave_detected']
        if wave_detected == 1:
            local_lows_index = extract_each_row_local_lows_highs(row, True, False, True)    # [3, 5, 7]
            local_lows_price = extract_each_row_local_lows_highs(row, True, False, False)   # [300, 400, 600]
            local_highs_index = extract_each_row_local_lows_highs(row, False, True, True)    
            local_highs_price = extract_each_row_local_lows_highs(row, False, True, False)
            local_lows = list(zip(local_lows_index, local_lows_price))
            local_highs = list(zip(local_highs_index, local_highs_price))
            for i in range(1, len(local_lows)):
                prev_index, prev_price = local_lows[i-1]
                cur_index, cur_price = local_lows[i]
                high1_index, high1_price = local_highs[i-1]
                each_pair = f"{prev_index}, {prev_price};{cur_index}, {cur_price}"
                if each_pair not in unique_pairs_local_lows:
                    unique_pairs_local_lows[each_pair] = [high1_index, high1_price]
    return unique_pairs_local_lows

def store_unique_pairs_local_lows_within_fib_levels(unique_pairs_local_lows, retracement_ratio=0.618):
    # Takes a dictionary from 'store_unique_pairs_local_lows'
    # Returns dictionary with low2 being within fib levels of (high1 - low1)
    unique_pairs_local_lows_within_fib_levels = copy.deepcopy(unique_pairs_local_lows)
    result = {}
    for lows, (high1_index, high1_price) in unique_pairs_local_lows_within_fib_levels.items():
        # '315, 17232.35;323, 17996.33'
        low1, low2 = lows.split(";")
        # ['315, 17232.35', '323, 17996.33']
        low1_index, low1_price = low1.split(',')
        low1_index = int(low1_index)
        low1_price = float(low1_price)        
        low2_index, low2_price = low2.split(',')
        low2_index = int(low2_index)
        low2_price = float(low2_price)

        fib_level = high1_price - (high1_price - low1_price) * retracement_ratio
        if low1_price < low2_price <= fib_level:
            result[lows] = [low1_index, low1_price, high1_index, high1_price, low2_index, low2_price]
            
    return result

def search_high2(df, unique_pairs_local_lows_within_fib_levels, high2_retracement_ratio=0.382, debugging=False):
    # Takes a dictionary from 'store_unique_pairs_local_lows_within_fib_levels'
    # Search for high2 price for each pair of local lows
    unique_waves_success = {}
    unique_waves_failure = {}
    for lows, (low1_index, low1_price, high1_index, high1_price, low2_index, low2_price) in unique_pairs_local_lows_within_fib_levels.items():
        cur_max = 0
        cur_min = float('inf')
        high2_exceeded_high1_before = False
        for i, row in df.iloc[low2_index+2:].iterrows():    # 'low2_index+2' to avoid look-ahead bias
            cur_high = row['high']
            cur_low = row['low']
            cur_max = max(cur_max, cur_high)
            cur_min = min(cur_min, cur_low)
            if debugging:
                print(f"row : {i} / {lows} is being processed / {(low1_index, low1_price, high1_index, high1_price, low2_index, low2_price)} / cur_max:{cur_max} / cur_min:{cur_min} / cur_high:{cur_high} / cur_low:{cur_low}")
            
            # Success case
            if cur_max > high1_price:
                if debugging:
                    print(f"\tcur_max {cur_max} exceeds high1_price of {high1_price}")
                # If it is the last row, record it in success_waves
                if i == df.index[-1]:
                    point_falls_below_retracement_ratio_index, point_falls_below_retracement_ratio_price = i, cur_low
                    if debugging:
                        print(f"\tAfter cur_max {cur_max} exceeded high1_price of {high1_price}, since it is the last row of the file -> appended to success_waves")
                    if not df.loc[low2_index+2 : i-1,'high'].empty:
                        high2_index = df.loc[low2_index+2 : i-1,'high'].idxmax()
                        high2_price = df.loc[low2_index+2 : i-1,'high'].max()
                        unique_waves_success[lows] = [[low1_index, low1_price], [high1_index, high1_price], [low2_index, low2_price], [high2_index, high2_price], [point_falls_below_retracement_ratio_index, point_falls_below_retracement_ratio_price]]
                    break
                if not high2_exceeded_high1_before:
                    high2_exceeded_high1_before = True
                    if debugging:
                        print(f"\tGo to next row")
                    continue
                # Find the point where high1 retraces equal to or more than Fibonacci retracement ratio
                fib_level = cur_max - ((cur_max - low2_price) * high2_retracement_ratio)
                if debugging:
                    print(f"\tfib_level of {high2_retracement_ratio}: {fib_level}")
                if cur_low <= fib_level:
                    if debugging:
                        print(f"\tcur_low {cur_low} is less than fib_level of {fib_level} -> appended to success_waves")
                    point_falls_below_retracement_ratio_index, point_falls_below_retracement_ratio_price = i, cur_low
                    if not df.loc[low2_index+2 : i-1,'high'].empty:
                        high2_index = df.loc[low2_index+2 : i-1,'high'].idxmax()
                        high2_price = df.loc[low2_index+2 : i-1,'high'].max()
                        unique_waves_success[lows] = [[low1_index, low1_price], [high1_index, high1_price], [low2_index, low2_price], [high2_index, high2_price], [point_falls_below_retracement_ratio_index, point_falls_below_retracement_ratio_price]]
                    break
                if debugging:
                    print(f"\tcur_low {cur_low} is still higher than fib_level of {fib_level}")
                continue
                
            # Failure case
            if cur_min <= low1_price:
                if debugging:
                    print(f"\tcur min {cur_min} falls below low1_price {low1_price}, Find between (low2_index+1: {low2_index+1}, current row-1: {i-1})")
                point_falls_below_low1_index, point_falls_below_low1_price = i, cur_low
                
                if not df.loc[low2_index+2 : i-1,'high'].empty:
                    if debugging:
                        print("Appended to failure_waves")
                    high2_index = df.loc[low2_index+2 : i-1,'high'].idxmax()
                    high2_price = df.loc[low2_index+2 : i-1,'high'].max()
                    unique_waves_failure[lows] = [[low1_index, low1_price], [high1_index, high1_price], [low2_index, low2_price], [high2_index, high2_price], [point_falls_below_low1_index, point_falls_below_low1_price]]
                break
    
    uncounted_waves = {k:v for k,v in unique_pairs_local_lows_within_fib_levels.items() if k not in {**unique_waves_success, **unique_waves_failure}}
    print(f"search_high2: Out of {len(unique_pairs_local_lows_within_fib_levels)} wave candidates, there were {len(unique_waves_success)} success waves, {len(unique_waves_failure)} failure waves, {len(uncounted_waves)} uncounted waves.")
    print(f"Uncounted waves: {uncounted_waves}")
    
    return unique_waves_success, unique_waves_failure

def save_combined_waves_df(df, combined_waves, filename, save_df=False):
    # Combine success and failure waves, Save to DataFrame optionally
    combined_lows = {}
    for lows, points in combined_waves.items():
        date = str(df.iloc[points[0][0]]['date']) + '; ' + str(df.iloc[points[2][0]]['date']) + '; ' + str(df.iloc[points[4][0]]['date'])
        low1_index, low1_price = points[0]
        high1_index, high1_price = points[1]
        low2_index, low2_price = points[2]
        high2_index, high2_price = points[3]
        retracement_index, retracement_price = points[4]
        diff = float(high2_price - high1_price)
        combined_lows[lows] = [date, high1_price, high2_price, diff]

    # Convert the dictionary to a DataFrame
    result_df = pd.DataFrame.from_dict(combined_lows, orient='index', columns=['dates', 'wave1_max', 'wave3_max', 'wave3_max - wave1_max'])
    
    # Save to CSV if requested
    if save_df:
        result_df.to_csv(filename, index=False)
    
    return combined_waves

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

def save_chart(df, filename, success_waves, failure_waves, plot_success_waves=True, plot_failure_waves=False):
    # Prepare the data for mplfinance
    candlestick_chart_df = df[['date', 'open', 'high', 'low', 'close']].copy()
    candlestick_chart_df['Date'] = pd.to_datetime(candlestick_chart_df['date'])
    candlestick_chart_df = candlestick_chart_df.set_index('Date', inplace=False)
    candlestick_chart_df = candlestick_chart_df[['open', 'high', 'low', 'close']]  # Ensure the columns are in the correct order

    # Create a candlestick chart -> save picture, dataset(axes)
    first_date, last_date = candlestick_chart_df.index[0], candlestick_chart_df.index[-1]
    picture, dataset = mpf.plot(candlestick_chart_df, type='candle', style='charles', volume=False, figsize=(14,9), returnfig=True)

    # Set a title
    date_range = f"Bitcoin Hourly Price Movements with Detected Elliott Waves\n\nDate: ({first_date} - {last_date})"
    title = dataset[0].set_title(date_range, fontsize=16, pad=20)
    # title.set_y(1.4)    # title y location
    
    # Set margin space around the subplots -> Does not seem to work for some reason.
    picture.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
    
    # Remove y-label
    dataset[0].set_ylabel('')

    # Highlight detected waves
    success_waves = list(success_waves.values())
    failure_waves = list(failure_waves.values())
    markers = ['o', 's', 'd', "*"]
    if plot_success_waves:
        for i, wave in enumerate(success_waves):
            x_coords = [point[0] for point in wave]
            y_coords = [point[1] for point in wave]
            marker_index = i % len(markers)
            # plt.plot(df['date'].iloc[x_coords], y_coords, marker=markers[marker_index], linestyle='-', alpha=0.5)   # comment out when using mpf. This line plots waves with plt.
            
            # Plotting waves data on top of candlestick chart axes (dataset[0])
            dataset[0].plot(x_coords, y_coords, marker=markers[marker_index], linestyle='-', alpha=0.5) # dataset[0] = candlestick chart data(axes)
    if plot_failure_waves:
        for i, wave in enumerate(failure_waves):
            x_coords = [point[0] for point in wave]
            y_coords = [point[1] for point in wave]
            marker_index = i % len(markers)
            # plt.plot(df['date'].iloc[x_coords], y_coords, marker=markers[marker_index], linestyle='-', alpha=0.5)   # comment out when using mpf. This line plots waves with plt.
            
            # Plotting waves data on top of candlestick chart axes (dataset[0])
            dataset[0].plot(x_coords, y_coords, marker=markers[marker_index], linestyle=':', alpha=0.5) # dataset[0] = candlestick chart data(axes)
    
    plt.show()
    # picture.savefig(filename, bbox_inches='tight')
    picture.savefig(filename)
    # plt.close()

def block_sampling(filename, number_of_splits=30):
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
    
    # Stratified Random Sampling
    divisor = len(green_ratios) // 3
    red = random.sample(green_ratios[:divisor], max(1, divisor//2))
    green = random.sample(green_ratios[-divisor:], max(1, divisor//2))
    sideways = random.sample(green_ratios[divisor:-divisor], max(1, divisor//2))

    print(f"\nYou have requested to split your main file into {number_of_splits} blocks of files.")
    print(f"\nStratified Sampling done. Each block is categorized by the number of green candles / number of candles within each block.")
    print(f"\nTotal Blocks: {green_ratios}\n")
    print(f"Random Sampling is completed. We will process the following blocks, and get aggregated results.")
    print(f"Red: {red}")
    print(f"Green: {green}")
    print(f"Sideways: {sideways}\n")
    filenumbers = [x for x, y in red] + [x for x, y in green] + [x for x, y in sideways]
    
    return filenumbers

def run(filename, retracement_ratio=0.618, high2_retracement_ratio=0.382, reset_threshold=100000, folder='hypothesis_test'):
    # Process the given file to analyze
    # Return detected waves that meet the critera, and those that don't meet the critera
    
    # Data preparation
    df = load_file(filename)
    df = convert_UNIX_to_datetime(df)
    df = add_green_red(df)
    df = add_tail_range(df)
    local_low = find_local_minima(df)
    add_columns(df, local_low, "local_minima", 0, 1)
    df = add_local_lows(df, reset_threshold)
    df = convert_local_lows_to_dates(df)
    df = detect_waves(df)
    df = add_local_highs(df)

    # Waves Detection
    waves = store_unique_pairs_local_lows(df)
    waves = store_unique_pairs_local_lows_within_fib_levels(waves, retracement_ratio)
    success_waves, failure_waves = search_high2(df, waves, high2_retracement_ratio)
    combined_waves = {**success_waves, **failure_waves}
    
    # Save Results to files
    base_name = filename.split(".")[0]
    save_combined_waves_df(df, combined_waves, f"{folder}/{base_name}_result.csv", True)
    save_to_csv(df, f"{folder}/{base_name}_processed.csv", True)
    save_chart(
        df, 
        f"{folder}/{base_name}_chart.jpg", 
        success_waves, 
        failure_waves, 
        plot_success_waves=True, 
        plot_failure_waves=True
    )
    
    return success_waves, failure_waves


if __name__ == "__main__": 
    filename = "btc_historical.csv"
    folder = "hypothesis_test"
    # os.makedirs(folder, exist_ok=True)
    # run(filename, retracement_ratio=0.618, reset_threshold=100000, folder=folder)
    pass