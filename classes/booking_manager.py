from datetime import datetime

from classes.datetime_manager import DTManager as dtm

MAX_BOOKING_TIME = 8


class BookingManager():
    def check_booking(start: datetime, end: datetime, reserved_slots: list) -> int:
        if BookingManager.check_timeframe(start, end):
            return -1

        if BookingManager.check_duration(start, end):
            return -2

        if BookingManager.check_conflict(start, end, reserved_slots):
            return -3

        return 0

    def check_timeframe(start: datetime, end: datetime) -> bool:
        return start >= end

    def check_duration(start: datetime, end: datetime) -> bool:
        difference: int = dtm.date_difference(start, end)

        return MAX_BOOKING_TIME < difference

    def check_conflict(start: datetime, end: datetime, reserved_slots: list) -> bool:
        for slots in reserved_slots:
            res_start: datetime = dtm.string_to_datetime(slots[0])
            res_end: datetime = dtm.string_to_datetime(slots[1])

            if res_start <= start < res_end:
                return True
            elif res_start < end <= res_end:
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
