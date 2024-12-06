"""
Feedback strings for variable-based exercises
"""
from __future__ import print_function


def _existence_error(varname):
    error_message = f"""The variable {varname} does not exist.
    Ensure you have named the variable properly,
    bearing in mind that capital letters matter.
    """
    return error_message


def _size_error(varname):
    error_message = f"""The variable {varname} is the wrong size.
    Try using len({varname}) to determine the size of the array, or
    print({varname} to check the values look as you expect them to.
    """
    return error_message


def _value_error(varname, exp, res):
    error_message = f"""The variable {varname} has the wrong value(s)\n
        We expected the output:
        {exp}
        but instead we got:
        {res}
        Try using print({varname}) to check the values look as you expect them
        to and ensure the expression used to calculate the variable
        is correct.
        """
    return error_message


def _import_error():
    error_message = """Your code fails to execute.
    Please refer to the error messages printed in the terminal to resolve
    any errors in your code.
    """
    return error_message


def print_error_message(error, varname, exp, res):
    """given information on the variable, display meaningful feedback in the
    terminal as to why the submitted code has failed (or passed).

    Parameters
    ==========
    error : str
        Possible error strings are:
            - 'success' : variable is defined correctly
            - 'existence' : variable has not been defined
            - 'size' : variable is the wrong size (e.g. wrong length of array)
            - 'import' : main.py cannot be imported
    varname : str
        name of the variable under investigation
    exp : any
        expected value of varname
    res : any
        actual value of varname
    """
    from AutoFeedback.bcolors import bcolors

    pval_string = ""
    if hasattr(exp, "pval"):
        if exp.pval < 0.05:
            error = "value"
        else:
            error = "success"
            pval_string = f" The p-value is {exp.pval}."

    if (str(error) == "success"):
        print(f"{bcolors.OKGREEN}Variable {varname} is correct!{pval_string}\
              \n{bcolors.ENDC}")

    else:
        if (str(error) == "existence"):
            emsg = _existence_error(varname)
        elif (str(error) == "size"):
            emsg = _size_error(varname)
        elif (str(error) == "value"):
            if hasattr(exp, "get_error") and callable(exp.get_error):
                emsg = exp.get_error(f"variable {varname}")
            else:
                emsg = _value_error(varname, exp, res)
        elif (str(error) == "import"):
            emsg = _import_error()
        else:
            emsg = f"something not right with {varname}"
        print(f"{bcolors.FAIL}{emsg}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}")


def output_check(expected, executable="main.py"):
    """Check whether printed information matches expected

    Parameters
    ==========
    expected : str
        The expected contents of stdout
    executable : str
        name of the python executable which when executed should print
        `expected` to screen

    Returns
    =======
    check : bool
        True if stdout is expected, False otherwise
    """
    import subprocess
    import sys
    from AutoFeedback.bcolors import bcolors

    def run(cmd):
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                )
        stdout = proc.communicate()

        return stdout

    out = run([sys.executable, executable])
    screen_out = str(out).split("'")[1]

    check = screen_out == expected + "\\n"

    errmsg = """The text printed to screen is not correct. Ensure you have
        printed the correct variables, in the correct order,
        and that nothing else is printed."""

    if not (check):
        print(f"{bcolors.FAIL}test_output has failed. \n{errmsg}")
    else:
        print(f"{bcolors.OKGREEN}Printing is correct!\n")

    print(f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}")

    return check
