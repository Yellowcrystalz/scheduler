from datetime import datetime

from classes.datetime_manager import DTManager as dtm

MAX_BOOKING_TIME = 8


class BookingManager():
    def check_booking(start: str, end: str, reserved_slots: list) -> int:
        start_dt: datetime = BookingManager.string_to_datetime(start)
        end_dt: datetime = BookingManager.string_to_datetime(end)

        if BookingManager.check_timeframe(start_dt, end_dt):
            return -1

        if BookingManager.check_duration(start_dt, end_dt):
            return -2

        if BookingManager.check_conflict(start_dt, end_dt, reserved_slots):
            return -3

        return 0

    def check_timeframe(start_dt: datetime, end_dt: datetime) -> bool:
        return start_dt >= end_dt

    def check_duration(start_dt: datetime, end_dt: datetime) -> bool:
        difference: int = dtm.date_difference(start_dt, end_dt)

        return MAX_BOOKING_TIME < difference

    def check_conflict(start_dt: datetime, end_dt: datetime, reserved_slots: list) -> bool:
        for slots in reserved_slots:
            res_start: datetime = dtm.string_to_datetime(slots[0])
            res_end: datetime = dtm.string_to_datetime(slots[1])

            if res_start <= start_dt < res_end:
                return True
            elif res_start < end_dt <= res_end:
                return True

        return False

    def get_availability(reserved_slots: list, date: str = "today", offset: int = 0) -> list:
        interval: tuple = dtm.get_interval_utc(date, offset)
        schedule: list = [0] * 48

        for slots in reserved_slots:
            res_start: datetime = dtm.string_to_datetime(slots[0])
            res_end: datetime = dtm.string_to_datetime(slots[1])

            start: int = dtm.date_difference(interval[0], res_start)
            end: int = dtm.date_difference(interval[0], res_end)

            for i in range(start, end):
                schedule[i] = 1

        return schedule
