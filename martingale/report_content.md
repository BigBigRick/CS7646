# Project 1: Martingale
**Author: ryang386**

---

## Introduction

This report presents the results of Monte Carlo simulations evaluating the Martingale betting strategy on an American roulette wheel. The strategy involves betting on black, starting with $1, and doubling the bet after each loss until a win occurs. Two experiments were conducted: one with unlimited bankroll and one with a $256 bankroll limit.

---

## Experiment 1: Unlimited Bankroll

### Figure 1: 10 Episodes
[Insert figure1.png]
*Figure 1: 10 Episodes of Martingale Strategy (Unlimited Bankroll)*

### Figure 2: Mean with Standard Deviation
[Insert figure2.png]
*Figure 2: Mean Winnings with Standard Deviation (1000 Episodes)*

### Figure 3: Median with Standard Deviation
[Insert figure3.png]
*Figure 3: Median Winnings with Standard Deviation (1000 Episodes)*

---

### Question 1: Probability of Winning $80

Based on the simulation results, the estimated probability of winning exactly $80 within 1000 sequential bets is **1.0 (100%)**.

Out of 1000 episodes simulated, all 1000 episodes reached the $80 target:

P(win $80) = 1000/1000 = 1.0

This high success rate occurs because with unlimited bankroll, the gambler can always double the bet after a loss, eventually recovering all losses plus gaining $1 profit per winning cycle.

---

### Question 2: Expected Value of Winnings

The estimated expected value of winnings after 1000 sequential bets is **$80.00**.

This is calculated as the mean of the final winnings across all 1000 episodes:

E[winnings] = (1/n) × Σ Xi = $80.00

Since every episode reaches the $80 target and stops betting (filling forward with $80), the expected value equals the target amount.

---

### Question 3: Standard Deviation Lines Analysis

**Do the standard deviation lines stabilize?** Yes, both the upper (mean + std) and lower (mean - std) lines stabilize at $80 as the number of spins increases.

**Do the standard deviation lines converge?** Yes, the lines converge to the same value of $80.

**Explanation:** As more spins occur, more episodes reach the $80 target and stop betting. Once an episode reaches $80, its value remains constant at $80 for all subsequent spins. Eventually, all episodes have reached $80, so the mean becomes $80 and the standard deviation becomes 0. This causes both the upper and lower standard deviation lines to converge to $80.

---

## Experiment 2: Limited Bankroll ($256)

### Figure 4: Mean with Standard Deviation
[Insert figure4.png]
*Figure 4: Mean Winnings with Standard Deviation (Limited Bankroll)*

### Figure 5: Median with Standard Deviation
[Insert figure5.png]
*Figure 5: Median Winnings with Standard Deviation (Limited Bankroll)*

---

### Question 4: Probability of Winning $80

Based on the simulation results, the estimated probability of winning exactly $80 within 1000 sequential bets with a $256 bankroll is **0.651 (65.1%)**.

Out of 1000 episodes, 651 episodes successfully reached the $80 target:

P(win $80) = 651/1000 = 0.651

The probability is significantly lower than Experiment 1 because the limited bankroll prevents the gambler from continuing to double bets after a losing streak. When the gambler loses $256, they are bankrupt and cannot recover.

---

### Question 5: Expected Value of Winnings

The estimated expected value of winnings after 1000 sequential bets is **-$36.62**.

This negative expected value is calculated as:

E[winnings] = (1/n) × Σ Xi = -$36.62

The negative expected value occurs because while 65.1% of episodes win $80, the remaining 34.9% lose $256. The expected value can be approximated as:

E[winnings] ≈ 0.651 × $80 + 0.349 × (-$256) = $52.08 - $89.34 = -$37.26

This approximation is close to the simulated result, confirming that the large losses from bankruptcy outweigh the gains from successful episodes.

---

### Question 6: Standard Deviation Lines Analysis

**Do the standard deviation lines stabilize?** Yes, both lines stabilize after sufficient spins. The upper line stabilizes near $80 and the lower line stabilizes near -$256.

**Do the standard deviation lines converge?** No, the lines do not converge. They remain separated by a significant distance (approximately $320).

**Explanation:** Unlike Experiment 1, the outcomes in Experiment 2 are bimodal: episodes either reach $80 (success) or -$256 (bankruptcy). This creates two distinct groups of final outcomes, resulting in high variance. The standard deviation remains large because of the spread between winning ($80) and losing (-$256) outcomes. The lines stabilize because all episodes eventually terminate at one of these two values, but they do not converge because the outcomes remain distributed between these two extremes.

---

## Question 7: Benefits of Expected Values

Using expected values instead of single random episode results offers several important benefits:

1. **Reduces noise and randomness:** A single episode outcome is heavily influenced by random chance. Expected values average out this randomness across many trials, providing a more reliable estimate of typical performance.

2. **Reveals true underlying probabilities:** Individual episodes can be misleading. For example, one lucky episode might win $80 quickly, while another might go bankrupt. The expected value shows what happens "on average" over many repetitions.

3. **Enables statistical analysis:** With expected values and standard deviations, we can quantify uncertainty and make probabilistic statements about outcomes. This is not possible with a single trial.

4. **Better decision-making:** For gambling and trading strategies, expected value tells us whether a strategy is profitable in the long run. A positive expected value suggests potential profitability, while a negative expected value (like -$36.62 in Experiment 2) indicates expected losses.

5. **Reproducibility:** Expected values computed from large samples are more reproducible and stable compared to individual random outcomes.

In Experiment 2, if we only ran one episode and happened to win $80, we might incorrectly conclude that the strategy is profitable. However, the expected value of -$36.62 reveals that repeating this strategy will lead to losses over time.

---

## Conclusion

The Martingale strategy appears to guarantee success with unlimited bankroll (100% win rate, $80 expected value). However, this is unrealistic. With a realistic $256 bankroll limit, the strategy has only a 65.1% success rate and a negative expected value of -$36.62. This demonstrates that the Martingale strategy is not a profitable long-term gambling approach when bankroll constraints are considered.
