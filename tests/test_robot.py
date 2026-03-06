"""Tests for financial_robot.robot (FinancialRobot)."""

import pytest

from financial_robot.robot import FinancialRobot


@pytest.fixture
def robot():
    return FinancialRobot()


class TestGreetingAndMeta:
    def test_greeting_en(self, robot):
        response = robot.respond("hello")
        assert "Lec01" in response

    def test_greeting_zh(self, robot):
        response = robot.respond("你好")
        assert "财务" in response or "Lec01" in response

    def test_help(self, robot):
        response = robot.respond("help")
        assert "compound interest" in response.lower() or "复利" in response

    def test_exit(self, robot):
        response = robot.respond("bye")
        assert "再见" in response or "Goodbye" in response

    def test_empty_input(self, robot):
        response = robot.respond("")
        assert response  # must return something

    def test_unknown_input(self, robot):
        response = robot.respond("what is the weather today?")
        assert "help" in response.lower() or "抱歉" in response


class TestCompoundInterestIntent:
    def test_full_params_en(self, robot):
        response = robot.respond("compound interest principal=10000 rate=0.05 periods=10")
        assert "16,288" in response or "16288" in response

    def test_missing_params(self, robot):
        response = robot.respond("compound interest principal=1000")
        assert "rate" in response.lower() or "利率" in response


class TestSimpleInterestIntent:
    def test_full_params(self, robot):
        response = robot.respond("simple interest principal=1000 rate=0.05 time=2")
        assert "100" in response  # interest = 100

    def test_missing_params(self, robot):
        response = robot.respond("simple interest principal=1000")
        assert "rate" in response.lower() or "利率" in response


class TestLoanIntent:
    def test_full_params(self, robot):
        response = robot.respond("loan principal=500000 rate=0.045 months=360")
        assert "2,533" in response or "2533" in response

    def test_missing_params(self, robot):
        response = robot.respond("loan principal=100000")
        assert "rate" in response.lower() or "利率" in response


class TestROIIntent:
    def test_full_params(self, robot):
        response = robot.respond("roi gain=500 cost=2000")
        assert "25.00%" in response

    def test_missing_params(self, robot):
        response = robot.respond("roi gain=500")
        assert "cost" in response.lower() or "成本" in response


class TestPresentValueIntent:
    def test_full_params(self, robot):
        response = robot.respond("present value fv=1100 rate=0.1 periods=1")
        assert "1,000" in response or "1000" in response

    def test_missing_params(self, robot):
        response = robot.respond("present value fv=1000")
        assert "rate" in response.lower() or "利率" in response


class TestFutureValueIntent:
    def test_full_params(self, robot):
        response = robot.respond("future value pv=1000 rate=0.1 periods=1")
        assert "1,100" in response or "1100" in response

    def test_missing_params(self, robot):
        response = robot.respond("future value pv=1000")
        assert "rate" in response.lower() or "利率" in response
