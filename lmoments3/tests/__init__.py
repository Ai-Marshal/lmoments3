import unittest
import lmoments3 as lm
from lmoments3 import distr
from lmoments3 import stats
from numpy.testing import assert_almost_equal


class DistributionTestCase(unittest.TestCase):
    dist = None
    paras = {}
    distr_f = None
    inputs_qua = [0.2, 0.5, 0.8]
    inputs_cdf = [2, 5, 8]
    inputs_pdf = [4, 5, 6, 7]

    @classmethod
    def setUpClass(cls):
        cls.testdata = [2.0, 3.0, 4.0, 2.4, 5.5, 1.2, 5.4, 2.2, 7.1, 1.3, 1.5]
        cls.lmu = lm.samlmu(cls.testdata)
        if cls.dist:
            cls.distr_f = getattr(distr, cls.dist)
        super(DistributionTestCase, cls).setUpClass()

    def assertAlmostEqual(self, first, second, places=6):
        return assert_almost_equal(first, second, decimal=places)

    def test_n_paras(self):
        if self.dist:
            n = stats.distr_n_params(self.dist)
            self.assertEqual(len(self.paras), n)

    def test_fit(self):
        if self.distr_f:
            result = self.distr_f.lmom_fit(self.testdata)
            for para in iter(self.paras):
                self.assertAlmostEqual(result[para], self.paras[para])

    def test_lmom(self):
        if self.dist:
            f = getattr(lm, 'lmom' + self.dist)
            lmom = f(self.correct_fit)
            self.assertAlmostEqual(lmom, self.correct_lmom)

    def test_lmr(self):
        if self.dist:
            f = getattr(lm, 'lmr' + self.dist)
            lmr = f(self.correct_fit, 4)
            self.assertAlmostEqual(lmr, self.correct_lmr)

    def test_nlogl(self):
        if self.dist:
            nlogl = stats.neg_log_lik(self.testdata, self.dist)
            self.assertAlmostEqual(self.correct_nlogl, nlogl)

    def test_qua(self):
        if self.distr_f:
            d = self.distr_f(**self.paras)
            qua = [d.ppf(self.inputs_qua[0]),
                   d.ppf(self.inputs_qua[1]),
                   d.ppf(self.inputs_qua[2])]
            qua2 = d.ppf(self.inputs_qua)
            self.assertAlmostEqual(qua, self.correct_qua)
            self.assertAlmostEqual(qua2, self.correct_qua)

    def test_cdf(self):
        if self.distr_f:
            d = self.distr_f(**self.paras)
            cdf = [d.cdf(self.inputs_cdf[0]),
                   d.cdf(self.inputs_cdf[1]),
                   d.cdf(self.inputs_cdf[2])]
            cdf2 = d.cdf(self.inputs_cdf)
            self.assertAlmostEqual(cdf, self.correct_cdf)
            self.assertAlmostEqual(cdf2, self.correct_cdf)

    def test_pdf(self):
        if self.distr_f:
            d = self.distr_f(**self.paras)
            pdf = [d.pdf(self.inputs_pdf[0]),
                   d.pdf(self.inputs_pdf[1]),
                   d.pdf(self.inputs_pdf[2]),
                   d.pdf(self.inputs_pdf[3])]
            pdf2 = d.pdf(self.inputs_pdf)
            self.assertAlmostEqual(self.correct_pdf, pdf)
            self.assertAlmostEqual(self.correct_pdf, pdf2)

    def test_rand(self):
        if self.distr_f:
            d = self.distr_f(**self.paras)
            rand = d.rvs(size=10)
            self.assertEqual(len(rand), 10)
