import numpy as np
from numpy.polynomial.polynomial import Polynomial

def mad(data, axis=0, scale=1.4826):
    """
    Median of absolute deviation along a given axis.  

    Normalized to match the definition of the sigma for a gaussian
    distribution.
    """
    if data.ndim == 1:
        med = np.ma.median(data)
        ret = np.ma.median(np.abs(data-med))
    else:
        med = np.ma.median(data, axis=axis)
        if axis>0:
            sw = np.ma.swapaxes(data, 0, axis)
        else:
            sw = data
        ret = np.ma.median(np.abs(sw-med), axis=0)
    return scale * ret

def robust_average(a, sigma=None, axis=None, clip=5, mad=False,
                   mask=None, mini_output=False, scale_var=True):
    """ Perform an iteratively clipped weighted averaging.

    After each step, chi2 for values in a are computed and outlying
    values are weighted to zeros before a second step. A mask of
    detected outliers is kept and return.

    Parameters:
    -----------
    sigma: the average will be weighted by 1/sigma**2
    axis: int, compulsory
          Axis along which the means are computed.
    clip: float
          Outliers lying at more than clip * std from the mean will be
          iteratively discarded from the averaging.
    mad: bool
         If True, use the median of absolute deviation to evaluate the
         width of the distribution. Can be usefull for large numbers
         of outliers but slow down the computation.
    mask: bool array
          Specify values to discard from the mean (outlier rejection
          is still performed besides this).
    mini_output: bool
                 Shorten the return value to the average.
    scale_var: bool
               If true, the return variance is 1 / w ** 2 * std**2
               where std is the standard deviation of residuals else,
               return simply 1 / (w ** 2). The scaled estimate is not
               reliable for small samples.

    Returns
    -------
    m: the weighted average along the given axis
    if mini_output:
    mask: the mask finally applied to the data
    var: the inverse sum of weights scaled by the variance of the residuals
    rchi2: the reduced chi2
    """
    data = np.ma.masked_invalid(a)
    if mask is not None:
        data.mask |= mask
    #reps = [1,]*len(a.shape)
    #reps[axis] = a.shape[axis]
    mshape = [s for s in data.shape]
    mshape[axis] = 1

    if sigma is None:
        sigma = np.ones(a.shape)

    wrong = np.ones(1, dtype='bool')  # do it once
    while wrong.any():
        m, w = np.ma.average(data, weights=1 / sigma ** 2,
                             axis=axis, returned=True)
        m = m.reshape(mshape)
        r = (data - m) / sigma
        if mad:  # robust but slow. Can save a whole iteration though
            dev = np.ma.median(abs(r), axis=axis).reshape(mshape) * 1.4826
        else:
            dev = r.std(axis=axis).reshape(mshape)
        if data.shape[axis] < 2:
            #print('Warning: cannot compute a meaningful deviation of residuals')
            dev = np.ones_like(dev)
        wrong = abs(r) > clip * dev
        data.mask = wrong.filled(fill_value=True)
    dev = dev.squeeze()
    var = 1 / w
    if scale_var:
        var *= dev ** 2
    if mini_output:
        return m.squeeze()
    else:
        return m.squeeze(), data.mask, var, dev ** 2

def robust_polyfit(x, y, degree, clip_sigma=3, max_iterations=10, min_points=5):
    """
    Perform a robust polynomial fit, iteratively clipping outliers.

    Parameters:
    - x: array-like, independent variable
    - y: array-like, dependent variable
    - degree: int, degree of the polynomial to fit
    - clip_sigma: float, number of standard deviations to use for clipping
    - max_iterations: int, maximum number of iterations for fitting
    - min_points: int, minimum number of points required for fitting

    Returns:
    - Polynomial object with robust fit parameters
    """
    x, y = np.asarray(x), np.asarray(y)
    mask = np.ones(len(x), dtype=bool)  # start with all points

    for _ in range(max_iterations):
        # Fit polynomial
        poly = Polynomial.fit(x[mask], y[mask], degree)
        
        # Calculate residuals
        residuals = y - poly(x)
        
        # Calculate standard deviation of residuals
        residual_std = np.std(residuals[mask])
        
        # Update mask to exclude new outliers
        new_mask = np.abs(residuals) < clip_sigma * residual_std
        
        # If nothing changed, or we've reached the minimum number of points, stop
        if np.array_equal(mask, new_mask) or np.sum(mask) <= min_points:
            break
        
        mask = new_mask

    # Final fit with the last mask
    return Polynomial.fit(x[mask], y[mask], degree)

# Example usage
if __name__ == "__main__":
    # Generate some noisy data with an outlier
    np.random.seed(0)
    x = np.linspace(0, 10, 100)
    y = 2*x**2 + 3*x + 1 + np.random.normal(0, 10, len(x))
    y[int(len(y)/2)] += 1000  # Add an outlier

    # Fit with robust_polyfit
    robust_poly = robust_polyfit(x, y, degree=2, clip_sigma=3)
    
    # Print the fitted parameters
    print("Fitted polynomial coefficients:", robust_poly.coef)
    
    # Plotting (optional with matplotlib)
    import matplotlib.pyplot as plt
    plt.scatter(x, y, label='Data')
    plt.plot(x, robust_poly(x), 'r', label='Robust Fit')
    plt.legend()
    plt.show()
