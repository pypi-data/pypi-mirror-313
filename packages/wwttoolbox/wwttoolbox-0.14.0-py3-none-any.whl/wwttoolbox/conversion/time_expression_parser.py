from datetime import datetime, timedelta, timezone


class TimeExpressionParser:

    def __init__(self, expression: str):
        self.expr = expression

    def is_valid(self) -> bool:
        base_element = self.is_using_now() or self.is_using_ref()

        if len(self.expr) == 3 and self.is_using_now():
            return True  # just 'now' is valid

        operator = self.get_operator() in ["+", "-"]
        offset_unit = self.get_offset_unit() is not None
        offset_value = self.get_offset_value() is not None

        return base_element and operator and offset_unit and offset_value

    def is_using_now(self) -> bool:
        return self.expr.startswith("now")

    def is_plain_now(self) -> bool:
        return self.expr == "now"

    def is_using_ref(self) -> bool:
        return self.expr.startswith("ref")

    def get_operator(self) -> str:
        if len(self.expr) < 4:
            return None

        return self.expr[3]

    def get_offset_unit(self) -> str:
        if len(self.expr) < 5:
            return None

        unit = self.expr[-1]
        if unit in ["s", "m", "h", "d", "y"]:
            return unit

        return None

    def get_offset_value(self) -> int:
        try:
            return int(self.expr[4:-1])
        except Exception:
            return None

    def get_timedelta(self):
        """Returns a timedelta object based on the expression.

        The timedelta is signed based on the operator.

        Returns:
        timedelta: A timedelta object (signed).
        """
        if self.is_plain_now():
            return timedelta(seconds=0)

        offset_value = self.get_offset_value()
        offset_unit = self.get_offset_unit()

        offset_signed = offset_value if self.get_operator() == "+" else -offset_value

        if offset_unit == "s":
            return timedelta(seconds=offset_signed)
        elif offset_unit == "m":
            return timedelta(minutes=offset_signed)
        elif offset_unit == "h":
            return timedelta(hours=offset_signed)
        elif offset_unit == "d":
            return timedelta(days=offset_signed)
        elif offset_unit == "y":
            return timedelta(days=offset_signed * 365)
        else:
            raise ValueError(f"Invalid offset unit: '{offset_unit}'")

    def get_datetime(self, ref_time: datetime | None = None) -> datetime:
        """Returns a datetime object based on the expression.

        The base time is either the current time in UTC or a reference time.

        Returns:
        datetime: A datetime object.
        """
        delta = self.get_timedelta()

        if self.is_using_now():
            return datetime.now(timezone.utc) + delta
        elif self.is_using_ref():
            if ref_time is None:
                raise ValueError(
                    f"No reference time provided for expression: '{self.expr}'"
                )
            else:
                return ref_time + delta
        else:
            raise ValueError(f"Invalid expression: '{self.expr}'")
