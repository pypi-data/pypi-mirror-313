''' The module provides two second order methods to solve non-linear problems:

- least_squares a wrapper around scipy.optimize.least_squares taking advantage of automatic jax differentiation and suitable only for problems with small number of parameters because it forms the jacobian of the model (WIP)
- fit_tncg suitable for larger problem but so far much less robust to ill-conditionned problems
'''
import jax
import jax.numpy as jnp


# ============== #
#                #
#     TNCG       #
#                #
# ============== #
def fit_tncg(func, init_param, 
             niter=10, tol=5e-3, 
             lmbda=1e2, 
             **kwargs):
    """ Hessian-free second order optimization algorithm

    The following implementation of TN-CG is largely based on
    recommendations given in Martens, James (2010, Deep learning via
    Hessian-free optimization, Proc. International  Conference on
    Machine Learning).

    Parameters
    ----------
    func: function
        function to minimize. Should return a float.

    init_param: 
        entry parameter of the input func

    niter: int
        maximum number of iterations

    tol: float
        targeted func variations below which the iteration will stop

    lmbda: float
        lambda parameter of the tncg algorithm. (optstate)

    **kwargs other func entries 

    Returns
    -------
    list
        - best parameters
        - loss (array)

    Example
    -------
    ```python
    import jax
    from edris import simulation, minimize
    key = jax.random.PRNGKey(1234)
    truth, simu = simulation.get_simple_simulation(key, size=1_000)

    def get_total_chi2(param, data):
        # model for a line with error on both axes but no intrinsic scatter.
        x_model = param["x_model"]
        y_model = x_model * param["a"] + param["b"]
    
        chi2_y = jnp.sum( ((data["x_obs"] - x_model)/data["x_err"])**2 )
        chi2_x = jnp.sum( ((data["y_obs"] - y_model)/data["y_err"])**2 )
    
        return chi2_y + chi2_x

    init_param = {"a": 8., "b":0., "x_model": simu["x_obs"]} # careful, must be float
    best_params, loss = minimize.fit_tncg(get_total_chi2, init_param, data=simu)
    ```
    
    """
    # handle kwargs more easily
    func_ = lambda x: func(x, **kwargs)
    fg = jax.value_and_grad(func_)
    
    # - internal function --- #
    def hessian_vector_product(g, x, v):
        return jax.jvp(g, (x,), (v,))[1]

    def step_tncg(x, optstate):
        loss, grads = fg(x)
        lmbda = optstate['lmbda']
        fvp = lambda v: jax.tree_map(lambda d1, d2: d1 + lmbda*d2, hessian_vector_product(jax.grad(func_), x, v), v)
        updates, _ = jax.scipy.sparse.linalg.cg(fvp, grads, maxiter=50)
        coco = jax.tree_util.tree_reduce(lambda x, y: x+y, jax.tree_util.tree_map(lambda x, y: (-x*y).sum(), grads, updates))
        return updates, loss, optstate, coco

    #step_tncg = jax.jit( step_tncg )
    # ----------------------- #
    
    x = init_param
    optstate = {'lmbda': lmbda}
    losses = []

    for i in range(niter):
        updates, loss, optstate, coco = step_tncg(x, optstate)
        x1 = jax.tree_util.tree_map(lambda x, y: x - y, x, updates)
        dloss = func_(x1) - loss
        losses.append(loss)
        rho = dloss / coco
        
        if rho < 0.25:
            optstate['lmbda'] = optstate['lmbda'] * 1.5
        elif rho > 0.75:
            optstate['lmbda'] = optstate['lmbda'] * 0.3
            
        if dloss < 0: # accept the step
            x = x1
            
        if tol is not None and dloss > -tol:
            break
        
    return x, losses
