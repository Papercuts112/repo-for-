"""Tests for financial_robot.calculator (FinancialCalculator)."""

import math
import pytest

from financial_robot.calculator import FinancialCalculator


class TestCompoundInterest:
    def test_basic(self):
        result = FinancialCalculator.compound_interest(1000, 0.1, 1)
        assert math.isclose(result, 1100.0)

    def test_multi_period(self):
        result = FinancialCalculator.compound_interest(1000, 0.05, 10)
        assert math.isclose(result, 1628.8946267774416)

    def test_zero_rate(self):
        assert FinancialCalculator.compound_interest(5000, 0, 5) == 5000

    def test_zero_periods(self):
        assert FinancialCalculator.compound_interest(5000, 0.1, 0) == 5000

    def test_negative_principal_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            FinancialCalculator.compound_interest(-100, 0.05, 5)

    def test_negative_periods_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            FinancialCalculator.compound_interest(100, 0.05, -1)

    def test_rate_below_minus_one_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.compound_interest(100, -1.5, 5)


class TestSimpleInterest:
    def test_basic(self):
        result = FinancialCalculator.simple_interest(1000, 0.05, 2)
        assert math.isclose(result, 100.0)

    def test_zero_rate(self):
        assert FinancialCalculator.simple_interest(1000, 0, 5) == 0

    def test_negative_principal_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.simple_interest(-100, 0.05, 1)

    def test_negative_rate_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.simple_interest(100, -0.05, 1)

    def test_negative_time_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.simple_interest(100, 0.05, -1)


class TestLoanMonthlyPayment:
    def test_zero_rate(self):
        result = FinancialCalculator.loan_monthly_payment(12000, 0, 12)
        assert math.isclose(result, 1000.0)

    def test_typical_mortgage(self):
        # 500 000 at 4.5% for 30 years
        result = FinancialCalculator.loan_monthly_payment(500_000, 0.045, 360)
        assert math.isclose(result, 2533.43, rel_tol=1e-4)

    def test_negative_principal_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.loan_monthly_payment(-1000, 0.05, 12)

    def test_zero_months_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.loan_monthly_payment(10000, 0.05, 0)

    def test_negative_rate_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.loan_monthly_payment(10000, -0.05, 12)


class TestROI:
    def test_basic(self):
        result = FinancialCalculator.roi(500, 2000)
        assert math.isclose(result, 25.0)

    def test_negative_gain(self):
        result = FinancialCalculator.roi(-200, 1000)
        assert math.isclose(result, -20.0)

    def test_zero_cost_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.roi(100, 0)

    def test_negative_cost_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.roi(100, -500)


class TestPresentValue:
    def test_basic(self):
        result = FinancialCalculator.present_value(1100, 0.1, 1)
        assert math.isclose(result, 1000.0)

    def test_zero_rate(self):
        assert FinancialCalculator.present_value(5000, 0, 10) == 5000

    def test_negative_future_value_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.present_value(-100, 0.05, 5)

    def test_rate_minus_one_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.present_value(1000, -1, 5)


class TestFutureValue:
    def test_basic(self):
        result = FinancialCalculator.future_value(1000, 0.1, 1)
        assert math.isclose(result, 1100.0)

    def test_matches_compound_interest(self):
        pv = 5000
        rate = 0.07
        n = 8
        assert math.isclose(
            FinancialCalculator.future_value(pv, rate, n),
            FinancialCalculator.compound_interest(pv, rate, n),
        )

    def test_negative_pv_raises(self):
        with pytest.raises(ValueError):
            FinancialCalculator.future_value(-100, 0.05, 5)
