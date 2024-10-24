from datetime import datetime, timedelta

from database.python.db_manager import DBManager

MAX_BOOKING_TIME = 8


class BookingManager():
    def check_booking(start: str, end: str, reserved_slots: list) -> int:
        start_dt: datetime = await BookingManager.string_to_datetime(start)
        end_dt: datetime = await BookingManager.string_to_datetime(end)

        if not BookingManager.check_timeframe(start_dt, end_dt):
            return -1

        if not BookingManager.check_duration(start_dt, end_dt):
            return -2

        if not BookingManager.check_conflict(start_dt, end_dt, reserved_slots):
            return -3

        return 0

    def check_timeframe(start_dt: datetime, end_dt: datetime) -> bool:
        return start_dt < end_dt

    def check_duration(start_dt: datetime, end_dt: datetime) -> bool:
        difference: int = BookingManager.date_difference(start_dt, end_dt)

        return MAX_BOOKING_TIME >= difference

    def check_conflict(start_dt: datetime, end_dt: datetime, reserved_slots: list) -> bool:
        for slots in reserved_slots:
            res_start: datetime = BookingManager.string_to_datetime(slots[0])
            res_end: datetime = BookingManager.string_to_datetime(slots[1])

            if res_start <= start_dt < res_end:
                return False
            elif res_start < end_dt <= res_end:
                return False

        return True

    def string_to_datetime(string_date: str) -> datetime:
        return datetime.strptime(string_date, "%Y-%m-%d %H:%M")

    def date_difference(start: datetime, end: datetime) -> int:
        difference: int = 0

        delta_difference: timedelta = end - start
        difference += delta_difference.days * 48
        difference += int(delta_difference.seconds / 1800)

        return difference
