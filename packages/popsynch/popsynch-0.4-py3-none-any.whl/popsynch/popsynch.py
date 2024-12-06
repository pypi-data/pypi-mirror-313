import math
import numpy as np
import scipy as sp
from scipy.optimize import basinhopping


def discrete_uniform_circ_state_dm(p):
    """
    Generates the distance matrix of a finite uniform discretization of the circle of circumference 1 into p
    equal-length arcs (states). The distance between two states 0 <= i,j < p is given by
            
            d(i,j) = min(|i-j|, p-|i-j|) / p.
            
    The normalization by p ensures adjacent states have distance 1/p, and approximates the circle with circumference 1.
    
    Parameters
    ----------
    p : int
        The number of states in the cyclic state space
    
    Returns
    -------
    dm : (p,p)-ndarray
        The metric matrix
    """
    I, J = np.indices((p,p))
    T = np.abs(I-J)
    dm = np.minimum(T, p-T)/p
    
    return dm


def discrete_general_circ_state_dm(a):
    """
    Generates the distance matrix of a finite discretization of the circle of circumference 1 into p arcs (states)
    which may not be of equal length. Associate to each of p states an arc [a_i, a_{i+1}) in the circle, [0,1),
    with a_0=0, a_{p+1}=1. The distance between state i and state j is

        d(i,j) = min( |a_i-a_j + a_{i+1}-a_{j+1}|, 2-|a_i-a_j + a_{i+1} - a_{j+1}| )/2.

    Parameters
    ----------
    a : np.array
        p+1 distinct values in [0,1) including 0 and 1

    Returns
    -------
    dm : (p,p)-ndarray
        The metric matrix
    """
    a = np.sort(a)
    p = len(a)-1
    
    dm = np.zeros((p,p), dtype=np.float64)
    for i in range(p):
        for j in range(p):
            dm[i,j] = np.min( (np.abs(a[i]-a[j] + a[i+1]-a[j+1]), 2 - np.abs(a[i]-a[j] + a[i+1]-a[j+1])) ) / 2
    
    return dm


def circ_wassp_to_delta(x, a, p=2):
    """
    Computes the exact squared Wasserstein-p optimal transport distance between an empirical distribution,

        sum_i=1^n delta_{x[i]}/n,

    supported at n points in S^1 ~ [0,1), and a delta distribution, delta_a, supported at a in [0,1). [0,1) is treated
    as the circle of circumference 1 by taking the distance between a and b to be d(a,b) = min(|a-b|, 1-|a-b|).
    
    Parameters
    ----------
    x : np.array
        n floats in [0,1) defining the support of the empirical distribution
    a : float
        The location of the target delta distribution in [0,1)
    p : int
        integer >= 1 specifying the power of the Wasserstein metric
        
    Returns
    -------
    d : the Wasserstein-p optimal transport distance
    """
    return np.sum(np.min([np.abs(x-a), 1-np.abs(x-a)], axis=0) ** p)/len(x)
    
    
def circ_synchrony(x, method='exact', bhoptimizer_kwargs=None, return_evals=False):
    """
    Computes the exact or approximate measure of synchrony of a population of n point masses, x = {x[i]}_{i=1}^n,
    in the circle, S^1 ~ [0,1). Synchrony is defined to be 1 minus the square root of the generalized variance of the
    empirical distribution
    
    sum_i=1^n delta_{x[i]}/n
    
    normalized by the square root of the maximum generalized variance of any distribution on the circle.
    The maximal generalized variance is achieved by the uniform distribution, and is equal to 1/12 for the circle with
    circumference 1.
    
    The generalized variance is equivalent to the minimum squared Wasserstein-2 distance between the
    empirical distribution and any fixed delta distribution in [0,1), which is treated as the circle of circumference 1
    by taking the distance between two phases, a and b, to be min(|a-b|, 1-|a-b|).
    
    Parameters
    ----------
    x : np.array
        n floats in [0,1) defining the support of the empirical distribution
    method : string
        'exact' efficiently computes an exact minimizing delta distribution and resulting measure of synchrony
        'optimize' estimates the global minimizing distribution using the global basinhopping optimization method
    bhoptimizer_kwargs : dict or None
        optional dictionary of arguments to pass to the basinhopping optimization method. Only used if method='optimize'
    return_evals : bool
        specifies if the number of evaluations of the Wasserstein-2 distance should be returned

    Returns
    -------
    synchrony : float
        the normalized measure of synchrony
    barycenter : float
        the location of a delta distribution which achieves the minimal Wasserstein-2 optimal transport distance
    num_eval (optional) : int
        the number of evaluations of the Wasserstein-2 distance of x to a fixed delta
    """
    # determine number of points in empirical distribution
    n = len(x)

    if method=='exact':
        # compute antipodal points of supports of empirical distribution
        antips = np.unique((x + 1/2) %1)
        
        # calculate possible locations of minimizing distribution by searching over each antipodal-point interval
        possible_mins = np.zeros(len(antips)+1)
        for j in range(len(antips)+1):
            if j == 0:
                min_z = 0
                max_z = antips[j]
            elif j==len(antips):
                min_z = antips[j-1] 
                max_z = 1
            else:
                min_z = antips[j-1]
                max_z = antips[j]
    
            x_total = x.sum()
            x_total = x_total + ((np.abs(x-(min_z+max_z)/2) >= .5) & (x <= min_z)).sum()
            x_total = x_total - ((np.abs(x-(min_z+max_z)/2) >= .5) & (x > min_z)).sum()
    
            possible_mins[j] = x_total/n % 1
    
            # check if solution is within the current antipodal-point interval, ignore if not
            if possible_mins[j] > max_z or possible_mins[j] < min_z:
                possible_mins[j] = np.nan
    
        possible_mins = np.concatenate((possible_mins, antips, np.array([0])))
        # compute distances at possible mins and store smallest
        global_min = np.inf
        for possible_min in possible_mins:
            if not np.isnan(possible_min):
                test_min = circ_wassp_to_delta(x, possible_min, p=2)
                if test_min < global_min:
                    x_min = possible_min
                    global_min = test_min
        
        # the total number of evaluations of the Wasserstein-2 distance of x to a fixed delta
        num_eval = np.nansum(~np.isnan(possible_mins))

    elif method=='optimize':
        def bounded_accept_test(**kwargs):
            """
            modifies the stepper in scipy.basinhopping to only accept proposals which are within [0,1)
            """
            x = kwargs["x_new"]
            return (x<1) and (x>=0)
        
        # setup default optimizer arguments
        if bhoptimizer_kwargs is None:
            bhoptimizer_kwargs = dict()
         
        if 'minimizer_kwargs' not in bhoptimizer_kwargs.keys():
            bhoptimizer_kwargs['minimizer_kwargs'] = {"method": "BFGS"}
            
        bhoptimizer_kwargs['accept_test'] = bounded_accept_test

        # run global basinhopping optimization
        func = lambda a: circ_wassp_to_delta(x, a, p=2)
        res = basinhopping(func, 1/2, **bhoptimizer_kwargs)
        global_min = res['fun']
        x_min = res['x'][0]
        num_eval = res['nfev']

    # The maximum generalized variance of any distribution on the circle S^1~[0,1); acheived by the uniform distribution
    normalization = 1/12

    # The maximum generalized variance of an empirical distribution of n, equally-weighted point masses on the circle S^1~[0,1);
    # acheived by uniformly-spaced deltas
    # normalization = (1 + 3*n + 2*(n ** 2) - 6*(1 + n)*np.ceil(n/2) + 6 np.ceil(n/2) ** 2)/(6*(n**2))

    if return_evals:
        return 1 - np.sqrt(global_min / normalization), x_min, num_eval
    else:
        return 1 - np.sqrt(global_min / normalization), x_min


def discrete_uniform_circ_synchrony(x):
    """
    Computes the exact measure of synchrony of a distribution on a finite cyclic state space with p states:
    M={0,1,...,p-1} and

            d(i,j) = min(|i-j|, p-|i-j|) / p,

    for 0 <= i,j < p.

    Synchrony is defined as 1 minus the square root of the generalized variance of the given distribution, which is
    equivalent to the minimal Wasserstein-2 distance between the given distribution and any of the p delta distributions
    on M. The generalized variance is normalized by the maximum variance of any distribution on M, which
    is achieved by the uniform distribution for this metric space.

    Parameters
    ----------
    x : (p,) np.array
        An array of p non-negative integers or floats in [0,1) defining the distribution on {0,1,...,p-1}

    Returns
    -------
    synchrony : float
        The normalized measure of synchrony
    barycenter : float
        The location of a delta distribution which achieves the global minimal Wasserstein-2 optimal transport distance
    """
    # number of states
    p = len(x)
    
    # normalize to a distribution if necessary
    if not math.isclose(x.sum(),1):
        x = x/x.sum()
    
    # compute the Wasserstein-2 OT cost matrix 
    dm = discrete_uniform_circ_state_dm(p)
    C = dm*dm
    
    # find the measure of synchrony of the distribution x
    wass2dists = np.dot(C,x)
    
    # the maximum generalized variance in the cyclic state space is achieved by the uniform distribution
    normalization = np.dot(C, np.ones(p)/p)[0]
    
    return 1 - np.sqrt(wass2dists.min() / normalization), wass2dists.argmin()


def discrete_general_circ_synchrony(x, a=None, normalization=None):
    """
    Compute the measure of synchrony of the distribution x on a finite cyclic state space specified by p arcs
    [a_i, a_{i+1}) in the circle, [0,1), with a_0=0, a_{p+1}=1. Distance between each pair of states is given by the
    arclength between the midpoints:

        min( |a_i-a_j + a_{i+1}-a_{j+1}|, 2-|a_i-a_j + a_{i+1} - a_{j+1}| )/2

    Parameters
    ----------
    x : (p,) np.array
        An array of p non-negative integers or floats in [0,1) defining the distribution on {0,1,...,p-1}
    a : np.array or None
        An array of p+1 distinct values in [0,1) including 0 and 1, or None. If None, uniform discretization is used
    normalization : float
        The normalization constant for the given cyclic state space (can be precomputed by finite_state_normalization())

    Returns
    -------
    dm : (p,p)-ndarray
        The metric matrix
    """
    p = len(x)
    if a is None:
        a = np.linspace(0, 1, p + 1)

    a = np.sort(a)

    # normalize to a distribution if necessary
    if not math.isclose(x.sum(), 1):
        x = x / x.sum()

    # Compute the discrete cyclic distance matrix and Wasserstein-2 cost matrix
    dm = discrete_general_circ_state_dm(a)
    C = dm * dm

    # Compute the measure of synchrony and barycenter
    return finite_state_synchrony(x, C, normalization=normalization)


def finite_state_normalization(C):
    """
    Let M = {0,...,p-1} be a finite metric state space with distance matrix D, and let C = D^2 be the Wasserstein-2
    cost matrix associated with M. Then maximum generalized variance of any distribution on M is achieved by the
    distribution which maximizes the minimum Wasserstein-2 distance from to any delta distribution d_i, i=0,...,p-1.
    Such a distribution, pi*, will maximize the minimum component of C.pi. This maximization
    problem can be rewritten as a linear program

    maximize    t
    subject to
                t <= (C.pi)[i,:]  i=0,...,p-1
                pi.sum() = 1
                pi >= 0
   
   This can be rewritten in standard form by letting x = [pi[0],...,pi[p-1],t] be a vector of unknowns and
   c = [0,...0,-1] so to solve

    minimize    c.x
                subject to
                A_ub.x <= b_ub = [0,0,...,0]   (where A_ub = [-1*C;np.ones(p)])
                A_eq.x == b_eq = 1   (where A_eq = [1,1,...,1,0])
                [0,..,0] = lb <= x[:-1]

    The solution is the normalization constant used to define a measure of population synchrony.
    
    Parameters
    ----------
    C : (p,p) nd.array
        The Wasserstein-2 cost matrix for the finite state space

    Returns
    -------
    normalization : float64
        The maximum generalized variance over all distributions on the given state space
    pi_star : (p,) nd.array
        A distribution achieving the maximal generalized variance over the given state space
    """
    p = C.shape[0]
    c = np.zeros(p+1)
    c[-1] = -1

    A_ub = np.concatenate((-1*C,np.ones((p,1))), axis=1)
    b_ub = np.zeros(p)

    A_eq = np.ones( (1,p+1) )
    A_eq[0,-1] = 0
    b_eq = 1

    bounds = [(0,None) for _ in range(p)] + [(None,None)]

    res = sp.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs', callback=None, options=None, x0=None, integrality=None)
    
    normalization = -res.fun
    pi_star = res.x[:-1]
    
    return normalization, pi_star


def finite_state_synchrony(x, C, normalization=None):
    """
    Let M = {0,...,p-1} be a finite metric state space with distance matrix D[i,j]=d(i,j), and C = D^2 be the
    Wasserstein-2 cost matrix associated with M. This function returns the normalized synchrony measure of a
    distribution, pi, over (M,d).

    Parameters
    ----------
    x : (p,) np.array
        An array of p non-negative integers or floats in [0,1) defining the distribution on {0,...,p-1}
    C : (p,p) nd.array
        The Wasserstein-2 cost matrix for a finite state space
    normalization : float
        The normalization constant for C (can be precomputed by finite_state_normalization())
        
    Returns
    -------
    synchrony : float
        The normalized measure of synchrony
    barycenter : float
        The location of a delta distribution which achieves the global minimal Wasserstein-2 optimal transport distance
    """
    p = len(x)
    
    # Compute squared Wasserstein-2 distances to each delta distribution
    wass2dists = np.dot(C,x)

    # Compute normalization constant for this finite state space
    if normalization is None:
        normalization, _ = finite_state_normalization(C)

    return 1 - np.sqrt(wass2dists.min() / normalization), wass2dists.argmin()


def rect_synchrony(x, low=0, high=1):
    """
    Computes the exact synchrony of a population of n point masses, x = {x[i]}_{i=1}^n, in the Euclidean rectangular
    parallelepiped, prod_{i} [low[i],high[i]]. Synchrony is defined to be 1 minus the square root of the generalized
    variance of the empirical distribution

    sum_i=1^n delta_{x[i]}/n

    normalized by the square root of the maximum generalized variance of any distribution on the space. For a
    rectangular parallelepiped, the maximal generalized variance, \nu, is achieved by a symmetric distribution
    supported on the corners, and is equal to the squared radius of the minimal enclosing sphere, which is the square
    of half the distance between diagonal corners.  Then synchony is equal to  1 - (Var(x)/ \nu)^1/2.

    Parameters
    ----------
    x : array
        array of floats specifying the n, d-dimensional points--the support of the distribution in R^d
    low : enumerable or numeric
        lower bound of each coordinate of the box
    high : enumerable or numeric
        upper bound of each coordinate of the box

    Returns
    -------
    synchrony : float
        the normalized measure of synchrony
    barycenter : float
        the location of a delta distribution which achieves the minimal Wasserstein-2 optimal transport distance
    """
    # ensure correct data types and dimensions
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, np.newaxis]

    # determine the number of points and the dimension of the empirical distribution
    n, d = x.shape

    low = np.array([low]).flatten()
    high = np.array([high]).flatten()
    if len(low) == 1 and len(high) == 1:
        low = low[0] * np.ones(d)
        high = high[0] * np.ones(d)

    if (len(low) != len(high)) or len(low) != d:
        raise ValueError(
            f"The rectangle must be specified by equal length lists, len(low)={len(low)}, len(high)={len(low)}, each with the same length as the dimension of the sample (current dim={d}).")

    # compute the exact normalization constant
    normalization = np.sum((high - low) ** 2) / 4

    # compute the usual Euclidean barycenter (mean) and variance
    barycenter = np.mean(x, axis=0)

    xbar = barycenter.reshape(1, -1)
    x2 = np.sum(x ** 2, axis=1).reshape(-1, 1)
    y2 = np.sum(xbar ** 2, axis=1)
    xy = np.matmul(x, xbar.T)

    wass_dist = np.sum(x2 - 2 * xy + y2) / n

    return 1 - np.sqrt(wass_dist / normalization), barycenter


def ball_synchrony(x, radius=1):
    """
    Computes the exact synchrony of a population of n point masses, x = {x[i]}_{i=1}^n, in the Euclidean ball with given
    radius, centered at the origin: {x | ||x|| <= radius}. Synchrony is defined to be 1 minus the square root of the
    generalized variance of the empirical distribution

    sum_i=1^n delta_{x[i]}/n

    normalized by the square root of the maximum generalized variance of any distribution on the space.
    For a ball, the maximal generalized variance, \nu, is achieved by the uniform distribution supported on the
    boundary sphere, and is equal to the squared radius of the ball itself.  Then synchony is equal to
    1 - (Var(x)/ \nu)^1/2.

    Parameters
    ----------
    x : array
        array of floats specifying the n, d-dimensional points--the support of the distribution in R^d
    radius : float > 0
        the positive radius of the ball

    Returns
    -------
    synchrony : float
        the normalized measure of synchrony
    barycenter : float
        the location of a delta distribution which achieves the minimal Wasserstein-2 optimal transport distance
    """
    # ensure correct data types and dimensions
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, np.newaxis]

    n, d = x.shape

    # ensure points are inside the ball
    vector_norms = np.linalg.norm(x, axis=1)
    if np.any(vector_norms > radius):
        raise ValueError(
            f"Sample points are outside the ball of given radius={radius}.")

    # compute the exact normalization constant
    normalization = radius

    # compute the usual Euclidean barycenter (mean) and variance
    barycenter = np.mean(x, axis=0)

    xbar = barycenter.reshape(1, -1)
    x2 = np.sum(x ** 2, axis=1).reshape(-1, 1)
    y2 = np.sum(xbar ** 2, axis=1)
    xy = np.matmul(x, xbar.T)

    wass_dist = np.sum(x2 - 2 * xy + y2) / n

    return 1 - np.sqrt(wass_dist) / normalization, barycenter