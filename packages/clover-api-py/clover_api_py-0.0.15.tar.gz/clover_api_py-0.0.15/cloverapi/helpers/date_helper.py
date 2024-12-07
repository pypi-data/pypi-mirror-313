from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Union

class DateHelper:
    @staticmethod
    def filters_period(period: Union[str, int]):
        """
        Get the start and end timestamps for a specified period.

        :param period: Reporting period (e.g., 'daily', 'weekly', 'monthly', etc.) or an integer for last n days.
        :return: Tuple of start and end timestamps in milliseconds.
        """
        time_ranges = {
            "day": DateHelper.today,
            "today": DateHelper.today,
            "yesterday": DateHelper.yesterday,
            "week": DateHelper.current_week,
            "month": DateHelper.current_month,
            "quarter": DateHelper.current_quarter,
            "year": DateHelper.current_year,
        }

        if isinstance(period, str):
            method = time_ranges.get(period)
            if not method:
                raise ValueError(f"Unsupported period: {period}. Use one of {list(time_ranges.keys())}.")
            return method()
        elif isinstance(period, int):
            return DateHelper.last_n_days(period)
        else:
            raise ValueError("Period must be a recognized string or an integer for last n days.")

    @staticmethod
    def today():
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1) - timedelta(microseconds=1)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def yesterday():
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        end = start + timedelta(days=1) - timedelta(microseconds=1)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def current_week():
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=now.weekday())  # Monday
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7) - timedelta(microseconds=1)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def current_month():
        now = datetime.now(timezone.utc)
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = (start + relativedelta(months=1)) - timedelta(microseconds=1)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def current_quarter():
        now = datetime.now(timezone.utc)
        quarter_start_month = (now.month - 1) // 3 * 3 + 1
        start = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = (start + relativedelta(months=3)) - timedelta(microseconds=1)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def current_year():
        now = datetime.now(timezone.utc)
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def last_n_days(n):
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=n)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return DateHelper._to_milliseconds(start), DateHelper._to_milliseconds(end)

    @staticmethod
    def custom_range(start_date, end_date):
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("start_date and end_date must be datetime objects")
        return DateHelper._to_milliseconds(start_date), DateHelper._to_milliseconds(end_date)

    @staticmethod
    def _to_milliseconds(dt):
        return int(dt.timestamp() * 1000)

    @staticmethod
    def ms_to_date(ms):
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

    @staticmethod
    def group_by_period(
        data: List[Dict], group_by: str, date_key: str = "createdTime", value_key: str = "total"
    ) -> Dict:
        """
        Group data by a specified period (day, week, quarter, or year).

        :param data: List of dictionaries to group (e.g., orders or inventory items).
        :param group_by: Grouping period ('day', 'week', 'quarter', or 'year').
        :param date_key: Key in the dictionary containing the date in milliseconds.
        :param value_key: Key in the dictionary containing the value to aggregate (e.g., 'total').
        :return: Dictionary grouped by the specified period with aggregated totals.
        """
        grouped_data = {}

        for item in data:
            created_time = DateHelper.ms_to_date(item[date_key])  # Convert ms to datetime

            if group_by == "day":
                key = created_time.date()
            elif group_by == "week":
                key = created_time.strftime("%Y-W%U")  # ISO week format
            elif group_by == "quarter":
                quarter = (created_time.month - 1) // 3 + 1
                key = f"{created_time.year}-Q{quarter}"
            elif group_by == "year":
                key = created_time.year
            else:
                raise ValueError(f"Unsupported group_by: {group_by}. Use 'day', 'week', 'quarter', or 'year'.")

            if key not in grouped_data:
                grouped_data[key] = {"total_count": 0, "total_amount": 0}

            grouped_data[key]["total_count"] += 1
            grouped_data[key]["total_amount"] += item.get(value_key, 0)

        return grouped_data