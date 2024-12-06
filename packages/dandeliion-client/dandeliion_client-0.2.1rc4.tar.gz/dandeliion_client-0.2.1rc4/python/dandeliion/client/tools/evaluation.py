'''Safe function evaluation code along side automatic derivatives using JAX'''
import asteval

import jax.numpy as jnp
import jax
import os

import numpy as np
import scipy.integrate
import dill
import codecs

jax.config.update("jax_enable_x64", True)
jax.config.update('jax_platform_name', 'cpu')

# verify that jax is running on double precision
assert jax.random.uniform(jax.random.PRNGKey(0), (1000,), dtype=jnp.float64).dtype == 'float64'

DEFAULT_SAFE = True  # TODO read from/set in config to False for client?


# whitelist jax-numpy functions using the same list of trusted numpy functions from asteval package
jax_symtable = {}
for sym in asteval.astutils.FROM_NUMPY:
    if hasattr(jnp, sym):
        jax_symtable[sym] = getattr(jnp, sym)

for name, sym in asteval.astutils.NUMPY_RENAMES.items():
    if hasattr(jnp, sym):
        jax_symtable[name] = getattr(jnp, sym)

# whitelist jax grad and vmap functions
jax_symtable['jax_grad'] = jax.grad
jax_symtable['jax_vmap'] = jax.vmap


# function to create a function from source
def create_func_obj(func_code_str, gbl={}):
    lcl = {}
    exec(func_code_str, gbl, lcl)
    if lcl:
        return list(lcl.values())[0]
    else:
        raise Exception('Failed to create function')


# serialize function/equation
def serialize(func):
    if not isinstance(func, str):
        return codecs.encode(dill.dumps(func), "base64").decode()
    else:
        return func


# deserialize function/equation
def deserialize(data):
    try:
        return dill.loads(codecs.decode(data.encode(), "base64"))
    except Exception:
        return data


# function templates when evaluating a function string
# this will be run in a python sandbox to ensure it is safe
template_eq = '''
def f(x):
    value = {0}
    # multiply by 1.0 to ensure dtype is float
    return 1.0 * value
'''

template_f = '''
f = {0}
'''

template_div = '''
# auto differentiate the function
f = jax_grad(f)
'''

template_vec = '''
# vectorize function (incase it returns a scalar)
f = jax_vmap(f)
'''

template_eval = '''
# evaluate function
f_x = f(x_eval)
'''


def build_function(func, source=False, vectorise=True):

    if callable(func):
        # create source and then recreate function (ensures that all declarations were local
        # and that function can be pickled and restored correctly)
        f_string = dill.source.getsource(dill.detect.code(func))
        if source:
            return f_string + template_f.format(func.__name__)
        func = create_func_obj(f_string)
    elif isinstance(func, str) or isinstance(func, float):
        if source:
            func = template_eq.format(func)
        else:
            func = create_func_obj(template_eq.format(func), gbl=jax_symtable)
    else:
        raise ValueError('Unsupported function format!', type(func))

    if vectorise:
        if source:
            func += template_vec
        else:
            func = jax.vmap(func)

    return func


def build_div_function(func, source=False):

    func = build_function(func=func, source=source, vectorise=False)

    if source:
        return func + template_div + template_vec
    else:
        return jax.vmap(jax.grad(func))


def evaluate_function(func, lower=0, upper=1, steps=1001, safe=DEFAULT_SAFE):

    '''A function that takes a function, equation or list with CSV data and returns the
    evaluated function.

    Paramters
    ---------
    func: str, function, list
        A string containing an equation that uses the variable "x". The equation is allowed
        to be non-finite at the lower bound only (e.g. 1/x with lower=0 is fine), otherwise
        it will raise an error.
        OR a python function. The function has to define everything it uses within its local
        scope if safe=True is used (i.e. all called custom functions have to be inner functions)
        OR list of CSV data. The CSV data has the x values in its first column and the function
        values in the second. The x values have to be equally spaced and have to cover at least
        the interval defined by [upper, lower].
    lower: float
        Lower evaluation point.  Default 0. If func is CSV data, upper evaluation point will
        be the closest data point below this value.
    upper: float
        Upper evaluation point. Default 1. If func is CSV data, upper evaluation point will
        be the closest data point above this value.
    steps: int
        Number of evaluation points. Default 1001 (ignored if func is CSV data)
    safe: boolean
        Flag to indicate whether evaluation should be restricted to ''safe'' input (i.e.
        table and equations, but not to python functions

    Returns
    -------
    x: list
        The evaluated x points
    f_x: list
        The function evaluated at x_eval.  If the function is not finite at the lower bound
        linear interpolation is used to estimate the function at this point.
    '''

    if not func:
        raise ValueError('No function provided!')
    if isinstance(func, dict):
        if not isinstance(func.get('x', None), list) or \
           len(func.get('y', [])) != len(func['x']):
            raise Exception("Invalid data table provided! Has to contain 'x' and 'y' entries, both containing "
                            + "lists of equal length")
        x = np.array(func['x'], dtype=float)
        idx_sorted = x.argsort()
        x = x[idx_sorted]
        fx = np.array(func['y'], dtype=float)[idx_sorted]
        # check if requested range covered and equidistant steps
        if (min(x) > lower or max(x) < upper or any(np.diff(x) != np.diff(x)[0])):
            raise Exception("Invalid data table provided!"
                            + " 'x' has to be a list of equidistant steps covering the requested range")
        # find closest datapoints outside range and cut there
        idx_min = np.argwhere(x <= lower).max()
        idx_max = np.argwhere(x >= upper).min() + 1
        return x[idx_min:idx_max].tolist(), fx[idx_min:idx_max].tolist()

    # create evaluation points & function
    x = jnp.linspace(lower, upper, steps)
    func = build_function(func=func, source=safe)

    if safe:
        f_x = _eval_safely(f_string=func, x_eval=x)
    else:
        f_x = func(x).tolist()

    return x.tolist(), f_x


def evaluate_div_function(func, lower=0, upper=1, steps=1001, safe=DEFAULT_SAFE):

    '''A function that takes a function or equation and returns the
    evaluated derivative.

    Paramters
    ---------
    func: str, function, list
        A string containing an equation that uses the variable "x". The equation is allowed
        to be non-finite at the lower bound only (e.g. 1/x with lower=0 is fine), otherwise
        it will raise an error.
        OR a python function. The function has to define everything it uses within its local
        scope if safe=True is used (i.e. all called custom functions have to be inner functions).
    lower: float
        Lower evaluation point.  Default 0. If func is CSV data, upper evaluation point will
        be the closest data point below this value.
    upper: float
        Upper evaluation point. Default 1. If func is CSV data, upper evaluation point will
        be the closest data point above this value.
    steps: int
        Number of evaluation points. Default 1001 (ignored if func is CSV data)

    Returns
    -------
    x: list
        The evaluated x points
    f_div_x: list
        The function's derivative evaluated at x. If the derivative is not finite at the lower
        bound linear interpolation is used to estimate the function at this point.
    '''

    if not func:
        raise ValueError('No function provided!')

    # create evaluation points & function
    x = jnp.linspace(lower, upper, steps)
    func = build_div_function(func=func, source=safe)

    if safe:
        f_div_x = _eval_safely(f_string=func, x_eval=x)
    else:
        f_div_x = func(x).tolist()

    return x.tolist(), f_div_x


def evaluate_int_function(func, lower=0, upper=1, steps=1001, safe=DEFAULT_SAFE):

    '''A function that takes a function, equation or list with CSV data and returns the
    evaluated integral.

    Paramters
    ---------
    func: str, function, list
        A string containing an equation that uses the variable "x". The equation is allowed
        to be non-finite at the lower bound only (e.g. 1/x with lower=0 is fine), otherwise
        it will raise an error.
        OR a python function. The function has to define everything it uses within its local
        scope if safe=True is used (i.e. all called custom functions have to be inner functions)
        OR list of CSV data. The CSV data has the x values in its first column and the function
        values in the second. The x values have to be equally spaced and have to cover at least
        the interval defined by [upper, lower].
    lower: float
        Lower evaluation point.  Default 0. If func is CSV data, upper evaluation point will
        be the closest data point below this value.
    upper: float
        Upper evaluation point. Default 1. If func is CSV data, upper evaluation point will
        be the closest data point above this value.
    steps: int
        Number of evaluation points. Default 1001 (ignored if func is CSV data)

    Returns
    -------
    x: list
        The evaluated x points
    f_int_x: list
        The function's integral evaluated at x_eval.  The constant of integration is picked
        to make the first value of this list `0`.
    '''

    if isinstance(func, tuple):
        # already evaluated function, just use the data
        x = func[0]
        f_x = func[1]
    else:
        # evaluate function
        x, f_x = evaluate_function(func=func, lower=lower, upper=upper, steps=steps, safe=safe)

    f_int_x = scipy.integrate.cumulative_trapezoid(f_x, x, initial=0).tolist()
    return x, f_int_x


# file loading function to blacklist
numpy_blacklist = [
    'frombuffer',
    'fromfile',
    'fromregex',
    'fromstring',
    'genfromtxt',
    'load',
    'loads',
    'loadtxt'
]


def _eval_safely(f_string, x_eval):
    '''A function that takes in a string containing a function and a list of evaluation
    points and returns the evaluated function.
    Only a subset of trusted jax.numpy functions can be used.

    Paramters
    ---------
    f_string: str
        A string containing a function that uses the variable "x".  The function is allowed
        to be non-finite at the lower bound only (e.g. 1/x with lower=0 is fine), otherwise
        it will raise an error.
    x_eval: list
        The values to evaluate the function at

    Returns
    -------
    f_x: list
        The function evaluated at x_eval.  If the function is not finite at the lower bound
        linear interpolation is used to estimate the function at this point.
    '''
    eval_interpreter = asteval.Interpreter(
        err_writer=open(os.devnull, 'w'),
        usersyms=jax_symtable,
        use_numpy=True,
        no_for=True,
        no_while=True,
        no_try=True,
        no_ifexp=True,
        no_listcomp=True,
        no_augassign=True,
        no_assert=True,
        no_delete=True,
        no_print=True,
        no_raise=True,
        no_if=True,
        max_statement_length=10000
    )
    # blacklist numpy load and save functions
    for black_function in numpy_blacklist:
        if black_function in eval_interpreter.symtable:
            del eval_interpreter.symtable[black_function]

    eval_interpreter.symtable['x_eval'] = x_eval
    x_eval = x_eval.tolist()

    # run the template
    eval_interpreter(f_string + template_eval)
    if len(eval_interpreter.error) > 0:
        raise SyntaxError("Can't evaluate function")

    f_x = _check_finite(eval_interpreter.symtable['f_x'])
    return f_x


def _check_finite(y):
    '''Check if the input JAX array has all finite values.  If the first
    value is not finite use linear extrapolation to estimate it, otherwise
    if any other value is not finite raise a ValueError.

    Paramters
    ---------
    y : jax.numpy.array
        A JAX array of values

    Returns
    -------
    y_out : list
        A python list of finite values
    '''
    fdx = ~jnp.isfinite(y)
    if fdx[1:].any():
        raise ValueError('The function not finite at all points above the lower bound')
    if fdx[0]:
        y = y.at[0].set(2 * y[1] - y[2])
    return y.tolist()


def validate_data(data, lower, upper):
    if not isinstance(data, dict):
        raise ValueError("data has to be 'dict'")
    if 'x' not in data:
        raise ValueError("data must contain entry for 'x' values")
    if 'y' not in data:
        raise ValueError("data must contain entry for 'y' aka f(x) values")
    if len(data['x']) != len(data['y']):
        raise ValueError("'x' and 'y' must be of same length!")
    if not all(data['x'][i] <= data['x'][i + 1] for i in range(len(data['x']) - 1)):
        raise ValueError("'x' values must be sorted.")
    if min(data['x']) > lower or max(data['x']) < upper:
        raise ValueError("'x' values must at least cover range [%d, %d]." % (lower, upper))
