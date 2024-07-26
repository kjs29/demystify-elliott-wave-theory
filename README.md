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
  1. The entire data set is divided into 16 time blocks.
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
  - _Example_
    If local_lows = [10, 90, 85], and we encounter a new local low of 70, two of the previous local lows (85 and 90) are removed because 70 < 85, and 70 < 90, respectively. If the resetting threshold is 1 or 2, the original local_lows gets cleared and 70 is added, so the list becomes [70]. If local_lows = [10, 90, 85] and the resetting threshold is 3, local_lows becomes [10, 70].

### Detecting Waves

- **Wave Detection:** Waves 1 and 2 are detected if there are at least two local lows that increase in value in chronological order. [1](#detecting_waves)

### Finding Local Highs

- **Local High Identification:** The highest high between consecutive local lows is identified.

### Comparing Waves

- **Wave Comparison:** For each detected wave, wave 1 and wave 3 maxima are compared, and the differences are calculated.

### Saving Unique Local Lows

- **Handling Overlapping Segments:** When dealing with wave data in time series, there were many overlapping wave segments. To remove these overlapping segments, I recorded the unique local lows and saved them along with their corresponding dates in a CSV file.

### Plotting the Stock Chart

- **Stock Chart Plotting:** The stock chart is plotted, highlighting local lows.

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

# Result

## Sampling Distribution

<img src="https://github.com/user-attachments/assets/ea9f2b78-1715-4d33-ba59-9f65e540c086" alt="image" width="600" height="400"/>

## Sample Market Conditions

### Red [3,1]

<img src="https://github.com/user-attachments/assets/626e5d34-6f73-4dd7-b693-79986a4a54d4" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/cbdf6eae-133e-4c9a-9767-7f77d21809c1" alt="image" width="400" height="300"/>

### Green [14,7]

<img src="https://github.com/user-attachments/assets/26269a95-e179-4675-9e60-e098c72fac3a" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/50af9679-fc75-4849-8a62-a1a8f68a0252" alt="image" width="400" height="300"/>

### Sideways

### [1, 6]

### [4, 13]

### [10]

<img src="https://github.com/user-attachments/assets/2f566a06-d2f7-4dcb-b5ff-bdbb0a517a95" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/c76efc61-beb8-42c1-85a4-6bbc1cb44006" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/dd5624d5-e65e-4b05-af37-acc795eb1cae" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/e4b32fc5-bcac-4046-a7b6-8adac01b425e" alt="image" width="400" height="300"/>
<img src="https://github.com/user-attachments/assets/f6a0ced2-e4ae-4bab-9c25-0dd93f904a03" alt="image" width="400" height="300"/>

## Boxplot

<img src="https://github.com/user-attachments/assets/84fede69-7cd4-43f4-ba41-cc90ad0d6f2f" alt="image" width="500" height="300"/>

# Sample Data

_Red_: `[[3, 0.4743], [9, 0.4907]] # [index, green candle ratio]`

_Green_: `[[14, 0.5243], [7, 0.52]]`

_Sideways_: `[[1, 0.5071], [6, 0.5007], [4, 0.5043], [13, 0.5021], [10, 0.5]]`

_Samples to run_: `[3, 9, 14, 7, 1, 6, 4, 13, 10]`

Number of samples: 750

Sample Standard Deviation: 766.9509743448738

Sample Mean : 60.1894

Degrees of Freedom: 749

**Test statistic (t)**: 2.1492321617926176

**P-value**: 0.01596788054432838

P-value is less than the standard significance level $\alpha$ of 0.05. This indicates that there is sufficient evidence to reject the null hypothesis.

# Conclusion & Discussions

In conclusion, the statistical test conducted in this project provides strong statistical evidence against the null hypothesis. The rejection of the null hypothesis indicates that the data provides strong evidence that wave 3 consistently reaches higher prices than wave 1, after an uptrend and its subsequent corrective wave falling within a Fibonacci retracement range. It can also be interpreted as it is very unlikely that the observed differences where wave 3 exceeds wave 1 are due to random chance.

As someone who is still building their statistical knowledge, I remain cautious and open to identifying any potential biases that may have influenced my research. Nonetheless, the result is genuinely exciting for me as an aspiring quantitative trader / researcher. While my heart wants to fully embrace these findings, I must moderate my enthusiasm with an analytical perspective.

The journey of creating this project - encompassing the study of Elliott Wave Theory, statistical inference, hypothesis testing, and programming - has brought me immense satisfaction and joy. I would like to express my gratitude to Mr. Elliott.

<a name="detecting_waves">1.</a>

In detecting waves 1 and 2, two local lows, in hindsight, suffice the condition. However, because a local low from the way it was set up requires subsequent higher points, this approach inherently involves a look-ahead bias since we cannot rely on future information to make current decisions. For example, when Wave 2 is in progress, it is uncertain whether the price will decline further or reverse. Despite this limitation, the method remains valuable for hypothesis testing as it provides an opportunity to validate or refute specific market behavior ($H_{A}$). Establishing clear entry and exit strategies based on historical and currently available data is necessary. One example might be an entry strategy in a lower time frame after a new local minimum is found within the Fibonacci retracement range of the first wave to avoid look-ahead bias.

In hypothesis testing, the assumptions I make should be aligned with the specific patterns or behaviors I am investigating. If my goal is to determine whether the second motive wave's high value (wave 3) exceeds the first motive wave's high value (wave 1), then my assumptions should reflect the conditions under which I believe this pattern occurs. For example, comparing two uptrend motive waves in the context of Elliott Wave Theory requires three increasing local low values. One interesting point I would like to share is that I feel I gained more knowledge through the statistical research process than when I was reading books about Elliott Wave Theory. Research often helps confirm whether we truly understand what we think we know.

## References

Prechter, R., & Frost, A. J. (2017). _Elliott Wave Principle: Key to Market Behavior_ (11th ed.). New Classics Library.

Neely, G. (1990). _Mastering Elliott Wave_ (2.0) [E-book]. Windsor Books. (Original work published 1988)
