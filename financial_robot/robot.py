"""
Intent recognition and response module for the Intelligent Financial Robot (Lec01).

Parses natural-language queries (English and Chinese) and dispatches them to
the appropriate FinancialCalculator method.
"""

import re
from typing import Optional

from .calculator import FinancialCalculator


# ---------------------------------------------------------------------------
# Intent definitions
# ---------------------------------------------------------------------------

INTENTS = {
    "compound_interest": [
        r"compound\s+interest",
        r"复利",
        r"future\s+value.*invest",
        r"invest.*future\s+value",
    ],
    "simple_interest": [
        r"simple\s+interest",
        r"单利",
    ],
    "loan": [
        r"loan",
        r"mortgage",
        r"月供",
        r"贷款",
        r"repayment",
    ],
    "roi": [
        r"\broi\b",
        r"return\s+on\s+invest",
        r"投资回报",
        r"收益率",
    ],
    "future_value": [
        r"future\s+value",
        r"\bfv\b(?!\s*=)",
        r"终值",
        r"未来价值",
    ],
    "present_value": [
        r"present\s+value",
        r"\bpv\b(?!\s*=)",
        r"现值",
    ],
    "help": [
        r"\bhelp\b",
        r"帮助",
        r"功能",
        r"what\s+can\s+you",
        r"how\s+to\s+use",
    ],
    "greeting": [
        r"^(hi|hello|hey|你好|您好|嗨)[\s!！。]*$",
    ],
    "exit": [
        r"^(exit|quit|bye|再见|退出|拜拜)[\s!！。]*$",
    ],
}

HELP_TEXT = """\
智能财务机器人 Lec01 — 功能列表 / Available Features:
  1. 复利计算   (compound interest)  : compound interest principal=<P> rate=<R> periods=<N>
  2. 单利计算   (simple interest)    : simple interest principal=<P> rate=<R> time=<T>
  3. 贷款月供   (loan payment)       : loan principal=<P> rate=<R> months=<M>
  4. 投资回报率 (ROI)                : roi gain=<G> cost=<C>
  5. 现值计算   (present value)      : present value fv=<FV> rate=<R> periods=<N>
  6. 终值计算   (future value)       : future value pv=<PV> rate=<R> periods=<N>

示例 / Examples:
  compound interest principal=10000 rate=0.05 periods=10
  loan principal=500000 rate=0.045 months=360
  roi gain=2000 cost=10000
"""


def _extract(text: str, *keys: str) -> Optional[float]:
    """Extract a numeric value for the first matching key in *text*."""
    for key in keys:
        match = re.search(
            r"(?:^|\s|,|，)" + re.escape(key) + r"\s*[=:]\s*([-\d.]+)",
            text,
            re.IGNORECASE,
        )
        if match:
            return float(match.group(1))
    return None


def _match_intent(text: str) -> Optional[str]:
    """Return the intent name for *text*, or None if unknown."""
    lower = text.lower()
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                return intent
    return None


class FinancialRobot:
    """Conversational interface for the intelligent financial robot."""

    def __init__(self) -> None:
        self._calc = FinancialCalculator

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def respond(self, user_input: str) -> str:
        """Return a response string for the given *user_input*.

        Args:
            user_input: Raw text from the user.

        Returns:
            A human-readable response string.
        """
        text = user_input.strip()
        if not text:
            return "请输入您的问题 / Please enter your query."

        intent = _match_intent(text)

        if intent == "greeting":
            return "您好！我是智能财务机器人 Lec01。输入 'help' 查看支持的功能。\nHello! I am the Intelligent Financial Robot Lec01. Type 'help' to see available features."

        if intent == "exit":
            return "再见！感谢使用智能财务机器人。\nGoodbye! Thank you for using the Intelligent Financial Robot."

        if intent == "help":
            return HELP_TEXT

        if intent == "compound_interest":
            return self._handle_compound_interest(text)

        if intent == "simple_interest":
            return self._handle_simple_interest(text)

        if intent == "loan":
            return self._handle_loan(text)

        if intent == "roi":
            return self._handle_roi(text)

        if intent == "present_value":
            return self._handle_present_value(text)

        if intent == "future_value":
            return self._handle_future_value(text)

        return (
            "抱歉，我还不理解您的问题。输入 'help' 查看支持的功能。\n"
            "Sorry, I don't understand your query. Type 'help' to see available features."
        )

    def chat(self) -> None:
        """Start an interactive command-line chat session."""
        print("=" * 60)
        print("  智能财务机器人 Lec01 / Intelligent Financial Robot Lec01")
        print("=" * 60)
        print("输入 'help' 查看功能列表，输入 'exit' 退出。")
        print("Type 'help' for features, 'exit' to quit.\n")

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见！ / Goodbye!")
                break

            response = self.respond(user_input)
            print(f"Robot: {response}\n")

            if _match_intent(user_input) == "exit":
                break

    # ------------------------------------------------------------------
    # Intent handlers
    # ------------------------------------------------------------------

    def _handle_compound_interest(self, text: str) -> str:
        principal = _extract(text, "principal", "本金", "p")
        rate = _extract(text, "rate", "利率", "r")
        periods = _extract(text, "periods", "期数", "年数", "n")

        if None in (principal, rate, periods):
            return (
                "请提供: principal(本金), rate(利率), periods(期数)\n"
                "Example: compound interest principal=10000 rate=0.05 periods=10"
            )

        try:
            result = self._calc.compound_interest(principal, rate, int(periods))
            return (
                f"复利终值 / Compound Interest Future Value:\n"
                f"  本金 Principal : {principal:,.2f}\n"
                f"  年利率 Rate    : {rate * 100:.2f}%\n"
                f"  期数 Periods   : {int(periods)} years\n"
                f"  终值 Result    : {result:,.2f}"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"

    def _handle_simple_interest(self, text: str) -> str:
        principal = _extract(text, "principal", "本金", "p")
        rate = _extract(text, "rate", "利率", "r")
        time = _extract(text, "time", "时间", "t")

        if None in (principal, rate, time):
            return (
                "请提供: principal(本金), rate(利率), time(时间/年)\n"
                "Example: simple interest principal=10000 rate=0.05 time=3"
            )

        try:
            result = self._calc.simple_interest(principal, rate, time)
            return (
                f"单利计算 / Simple Interest:\n"
                f"  本金 Principal : {principal:,.2f}\n"
                f"  年利率 Rate    : {rate * 100:.2f}%\n"
                f"  时间 Time      : {time} years\n"
                f"  利息 Interest  : {result:,.2f}\n"
                f"  总额 Total     : {principal + result:,.2f}"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"

    def _handle_loan(self, text: str) -> str:
        principal = _extract(text, "principal", "本金", "贷款金额", "p")
        rate = _extract(text, "rate", "利率", "r")
        months = _extract(text, "months", "月数", "期限", "m")

        if None in (principal, rate, months):
            return (
                "请提供: principal(贷款金额), rate(年利率), months(还款月数)\n"
                "Example: loan principal=500000 rate=0.045 months=360"
            )

        try:
            payment = self._calc.loan_monthly_payment(principal, rate, int(months))
            total = payment * int(months)
            interest = total - principal
            return (
                f"贷款月供计算 / Loan Monthly Payment:\n"
                f"  贷款金额 Principal    : {principal:,.2f}\n"
                f"  年利率 Annual Rate    : {rate * 100:.2f}%\n"
                f"  还款期数 Months       : {int(months)}\n"
                f"  月供 Monthly Payment  : {payment:,.2f}\n"
                f"  还款总额 Total Paid   : {total:,.2f}\n"
                f"  总利息 Total Interest : {interest:,.2f}"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"

    def _handle_roi(self, text: str) -> str:
        gain = _extract(text, "gain", "收益", "g")
        cost = _extract(text, "cost", "成本", "投入", "c")

        if None in (gain, cost):
            return (
                "请提供: gain(净收益), cost(投入成本)\n"
                "Example: roi gain=2000 cost=10000"
            )

        try:
            result = self._calc.roi(gain, cost)
            return (
                f"投资回报率 / Return on Investment (ROI):\n"
                f"  净收益 Gain : {gain:,.2f}\n"
                f"  成本 Cost   : {cost:,.2f}\n"
                f"  ROI         : {result:.2f}%"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"

    def _handle_present_value(self, text: str) -> str:
        fv = _extract(text, "fv", "future_value", "终值", "未来价值")
        rate = _extract(text, "rate", "利率", "r")
        periods = _extract(text, "periods", "期数", "n")

        if None in (fv, rate, periods):
            return (
                "请提供: fv(终值), rate(折现率), periods(期数)\n"
                "Example: present value fv=15000 rate=0.05 periods=10"
            )

        try:
            result = self._calc.present_value(fv, rate, int(periods))
            return (
                f"现值计算 / Present Value:\n"
                f"  终值 Future Value : {fv:,.2f}\n"
                f"  折现率 Rate       : {rate * 100:.2f}%\n"
                f"  期数 Periods      : {int(periods)}\n"
                f"  现值 PV           : {result:,.2f}"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"

    def _handle_future_value(self, text: str) -> str:
        pv = _extract(text, "pv", "present_value", "现值")
        rate = _extract(text, "rate", "利率", "r")
        periods = _extract(text, "periods", "期数", "n")

        if None in (pv, rate, periods):
            return (
                "请提供: pv(现值), rate(利率), periods(期数)\n"
                "Example: future value pv=10000 rate=0.05 periods=10"
            )

        try:
            result = self._calc.future_value(pv, rate, int(periods))
            return (
                f"终值计算 / Future Value:\n"
                f"  现值 Present Value : {pv:,.2f}\n"
                f"  年利率 Rate        : {rate * 100:.2f}%\n"
                f"  期数 Periods       : {int(periods)}\n"
                f"  终值 FV            : {result:,.2f}"
            )
        except ValueError as exc:
            return f"输入错误 / Input error: {exc}"
