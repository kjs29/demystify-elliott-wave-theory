# Demystify-elliott-wave-theory

A Statistical Analysis of Elliott Wave Theory

# Introduction

Elliott Wave Theory was developed by Ralph Nelson Elliott in the 1930s. He believed that stock markets traded in repetitive patterns. He proposed that these patterns and price trends resulted from investor psychology. He argued that crowd psychology, where the consensus swings between optimism and pessimism, causes recurring fractal patterns in price movements.

‘Wave’ refers to the movement of a market, measured in price. (Neely, 1988/1990)

There are two modes of wave development: motive and corrective. Motive waves subdivide into five waves and always move in the same direction as the trend of one larger degree. There are two types of motive waves: impulse and diagonal. (Prechter & Frost, 2017)

Motive wave refers to a price movement toward the main trend. Corrective wave refers to price movement in the opposite direction of the main trend.

<img src="https://github.com/user-attachments/assets/bc9ebb9f-3aa4-4e61-978f-3ecea8eeb941" alt="image" width="400" height="400"/>

### Types of waves in Elliott Wave Theory

- Motive (Main trend)

  - Impulse
  - Diagonal

- Corrective (Correction)
  - Flat
  - Zig-zag
  - Triangle

<img src="https://github.com/user-attachments/assets/37bb78a4-a4c0-49e5-99dd-39232c97e428" alt="image" width="400" height="400"/>

<img src="https://github.com/user-attachments/assets/e7a5afc7-dd59-4533-b6e5-dcce66c2e284" alt="image" width="400" height="400"/>

The images above represent two types of motive waves.

There are a few rules and several guidelines in Elliott Wave Theory, and some books claim slightly different variations of them. One of the rules says that wave 2 never retraces more than 100% of wave 1. Another rule says that wave 3 can never be the shortest of three impulse waves.

There are many guidelines in Elliott Wave Theory. Some of them include ratio analysis. Elliott Wave Theory specifies that a correction retraces a Fibonacci percentage of the preceding wave. Sharp corrections tend more often to retrace 61.8% or 50% of the previous wave, particularly when they occur as wave 2 of an impulse. (Prechter & Frost, 2017)

<img src="https://github.com/user-attachments/assets/9c013ef3-3c6a-4c0b-abce-e8c7fae9e1ce" alt="image" width="310" />

<img src="https://github.com/user-attachments/assets/283e9775-cd16-4bc3-8245-0d5b63a0da8b" alt="image" width="600" height="300"/>

_Image source: Elliott Wave Principle_

# Purpose

I watched YouTube videos where people claimed they achieved significant profits with the Elliott Wave Theory in cryptocurrency trading. When Elliott Wave Theory was developed, cryptocurrency didn’t exist, and I want to find out if it applies to the cryptocurrency market.

Day traders often seek to recognize the patterns in their trading. For example, upon identifying wave 1, they are inclined to go long, anticipating that wave 3 will exceed wave 1.

# Objective

I want to conduct a statistical test on a hypothesis derived from the Elliott Wave Theory to examine its validity in the context of cryptocurrency trading.

This project will test whether sub-motive waves follow the uptrend as the Elliott Wave Theory claims in a bull market. Specifically, I would like to verify if the highest value of wave 3 exceeds the highest value of wave 1, as illustrated in Image 1.

# Methodology

## Hypotheses

One of the critical claims of this theory is that within an uptrend, the third wave in a motive sequence exceeds the highest point of the first wave, particularly after the second wave retraces to a level equal to or lower than specific Fibonacci retracement levels of the first wave. To verify this, the project aims to test the following hypotheses:

<img src="https://github.com/user-attachments/assets/96540d0d-ec90-4ce8-91a9-ca71ab15315a" alt="image" width="600" height="400"/>

### I will use these terms in the hypotheses set up:

**Price points**

- $low1$: Starting price of wave 1
- $high1$: Highest price of wave 1 (ending price of wave 1)
- $low2$: Starting price of wave 2 (ending price of wave 2)
- $high2$: Highest price of wave 3 (ending price of wave 3)

**Amplitude of Waves**

- $Amplitude_{wave1}$: $high1 - low1$
- $Amplitude_{wave2}$: $high1 - low2$
- $Amplitude_{wave3}$: $high2 - low2$

### Null Hypothesis:

There is no significant upward movement ($Amplitude_{wave3}$) after an uptrend motive wave and its subsequent corrective wave which retraces to a level between 61.8% and 99.9% of the first wave. $Amplitude_{wave3}$ is not greater than $Amplitude_{wave2}$, implying that $high2$ does not exceed $high1$.

$H_{0}: (high2 - low2) \leq (high1 - low2)$ $\text{ }$ or $\text{ }$ $Amplitude_{wave3}$ $\leq$ $Amplitude_{wave2}$ $\text{ }$  or $\text{ }$ $high2 \leq high1$ $\text{ }$

### Alternative Hypothesis: 

There is a significant upward movement ($Amplitude_{wave3}$) after an uptrend motive wave and its subsequent corrective wave which retraces to a level between 61.8% and 99.9% of the first wave. $Amplitude_{wave3}$ is greater than $Amplitude_{wave2}$, implying that $high2$ exceeds $high1$.

$H_{A}: (high2 - low2) > (high1 - low2)$ $\text{ }$ or $\text{ }$ $Amplitude_{wave3} > Amplitude_{wave2}$ $\text{ }$  or $\text{ }$ $high2 > high1$ $\text{ }$

To clarify the retracement percentages, if the first wave starts at 0 and reaches a maximum of 100, the second wave retraces to a level between 38.2 (100 - 61.8) and 0.1 (100 - 99.9) when retracement ratio is 0.618.

## Data Collection

- Bitcoin 1-hour historical data (BTCUSD: Bitcoin All Time History Index) from Tradingview.com
  - Date range: (2022-01-01 00:00 - 2024-07-22 19:00 UTC) 22412 rows

- **Sampling Method**:

  To ensure an unbiased and representative analysis, a mixture of block sampling and stratified random sampling was adopted.

  1. The entire data set is divided into 40 time blocks.
  
  2. Calculate the number of rows with green candles versus the number of entire rows within each block. The segments are categorized into green, red, and sideways market conditions.
  
  3. Using the random Python module, the samples are drawn from each category to ensure a balanced representation of different market conditions.

## Data Preparation and Analysis

The data preparation and analysis process is implemented using Python and involves the following steps:

### Data Loading and Conversion

- **Loading Data:** The data is loaded from a CSV file into a pandas DataFrame.
- **Date Conversion:** It converts UNIX timestamps to a readable date format.

### Adding Indicators

- **Color Coding Candles:** Each candle is classified as 'green', 'red', or 'doji' based on the relationship between its open and close prices.
- **Tail Range Calculation:** The tail range for each candle is calculated and stored.

### Finding Local Minima

- **Local Minima Identification:** Local minima are points where neighboring values are higher.
- **Finding Local Minima:** Local minima are identified using the `scipy.signal.find_peaks` function. [source code](https://github.com/scipy/scipy/blob/v1.14.0/scipy/signal/_peak_finding.py#L729-L1010) is here.
- **Distance Parameter:** Distance is set to 1 (default) to search every potential minimum point without any additional spacing requirement.

### Updating Local Lows

- **Updating Local Low:** The local low is updated whenever a new local minimum is lower than the current local low. Existing local lows that are higher than the new price are removed, ensuring that the oldest local lows are the lowest, and as time progresses, the newer local lows tend to be higher.
- **Resetting Threshold:** The resetting threshold feature ensures that the algorithm does not get stuck on local minima that are no longer relevant as new, significantly lower minima are found. This helps in dynamically adjusting the list of local lows to reflect more meaningful and current price movements. Simply, the higher threshold is, the wider range of timeline you are allowing it to test.

  _Example_

  If local_lows = [10, 90, 85], and we encounter a new local low of 70, two of the previous local lows (85 and 90) are removed because 70 < 85, and 70 < 90, respectively. If the resetting threshold is 1 or 2, the original local_lows gets cleared and 70 is added, so the list becomes [70]. If local_lows = [10, 90, 85] and the resetting threshold is 3, local_lows becomes [10, 70].

### Detecting Waves

- **Wave Detection:** Wave 1 and 2 are detected if there are at least two local lows that increase in value in chronological order. These pairs are candidates to test since the hypothesis is testing at low 2 whether it will exceed previous high1. [1](#detecting_waves)

- `store_unique_pairs_local_lows()` stores all the unique pairs of consecutive local lows in a dictionary where key is the pair of local lows, and the value is highest point between the local lows.

  ```py
  unique_pairs = store_unique_pairs_local_lows(df)
  print(unique_pairs)
  ```

  ```
  {
      '4, 46638.43;7, 46959.19': [5, 47515.8],
      '11, 46631.96;14, 46864.99': [13, 47196.88],
      '14, 46864.99;20, 47295.19': [17, 47952.97],
      '14, 46864.99;22, 47266.73': [17, 47952.97],
      '11, 46631.96;28, 46781.88': [17, 47952.97],
      '28, 46781.88;32, 46999.49': [31, 47305.53],
      ...
      '440, 41146.63;442, 41309.03': [441, 41684.71]
  }
  ```
### Finding Local Highs

- **Finding Local Highs:** The highest high between consecutive local lows is identified. Used for finding high1.

- **Searching high2:** Continuously update current maximum, and current minimum value. Starts searching for high2, given that there are low1, and low2.

This algorithm ensures that it captures significant price movements after low2, identifies potential high2 points based on given conditions, and categorizes waves into success or failure based on their behavior relative to high1 and the Fibonacci retracement level.
  ```
  Searching High2 Algorithm

  - Iterate through a dictionary that contains all pairs of (low1, low2):
  
    - Track the current maximum (cur_max) and current minimum (cur_min).
    - Iterate through the DataFrame starting from low2_index + 2 to avoid look-ahead bias:
        # Success Case:
        - If cur_max exceeds high1_price:
          - If it is the last row, record the current high2 information and add it to success waves, then break.
          - Otherwise, if cur_low is less than or equal to the Fibonacci retracement level of (low2_price, cur_max):
            - Add to success waves with the current high2 information and break.
          - If cur_max exceeds high1_price but the current row is not the last one and cur_low is greater than the Fibonacci level, continue to the next row.

        # Failure Case:
        - If cur_min is less than or equal to low1_price and high2_exceeded_high1_before is False:
          - If the current row is low2_index + 2, set high2_price conservatively to the current open price, add it to failure waves, and break.
          - Otherwise, find the maximum high between low2_index + 2 and the current row minus 1, set this as high2_price, add it to failure waves, and break.

        - If neither success nor failure conditions are met, continue iterating through the DataFrame.

  - After iterating through all pairs, print the count of success waves, failure waves, and uncounted waves.
  ```

### Calculating Fibonacci retracement levels

- **Calculation:**

  Fibonacci retracement level = high1 - (high1 - low1) * retracement_ratio

  Fibonacci retracement range = (low1, Fibonacci retracement level)

  Example
  ```py
  low1 = 100
  high1 = 200
  low2 = 130
  retracement_ratio = 0.618
  fib_level = 200 - (200 - 100) * 0.618 = 138.2
  fib_range = (100, 138.2)
  ```

### Trading Strategy 1


Entry: Buy at the open price of the candle that is two candles after low2 (i.e., low2_index + 2).

Exit:

  - Success: Sell at the retracement price.
  
  - Failure: Sell at low1 if high2 is less than or equal to high1.


### Plotting the Chart

- **Chart Plotting:** The chart is plotted with detected waves on candlestick chart. Waves where its high2 is greater than high1 are plotted with a solid line, and other waves are plotted with dotted-line. Different markers are used to visualize waves effectively. Modules used for charting are `mplfinance`, and `matplotlib.pyplot`.

# Statistical Tests

## Paired sample t-test (one-tailed)

The paired sample t-test is particularly suitable for this analysis as it allows for the comparison of the means of two related groups. Specifically, this test is used to compare the highest values of the first and third waves within the same market condition. By employing this method, we can determine if there is a statistically significant difference between these two means.

Conditions for sample t-test:

- Independence: Sample observations must be independent. Since each sample observation is the difference between two related groups, each individual pair must be independent of another pair. In time series data, whether one pair's difference influences the neighboring pair's difference is questionable, however, during the data collection I ensured independence by using block sampling and performing stratified random sampling methods.

- Normality: If the sample size is at least 30 and there are no particularly extreme outliers, then we typically assume the sampling distribution is nearly normal. The sampling distribution histogram is illustrated in the result section below, and it follows a normal curve.

Sample Mean of Difference: <img src="https://github.com/user-attachments/assets/05f4aace-7317-4346-8572-1c840d1c4a6e" alt="image" width="300" height="70" style="inline"/>

Sample Standard Deviation: <img src="https://github.com/user-attachments/assets/f14e6707-73e6-4a0d-b961-a8275697751f" alt="image" width="200" height="70" style="inline"/>

Sample Standard Error: <img src="https://github.com/user-attachments/assets/5a901673-1bc7-485a-beef-8b60e47e6c4a" alt="image" width="150" height="70" style="inline"/>

T-Statistic: <img src="https://github.com/user-attachments/assets/52d41e24-845f-45b6-a9c8-322ac057f079" alt="image" width="160" height="70" style="inline"/>

Degrees of Freedom: <img src="https://github.com/user-attachments/assets/c15a9fa4-4248-40f4-9cff-ac65323771ba" alt="image" width="140" height="70" style="inline"/>

## Expected Value

Expected Value, in general, is the value that is most likely the result of the next repeated trial of a statistical experiment.

The expected value (EV) helps determine if following a trading strategy will earn money in the long term. If the EV is positive, it suggests that the strategy is likely to be profitable over time. Conversely, a negative EV indicates potential long-term losses.

To evaluate the profitability of this trading strategy, we use the discrete expected value formula. The discrete expected value formula is used to determine the long-term average outcome of a trading strategy based on the probabilities of different outcomes and their respective values.

Expected Value: <img src="https://github.com/user-attachments/assets/e9ce69bd-5c49-4050-b8e2-db4919febb11" alt="image" width="200" height="70" style="inline"/>

# Result

## Samples data
  
The first elements refer to index, and the second elements represent correlation coefficient between the time and price.

  - Red: `[[37, -0.5441], [10, -0.301], [14, -0.8702], [36, -0.6594], [8, -0.5549], [21, -0.4307]]`

  - Sideways: `[[23, -0.2944], [18, 0.4168], [12, 0.1345], [16, 0.1812], [3, 0.0218], [11, -0.039]]`

  - Green: `[[27, 0.5306], [38, 0.6503], [9, 0.6352], [40, 0.5726], [4, 0.9428], [15, 0.7893]]`

Blocks used for Samples: `[37, 10, 14, 36, 8, 21, 23, 18, 12, 16, 3, 11, 27, 38, 9, 40, 4, 15]`

Number of Samples: 1173

Sample Standard Deviation: 1393.7234320939415

Sample Standard Error: 40.69373903394007

Sample Mean: 34.0213810741688

Degrees of Freedom: 1172

t-statistic: 0.8360347778756266

p-value: 0.20165287546619798

Success Ratio: 0.4356351236146633

p-value of 0.20165287546619798 is greater than the standard significance level of 0.05, so it fails to reject the null hypothesis.

### Test Strategy 1 Result:

Total # of Success Outcome: 511 / Total # of Failure Outcome: 662

P(Success): 0.4356351236146633

P(Failure): 0.5643648763853367

Average Success profit: 349.293170254403

Average Failure loss: -326.00871601208456

Overall Expected Value: -31.82349531116796

## Screenshot

![image](https://github.com/user-attachments/assets/031917a6-235e-4449-8eb4-4adf528f0e8d)


## Parameters used

```py
number_of_splits=40
# Divide into 40 blocks

retracement_ratio=0.618
# Determines the price range for the potential low2 point.

high2_retracement_ratio=0.618
# Determines the price range for the potential low3 point.

reset_threshold=1000000
# The higher reset_threshold is, the wider range it detects
```

# Visualization

## Sampling Distribution

<img src="https://github.com/user-attachments/assets/9c9fae5c-5941-4cd3-b682-95f3ad6072c8" alt="image" width="700" height="500"/>

## Boxplot

<img src="https://github.com/user-attachments/assets/7233ca76-349f-46d4-9c2b-19094cb2f74d" alt="image" width="700" height="500"/>


## Chart

For each wave, four points (low1, high1, low2, high2) are plotted since we don't need 5th or 6th point for the hypothesis.

If a wave's high2 point exceeds high1 point, it is drawn by line, otherwise dotted-line.

Waves are detected based on the parameters used for this sample test. 

- If `retracement_ratio=0.618`, low2 would not be detected if wave2 retraced less than 0.618 of the wave1.

- If `high2_retracement_ratio=0.382`, wave3 will keep searching for the highest point until current candle retraces equal to or more than 0.382 of wave3.

- If there is another trough between the troughs within a wave, they are not counted.

  <img src="https://github.com/user-attachments/assets/457d6ee1-6be6-4525-80e0-60e22c9d6d9a" alt="image" width="300" height="200"/>Counted(blue)<img src="https://github.com/user-attachments/assets/63904ae1-78ec-4e4f-a633-d0fbed22d3ac" alt="image" width="300" height="200"/>Not counted(red)

  I chose to count this way so that the project focuses more on clear and distinct wave patterns.
  

### Samples from Red Blocks
<img src="https://github.com/user-attachments/assets/2008ebc2-d0cf-4477-a961-5b138b8c7d40" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/531cb94f-60ff-40b2-82c8-5b193a07748c" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/1ba0010f-5d28-4433-b7aa-bda9baa8338b" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/22955eff-b7bf-44b0-98f0-853abb8990ce" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/4aa2bfb5-4c29-4dc3-a2b6-46039bf76bc9" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/9e8e99aa-2ec6-4493-aff3-e16273063a5b" alt="image" width="700" height="500"/>

### Samples from Green Blocks
<img src="https://github.com/user-attachments/assets/752d431e-b7ce-467a-9248-8c32f7cc00d1" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/a1222f98-bc0c-4029-9be2-49df10aab0f8" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/56678f95-1f71-4d60-a6eb-6a1003f4be66" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/cefd874a-d62e-4731-88de-5a0e5575e568" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/ed345021-019f-4684-b8a6-14489503f5b3" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/a288541c-8a85-417f-a4c9-a9775a8beb5d" alt="image" width="700" height="500"/>

### Samples from Sideways Blocks
<img src="https://github.com/user-attachments/assets/c3cce8f5-514a-495d-b666-77450d4d07e9" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/894a4118-1c20-405a-b64c-27fe511822c5" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/b9d56e14-fa15-4ac2-b85c-d55707def2a0" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/e6d8f8c3-cee6-4b33-b9d8-ad7d92f46813" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/45af0006-8180-4439-b448-eee93c75896f" alt="image" width="700" height="500"/>
<img src="https://github.com/user-attachments/assets/334ad606-bcb9-43ef-bfcd-136e4ef10d28" alt="image" width="700" height="500"/>

# Conclusion & Discussions

The statistical test conducted in this project did not provide strong evidence to reject the null hypothesis. The p-value obtained from the paired sample t-test was 0.12369275505181164, which is greater than the standard significance level of 0.05. This result means that we fail to reject the null hypothesis, indicating that the data does not provide sufficient evidence to conclude that wave 3 consistently reaches higher prices than wave 1 after an uptrend and its subsequent corrective wave falling within a Fibonacci retracement range. It can be interpreted as that there is approximately 12% probability that the observed differences (where wave 3 exceeds wave 1) could be due to random chances, assuming the null hypothesis is true. This is not low enough to conclude that there is a significant pattern where wave 3 consistently exceeds wave 1. 

While there is no sufficient evidence of wave 3 exceeding wave 1, the analysis shows that the probability of wave 3 exceeding wave 1 is still higher than 50%. This suggests that there may be a practical implication in trading. The higher probability of wave 3 exceeding wave 1 indicates that there might be underlying tendency in the market that can be exploited for trading strategies.

Further research could involve 

- Exploring different timeframes, market conditions, and Fibonacci retracement levels to further investigate the observed patterns

- Testing the hypothesis with different statistical inference methods or technologies such as machine learning

As someone who is still building his statistical knowledge, I remain cautious and open to identifying any potential biases that may have influenced my research. Throughout the project, the p-value varied significantly with subtle adjustments. The process of getting closer to the truth is genuinely exciting to me as an aspiring quantitative trader / researcher, and each time I believed that I was taking steps toward gaining a deeper understanding of the phenomena.

The journey of creating this project - encompassing the study of Elliott Wave Theory, statistical inference, hypothesis testing, and programming - has brought me immense satisfaction and joy. I would like to express my gratitude to Mr. Elliott.

<a name="detecting_waves">1.</a>

In detecting waves 1 and 2, two local lows, in hindsight, suffice the condition. However, because a local low from the way it was set up requires subsequent higher points, this approach inherently involves a look-ahead bias since we cannot rely on future information to make current decisions. For example, when Wave 2 is in progress, it is uncertain whether the price will decline further or reverse. Despite this limitation, the method remains valuable for hypothesis testing as it provides an opportunity to validate or refute specific market behavior ($H_{A}$). Establishing clear entry and exit strategies based on historical and currently available data is necessary. One example might be an entry strategy in a lower time frame after a new local minimum is found within the Fibonacci retracement range of the first wave to avoid look-ahead bias.

In hypothesis testing, the assumptions I make should be aligned with the specific patterns or behaviors I am investigating. If my goal is to determine whether the second motive wave's high value (wave 3) exceeds the first motive wave's high value (wave 1), then my assumptions should reflect the conditions under which I believe this pattern occurs. For example, comparing two uptrend motive waves in the context of Elliott Wave Theory requires three increasing local low values. One interesting point I would like to share is that I feel I gained more knowledge through the statistical research process than when I was reading books about Elliott Wave Theory. Research often helps confirm whether we truly understand what we think we know.

## References

Prechter, R., & Frost, A. J. (2017). _Elliott Wave Principle: Key to Market Behavior_ (11th ed.). New Classics Library.

Neely, G. (1990). _Mastering Elliott Wave_ (2.0) [E-book]. Windsor Books. (Original work published 1988)
