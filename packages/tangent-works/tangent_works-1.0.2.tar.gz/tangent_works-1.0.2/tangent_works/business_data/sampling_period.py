from abc import ABC, abstractmethod
import numbers
import pandas as pd


class SamplingPeriod(ABC):
    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def is_monthly(self) -> bool:
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    def __radd__(self, other):
        return self + other

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __rsub__(self, other):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        return self * other

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    @classmethod
    def from_string(cls, data: str):
        if 'sec' in data:
            return PeriodSeconds.from_string(data)
        elif 'mon' in data:
            return PeriodMonths.from_string(data)
        else:
            raise ValueError(f"Can't parse {data} into SamplingPeriod.")


class PeriodSeconds(SamplingPeriod):
    def __init__(self, seconds: int):
        self._period = pd.DateOffset(seconds=seconds)

    @property
    def value(self) -> int:
        return self._period.seconds

    @property
    def is_monthly(self) -> bool:
        return False

    def __lt__(self, other):
        if isinstance(other, PeriodSeconds):
            return self.value < other.value

        raise ValueError(f"Can't compare PeriodSeconds to {type(other)}")

    def __gt__(self, other):
        if isinstance(other, PeriodSeconds):
            return self.value > other.value

        raise ValueError(f"Can't compare PeriodSeconds to {type(other)}")

    def __le__(self, other):
        if isinstance(other, PeriodSeconds):
            return self.value <= other.value

        raise ValueError(f"Can't compare PeriodSeconds to {type(other)}")

    def __ge__(self, other):
        if isinstance(other, PeriodSeconds):
            return self.value >= other.value

        raise ValueError(f"Can't compare PeriodSeconds to {type(other)}")

    def __add__(self, other):
        if isinstance(other, PeriodSeconds):
            return PeriodSeconds(self.value + other.value)

        if isinstance(other, pd.Timestamp):
            return other + self._period

        raise ValueError(f"Can't add PeriodSeconds to {type(other)}")

    def __sub__(self, other):
        if isinstance(other, PeriodSeconds):
            return PeriodSeconds(self.value - other.value)

        raise ValueError(f"Can't subtract {type(other)} from PeriodSeconds")

    def __rsub__(self, other):
        if isinstance(other, pd.Timestamp):
            return other - self._period

        raise ValueError(f"Can't subtract PeriodSeconds from {type(other)}")

    def __neg__(self):
        return PeriodSeconds(-self.value)

    def __mul__(self, other):
        if isinstance(other, numbers.Integral):
            return PeriodSeconds(int(self.value * other))

        raise ValueError(f"Can't multiply PeriodSeconds by {type(other)}")

    def __eq__(self, other):
        if not isinstance(other, PeriodSeconds):
            return False

        return self.value == other.value

    def to_string(self) -> str:
        return f"{self.value} seconds"

    @classmethod
    def from_string(cls, data: str):
        value, unit = data.split(" ")

        try:
            value = int(value)
        except:
            raise ValueError(f"Can't parse {data} into PeriodSeconds - value must be an integer.")

        if unit == "seconds":
            return PeriodSeconds(value)
        else:
            raise ValueError(f"Can't parse {data} into SamplingPeriod - invalid unit.")


class PeriodMonths(SamplingPeriod):
    def __init__(self, months: int):
        self._period = pd.DateOffset(months=months)

    @property
    def value(self) -> int:
        return self._period.months

    @property
    def is_monthly(self) -> bool:
        return True

    def __lt__(self, other):
        if isinstance(other, PeriodMonths):
            return self.value < other.value

        raise ValueError(f"Can't compare PeriodMonths to {type(other)}")

    def __gt__(self, other):
        if isinstance(other, PeriodMonths):
            return self.value > other.value

        raise ValueError(f"Can't compare PeriodMonths to {type(other)}")

    def __le__(self, other):
        if isinstance(other, PeriodMonths):
            return self.value <= other.value

        raise ValueError(f"Can't compare PeriodMonths to {type(other)}")

    def __ge__(self, other):
        if isinstance(other, PeriodMonths):
            return self.value >= other.value

        raise ValueError(f"Can't compare PeriodMonths to {type(other)}")

    def __add__(self, other):
        if isinstance(other, PeriodMonths):
            return PeriodMonths(self.value + other.value)

        if isinstance(other, pd.Timestamp):
            return other + self._period

        raise ValueError(f"Can't add PeriodMonths to {type(other)}")

    def __sub__(self, other):
        if isinstance(other, PeriodMonths):
            return PeriodMonths(self.value - other.value)

        raise ValueError(f"Can't subtract {type(other)} from PeriodMonths")

    def __rsub__(self, other):
        if isinstance(other, pd.Timestamp):
            return other - self._period

        raise ValueError(f"Can't subtract PeriodMonths from {type(other)}")

    def __neg__(self):
        return PeriodMonths(-self.value)

    def __mul__(self, other):
        if isinstance(other, numbers.Integral):
            return PeriodMonths(int(self.value * other))

        raise ValueError(f"Can't multiply PeriodMonths by {type(other)}")

    def __eq__(self, other):
        if not isinstance(other, PeriodMonths):
            return False

        return self.value == other.value

    def to_string(self) -> str:
        return f"{self.value} months"

    @classmethod
    def from_string(cls, data: str):
        value, unit = data.split(" ")

        try:
            value = int(value)
        except:
            raise ValueError(f"Can't parse {data} into PeriodMonths - value must be an integer.")

        if unit == "months":
            return PeriodMonths(value)
        else:
            raise ValueError(f"Can't parse {data} into SamplingPeriod - invalid unit.")
