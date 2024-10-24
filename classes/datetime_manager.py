from datetime import datetime, timedelta


class DTManager():
    def string_to_datetime(string_date: str, expanded: bool = True) -> datetime:
        if expanded:
            return datetime.strptime(string_date, "%Y-%m-%d %H:%M")
        else:
            return datetime.strptime(string_date, "%Y-%m-%d")

    def datetime_to_string(dt: datetime, expanded: bool = True) -> str:
        if expanded:
            return datetime.strftime(dt, "%Y-%m-%d %H:%M")
        else:
            return datetime.strftime(dt, "%Y-%m-%d")

    def date_difference(start: datetime, end: datetime) -> int:
        difference: int = 0

        delta_difference: timedelta = end - start
        difference += delta_difference.days * 48
        difference += int(delta_difference.seconds / 1800)

        return difference

    def convert_to_utc(local_dt: datetime, offset: int = 0) -> datetime:
        return local_dt - timedelta(hours=offset)

    def convert_from_utc(utc_dt: datetime, offset: int = 0) -> datetime:
        return utc_dt + timedelta(hours=offset)

    def get_interval_utc(date: str = "today", offset: int = 0) -> tuple:
        if date == "today":
            date = datetime.now().strftime("")

        start_utc = DTManager.convert_to_utc(datetime.strptime(date, "%Y-%m-%d"), offset)
        end_utc = start_utc + timedelta(days=1)

        return (start_utc, end_utc)
