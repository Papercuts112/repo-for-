"""Entry point for the Intelligent Financial Robot (Lec01)."""

from financial_robot import FinancialRobot


def main() -> None:
    robot = FinancialRobot()
    robot.chat()


if __name__ == "__main__":
    main()
