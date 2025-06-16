import logging
import time


class Calculator:
    def __init__(self):
        pass

    def add(self, a=0, b=0):
        return a + b

    def subtract(self, a=0, b=0):
        return a - b

    def multiply(self, a=0, b=0):
        return a * b

    def divide(self, a=0, b=0):
        return a / b


def main():
    log = logging.getLogger("main")
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)

    calc = Calculator()
    log.info(f"add: {calc.add(1, 2)}")
    log.info(f"subtract: {calc.subtract(1, 2)}")
    log.info(f"multiply: {calc.multiply(1, 2)}")
    log.info(f"divide: {calc.divide(1, 2)}")

    while True:
        log.info("go sleep")
        time.sleep(60)


if __name__ == "__main__":
    main()
