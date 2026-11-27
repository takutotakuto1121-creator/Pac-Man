import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification

x, y = make_classification(
    n_samples=1000,
    n_redundant=0,
    n_informative=2,
    n_clusters_per_class=1,
    n_classes=3,
    random_state=42
    )

plt.scatter(x[:, 0], x[:, 1], c = y, alpha = 0.5)
plt.show()

X, Y = make blobs(
    n_samples=100,

)


