"""
Martingale Simulation
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def author():
    return "ryang386"

def study_group():
    return 0

def gtid():
    return 904206790

def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result

def run_episode(win_prob, bankroll=None):
    winnings = np.zeros(1001)
    episode_winnings = 0
    spin = 0
    
    while spin < 1000 and episode_winnings < 80:
        if bankroll is not None and episode_winnings <= -bankroll:
            winnings[spin+1:] = -bankroll
            return winnings
            
        won = False
        bet = 1
        
        while not won and spin < 1000:
            if bankroll is not None:
                available = bankroll + episode_winnings
                if bet > available:
                    bet = available
                if bet <= 0:
                    winnings[spin+1:] = episode_winnings
                    return winnings
            
            won = get_spin_result(win_prob)
            spin += 1
            
            if won:
                episode_winnings += bet
            else:
                episode_winnings -= bet
                bet *= 2
            
            winnings[spin] = episode_winnings
            
            if episode_winnings >= 80:
                winnings[spin+1:] = episode_winnings
                return winnings
            
            if bankroll is not None and episode_winnings <= -bankroll:
                winnings[spin+1:] = -bankroll
                return winnings
    
    return winnings

def run_simulation(num_episodes, bankroll=None):
    win_prob = 18/38
    results = np.zeros((num_episodes, 1001))
    
    for i in range(num_episodes):
        results[i] = run_episode(win_prob, bankroll)
    
    return results

def test_code():
    np.random.seed(gtid())
    
    # Figure 1: 10 episodes
    plt.figure(figsize=(10, 8))
    for i in range(10):
        data = run_episode(18/38)
        plt.plot(range(len(data)), data, label=f'Episode {i+1}')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 1: 10 Episodes of Martingale Strategy (Unlimited Bankroll)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure1.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Run 1000 episodes for exp1
    data = run_simulation(1000)
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    median = np.median(data, axis=0)
    x = range(len(mean))
    
    # Figure 2: Mean +/- std
    plt.figure(figsize=(10, 8))
    plt.plot(x, mean, 'b-', label='Mean', linewidth=1.5)
    plt.plot(x, mean + std, 'g--', label='Mean + Std', linewidth=1)
    plt.plot(x, mean - std, 'r--', label='Mean - Std', linewidth=1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 2: Mean Winnings (Unlimited Bankroll, 1000 Episodes)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure2.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Figure 3: Median +/- std
    plt.figure(figsize=(10, 8))
    plt.plot(x, median, 'b-', label='Median', linewidth=1.5)
    plt.plot(x, median + std, 'g--', label='Median + Std', linewidth=1)
    plt.plot(x, median - std, 'r--', label='Median - Std', linewidth=1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 3: Median Winnings (Unlimited Bankroll, 1000 Episodes)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure3.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Exp1 stats
    final = data[:, -1]
    print("Exp1:")
    print(f"  P(win $80) = {np.sum(final >= 80) / 1000}")
    print(f"  E[winnings] = {np.mean(final)}")
    
    # Run 1000 episodes for exp2 (limited bankroll)
    data2 = run_simulation(1000, bankroll=256)
    mean2 = np.mean(data2, axis=0)
    std2 = np.std(data2, axis=0)
    median2 = np.median(data2, axis=0)
    
    # Figure 4: Mean +/- std (limited)
    plt.figure(figsize=(10, 8))
    plt.plot(x, mean2, 'b-', label='Mean', linewidth=1.5)
    plt.plot(x, mean2 + std2, 'g--', label='Mean + Std', linewidth=1)
    plt.plot(x, mean2 - std2, 'r--', label='Mean - Std', linewidth=1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 4: Mean Winnings (Limited Bankroll $256, 1000 Episodes)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure4.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Figure 5: Median +/- std (limited)
    plt.figure(figsize=(10, 8))
    plt.plot(x, median2, 'b-', label='Median', linewidth=1.5)
    plt.plot(x, median2 + std2, 'g--', label='Median + Std', linewidth=1)
    plt.plot(x, median2 - std2, 'r--', label='Median - Std', linewidth=1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Number')
    plt.ylabel('Winnings ($)')
    plt.title('Figure 5: Median Winnings (Limited Bankroll $256, 1000 Episodes)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure5.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Exp2 stats
    final2 = data2[:, -1]
    print("Exp2:")
    print(f"  P(win $80) = {np.sum(final2 >= 80) / 1000}")
    print(f"  E[winnings] = {np.mean(final2)}")

if __name__ == "__main__":
    test_code()
