# SurvLIMEpy

This is a very initial implementation of [Functional relevance based on the continuous Shapley value](https://arxiv.org/abs/2411.18575). There is still a lot of work to do.

## Install
**SurvLIMEpy** can be installed from PyPI:

```
pip install ShapleyFDA
```

## How to use
```python
import numpy as np
from shapley_fda import ShapleyFda
from matplotlib import pyplot as plt

# Generate and visualise the data
step = 0.01
sample_size = 500
intercept = 0
slope = 1
abscissa_points = np.arange(0, 1 + step, step)
total_abscissa_points = abscissa_points.shape[0]
if total_abscissa_points % 2 == 0:
    middle_point = total_abscissa_points/2
else:
    middle_point = (total_abscissa_points + 1)//2
# Generate normal observations
np.random.seed(1234)
data = np.random.normal(
    size=(sample_size, total_abscissa_points),
    loc=0,
    scale=1
)
data = np.divide(data, np.sqrt(total_abscissa_points))
brownian = np.cumsum(data, axis=1)
trend = np.reshape(
    np.add(intercept, np.multiply(slope, abscissa_points)),
    newshape=(1, -1)
)
col_vector_ones_sample_size = np.ones(shape=(sample_size, 1))
trend_matrix = np.matmul(
    col_vector_ones_sample_size,
    trend
)
brownian_trend = np.add(brownian, trend_matrix)
_ = plt.plot(abscissa_points, brownian_trend.T)

def pred_fn(X):
    result = np.abs(X[:, middle_point])
    return result
target = pred_fn(brownian_trend)

# Use ShapleyFDA library
num_intervals = 10
num_permutations = 100
shapley_fda = ShapleyFda(
    X=brownian_trend,
    abscissa_points=abscissa_points,
    target=target,
    domain_range=(0, 1),
    verbose=False,
)
shapley_value = shapley_fda.compute_shapley_value(
    num_permutations=num_permutations,
    predict_fns=pred_fn,
    num_intervals=num_intervals,
    compute_mrmr_r2=False,
    compute_mrmr_distance_correlation=False,
)
```

## Citations
Please if you use this package, do not forget to cite us:
```
@misc{delicado2024functionalrelevancebasedcontinuous,
    title={Functional relevance based on the continuous Shapley value}, 
    author={Pedro Delicado and Cristian Pachón-García},
    year={2024},
    eprint={2411.18575},
    archivePrefix={arXiv},
    primaryClass={stat.ML},
    url={https://arxiv.org/abs/2411.18575}, 
}
```
