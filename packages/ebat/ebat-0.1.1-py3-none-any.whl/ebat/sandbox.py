import os

import torchvision

if __name__ == "__main__":
    data = torchvision.datasets.MNIST("data/", download=True)
    print(data)
