"""
Check a student-defined plot matches expected, and provide feedback
"""
from AutoFeedback.varchecks import check_value
import matplotlib.pyplot as plt


def _grab_figure():
    """ get figure handle for plot to be investigated
    Parameters
    ==========

    Returns
    =======
    fighand : matplotlib.pyplot figure handle
    """
    import sys
    from matplotlib.axes._axes import Axes
    fighand = None
    try:
        if any(["kernel_launcher.py" in j for j in sys.argv]):
            try:
                from __main__ import fighand
                if not isinstance(fighand, Axes):
                    raise ImportError
            except ImportError:
                print("""If you are seeing this error, you may have deleted an
important line of code from your notebook: in the code cell where you are
plotting your figure insert the line

fighand = plt.gca()
""")
                raise ImportError
        else:
            plt.ion()  # make any show commands non-blocking
            __import__('main')
            fighand = plt.gca()
            # plt.close() # close any open figures
    except ModuleNotFoundError:
        raise ModuleNotFoundError
    return fighand


def _extract_plot_elements(fighand, lines=True, patches=False,
                           axislabels=False, axes=False, legend=False):
    """Get all relevant attributes of the plot under investigation

    Parameters
    ==========
    fighand : matplotlib.pyplot figure handle
        handle for figure under investigation
    lines : bool
        If True, extract any xy-plotted lines in the figure
    patches : bool
        If True, extract any patches in the figure (e.g. for histrograms)
    axislabels : bool
        If True, extract the axis labels
    axes : bool
        If True, extract the axis limits
    legend : bool
        If True, extract the legend data

    Returns
    =======
    line_data, patch_data, axes_data, labels, legend_data
        these are lists or None, depending on what has been extracted.
    """
    line_data, patch_data, axes_data, labels, legend_data =\
        None, None, None, None, [None]

    if lines:
        line_data = fighand.get_lines()

    if patches:
        patch_data = fighand.patches

    if axes:
        axes_data = [*fighand.get_xlim(), *fighand.get_ylim()]

    if axislabels:
        labels = [fighand.get_xlabel(), fighand.get_ylabel(),
                  fighand.get_title()]

    if legend:
        try:
            legend_data = [x.get_text()
                           for x in fighand.get_legend().get_texts()]
        except AttributeError:
            legend_data = []

    return line_data, patch_data, axes_data, labels, legend_data


def _check_linestyle(line, expected):
    """check whether the linestyle of line (matplotlib.lines.Line2D) matches
    any of expected (list of strings, e.g. ['-', '--', '-.'])"""
    style = line.get_linestyle()
    return (style in expected)


def _check_marker(line, expected):
    """check whether the marker of line (matplotlib.lines.Line2D) matches any
    of expected (list of strings, e.g. ['.', ',', 'o'])"""
    style = line.get_marker()
    return (style in expected)


def _check_colour(line, expected):
    """check whether the colour of line (matplotlib.lines.Line2D) matches any
    of expected (list of colour identifiers, e.g. ['r','red',(1.0,0.0,0.0,1)])
    """
    color = line.get_color()
    return (color in expected)


def _check_linedata(line, expline, no_diagnose=False):
    """check whether the data in line (matplotlib.lines.Line2D) matches with
    expline (plotclass.line)

    optionally, if no_diagnose==True, then don't provide any feedback on the
    comparison. This is necessary for sorting the lines into the correct order
    if there are multiple lines, we must check repeatedly if the lines match,
    and only want to provide feedback once we are sure we're comparing the
    correct lines.
    """
    x, y = zip(*line.get_xydata())
    return expline.check_linedata(x, y, no_diagnose)


def _check_patchdata(patch, exppatch):
    """check whether the data in patch (matplotlib.patches.Patch) matches with
    exppatch (plotclass.line)
    """
    x, y = [], []
    for p in patch:
        xd, yd = p.get_xy()
        yd = p.get_height()
        x.append(xd + 0.5 * p.get_width())
        y.append(yd)
    return exppatch.check_linedata(x, y)


def _check_legend(legend_data, expected):
    """check whether the data in legend_data (list) matches with
    expected (list)
    """
    return legend_data and check_value(legend_data, expected)


def _check_axes(l1, l2):
    """check whether axis limits (l1) match expected (l2)"""
    return check_value(l1, l2)


def _reorder(a, b):
    """given two lists of lines, a and b, reorder a until it matches b, or we
    fail to find a match. This way, if students plot data sets in a different
    order than expected, we can still check the data"""
    from itertools import permutations
    for perm in permutations(b):
        if (all([_check_linedata(x, y, no_diagnose=True)
                 for x, y in zip(perm, a)])):
            return (perm)
    return b


def _e_string(error, label):
    """ construct an error string comprising the specific fault with the plot
    and the label of the object at fault. E.G data_('xyline')
    """
    if label:
        return f'{error}("{label}")'
    else:
        return f"{error}('')"


def check_plot(explines, exppatch=None, explabels=None, expaxes=None,
               explegend=False, output=False, check_partial=False):
    """given information on a plot which the student has been asked to
    produce, check whether it has been done correctly, and provide feedback

    Parameters
    ==========
    explines : list of plotclass.line
        the lines we expect to be plotted in the figure
    exppatch : list of plotclass.line  or None
        any patches we expect to be plotted in the figure
        (e.g. for histrograms)
    explabels : list or None
        expected axis labels [x-label, y-label, title]
    expaxes : list or None
        expected axis limits [x_low, x_high, y_low, y_high]
    explegend : list or None
        expected legend entries
    output : bool
        if True, print output to screen. otherwise execute quietly
    check_partial : bool
        if more than one line is to be plotted, check only whether at least one
        has been plotted

    Returns
    =======
    bool: True if plot looks as expected (or partially if check_partial),
    False otherwise.
    """
    from AutoFeedback.plot_error_messages import print_error_message
    from itertools import zip_longest

    try:
        fighand = _grab_figure()
        lines, patch, axes, labels, legends =\
            _extract_plot_elements(fighand, lines=(len(explines) > 0),
                                   patches=exppatch, axes=bool(expaxes),
                                   axislabels=bool(explabels),
                                   legend=explegend)
        explegends = [line.label for line in explines
                      if line.label is not None]
        if explines:
            expline = explines[0]
        else:
            expline = exppatch

        if not check_partial:
            if explines:
                assert (len(lines) == len(explines)
                        ), _e_string("_datasets", "")
            if explegend:
                assert (len(legends) == len(explegends)
                        ), _e_string("_legend", "")

        if (explines and not lines):
            assert (False), "_datasets"

        if (explines):
            lines = _reorder(explines, lines)

            for line, expline, legend in zip_longest(lines, explines, legends):
                if expline:
                    assert (_check_linedata(line, expline)), _e_string(
                        "_data", expline.label)
                    if expline.linestyle:
                        assert (_check_linestyle(line, expline.linestyle)
                                ), _e_string("_linestyle", expline.label)
                    if expline.marker:
                        assert (_check_marker(line, expline.marker)
                                ), _e_string("_marker", expline.label)
                    if expline.colour:
                        assert (_check_colour(line, expline.colour)
                                ), _e_string("_colour", expline.label)
                    if expline.label and explegend:
                        if line.get_label()[0] != "_":
                            assert (_check_legend(line.get_label(),
                                                  expline.label)), \
                                _e_string("_legend", expline.label)
                        else:
                            assert (_check_legend(legend, expline.label)), \
                                _e_string("_legend", expline.label)
                    if output:
                        print_error_message(
                            _e_string("_partial", expline.label), expline)
        if (exppatch):
            assert (_check_patchdata(patch, exppatch)), _e_string("_data", "")
            if output:
                print_error_message(_e_string("_partial", ""), exppatch)
        if not explines and not exppatch:
            assert (False), "_data"
        if explabels:
            if len(explabels) == 2:
                explabels.append("")
            assert (_check_axes(labels, explabels)), _e_string("_labels", "")
        if expaxes:
            assert (_check_axes(axes, expaxes)), _e_string("_axes", "")
        if output:
            print_error_message("_success", expline)
        return True
    except AssertionError as error:
        if output:
            print_error_message(error, expline)
        return False
