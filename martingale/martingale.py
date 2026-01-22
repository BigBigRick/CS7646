"""
Project 1: Martingale
CS7646 - Machine Learning for Trading
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent displaying plots
import matplotlib.pyplot as plt
import random

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "xyang"  # Replace with your GT username

def study_group():
    """
    :return: The study group number
    :rtype: int
    """
    return 0  # Replace with your study group number

def get_spin_result(win_prob):
    """
    Given a win probability between 0 and 1, the function returns whether the 
    spin results in a win.
    
    :param win_prob: The probability of winning
    :type win_prob: float
    :return: The result of the spin.
    :rtype: bool
    """
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result

def run_episode_unlimited(win_prob, max_spins=1000, target_winnings=80):
    """
    Run a single episode with unlimited bankroll.
    
    :param win_prob: Probability of winning on black (18/38 for American roulette)
    :type win_prob: float
    :param max_spins: Maximum number of spins (default 1000)
    :type max_spins: int
    :param target_winnings: Target winnings to stop at (default $80)
    :type target_winnings: float
    :return: Array of winnings after each spin (including initial 0)
    :rtype: numpy.ndarray
    """
    winnings = np.zeros(max_spins + 1)  # +1 for initial state (winnings[0] = 0)
    episode_winnings = 0
    spin_count = 0
    
    while spin_count < max_spins and episode_winnings < target_winnings:
        won = False
        bet_amount = 1
        
        while not won and spin_count < max_spins:
            # Place bet and spin
            won = get_spin_result(win_prob)
            spin_count += 1
            
            if won:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2
            
            # Record winnings after this spin
            winnings[spin_count] = episode_winnings
            
            # Check if target reached
            if episode_winnings >= target_winnings:
                # Fill forward with target value
                if spin_count < max_spins:
                    winnings[spin_count+1:] = episode_winnings
                break
    
    return winnings

def run_episode_limited(win_prob, max_spins=1000, target_winnings=80, bankroll=256):
    """
    Run a single episode with limited bankroll.
    
    :param win_prob: Probability of winning on black (18/38 for American roulette)
    :type win_prob: float
    :param max_spins: Maximum number of spins (default 1000)
    :type max_spins: int
    :param target_winnings: Target winnings to stop at (default $80)
    :type target_winnings: float
    :param bankroll: Maximum bankroll (default $256)
    :type bankroll: float
    :return: Array of winnings after each spin (including initial 0)
    :rtype: numpy.ndarray
    """
    winnings = np.zeros(max_spins + 1)  # +1 for initial state (winnings[0] = 0)
    episode_winnings = 0
    spin_count = 0
    
    while spin_count < max_spins and episode_winnings < target_winnings:
        # Check if bankrupt
        if episode_winnings <= -bankroll:
            # Fill forward with -256
            winnings[spin_count+1:] = -bankroll
            break
            
        won = False
        bet_amount = 1
        
        while not won and spin_count < max_spins:
            # Calculate available money
            available = bankroll + episode_winnings  # bankroll is positive, winnings can be negative
            
            # Can't bet more than available
            if bet_amount > available:
                bet_amount = available
            
            # Check if we can't bet anything
            if bet_amount <= 0:
                # Fill forward with current winnings
                winnings[spin_count+1:] = episode_winnings
                break
            
            # Place bet and spin
            won = get_spin_result(win_prob)
            spin_count += 1
            
            if won:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2
            
            # Record winnings after this spin
            winnings[spin_count] = episode_winnings
            
            # Check if target reached
            if episode_winnings >= target_winnings:
                # Fill forward with target value
                if spin_count < max_spins:
                    winnings[spin_count+1:] = episode_winnings
                break
            
            # Check if bankrupt
            if episode_winnings <= -bankroll:
                # Fill forward with -256
                if spin_count < max_spins:
                    winnings[spin_count+1:] = -bankroll
                break
    
    return winnings

def experiment1_figure1(num_episodes=10, max_spins=1000):
    """
    Figure 1: Plot 10 episodes on one chart.
    """
    win_prob = 18.0 / 38.0  # American roulette: 18 black, 18 red, 2 green (0, 00)
    
    plt.figure(figsize=(10, 6))
    
    for episode in range(num_episodes):
        winnings = run_episode_unlimited(win_prob, max_spins)
        spins = np.arange(len(winnings))
        plt.plot(spins, winnings, alpha=0.7, linewidth=0.8)
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 1: 10 Episodes of Martingale Strategy (Unlimited Bankroll)')
    plt.legend([f'Episode {i+1}' for i in range(num_episodes)], loc='best', fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.savefig('figure1.png', dpi=150, bbox_inches='tight')
    plt.close()

def experiment1_figure2(num_episodes=1000, max_spins=1000):
    """
    Figure 2: Mean and standard deviation lines for 1000 episodes.
    """
    win_prob = 18.0 / 38.0
    max_length = max_spins + 1
    
    # Store all episodes
    all_winnings = []
    
    for episode in range(num_episodes):
        winnings = run_episode_unlimited(win_prob, max_spins)
        # Pad to max_length if needed
        if len(winnings) < max_length:
            winnings = np.pad(winnings, (0, max_length - len(winnings)), 'constant', 
                            constant_values=winnings[-1])
        all_winnings.append(winnings)
    
    all_winnings = np.array(all_winnings)
    
    # Calculate statistics
    mean_winnings = np.mean(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0, ddof=0)  # Population std dev
    
    spins = np.arange(max_length)
    
    plt.figure(figsize=(10, 6))
    plt.plot(spins, mean_winnings, 'b-', label='Mean', linewidth=2)
    plt.plot(spins, mean_winnings + std_winnings, 'r--', label='Mean + Std Dev', linewidth=1.5)
    plt.plot(spins, mean_winnings - std_winnings, 'r--', label='Mean - Std Dev', linewidth=1.5)
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 2: Mean Winnings with Standard Deviation (Unlimited Bankroll, 1000 Episodes)')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.savefig('figure2.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return all_winnings

def experiment1_figure3(all_winnings):
    """
    Figure 3: Median and standard deviation lines for 1000 episodes.
    """
    # Calculate statistics
    median_winnings = np.median(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0, ddof=0)  # Population std dev
    
    max_length = all_winnings.shape[1]
    spins = np.arange(max_length)
    
    plt.figure(figsize=(10, 6))
    plt.plot(spins, median_winnings, 'b-', label='Median', linewidth=2)
    plt.plot(spins, median_winnings + std_winnings, 'r--', label='Median + Std Dev', linewidth=1.5)
    plt.plot(spins, median_winnings - std_winnings, 'r--', label='Median - Std Dev', linewidth=1.5)
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 3: Median Winnings with Standard Deviation (Unlimited Bankroll, 1000 Episodes)')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.savefig('figure3.png', dpi=150, bbox_inches='tight')
    plt.close()

def experiment2_figure4(num_episodes=1000, max_spins=1000, bankroll=256):
    """
    Figure 4: Mean and standard deviation lines for 1000 episodes with limited bankroll.
    """
    win_prob = 18.0 / 38.0
    max_length = max_spins + 1
    
    # Store all episodes
    all_winnings = []
    
    for episode in range(num_episodes):
        winnings = run_episode_limited(win_prob, max_spins, bankroll=bankroll)
        # Pad to max_length if needed
        if len(winnings) < max_length:
            winnings = np.pad(winnings, (0, max_length - len(winnings)), 'constant', 
                            constant_values=winnings[-1])
        all_winnings.append(winnings)
    
    all_winnings = np.array(all_winnings)
    
    # Calculate statistics
    mean_winnings = np.mean(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0, ddof=0)  # Population std dev
    
    spins = np.arange(max_length)
    
    plt.figure(figsize=(10, 6))
    plt.plot(spins, mean_winnings, 'b-', label='Mean', linewidth=2)
    plt.plot(spins, mean_winnings + std_winnings, 'r--', label='Mean + Std Dev', linewidth=1.5)
    plt.plot(spins, mean_winnings - std_winnings, 'r--', label='Mean - Std Dev', linewidth=1.5)
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 4: Mean Winnings with Standard Deviation (Limited Bankroll $256, 1000 Episodes)')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.savefig('figure4.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return all_winnings

def experiment2_figure5(all_winnings):
    """
    Figure 5: Median and standard deviation lines for 1000 episodes with limited bankroll.
    """
    # Calculate statistics
    median_winnings = np.median(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0, ddof=0)  # Population std dev
    
    max_length = all_winnings.shape[1]
    spins = np.arange(max_length)
    
    plt.figure(figsize=(10, 6))
    plt.plot(spins, median_winnings, 'b-', label='Median', linewidth=2)
    plt.plot(spins, median_winnings + std_winnings, 'r--', label='Median + Std Dev', linewidth=1.5)
    plt.plot(spins, median_winnings - std_winnings, 'r--', label='Median - Std Dev', linewidth=1.5)
    
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 5: Median Winnings with Standard Deviation (Limited Bankroll $256, 1000 Episodes)')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.savefig('figure5.png', dpi=150, bbox_inches='tight')
    plt.close()

def calculate_statistics(all_winnings, experiment_num):
    """
    Calculate and optionally write statistics to file.
    """
    # Calculate final statistics after 1000 spins
    final_winnings = all_winnings[:, -1]
    
    # Probability of winning exactly $80
    exactly_80 = np.sum(final_winnings == 80)
    prob_exactly_80 = exactly_80 / len(final_winnings)
    
    # Expected value (mean)
    expected_value = np.mean(final_winnings)
    
    # Standard deviation
    std_dev = np.std(final_winnings, ddof=0)
    
    # Calculate statistics for each spin to analyze convergence
    mean_winnings = np.mean(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0, ddof=0)
    upper_std = mean_winnings + std_winnings
    lower_std = mean_winnings - std_winnings
    
    # Analyze convergence and stabilization
    # Check if std dev lines stabilize (variance of last 100 spins is small)
    if len(upper_std) >= 100:
        last_100_upper = upper_std[-100:]
        last_100_lower = lower_std[-100:]
        upper_stabilized = np.std(last_100_upper, ddof=0) < 1.0  # Threshold for stabilization
        lower_stabilized = np.std(last_100_lower, ddof=0) < 1.0
        upper_max = np.max(upper_std)
        lower_min = np.min(lower_std)
    else:
        upper_stabilized = False
        lower_stabilized = False
        upper_max = np.max(upper_std)
        lower_min = np.min(lower_std)
    
    # Check convergence (distance between upper and lower lines)
    std_distance = upper_std - lower_std
    if len(std_distance) >= 100:
        last_100_distance = std_distance[-100:]
        distance_stable = np.std(last_100_distance, ddof=0) < 1.0
        final_distance = std_distance[-1]
    else:
        distance_stable = False
        final_distance = std_distance[-1] if len(std_distance) > 0 else 0
    
    stats = {
        'experiment': experiment_num,
        'prob_exactly_80': prob_exactly_80,
        'expected_value': expected_value,
        'std_dev': std_dev,
        'exactly_80_count': exactly_80,
        'total_episodes': len(final_winnings),
        'upper_std_max': upper_max,
        'lower_std_min': lower_min,
        'upper_stabilized': upper_stabilized,
        'lower_stabilized': lower_stabilized,
        'std_distance_final': final_distance,
        'std_distance_stable': distance_stable,
        'mean_winnings': mean_winnings,
        'std_winnings': std_winnings,
        'upper_std': upper_std,
        'lower_std': lower_std
    }
    
    return stats

def test_code():
    """
    Test the martingale strategy implementation.
    """
    print("Testing martingale strategy...")
    
    # Test get_spin_result
    win_prob = 18.0 / 38.0
    wins = sum([get_spin_result(win_prob) for _ in range(10000)])
    print(f"Win probability test: {wins/10000:.4f} (expected ~{win_prob:.4f})")
    
    # Test single episode
    winnings = run_episode_unlimited(win_prob, max_spins=100)
    print(f"Single episode test - Final winnings: ${winnings[-1]}")
    print(f"Single episode test - Reached target: {winnings[-1] >= 80}")

if __name__ == "__main__":
    # Set random seed using GT ID (replace with your actual GT ID number)
    # For example, if GT ID is 123456789, use: np.random.seed(123456789)
    # Note: You need to replace this with your actual GT ID
    GT_ID = 123456789  # REPLACE WITH YOUR ACTUAL GT ID
    np.random.seed(GT_ID)
    random.seed(GT_ID)
    
    print("Running Experiment 1...")
    # Experiment 1: Unlimited bankroll
    experiment1_figure1(num_episodes=10)
    print("Figure 1 created.")
    
    all_winnings_exp1 = experiment1_figure2(num_episodes=1000)
    print("Figure 2 created.")
    
    experiment1_figure3(all_winnings_exp1)
    print("Figure 3 created.")
    
    # Calculate statistics for Experiment 1
    stats_exp1 = calculate_statistics(all_winnings_exp1, 1)
    print(f"\nExperiment 1 Statistics:")
    print(f"Probability of winning exactly $80: {stats_exp1['prob_exactly_80']:.4f} ({stats_exp1['exactly_80_count']}/{stats_exp1['total_episodes']})")
    print(f"Expected value after 1000 spins: ${stats_exp1['expected_value']:.2f}")
    print(f"Standard deviation: ${stats_exp1['std_dev']:.2f}")
    print(f"Upper std dev max value: ${stats_exp1['upper_std_max']:.2f}")
    print(f"Lower std dev min value: ${stats_exp1['lower_std_min']:.2f}")
    print(f"Upper std dev stabilized: {stats_exp1['upper_stabilized']}")
    print(f"Lower std dev stabilized: {stats_exp1['lower_stabilized']}")
    print(f"Std dev lines converge: {stats_exp1['std_distance_stable']}")
    print(f"Final distance between std dev lines: ${stats_exp1['std_distance_final']:.2f}")
    
    print("\nRunning Experiment 2...")
    # Experiment 2: Limited bankroll
    all_winnings_exp2 = experiment2_figure4(num_episodes=1000, bankroll=256)
    print("Figure 4 created.")
    
    experiment2_figure5(all_winnings_exp2)
    print("Figure 5 created.")
    
    # Calculate statistics for Experiment 2
    stats_exp2 = calculate_statistics(all_winnings_exp2, 2)
    print(f"\nExperiment 2 Statistics:")
    print(f"Probability of winning exactly $80: {stats_exp2['prob_exactly_80']:.4f} ({stats_exp2['exactly_80_count']}/{stats_exp2['total_episodes']})")
    print(f"Expected value after 1000 spins: ${stats_exp2['expected_value']:.2f}")
    print(f"Standard deviation: ${stats_exp2['std_dev']:.2f}")
    print(f"Upper std dev max value: ${stats_exp2['upper_std_max']:.2f}")
    print(f"Lower std dev min value: ${stats_exp2['lower_std_min']:.2f}")
    print(f"Upper std dev stabilized: {stats_exp2['upper_stabilized']}")
    print(f"Lower std dev stabilized: {stats_exp2['lower_stabilized']}")
    print(f"Std dev lines converge: {stats_exp2['std_distance_stable']}")
    print(f"Final distance between std dev lines: ${stats_exp2['std_distance_final']:.2f}")
    
    # Write detailed statistics to file for report analysis
    with open('p1_results.txt', 'w') as f:
        f.write("="*80 + "\n")
        f.write("PROJECT 1: MARTINGALE - EXPERIMENTAL RESULTS\n")
        f.write("="*80 + "\n\n")
        
        f.write("EXPERIMENT 1: UNLIMITED BANKROLL\n")
        f.write("-"*80 + "\n")
        f.write(f"Question 1: Probability of winning exactly $80\n")
        f.write(f"  Answer: {stats_exp1['prob_exactly_80']:.6f} ({stats_exp1['exactly_80_count']} out of {stats_exp1['total_episodes']} episodes)\n\n")
        
        f.write(f"Question 2: Expected value after 1000 spins\n")
        f.write(f"  Answer: ${stats_exp1['expected_value']:.2f}\n\n")
        
        f.write(f"Question Set 3: Standard deviation lines analysis\n")
        f.write(f"  Upper std dev (mean + stdev) max value: ${stats_exp1['upper_std_max']:.2f}\n")
        f.write(f"  Lower std dev (mean - stdev) min value: ${stats_exp1['lower_std_min']:.2f}\n")
        f.write(f"  Upper line stabilized: {stats_exp1['upper_stabilized']}\n")
        f.write(f"  Lower line stabilized: {stats_exp1['lower_stabilized']}\n")
        f.write(f"  Lines converge (distance stable): {stats_exp1['std_distance_stable']}\n")
        f.write(f"  Final distance between lines: ${stats_exp1['std_distance_final']:.2f}\n\n")
        
        f.write("\n" + "="*80 + "\n\n")
        
        f.write("EXPERIMENT 2: LIMITED BANKROLL ($256)\n")
        f.write("-"*80 + "\n")
        f.write(f"Question 4: Probability of winning exactly $80\n")
        f.write(f"  Answer: {stats_exp2['prob_exactly_80']:.6f} ({stats_exp2['exactly_80_count']} out of {stats_exp2['total_episodes']} episodes)\n\n")
        
        f.write(f"Question 5: Expected value after 1000 spins\n")
        f.write(f"  Answer: ${stats_exp2['expected_value']:.2f}\n\n")
        
        f.write(f"Question Set 6: Standard deviation lines analysis\n")
        f.write(f"  Upper std dev (mean + stdev) max value: ${stats_exp2['upper_std_max']:.2f}\n")
        f.write(f"  Lower std dev (mean - stdev) min value: ${stats_exp2['lower_std_min']:.2f}\n")
        f.write(f"  Upper line stabilized: {stats_exp2['upper_stabilized']}\n")
        f.write(f"  Lower line stabilized: {stats_exp2['lower_stabilized']}\n")
        f.write(f"  Lines converge (distance stable): {stats_exp2['std_distance_stable']}\n")
        f.write(f"  Final distance between lines: ${stats_exp2['std_distance_final']:.2f}\n\n")
        
        f.write("\n" + "="*80 + "\n\n")
        
        f.write("ADDITIONAL STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Experiment 1 - Standard deviation: ${stats_exp1['std_dev']:.2f}\n")
        f.write(f"Experiment 2 - Standard deviation: ${stats_exp2['std_dev']:.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("NOTE: Question 7 asks about the benefits of using expected values.\n")
        f.write("This is a conceptual question that should be answered based on\n")
        f.write("your understanding of statistics and the experimental results above.\n")
        f.write("="*80 + "\n")
    
    print("\nAll figures saved to current directory.")
    print("Detailed statistics written to p1_results.txt")
    print("Done!")
