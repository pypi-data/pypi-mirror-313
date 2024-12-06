import unittest
import scipy.stats
import numpy as np
from AutoFeedback.randomclass import randomvar as rv


class VarErrorTests(unittest.TestCase):
    def test_integer(self):
        r = rv(expectation=0)
        r.diagnosis = "integer"
        error_message = """The googlyboo should only take integer values
             You should be generating integer valued discrete random variables
             Your random variables should thus only ever take integer values
             """
        assert (error_message == r.get_error("googlyboo"))

    def test_range(self):
        r = rv(expectation=0, vmin=-1, vmax=1)
        r.diagnosis = "range"
        error_message = """The googlyboo fall outside the allowed range of
values for this type of random variable"""
        error_message += """\n The random variable should be between
 -1 and 1"""
        assert (error_message == r.get_error("googlyboo"))

    def test_range_up(self):
        r = rv(expectation=0, vmin=-1)
        r.diagnosis = "range"
        error_message = """The googlyboo fall outside the allowed range of values for this
 type of random variable"""
        error_message += """\n The random variable should be greater
 than or equal to -1"""
        assert (error_message[-1] == r.get_error("googlyboo")[-1])

    def test_range_lo(self):
        r = rv(expectation=0, vmax=-1)
        r.diagnosis = "range"
        error_message = """The googlyboo fall outside the allowed range of values for this
 type of random variable"""
        error_message += """\n The random variable should be less
 than or equal to -1"""
        assert (error_message[-1] == r.get_error("googlyboo")[-1])

    def test_hypo(self):
        r = rv(expectation=0)
        r.diagnosis = "hypothesis"
        r.pval = 0.06
        error_message = f"The p-value for the hypothesis test on googlyboo is 0.06"

        assert (error_message == r.get_error("googlyboo"))

        r.pval = 0.01
        error_message = f"The p-value for the hypothesis test on googlyboo is 0.01"
        error_message += """

    To test if you generating a random variable from the correct
    distribution the test code performs a series of hypothesis tests.
    In these tests the null hypothesis is that you are sampling from the
    desired distribution and the alternative is that you are not
    sampling the correct distribution.  The p value reported above gives
    the probability that your code would have generated the value it did
    under the assumption that the null hypothesis is true.  In other
    words, it is the probablity that your program is correct.  The
    pvalue should, therefore, be large.

    In statistics it is common practise to reject the null hypothesis in
    favour of the alternative when the pvalue is less than 5%.  However,
    there is always a finite probability that you will get a small p
    value even if your code is correct. If your p-value is very small
    then you should thus run the calculation again to check whether the
    hypothesis test is giving a type I error.  If your p-value is still
    very small then your code is most likely wrong.
    """
        assert (error_message == r.get_error("googlyboo"))

    def test_number(self):
        r = rv(expectation=0)
        r.diagnosis = "number"
        error_message = """The googlyboo is not generating the correct number
of random variables

            You should be generating a vector that contains multiple random
            variables in this object
            """
        assert (error_message == r.get_error("googlyboo"))

    def test_conf_error(self):
        r = rv(expectation=0)
        r.diagnosis = "conf_number"
        error_message = """The googlyboo is not generating the correct number
of random variables.

            googlyboo should return three random variables.  The first of these
            is the lower bound for the confidence limit.  The second is the
            sample mean and the third is the upper bound for the confidence
            limit
            """
        assert (error_message == r.get_error("googlyboo"))

    def test_unc_error(self):
        r = rv(expectation=0)
        r.diagnosis = "uncertainty_number"
        error_message = """The googlyboo is not generating the correct number
of random variables.

            googlyboo should return two random variables.  The first of these
            is the sample mean and the second is the width of the error bar
            for the specified confidence interval around the sample mean
            """
        assert (error_message == r.get_error("googlyboo"))

    def test_length(self):
        r = rv(expectation=0, vmin=0, vmax=1)
        r2 = rv(expectation=[0, 0, 0], vmin=[0, 0, 0], vmax=[1, 1, 1])
        message = """normal random variable between 0 and 1 with expectation 0"""
        assert (message == str(r) and len(r) == 1 and len(r2) == 3)

    def test_bernoulli(self):
        r = rv(expectation=0, variance=0.5, vmin=0, vmax=1, isinteger=True)
        assert (r.check_value(0) and r.check_value(1) and not r.check_value(
            0.5) and not r.check_value(-1) and not r.check_value(2))

    def test_vmin_only(self):
        r = rv(expectation=0, variance=1, vmin=0)
        assert (r.check_value(0) and r.check_value(
            1) and not r.check_value(-1))

    def test_vmax_only(self):
        r = rv(expectation=0, variance=1, vmax=1)
        assert (r.check_value(-1) and r.check_value(1)
                and not r.check_value(2))

    def test_multiple_bernoulli(self):
        r = rv(expectation=0.5, variance=0.25, vmin=0, vmax=1, isinteger=True)
        assert (r.check_value([0, 1, 0]) and not r.check_value(
            [0, 1, 2]) and not r.check_value([0, 1, -1]) and not r.check_value([0, 1, 0.5]))

    def test_bernoulli_vector(self):
        r = rv(expectation=[0, 0, 0], variance=[0.5, 0.5, 0.5], vmin=[
               0, 0, 0], vmax=[1, 1, 1], isinteger=[True, True, True])
        assert (r.check_value([0, 1, 0]) and not r.check_value(
            [0, 0, 0.5]) and not r.check_value([0, 1, 2]) and not r.check_value([0, 1, -1]))

    def test_vector(self):
        r = rv(expectation=[0, 0, 0], variance=[
               1, 1, 1], isinteger=[False, False, False])
        assert (r.check_value([0, 0, 0]) and not r.check_value([0]))

    def test_single_normal(self):
        r = rv(expectation=0, variance=1)
        assert r.check_value(scipy.stats.norm.ppf(0.026))
        r = rv(expectation=0, variance=1)
        assert (not r.check_value(scipy.stats.norm.ppf(0.002)))
        r = rv(expectation=0, variance=1)
        assert r.check_value(scipy.stats.norm.ppf(0.974))
        r = rv(expectation=0, variance=1)
        assert not r.check_value(scipy.stats.norm.ppf(0.98))

    def test_correct_multiple_normal(self):
        r = rv(expectation=[0, 0, 0], variance=[
               1, 1, 1], isinteger=[False, False, False])
        vals1 = [scipy.stats.norm.ppf(0.026), scipy.stats.norm.ppf(
            0.5), scipy.stats.norm.ppf(0.974)]
        vals2 = [scipy.stats.norm.ppf(0.02), scipy.stats.norm.ppf(
            0.02), scipy.stats.norm.ppf(0.005)]
        vals3 = [scipy.stats.norm.ppf(0.02), scipy.stats.norm.ppf(
            0.02), scipy.stats.norm.ppf(0.998)]
        assert (r.check_value(vals1) and not r.check_value(
            vals2) and not r.check_value(vals3))

    def test_correct_meanconv(self):
        r, vals = rv(expectation=0, variance=1, meanconv=True), []
        for i in range(1, 200):
            if np.random.uniform(0, 1) < 0.5:
                vals.append(scipy.stats.norm.ppf(
                    0.026, loc=0, scale=np.sqrt(1/i)))
            else:
                vals.append(scipy.stats.norm.ppf(
                    0.974, loc=0, scale=np.sqrt(1/i)))
        vals2 = []
        for i in range(1, 200):
            if np.random.uniform(0, 1) < 0.5:
                vals2.append(scipy.stats.norm.ppf(
                    0.002, loc=0, scale=np.sqrt(1/i)))
            else:
                vals2.append(scipy.stats.norm.ppf(
                    0.998, loc=0, scale=np.sqrt(1/i)))
        assert (r.check_value(vals) and not r.check_value(vals2))

    def test_correct_varconv(self):
        r, vals = rv(expectation=0, variance=1, dist="chi2", meanconv=True), []
        for i in range(1, 200):
            if np.random.uniform(0, 1) < 0.5:
                vals.append(scipy.stats.chi2.ppf(0.1, i-1)/(i-1))
            else:
                vals.append(scipy.stats.chi2.ppf(0.9, i-1)/(i-1))
        vals2 = []
        for i in range(1, 200):
            if np.random.uniform(0, 1) < 0.5:
                vals2.append(scipy.stats.chi2.ppf(0.002, i-1))
            else:
                vals2.append(scipy.stats.chi2.ppf(0.998, i-1)/(i-1))
        assert (r.check_value(vals) and not r.check_value(vals2)/(i-1))

    def test_single_chi2(self):
        r = rv(expectation=0, variance=1, dist="chi2", dof=5)
        assert r.check_value(scipy.stats.chi2.ppf(0.06, 5)/5)
        assert (not r.check_value(scipy.stats.chi2.ppf(0.005, 5)/5))
        r = rv(expectation=0, variance=1, dist="chi2", dof=5)
        assert r.check_value(scipy.stats.chi2.ppf(0.94, 5)/5)
        assert (not r.check_value(scipy.stats.chi2.ppf(0.998, 5)/5))

    def test_multiple_chi2(self):
        r = rv(expectation=[0, 0, 0], variance=[1, 1, 1],
               dist="chi2", dof=10, isinteger=[False, False, False])
        vals1 = [scipy.stats.chi2.ppf(
            0.06, 10)/10, scipy.stats.chi2.ppf(0.5, 10)/10, scipy.stats.chi2.ppf(0.94, 10)/10]
        vals2 = [scipy.stats.chi2.ppf(
            0.02, 10)/10, scipy.stats.chi2.ppf(0.02, 10)/10, scipy.stats.chi2.ppf(0.005, 10)/10]
        vals3 = [scipy.stats.chi2.ppf(
            0.02, 10)/10, scipy.stats.chi2.ppf(0.02, 10)/10, scipy.stats.chi2.ppf(0.998, 10)/10]
        assert (r.check_value(vals1) and not r.check_value(
            vals2) and not r.check_value(vals3))

    def test_single_conf(self):
        r, pref = rv(expectation=0, variance=1, dist="chi2",
                     dof=5, limit=0.5), scipy.stats.norm.ppf(0.75)
        goodvar1, goodvar2 = scipy.stats.chi2.ppf(
            0.06, 5)/5, scipy.stats.chi2.ppf(0.94, 5)/5
        badvar1, badvar2 = scipy.stats.chi2.ppf(
            0.005, 5)/5, scipy.stats.chi2.ppf(0.998, 5)/5
        assert r.check_value(pref*np.sqrt(goodvar1))
        assert (not r.check_value(pref*np.sqrt(badvar1)))
        r, pref = rv(expectation=0, variance=1, dist="chi2",
                     dof=5, limit=0.5), scipy.stats.norm.ppf(0.75)
        assert r.check_value(pref*np.sqrt(goodvar2))
        assert (not r.check_value(pref*np.sqrt(badvar2)))

    def test_conflim(self):
        r, pref = rv(expectation=0, variance=1, dist="conf_lim",
                     dof=9, limit=0.90), scipy.stats.norm.ppf(0.95)
        goodmean1, goodmean2 = scipy.stats.norm.ppf(
            0.1), scipy.stats.norm.ppf(0.9)
        badmean1, badmean2 = scipy.stats.norm.ppf(
            0.005), scipy.stats.norm.ppf(0.998)
        goodvar1, goodvar2 = scipy.stats.chi2.ppf(
            0.1, 9)/9, scipy.stats.chi2.ppf(0.9, 9)/9
        badvar1, badvar2 = scipy.stats.chi2.ppf(
            0.005, 9)/9, scipy.stats.chi2.ppf(0.998, 9)/9
        assert (r.check_value(
            [goodmean1-pref*np.sqrt(goodvar1), goodmean1, goodmean1+pref*np.sqrt(goodvar2)]) and
            r.check_value([goodmean2-pref*np.sqrt(goodvar2), goodmean2, goodmean2+pref*np.sqrt(goodvar1)]) and
            not r.check_value([goodmean1-pref*np.sqrt(goodvar1), badmean1, goodmean1+pref*np.sqrt(goodvar2)]) and
            not r.check_value([goodmean2-pref*np.sqrt(goodvar2), badmean2, goodmean2+pref*np.sqrt(goodvar1)]) and
            not r.check_value([goodmean1-pref*np.sqrt(badvar1), goodmean1, goodmean1+pref*np.sqrt(goodvar2)]) and
            not r.check_value([goodmean2-pref*np.sqrt(goodvar1), goodmean2, goodmean2+pref*np.sqrt(badvar2)]) and
            not r.check_value([goodmean2-pref*np.sqrt(goodvar1), goodmean2]))

    def test_uncertainty(self):
        r, pref = rv(expectation=0, variance=1, dist="uncertainty",
                     dof=16, limit=0.80), scipy.stats.norm.ppf(0.9)
        goodmean1, goodmean2 = scipy.stats.norm.ppf(
            0.06), scipy.stats.norm.ppf(0.94)
        badmean1, badmean2 = scipy.stats.norm.ppf(
            0.005), scipy.stats.norm.ppf(0.998)
        goodvar1, goodvar2 = scipy.stats.chi2.ppf(
            0.06, 16)/16, scipy.stats.chi2.ppf(0.94, 16)/16
        badvar1, badvar2 = scipy.stats.chi2.ppf(
            0.005, 16)/16, scipy.stats.chi2.ppf(0.998, 16)/16
        assert r.check_value([goodmean1, pref*np.sqrt(goodvar1)])
        assert r.check_value([goodmean2, pref*np.sqrt(goodvar2)])
        r, pref = rv(expectation=0, variance=1, dist="uncertainty",
                     dof=16, limit=0.80), scipy.stats.norm.ppf(0.9)
        assert not r.check_value([badmean1, pref*np.sqrt(goodvar1)])
        assert not r.check_value([badmean2, pref*np.sqrt(goodvar2)])
        r, pref = rv(expectation=0, variance=1, dist="uncertainty",
                     dof=16, limit=0.80), scipy.stats.norm.ppf(0.9)
        assert not r.check_value([goodmean1, pref*np.sqrt(badvar1)])
        assert not r.check_value([goodmean2, pref*np.sqrt(badvar2)])
        r, pref = rv(expectation=0, variance=1, dist="uncertainty",
                     dof=16, limit=0.80), scipy.stats.norm.ppf(0.9)
        assert not r.check_value(
            [goodmean1-pref*np.sqrt(goodvar1), goodmean1, goodmean1+pref*np.sqrt(goodvar2)])
