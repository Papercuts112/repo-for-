"""
Financial calculator module for the Intelligent Financial Robot (Lec01).

Provides core financial computations including compound interest,
loan payment, ROI, and present/future value calculations.
"""


class FinancialCalculator:
    """Performs common financial calculations."""

    @staticmethod
    def compound_interest(principal: float, rate: float, periods: int) -> float:
        """Calculate the future value using compound interest.

        Args:
            principal: Initial investment amount.
            rate: Annual interest rate as a decimal (e.g. 0.05 for 5%).
            periods: Number of compounding periods (years).

        Returns:
            Future value after compounding.

        Raises:
            ValueError: If principal or periods is negative, or rate < -1.
        """
        if principal < 0:
            raise ValueError("Principal must be non-negative.")
        if periods < 0:
            raise ValueError("Periods must be non-negative.")
        if rate < -1:
            raise ValueError("Rate must be greater than or equal to -1.")

        return principal * (1 + rate) ** periods

    @staticmethod
    def loan_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
        """Calculate the fixed monthly payment for a loan (annuity formula).

        Args:
            principal: Loan amount.
            annual_rate: Annual interest rate as a decimal.
            months: Loan term in months.

        Returns:
            Monthly payment amount.

        Raises:
            ValueError: If any argument is non-positive (months/principal) or rate < 0.
        """
        if principal <= 0:
            raise ValueError("Principal must be positive.")
        if months <= 0:
            raise ValueError("Months must be positive.")
        if annual_rate < 0:
            raise ValueError("Annual rate must be non-negative.")

        if annual_rate == 0:
            return principal / months

        monthly_rate = annual_rate / 12
        payment = principal * monthly_rate * (1 + monthly_rate) ** months / (
            (1 + monthly_rate) ** months - 1
        )
        return payment

    @staticmethod
    def roi(gain: float, cost: float) -> float:
        """Calculate Return on Investment (ROI) as a percentage.

        Args:
            gain: Net gain from the investment.
            cost: Initial investment cost (must be > 0).

        Returns:
            ROI as a percentage (e.g. 25.0 means 25%).

        Raises:
            ValueError: If cost is not positive.
        """
        if cost <= 0:
            raise ValueError("Cost must be positive.")
        return (gain / cost) * 100

    @staticmethod
    def present_value(future_value: float, rate: float, periods: int) -> float:
        """Calculate the present value of a future sum.

        Args:
            future_value: The amount to be received in the future.
            rate: Discount rate per period as a decimal.
            periods: Number of periods.

        Returns:
            Present value of the future sum.

        Raises:
            ValueError: If future_value is negative, periods is negative, or rate <= -1.
        """
        if future_value < 0:
            raise ValueError("Future value must be non-negative.")
        if periods < 0:
            raise ValueError("Periods must be non-negative.")
        if rate <= -1:
            raise ValueError("Rate must be greater than -1.")

        return future_value / (1 + rate) ** periods

    @staticmethod
    def future_value(present_value: float, rate: float, periods: int) -> float:
        """Calculate the future value of a present sum.

        Args:
            present_value: Current amount.
            rate: Interest rate per period as a decimal.
            periods: Number of periods.

        Returns:
            Future value after the given number of periods.

        Raises:
            ValueError: If present_value is negative, periods is negative, or rate < -1.
        """
        if present_value < 0:
            raise ValueError("Present value must be non-negative.")
        if periods < 0:
            raise ValueError("Periods must be non-negative.")
        if rate < -1:
            raise ValueError("Rate must be greater than or equal to -1.")

        return present_value * (1 + rate) ** periods

    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> float:
        """Calculate simple interest.

        Args:
            principal: Initial amount.
            rate: Annual interest rate as a decimal.
            time: Time in years.

        Returns:
            Interest earned (not total amount).

        Raises:
            ValueError: If any argument is negative.
        """
        if principal < 0:
            raise ValueError("Principal must be non-negative.")
        if rate < 0:
            raise ValueError("Rate must be non-negative.")
        if time < 0:
            raise ValueError("Time must be non-negative.")

        return principal * rate * time
