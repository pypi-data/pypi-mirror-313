import unittest
import AutoFeedback.variable_error_messages as vm
import AutoFeedback.function_error_messages as fm
from AutoFeedback.plot_error_messages import error_message 
from AutoFeedback.plot_error_messages import print_error_message as pr
import io
import contextlib

pm = error_message()


def colour_message(emsg):
    from AutoFeedback.bcolors import bcolors
    retmsg = f"{bcolors.FAIL}{emsg}{bcolors.ENDC}\n"
    retmsg += f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}\n"
    return retmsg


class VarErrorTests(unittest.TestCase):
    def checkprint(self, estring, error_message, exp=None, res=None):
        """ estring is the string passed to print_error_message,
        error_message is the expected error message that is printed"""
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vm.print_error_message(estring, "googlyboo", exp=exp,
                                   res=res)
        printed = f.getvalue()
        expected = colour_message(error_message)
        return printed == expected

    def test_var_existence(self):
        error_message = """The variable googlyboo does not exist.
    Ensure you have named the variable properly,
    bearing in mind that capital letters matter.
    """
        assert(vm._existence_error("googlyboo") == error_message)
        assert(self.checkprint("existence", error_message))

    def test_var_size(self):
        error_message = """The variable googlyboo is the wrong size.
    Try using len(googlyboo) to determine the size of the array, or
    print(googlyboo to check the values look as you expect them to.
    """
        assert(vm._size_error("googlyboo") == error_message)
        assert(self.checkprint("size", error_message))

    def test_var_value(self):
        error_message = """The variable googlyboo has the wrong value(s)\n
        We expected the output:
        this
        but instead we got:
        that
        Try using print(googlyboo) to check the values look as you expect them
        to and ensure the expression used to calculate the variable
        is correct.
        """
        assert(vm._value_error("googlyboo", "this", "that") == error_message)
        assert(self.checkprint("value", error_message, exp="this", res="that"))

    def test_var_import(self):
        error_message = """Your code fails to execute.
    Please refer to the error messages printed in the terminal to resolve
    any errors in your code.
    """
        assert(vm._import_error() == error_message)
        assert(self.checkprint("import", error_message))

    def test_var_success(self):
        from AutoFeedback.bcolors import bcolors
        error_message = f"{bcolors.OKGREEN}Variable googlyboo is correct!\
              \n{bcolors.ENDC}\n"
        error_message += f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}\n"
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vm.print_error_message("success", "googlyboo",
                                   exp=None, res=None)
        assert(f.getvalue() == error_message)

    def test_wrong_estring(self):
        error_message = "something not right with googlyboo"
        assert(self.checkprint("asdfdas", error_message))


class FuncErrorTests(unittest.TestCase):
    def checkprint(self, estring, error_message, funcname, inp=(0,), exp=7,
                   result=0, callname='print', msg=[None, None, None]):
        """ estring is the string passed to print_error_message,
        error_message is the expected error message that is printed"""
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            fm.print_error_message(estring, funcname, inp, exp, result,
                                   callname, msg)
        printed = f.getvalue()
        expected = colour_message(error_message)
        return printed == expected

    def test_func_existence(self):
        error_message = """The function googlyboo does not exist.
    Ensure you have named the function properly, bearing in mind that capital
    letters matter. Also ensure that you have used the proper syntax for the
    definition of a function, i.e.
        def googlyboo(inputs):
            ...
    """
        assert(fm._existence_error("googlyboo") == error_message)
        assert(self.checkprint("existence", error_message, "googlyboo"))

    def test_func_input(self):
        error_message = """The function googlyboo does not accept input correctly.
    The function is supposed to accept 3 input argument(s).
    Ensure you have specified the input arguments in the function definition.
    i.e.
        def googlyboo(input_1, input_2, ...):
            ...
    """
        assert(fm._input_error("googlyboo", 3) == error_message)
        assert(self.checkprint("inputs", error_message, "googlyboo",
                               inp=(1, 1, 1)))

    def test_func_value(self):
        error_message = """The function googlyboo returns the wrong value(s).
    When executed with the input(s), (7, 8, 9), we expected the output, 4, but
    instead we got 17.
    """
        assert(fm._value_error("googlyboo", (7, 8, 9), 4, 17) == error_message)
        assert(self.checkprint("outputs", error_message, "googlyboo",
                               inp=(7, 8, 9), exp=4, result=17))

    def test_func_return(self):
        error_message = """The function googlyboo does not return a value.
    Ensure that the function uses the correct syntax for a return statement.
    i.e.
        def googlyboo(input):
            ...
            return (answer)
    """
        assert(fm._return_error("googlyboo") == error_message)
        assert(self.checkprint("return", error_message, "googlyboo"))

    def test_func_call(self):
        error_message = """The function Manny does not call the function Bernard.
    Make sure that rather than repeating lines of code, your function passes
    input to the previously defined function, e.g.

        def Bernard(input):
            ...
            return (answer)
        def Manny(input):
            ...
            new_answer = some_operation + Bernard(input)
            return(new_answer)
    """
        assert(fm._call_error("Manny", "Bernard") == error_message)
        assert(self.checkprint("calls", error_message, "Manny",
                               callname="Bernard"))

    def test_func_exec(self):
        error_message = """The function googlyboo does not execute correctly.
    Test it by adding a function call, e.g.
        print(googlyboo(1, 2, 3))

Error reported:
    this
    and
    that
        """
        op = fm._execution_error("googlyboo", (1, 2, 3), msg=[
                                 "this", "and", "that"])
        assert(op == error_message)
        assert(self.checkprint("execution", error_message, "googlyboo",
                               inp=(1, 2, 3), msg=["this", "and", "that"]))


class dummyline:
    label = "googlyboo"


myline = dummyline()


class PlotErrorTests(unittest.TestCase):
    def checkprint(self, estring, error_message, line=myline):
        """ estring is the string passed to print_error_message,
        error_message is the expected error message that is printed"""
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            pr(f"{estring}('googlyboo')", line)
        printed = f.getvalue()
        expected = colour_message(error_message)
        return printed == expected

    def test_plot_data(self):
        error_message = """Data set googlyboo is plotted with incorrect data.
    Check that all variables are correctly defined, and that you are plotting
    the right variables in the right order (i.e. plt.plot(X,Y))"""
        assert(pm._data("googlyboo") == error_message)
        assert(self.checkprint("_data", error_message))

    def test_plot_linestyle(self):
        error_message = """Data set googlyboo is plotted with the incorrect linestyle.
    Set the linestyle with the optional third argument in the plot command e.g.
        plt.plot(X,Y,'--')
    for dashed lines or
        plt.plot(X,Y,'.')
    for dots."""
        assert(pm._linestyle("googlyboo") == error_message)
        assert(self.checkprint("_linestyle", error_message))

    def test_plot_marker(self):
        error_message = """Data set googlyboo is plotted with incorrect markers.
    Set the marker with the optional third argument in the plot command e.g.
        plt.plot(X,Y,'.')
    for points
        plt.plot(X,Y,'o')
    for circles."""
        assert(pm._marker("googlyboo") == error_message)
        assert(self.checkprint("_marker", error_message))

    def test_plot_colour(self):
        error_message = """Data set googlyboo is plotted with the incorrect colour.
    Set the colour with the optional third argument in the plot command e.g.
        plt.plot(X,Y,'k')
    for black or
        plt.plot(X,Y,'r')
    for red."""
        assert(pm._colour("googlyboo") == error_message)
        assert(self.checkprint("_colour", error_message))

    def test_plot_partial(self):
        error_message = """Dataset googlyboo plotted correctly!\n"""
        assert(pm._partial("googlyboo") == error_message)

    def test_plot_success(self):
        from AutoFeedback.bcolors import bcolors
        error_message = f"{bcolors.OKGREEN}Plot is correct!\n{bcolors.ENDC}\n"
        error_message += f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}\n"
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            pr("_success", myline)
        assert(f.getvalue() == error_message)
