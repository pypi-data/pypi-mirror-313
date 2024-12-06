import unittest
import AutoFeedback.variable_error_messages as vc
import io
import contextlib


class UnitTests(unittest.TestCase):
    def test_print(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            assert(vc.output_check("this\\nand that",
                                   executable="test/printtest.py"))

    def test_notprint(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            assert(not vc.output_check("this and that",
                                       executable="test/printtest.py"))
