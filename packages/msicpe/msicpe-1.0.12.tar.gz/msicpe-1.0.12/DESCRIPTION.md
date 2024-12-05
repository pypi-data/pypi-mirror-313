
A toolbox used for practical sessions at [CPE Lyon](https://www.cpe.fr/).
Developped and maintained for teaching usage only!

# Installation

## In a Jupyter Notebook

```!pip install -U msicpe```

## In a local environment

```pip install -U msicpe```

# Usage example

The example below uses the kurtosis method available in the `tsa` subpackage of `msicpe`.
It requires `numpy.randn` to generate a gaussian distribution of N points.

```python
import numpy as np
from msicpe.tsa import kurtosis
N=10000

x=np.randn(1,N)
kurt=kurtosis(x)

print(kurt)
```