"""
Define objects for comparison to matplotlib objects. I.E create something with
attributes comparable with matplotlib lines, axes etc. without having to create
a figure.
"""
from AutoFeedback.varchecks import check_value
from AutoFeedback import plot_error_messages


class line:
    """
    generic class for data plotted in a figure

    Attributes
    ----------
    xdata : list/np.array
        x-values for xydata/patch
    ydata : list/np.array
        y-values for xydata/patch
    linestyle : list of strings or None
        linestyles that will be accepted as correct, e.g. ['-', '--', '-.']
    colour : list of colour identifiers or None
       colours that will be accepted as correct
       e.g. ['r','red',(1.0,0.0,0.0,1)])
    label : str
        label attached to data (for legend entry for instance)
    marker : list of strings or None
        markers that will be accepted as correct, e.g. ['.', ',', 'o']
    diagnosis : str
        diagnosis of what is incorrect about the line
    """

    def __init__(self, xdata, ydata, linestyle=None, colour=None,
                 label=None, marker=None):
        self.xdata = xdata
        self.ydata = ydata
        self.linestyle = linestyle
        self.colour = colour
        self.label = label
        self.marker = marker
        self.diagnosis = "ok"

    def get_xydata(self):
        """mimic matplotlib.axes.get_xydata()"""
        return self.xdata, self.ydata

    def check_linedata(self, x, y, no_diagnose=False):
        """determine whether the xy data matches the expected data

        Parameters
        ----------
        x : list or np.array
            expected x data
        y : list or np.array
            expected y data
        no_diagnose : bool
            if True then don't provide any feedback on the comparison.

        Returns
        -------
        bool : True if data matches expected, False otherwise
        """
        goodx, goody = False, False
        if hasattr(self.xdata, "check_value") and\
                callable(self.xdata.check_value):
            goodx = self.xdata.check_value(x)
        else:
            goodx = check_value(x, self.xdata)
        if hasattr(self.ydata, "check_value") and\
                callable(self.ydata.check_value):
            goody = self.ydata.check_value(y)
        else:
            goody = check_value(y, self.ydata)
        if not goodx and not goody:
            self.diagnosis = "badxy"
        elif not goodx:
            self.diagnosis = "badx"
        elif not goody:
            self.diagnosis = "bady"
        if no_diagnose:
            # reset self.diagnose if we are just running check_linedata
            # to get the lines in the right order
            self.diagnosis = "ok"
        return (goodx and goody)

    def generic_error(self, label, axis):
        """Generic error message for incorrect data in plot"""
        return f"""The {axis}-coordinates of the points in the data set
{label} are incorrect

       The instructions in the README file explain the specific values
       for the coordinates of the points in your graph.
       Make sure you have read those instructions carefully and that you
       know what the coordinates of the points in your graph should be"""

    def get_error(self, label):
        """determine the error message to be printed, based on the diagnosis

        Parameters
        ----------
        label : str
            label for the data set to be plotted
        """
        if self.diagnosis == "badxy":
            emsg = plot_error_messages.error_message()
            error_message = emsg._data(label)
        elif self.diagnosis == "badx":
            if hasattr(self.xdata, "get_error") and\
                    callable(self.xdata.get_error):
                error_message = self.xdata.get_error(
                    f"""x coordinates of the data series in the graph labelled
{label}""")
            else:
                error_message = self.generic_error(label, "x")
        elif self.diagnosis == "bady":
            if hasattr(self.ydata, "get_error") and\
                    callable(self.ydata.get_error):
                error_message = self.ydata.get_error(
                    f"""y coordinates of the data series in the graph labelled
{label}""")
            else:
                error_message = self.generic_error(label, "y")
        return error_message
