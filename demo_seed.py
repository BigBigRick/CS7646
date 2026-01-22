"""
演示随机种子的作用
"""
import numpy as np

print("="*80)
print("Demo 1: Without random seed (different results each time)")
print("="*80)
for i in range(3):
    a = np.random.randint(0, 10, size=(3, 3))
    print(f"Run {i+1}:")
    print(a)
    print()

print("="*80)
print("Demo 2: With same random seed (same results each time)")
print("="*80)
for i in range(3):
    np.random.seed(693)  # Set same seed each time
    a = np.random.randint(0, 10, size=(3, 3))
    print(f"Run {i+1} (seed=693):")
    print(a)
    print()

print("="*80)
print("Demo 3: With different random seeds (different results)")
print("="*80)
for seed in [100, 200, 300]:
    np.random.seed(seed)
    a = np.random.randint(0, 10, size=(3, 3))
    print(f"Seed={seed}:")
    print(a)
    print()

print("="*80)
print("Demo 4: Actual effect in Script 4")
print("="*80)
np.random.seed(693)
a = np.random.randint(0, 10, size=(5, 4))
print("Array generated with seed 693:")
print(a)
print("\nThis array will be the same every time you run it!")
