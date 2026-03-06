# 智能财务机器人 Lec01 — Intelligent Financial Robot

A beginner-friendly Python chatbot that answers common financial questions and performs financial calculations through a conversational interface (English & Chinese).

## Features

| Function | Chinese | Example query |
|---|---|---|
| Compound Interest | 复利计算 | `compound interest principal=10000 rate=0.05 periods=10` |
| Simple Interest | 单利计算 | `simple interest principal=10000 rate=0.05 time=3` |
| Loan Monthly Payment | 贷款月供 | `loan principal=500000 rate=0.045 months=360` |
| Return on Investment | 投资回报率 | `roi gain=2000 cost=10000` |
| Present Value | 现值计算 | `present value fv=15000 rate=0.05 periods=10` |
| Future Value | 终值计算 | `future value pv=10000 rate=0.05 periods=10` |

## Project Structure

```
financial_robot/
├── __init__.py       # Package entry point
├── calculator.py     # Core financial calculation methods
└── robot.py          # NLP intent recognition & conversational interface
main.py               # Interactive CLI entry point
tests/
├── test_calculator.py
└── test_robot.py
```

## Getting Started

### Run the interactive robot

```bash
python main.py
```

### Example session

```
============================================================
  智能财务机器人 Lec01 / Intelligent Financial Robot Lec01
============================================================
输入 'help' 查看功能列表，输入 'exit' 退出。
Type 'help' for features, 'exit' to quit.

You: hello
Robot: 您好！我是智能财务机器人 Lec01。输入 'help' 查看支持的功能。
       Hello! I am the Intelligent Financial Robot Lec01. Type 'help' to see available features.

You: compound interest principal=10000 rate=0.05 periods=10
Robot: 复利终值 / Compound Interest Future Value:
  本金 Principal : 10,000.00
  年利率 Rate    : 5.00%
  期数 Periods   : 10 years
  终值 Result    : 16,288.95

You: loan principal=500000 rate=0.045 months=360
Robot: 贷款月供计算 / Loan Monthly Payment:
  贷款金额 Principal    : 500,000.00
  年利率 Annual Rate    : 4.50%
  还款期数 Months       : 360
  月供 Monthly Payment  : 2,533.43
  还款总额 Total Paid   : 912,034.08
  总利息 Total Interest : 412,034.08

You: exit
Robot: 再见！感谢使用智能财务机器人。
       Goodbye! Thank you for using the Intelligent Financial Robot.
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```
