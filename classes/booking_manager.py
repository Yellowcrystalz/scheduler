from datetime import datetime, timedelta

from database.python.db_manager import DBManager

MAX_BOOKING_TIME = 8.0

class BookingManager():
    async def valid_booking(user_start_date: str, user_end_date: str) -> bool:
        user_start_datetime = await BookingManager.string_to_date(user_start_date)
        user_end_datetime = await BookingManager.string_to_date(user_end_date)

        return user_start_datetime < user_end_datetime

    # async def can_book(user_start_date: str, user_end_date: str) -> bool:
        # for dates in bookings:
        #     start_date = datetime.strptime(dates[0], "%Y-%m-%d %H:%M") 
        #     end_date = datetime.strptime(dates[1], "%Y-%m-%d %H:%M") 

        #     if start_date <= user_start_date < end_date:
        #         return False
        #     elif start_date < user_end_date <= end_date:
        #         return False
        
        # return True
    
    async def string_to_date(string_date: str) -> datetime:
        return datetime.strptime(string_date, "%Y-%m-%d %H:%M") 
    
    async def date_difference(start: datetime, end: datetime) -> float:
        difference: float = 0.0
        delta_difference: timedelta = end - start
        difference += delta_difference.days * 48.0
        difference += delta_difference.seconds / 1800

        return difference