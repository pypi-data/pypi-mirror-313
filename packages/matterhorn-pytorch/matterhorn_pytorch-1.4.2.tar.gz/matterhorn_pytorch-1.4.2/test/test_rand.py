import os, sys
import torch
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt


if __name__ == "__main__":
    n = torch.normal(0.0, 1.0, (128, 16, 16, 16))
    plt.hist(n.mean(0).flatten(), bins = 100)
    plt.show()