"""
Feedback strings for function-based exercises
"""
from __future__ import print_function


def _existence_error(funcname):
    e_message = f"""The function {funcname} does not exist.
    Ensure you have named the function properly, bearing in mind that capital
    letters matter. Also ensure that you have used the proper syntax for the
    definition of a function, i.e.
        def {funcname}(inputs):
            ...
    """
    return e_message


def _input_error(funcname, numargs):
    e_message = f"""The function {funcname} does not accept input correctly.
    The function is supposed to accept {numargs} input argument(s).
    Ensure you have specified the input arguments in the function definition.
    i.e.
        def {funcname}(input_1, input_2, ...):
            ...
    """
    return e_message


def _value_error(funcname, inp, exp, res):
    e_message = f"""The function {funcname} returns the wrong value(s).
    When executed with the input(s), {inp}, we expected the output, {exp}, but
    instead we got {res}.
    """
    return e_message


def _return_error(funcname):
    e_message = f"""The function {funcname} does not return a value.
    Ensure that the function uses the correct syntax for a return statement.
    i.e.
        def {funcname}(input):
            ...
            return (answer)
    """
    return e_message


def _call_error(fname, cname):
    e_message = f"""The function {fname} does not call the function {cname}.
    Make sure that rather than repeating lines of code, your function passes
    input to the previously defined function, e.g.

        def {cname}(input):
            ...
            return (answer)
        def {fname}(input):
            ...
            new_answer = some_operation + {cname}(input)
            return(new_answer)
    """
    return e_message


def _execution_error(funcname, inp, msg=[None, None, None]):
    e_message = f"""The function {funcname} does not execute correctly.
    Test it by adding a function call, e.g.
        print({funcname}{inp})

Error reported:
    {msg[0]}
    {msg[1]}
    {msg[2]}
        """
    return e_message


def print_error_message(error, funcname, inp=(0,), exp=7, result=0,
                        callname='print', msg=[None, None, None]):
    """ given information on the execution of the function, display meaningfull
    feedback in the terminal as to why the submitted code has failed (or
    passed).

    Parameters
    ==========
    error : str
        Possible error strings are
            - 'success' (function works as expected)
            - 'existence' (function has not been defined)
            - 'inputs' (function does not accept input as expected)
            - 'outputs' (function does not produce correct output)
            - 'return' (function does not return a value/returns None)
            - 'calls' (function does not call other functions as required)
            - 'execution' (other error in the execution of the function)
    funcname : str
        name of the function under investigation
    inp : tuple
        input values for the function
    exp: any
        expected output of the function
    result : any
        actual output of the function
    callname : str
        name of the function that was supposed to be called within funcname
    msg : Exception
        Exception raised by the execution of funcname
    """
    from AutoFeedback.bcolors import bcolors

    pval_string = ""
    if hasattr(exp, "pval"):
        if exp.pval < 0.05:
            error = "outputs"
        else:
            error = "success"
            pval_string = f" The p-value is {exp.pval}."

    if (str(error) == "success"):
        print(f"{bcolors.OKGREEN}Function, {funcname} is correct!{pval_string}\
              \n{bcolors.ENDC}")

    else:
        if (str(error) == "existence"):
            emsg = _existence_error(funcname)
        elif (str(error) == "inputs"):
            emsg = _input_error(funcname, len(inp))
        elif (str(error) == "outputs"):
            if hasattr(exp, "get_error") and callable(exp.get_error):
                emsg = exp.get_error(
                    f"values returned from the function {funcname} with input\
                    parameters {inp}")
            else:
                emsg = _value_error(funcname, inp, exp, result)
        elif (str(error) == "return"):
            emsg = _return_error(funcname)
        elif (str(error) == "calls"):
            emsg = _call_error(funcname, callname)
        elif (str(error) == "execution"):
            emsg = _execution_error(funcname, inp, msg=msg)
        else:
            emsg = (f"something not right with {funcname}")
        print(f"{bcolors.FAIL}{emsg}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}")
