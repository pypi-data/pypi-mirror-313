"""
Check a students' function works as expected, and provide feedback
"""


def _input_vars(func, ins):
    """check that func accepts input as expected
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    """
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        if hasattr(inputs, "__len__"):
            func(*inputs)
        else:
            func(inputs)
        return True
    except TypeError as e:
        return ('positional' not in str(e))


def _returns(func, ins):
    """check that func returns a value
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    """
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        if hasattr(inputs, "__len__"):
            res = func(*inputs)
        else:
            res = func(inputs)
        if hasattr(res, "__len__"):
            res = list(res)
        return (res is not None)
    except Exception as e:
        raise e


def _check_outputs(func, ins, expected):
    """check that func(ins) returns the expected value
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    expected : expected return value of func(ins)
    """
    from AutoFeedback.varchecks import check_value
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        if hasattr(expected, "check_value") and callable(expected.check_value):
            if not hasattr(expected, "nsamples"):
                raise RuntimeError("""there should be an attribute called
nsamples in the class you have provided as reference""")
            res = func(*inputs)
            if expected.nsamples > 1:
                res = expected.nsamples * [0]
                for i in range(expected.nsamples):
                    res[i] = func(*inputs)

            return expected.check_value(res)
        else:
            res = func(*inputs)
            return (check_value(res, expected))
    except RuntimeError as e:
        raise e
    except Exception:
        return False


def _check_calls(func, call):
    """check that func calls another function called 'call'
    Parameters
    ==========
    func : function handle for function to be checked
    call : str, name of other function to be called
    """
    import inspect
    import ast
    try:
        all_names = [c.func for c in ast.walk(
            ast.parse(inspect.getsource(func))) if isinstance(c, ast.Call)]
        call_names = [name.id for name in all_names if
                      isinstance(name, ast.Name)]
        return (call in call_names)
    except Exception:
        return False


def _run_all_checks(funcname, inputs, expected, calls=[], output=True):
    """given information on a function which the student has been asked to
    define, check whether it has been defined correctly, and provide feedback

    Parameters
    ==========
    funcname : str
        name of function to be investigated
    inputs : list of tuples
        inputs with which to test funcname
    expected : list
        expected outputs of [funcname(inp) for inp in inputs]
    calls : list of strings
        names of any functions which funcname should call
    output : bool
        if True, print output to screen. otherwise execute quietly

    Returns
    =======
    bool: True if function works as expected, False otherwise.
    """
    from AutoFeedback.function_error_messages import print_error_message
    from AutoFeedback.utils import exists, get
    from AutoFeedback.randomclass import randomvar
    from copy import deepcopy as copy
    import scipy

    call = []
    ins = inputs[0]
    outs = expected[0]
    res = -999

    try:
        assert (exists(funcname, isfunc=True)), "existence"
        func = get(funcname)
        assert (_input_vars(func, inputs[0])), "inputs"

        assert (_returns(func, inputs[0])), "return"
        listOfOuts = []
        for ins, outs in zip(inputs, expected):
            res = func(*copy(ins))  # ensure the inputs are not overwritten
            if isinstance(expected[0], randomvar):
                listOfOuts.append(_check_outputs(func, ins, outs))
            else:
                assert _check_outputs(func, ins, outs), "outputs"
        if isinstance(expected[0], randomvar):
            outs.pval = 1 - scipy.stats.binom.cdf(listOfOuts.count(False),
                                                  len(listOfOuts), 0.05)
            assert outs.pval > 0.05, "outputs"

        for call in calls:
            assert (_check_calls(func, call)), "calls"
        if output:
            print_error_message("success", funcname,
                                inp=ins, exp=outs, result=res)
    except AssertionError as error:
        if output:
            print_error_message(error, funcname, inp=ins,
                                exp=outs, result=res, callname=call)
        if hasattr(outs, "pval") and outs.pval > 0.05:
            return True
        else:
            return False
    except Exception:
        if output:
            import traceback
            print_error_message("execution", funcname, inp=ins,
                                exp=outs, result=res, callname=call,
                                msg=traceback.format_exc().splitlines()[-3:])
        return False
    return True


def check_func(func, inputs=[], expected=[], calls=[], output=True):
    """given information on a function which the student has been asked to
    define, check whether it has been defined correctly, and provide feedback

    Parameters
    ==========
    func : function handle or str
        function handle or name of function to be investigated
    inputs : list of tuples
        inputs with which to test func
    expected : list
        expected outputs of [func(inp) for inp in inputs]
    inputs : list of tuples
        inputs with which to test func
    calls : list of strings
        names of any functions which func should call
    output : bool
        if True, print output to screen. otherwise execute quietly

    Returns
    =======
    bool: True if function works as expected, False otherwise.
    """
    from types import FunctionType

    if isinstance(func, FunctionType):

        if inputs == []:
            try:
                inputs = func.inputs
            except AttributeError:
                message = """Calling check_func with a function handle
requires either
1. The function have its inputs defined as an attribute, e.g.
    def func(x):
        return x**2
    func.inputs = [(1,), (2,)]
2. The inputs be provided as an argument to check_func, e.g.
    check_func(func, inputs=[(1,), (2,)])"""
                raise Exception(message)

        expected = [func(*inp) for inp in inputs]
        funcname = func.__name__
    else:
        funcname = func
        if (inputs == []) or (expected == []):
            message = """Calling check_func with a function name
requires the inputs and expected outputs to be provided as arguments
e.g.
    check_func('myfunc', inputs=[(1,), (2,)], expected=[2, 3])"""
            raise Exception(message)

    return _run_all_checks(funcname, inputs, expected, calls, output)
