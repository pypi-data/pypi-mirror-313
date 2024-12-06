import unittest
import numpy as np

import AutoFeedback.funcchecks as fc


def f2(x):
    return


def f1(x):
    return x**2


f1.inputs = [(1,), (2,), (3,)]


def f3(x, y):
    return (np.sqrt(f1(x)))


class UnitTests(unittest.TestCase):
    def test_1input_vars(self):
        assert (fc._input_vars(f1, 10))

    def test_2input_vars(self):
        assert (fc._input_vars(f3, (10, 11)))

    def test_not1input_vars(self):
        assert (not fc._input_vars(f3, (10, 11, 12)))

    def test_not2input_vars(self):
        assert (not fc._input_vars(f1, (10, 11)))

    def test_returns(self):
        assert (fc._returns(f3, (10, 11)))

    def test_notreturns(self):
        assert (not fc._returns(f2, (10)))

    def test_check_outputs(self):
        assert (fc._check_outputs(f1, (4,), 16))

    def test_2check_outputs(self):
        assert (fc._check_outputs(f1, (-10,), 100))

    def test_array_check_outputs(self):
        assert (fc._check_outputs(f1, (np.array([1, 2, 3]),), [1, 4, 9]))

    def test_notcheck_outputs1(self):
        assert (not fc._check_outputs(f1, (3,), 10))

    def test_notcheck_outputs2(self):
        assert (not fc._check_outputs(f3, (10, 11), 9))

    def test_calls(self):
        assert (fc._check_calls(f3, 'f1'))

    def test_notcalls(self):
        assert (not fc._check_calls(f3, 'f4'))

    def test_returnlist(self):
        def fretlist(x):
            return (1, 2)
        assert fc._returns(fretlist, (1,))

    def test_return_exception(self):
        def raise_exc(x):
            raise TypeError
        with self.assertRaises(Exception):
            fc._returns(raise_exc, (1,))

    def test_nsamples_error(self):
        a = f3
        a.check_value = f1
        with self.assertRaises(RuntimeError) as context:
            fc._check_outputs(f1, (1,), a)
        assert "there should be an attribute" in str(context.exception)

    def test_nsamples_return(self):
        def retlist(a):
            return a
        a = f3
        a.check_value = retlist
        a.nsamples = 2
        y = fc._check_outputs(f1, (1,), a)
        assert y == [1, 1]

    def test_nsamples_exception(self):
        a = f3
        a.check_value = f1
        a.nsamples = 2
        assert not fc._check_outputs(f1, (1,), a)


class SystemTests(unittest.TestCase):
    def test_f1(self):
        assert (fc.check_func('f1', [(3,), (-4,)], [9, 16],
                              output=False) and
                not fc.check_func('f2', [(3,), (-4,)], [9, 16],
                                  output=False))

    def test_f1_handle(self):
        assert (fc.check_func(f1, inputs=[(3,), (-4,)], output=False))

    def test_f1_inputs(self):
        assert (fc.check_func(f1, output=False))

    def test_inputerror(self):
        with self.assertRaises(Exception) as context:
            fc.check_func(f2)

        assert ('check_func with a function handle' in str(context.exception))

    def test_string_inputerror(self):
        with self.assertRaises(Exception) as context:
            fc.check_func('f2')

        assert ('check_func with a function name' in str(context.exception))

    def test_runtime_exception(self):
        import io
        import contextlib
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            fc.check_func('broken_function', [(1,)], [1])
        assert 'The function broken_function does not' in f.getvalue()
