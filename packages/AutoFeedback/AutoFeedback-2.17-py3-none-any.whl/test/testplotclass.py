import unittest
from AutoFeedback.plotclass import line

line1 = line([0, 1], [0, 1], label="xdata")


class UnitTests(unittest.TestCase):
    def test_generic_error(self):
        expected = """The giggle-coordinates of the points in the data set
google are incorrect

       The instructions in the README file explain the specific values
       for the coordinates of the points in your graph.
       Make sure you have read those instructions carefully and that you
       know what the coordinates of the points in your graph should be"""
        assert line1.generic_error("google", "giggle") == expected

    def test_get_badxy(self):
        line1.diagnosis = "badxy"
        expected = """Data set google is plotted with incorrect data.
    Check that all variables are correctly defined, and that you are plotting
    the right variables in the right order (i.e. plt.plot(X,Y))"""
        assert line1.get_error("google") == expected

    def test_get_badx_get_error(self):
        class dummy_xdata:
            self.data = [0, 1]
            def get_error(self, emsg):
                return emsg
        line2 = line([0, 1], [0, 1], label="xdata")
        line2.diagnosis = "badx"
        line2.xdata = dummy_xdata()
        expected = """x coordinates of the data series in the graph labelled
googly"""
        assert line2.get_error("googly") == expected

    def test_badx_generic_error(self):
        line1.diagnosis = "badx"
        expected = """The x-coordinates of the points in the data set
google are incorrect

       The instructions in the README file explain the specific values
       for the coordinates of the points in your graph.
       Make sure you have read those instructions carefully and that you
       know what the coordinates of the points in your graph should be"""
        assert line1.get_error("google") == expected

    def test_get_bady_get_error(self):
        class dummy_ydata:
            self.data = [0, 1]
            def get_error(self, emsg):
                return emsg
        line2 = line([0, 1], [0, 1], label="xdata")
        line2.diagnosis = "bady"
        line2.ydata = dummy_ydata()
        expected = """y coordinates of the data series in the graph labelled
googly"""
        assert line2.get_error("googly") == expected

    def test_bady_generic_error(self):
        line1.diagnosis = "bady"
        expected = """The y-coordinates of the points in the data set
google are incorrect

       The instructions in the README file explain the specific values
       for the coordinates of the points in your graph.
       Make sure you have read those instructions carefully and that you
       know what the coordinates of the points in your graph should be"""
        assert line1.get_error("google") == expected
