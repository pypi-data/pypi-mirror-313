from __future__ import annotations

from decimal import Decimal
from typing import Any
from typing import ClassVar


class EngineeringNumber:
    """Easy manipulation of numbers which use engineering notation"""

    _suffix_lookup: ClassVar = {
        "Y": "e24",
        "Z": "e21",
        "E": "e18",
        "P": "e15",
        "T": "e12",
        "G": "e9",
        "M": "e6",
        "k": "e3",
        "": "e0",
        "m": "e-3",
        "u": "e-6",
        "n": "e-9",
        "p": "e-12",
        "f": "e-15",
        "a": "e-18",
        "z": "e-21",
        "y": "e-24",
    }

    _exponent_lookup_scaled: ClassVar = {
        "-12": "Y",
        "-15": "Z",
        "-18": "E",
        "-21": "P",
        "-24": "T",
        "-27": "G",
        "-30": "M",
        "-33": "k",
        "-36": "",
        "-39": "m",
        "-42": "u",
        "-45": "n",
        "-48": "p",
        "-51": "f",
        "-54": "a",
        "-57": "z",
        "-60": "y",
    }

    def __init__(
        self,
        value: str | float | int | EngineeringNumber,
        precision: int = 2,
        significant: int = 0,
    ):
        """
        :param value: string, integer, or float representing the numeric value of the number
        :param precision: the precision past the decimal
        :param significant: the number of significant digits
        if given, significant takes precedence over precision
        """
        self.precision = precision
        self.significant = significant

        if isinstance(value, str):
            suffix_keys = [key for key in self._suffix_lookup if key != ""]

            str_value = str(value)
            for suffix in suffix_keys:
                if suffix in str_value:
                    str_value = str_value[:-1] + self._suffix_lookup[suffix]
                    break

            self.number = Decimal(str_value)

        elif isinstance(value, int | float | EngineeringNumber):
            self.number = Decimal(str(value))

        else:
            raise TypeError("value has unsupported type")

    def __repr__(self):
        """Returns the string representation"""
        # The Decimal class only really converts numbers that are very small into engineering notation.
        # So we will simply make all numbers small numbers and take advantage of the Decimal class.
        number_str = self.number * Decimal("10e-37")
        number_str = number_str.to_eng_string().lower()

        base, exponent = number_str.split("e")

        if self.significant > 0:
            abs_base = abs(Decimal(base))
            num_digits = 1
            num_digits += 1 if abs_base >= 10 else 0
            num_digits += 1 if abs_base >= 100 else 0
            num_digits = self.significant - num_digits
        else:
            num_digits = self.precision

        base = str(round(Decimal(base), num_digits))

        if "e" in base.lower():
            base = str(int(Decimal(base)))

        # Remove trailing decimal
        if "." in base:
            base = base.rstrip(".")

        return base + self._exponent_lookup_scaled[exponent]

    def __str__(self) -> str:
        return self.__repr__()

    def __int__(self) -> int:
        return int(self.number)

    def __float__(self):
        return float(self.number)

    @staticmethod
    def _to_decimal(other: str | float | int | EngineeringNumber) -> Decimal:
        if not isinstance(other, EngineeringNumber):
            other = EngineeringNumber(other)
        return other.number

    def __add__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self.number + self._to_decimal(other)))

    def __radd__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return self.__add__(other)

    def __sub__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self.number - self._to_decimal(other)))

    def __rsub__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self._to_decimal(other) - self.number))

    def __mul__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self.number * self._to_decimal(other)))

    def __rmul__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return self.__mul__(other)

    def __truediv__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self.number / self._to_decimal(other)))

    def __rtruediv__(self, other: str | float | int | EngineeringNumber) -> EngineeringNumber:
        return EngineeringNumber(str(self._to_decimal(other) / self.number))

    def __lt__(self, other: str | float | int | EngineeringNumber) -> bool:
        return self.number < self._to_decimal(other)

    def __gt__(self, other: str | float | int | EngineeringNumber) -> bool:
        return self.number > self._to_decimal(other)

    def __le__(self, other: str | float | int | EngineeringNumber) -> bool:
        return self.number <= self._to_decimal(other)

    def __ge__(self, other: str | float | int | EngineeringNumber) -> bool:
        return self.number >= self._to_decimal(other)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, str | float | int | EngineeringNumber):
            return NotImplemented
        return self.number == self._to_decimal(other)
