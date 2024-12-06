# popsynch (Quantifying Population Synchrony)

This Python module implements routines for computing a measure of population synchrony in compact metric spaces, as defined in [1]. 
Let $(M,d)$ be a compact metric space, and let $\pi \in \mathcal{P}(M)$ be a probability measure representing the distribution of a population over $M$. 
Then the synchrony of $\pi$ is defined to be
$$
F(\pi) = 1 - \frac{1}{\nu_{(M,d)}} \inf_{\alpha \in M} \left(\int_{M} d(x,\alpha)^2  d\pi(x) \right)^{1/2},
$$
where the synchrony normalization constant
$$
\nu_{(M,d)} = \sup_{\mu \in \mathcal{P}(M)} \inf_{\alpha \in M} \left(\int_{M} d(x,\alpha)^2  d\mu(x) \right)^{1/2}.
$$

This module currently implements routines to compute the synchrony normalization constant of any finite metric space, and synchrony
of distributions on finite metric spaces, empirical distributions on the circle, and empirical distributions on rectangular parallelepipeds and compact balls 
in Euclidean space.

## Installing popsynch

This module requires Python 3 (tested on Python>=3.12) and on [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/), which will be automatically installed with popsynch.

This module can be installed using pip and a local clone of the associated repository
```
$ git clone git@gitlab.com:biochron/popsynch.git
$ cd popsynch
$ pip install .
```

or through the Python Package Index (PyPI):
```
$ pip install popsynch
```

## Examples

Jupyter notebooks that show the functionality of the methods in this module can be found in `examples/`.

The example notebooks additionally require 
[Jupyter](https://jupyter.org/), [Pandas](https://pandas.pydata.org/), and [Matplotlib](https://matplotlib.org/), which can be installed with the command
```
$ pip install popsynch[notebooks]
```

## Author

* Francis C. Motta (fmotta@fau.edu)

## Citations

[1] Motta, F.C., McGoff, K., Cummins, B., Haase, S.B.,  (2024). Generalized Measures of Population Synchrony. (https://arxiv.org/abs/2406.15987)